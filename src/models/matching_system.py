# src/models/matching_system.py
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from src.utils.preprocessing import DataPreprocessor
from src.models.autoencoder import StudentAutoencoder

class StudentMatchingSystem:
    def __init__(self, encoding_dim=32):
        self.preprocessor = DataPreprocessor()
        self.encoding_dim = encoding_dim
        self.autoencoder = None
        self.processed_data = None
        self.original_data = None
        self.encoded_features = None
        
        # Define importance weights
        self.weights = {
            'Important': 1.0,
            'Neutral': 0.5,
            'Not Important': 0.1
        }

    def fit(self, df, epochs=50, batch_size=32):
        """Fit the matching system to the student data"""
        self.original_data = df.copy()
        
        # First fit the preprocessor
        self.preprocessor.fit(df)
        
        # Then preprocess the data
        self.processed_data = self.preprocessor.preprocess_data(df)
        
        # Initialize and train autoencoder
        self.autoencoder = StudentAutoencoder(
            input_dim=self.processed_data.shape[1],
            encoding_dim=self.encoding_dim
        )
        
        history = self.autoencoder.train(
            self.processed_data.values,
            epochs=epochs,
            batch_size=batch_size
        )
        
        # Generate encoded features
        self.encoded_features = self.autoencoder.encode(self.processed_data.values)
        
        return history

    def _calculate_penalties(self, student_data):
        """Calculate penalties based on preferences with weighted importance"""
        penalties = np.zeros(len(self.original_data))
        
        for idx, row in self.original_data.iterrows():
            # Age difference penalty - improved version
            age_importance = self.weights.get(student_data['Preference_Similar_Age'], 0.5)
            if age_importance > 0:
                age_diff = abs(student_data['Child_Age'] - row['Child_Age'])
                # Normalize age difference penalty
                # For ages 3-13, max difference is 10 years
                normalized_age_diff = age_diff / 10.0
                # Apply weighted penalty based on importance
                penalties[idx] += normalized_age_diff * age_importance * 0.5
            
            # Gender matching penalty - improved version
            gender_importance = self.weights.get(student_data['Preference_Same_Gender'], 0.5)
            if gender_importance > 0:
                if student_data['Child_Gender'] != row['Child_Gender']:
                    # Apply different penalties based on gender combinations
                    if student_data['Child_Gender'] in ['Male', 'Female'] and row['Child_Gender'] in ['Male', 'Female']:
                        # Binary gender mismatch
                        penalties[idx] += 0.3 * gender_importance
                    elif 'Prefer not to say' in [student_data['Child_Gender'], row['Child_Gender']]:
                        # One student prefers not to say
                        penalties[idx] += 0.1 * gender_importance
                    else:
                        # Other gender combinations
                        penalties[idx] += 0.2 * gender_importance
            
            # Time overlap penalty - improved version
            time_importance = self.weights.get(student_data['Preference_Overlapping_Time'], 0.5)
            if time_importance > 0:
                availability_cols = [col for col in self.original_data.columns 
                                   if col.startswith('Available_Time_')]
                
                # Count total available slots for each student
                student1_available = sum(1 for col in availability_cols 
                                     if student_data[col] == 'Available')
                student2_available = sum(1 for col in availability_cols 
                                     if row[col] == 'Available')
                
                # Count overlapping slots
                overlapping_slots = sum(1 for col in availability_cols 
                                    if student_data[col] == 'Available' 
                                    and row[col] == 'Available')
                
                if student1_available == 0 or student2_available == 0:
                    penalties[idx] += 0.5 * time_importance
                else:
                    # Calculate overlap ratio
                    overlap_ratio = overlapping_slots / min(student1_available, student2_available)
                    # Add penalty based on lack of overlap
                    penalties[idx] += (1 - overlap_ratio) * time_importance * 0.3
                
                # Additional penalty for different regions (time zone consideration)
                if student_data['Child_Region'] != row['Child_Region']:
                    penalties[idx] += 0.15 * time_importance
        
        return penalties

    def find_matches(self, student_data, top_n=5):
        """Find top matches for a given student with improved matching logic"""
        print("\nStarting matching process...")
        print(f"Input student data: {student_data}")
        
        # Convert single student data to DataFrame
        student_df = pd.DataFrame([student_data])
        
        try:
            processed_student = self.preprocessor.preprocess_data(student_df)
            processed_student = processed_student[self.processed_data.columns]
            encoded_student = self.autoencoder.encode(processed_student.values)
            
            # Calculate base similarity scores
            base_similarities = cosine_similarity(encoded_student, self.encoded_features)[0]
            
            # Calculate penalties
            penalties = self._calculate_penalties(student_data)
            
            # Adjust similarities based on penalties
            adjusted_similarities = base_similarities - penalties
            
            # Get top matches
            top_indices = np.argsort(adjusted_similarities)[-top_n:][::-1]
            
            matches = []
            for idx in top_indices:
                match_info = {
                    'student': {
                        key: int(value) if isinstance(value, np.integer) else float(value) if isinstance(value, np.floating) else value
                        for key, value in self.original_data.iloc[idx].to_dict().items()
                    },
                    'similarity_score': float(adjusted_similarities[idx]),
                    'base_similarity': float(base_similarities[idx]),
                    'penalty': float(penalties[idx]),
                    'age_difference': int(abs(student_data['Child_Age'] - self.original_data.iloc[idx]['Child_Age'])),
                    'shared_interests': self._get_shared_interests(student_data, self.original_data.iloc[idx]),
                    'overlapping_availability': self._get_overlapping_availability(student_data, self.original_data.iloc[idx])
                }
                matches.append(match_info)
            
            return matches
            
        except Exception as e:
            print(f"Error in find_matches: {str(e)}")
            raise
    
    def _get_shared_interests(self, student1, student2):
        """Get list of shared interests between two students"""
        base_interests = [
            'Science',
            'Coding/Game Design',
            'Reading/Writing',
            'Engineering',
            'Art',
            'Music',
            'Math'
        ]
        
        shared = []
        print("\nDebug: Checking shared interests")
        print("Student1 interests:")
        for k, v in student1.items():
            if k.startswith('Interest_') and v == 'Selected':
                print(f"- {k}: {v}")
        print("\nStudent2 interests:")
        for k, v in student2.items():
            if k.startswith('Interest_') and v == 'Selected':
                print(f"- {k}: {v}")
        
        for interest in base_interests:
            column_name = f"Interest_{interest.replace('/', '_')}"
            try:
                value1 = student1[column_name]
                value2 = student2[column_name]
                print(f"\nChecking interest: {interest}")
                print(f"Column name: {column_name}")
                print(f"Student1 value: {value1}")
                print(f"Student2 value: {value2}")
                
                if (value1 == 'Selected' and value2 == 'Selected'):
                    shared.append(interest)
                    print(f"Added to shared interests: {interest}")
            except KeyError as e:
                print(f"Warning: Interest column not found: {column_name}")
                print(f"Available columns in student1: {sorted([k for k in student1.keys() if k.startswith('Interest_')])}")
                print(f"Available columns in student2: {sorted([k for k in student2.keys() if k.startswith('Interest_')])}")
                continue
        
        print(f"\nFinal shared interests: {shared}")
        return shared
    
    def _get_overlapping_availability(self, student1, student2):
        """Get overlapping availability times between two students"""
        availability_cols = [col for col in self.original_data.columns 
                            if col.startswith('Available_Time_')]
        overlapping = []
        
        for col in availability_cols:
            try:
                if (student1[col] == 'Available' and 
                    student2[col] == 'Available'):
                    time_slot = col.replace('Available_Time_', '')
                    overlapping.append(time_slot)
            except KeyError as e:
                print(f"Warning: Availability column not found: {col}")
                continue
                
        return overlapping 
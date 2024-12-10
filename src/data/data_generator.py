# src/data/data_generator.py
import pandas as pd
import numpy as np
import random
import string

def generate_random_nickname():
    """Generate a random 10-character nickname"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

def generate_sample_data(n_samples=300, save_path=None):
    """Generate sample student data based on specified criteria"""
    
    # Initialize empty list for data
    data = []
    
    # Define time slots
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    times = ['Morning', 'Afternoon', 'Evening']
    
    # Define interests
    interests = [
        'Science', 
        'Coding/Game Design', 
        'Reading/Writing', 
        'Engineering',
        'Art', 
        'Music', 
        'Math'
    ]
    
    for _ in range(n_samples):
        student_data = {}
        
        # Basic Information
        student_data['Child_Nickname'] = generate_random_nickname()
        student_data['Child_Age'] = random.randint(3, 13)
        
        # Gender with 80% Male/Female distribution
        gender_choice = random.random()
        if gender_choice < 0.4:
            student_data['Child_Gender'] = 'Male'
        elif gender_choice < 0.8:
            student_data['Child_Gender'] = 'Female'
        elif gender_choice < 0.9:
            student_data['Child_Gender'] = 'Other'
        else:
            student_data['Child_Gender'] = 'Prefer not to say'
        
        # Region
        student_data['Child_Region'] = random.choice([
            'Western America', 'Central America', 'Eastern America'
        ])
        
        # Interests
        print("\nDebug: Generating interest data")
        for interest in interests:
            column_name = f'Interest_{interest.replace("/", "_")}'
            value = random.choices(['Selected', 'Not selected'], weights=[0.3, 0.7], k=1)[0]
            student_data[column_name] = value
            print(f"Interest: {interest}")
            print(f"Column name: {column_name}")
            print(f"Value: {value}")
        
        # Available Times
        for day in days:
            for time in times:
                available_prob = random.random()
                is_available = False
                
                if day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
                    if time == 'Morning':
                        is_available = available_prob < 0.1  # 10% chance
                    elif time == 'Afternoon':
                        is_available = available_prob < 0.2  # 20% chance
                    else:  # Evening
                        is_available = available_prob < 0.3  # 30% chance
                elif day == 'Saturday':
                    is_available = random.choice([True, False])  # 50% chance
                else:  # Sunday
                    is_available = available_prob < 0.3  # 30% chance for all slots
                
                student_data[f'Available_Time_{day}_{time}'] = 'Available' if is_available else 'Not available'
        
        # Matching Preferences
        student_data['Preference_Interaction_Outside_Class'] = random.choice(['Yes', 'No', 'Decide Later'])
        
        student_data['Preference_Overlapping_Time'] = random.choice(['Important', 'Not Important', 'Neutral'])
        
        # 80% Important for Age and Gender preferences
        for pref in ['Similar_Age', 'Same_Gender']:
            if random.random() < 0.8:
                student_data[f'Preference_{pref}'] = 'Important'
            else:
                student_data[f'Preference_{pref}'] = random.choice(['Not Important', 'Neutral'])
        
        data.append(student_data)
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV if path is provided
    if save_path:
        df.to_csv(save_path, index=False)
        print(f"Data saved to {save_path}")
    
    return df

if __name__ == "__main__":
    # Generate sample data and save to CSV
    df = generate_sample_data(n_samples=300, save_path='../../data/student_data.csv')
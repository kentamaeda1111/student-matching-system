# src/utils/preprocessing.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder


class DataPreprocessor:
   def __init__(self):
       self.scaler = StandardScaler()
       self.encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
       self.categorical_columns = [
           'Child_Gender', 'Child_Region',
           'Preference_Interaction_Outside_Class',
           'Preference_Overlapping_Time',
           'Preference_Similar_Age',
           'Preference_Same_Gender'
       ]
       self.encoded_feature_names = None
       
   def fit(self, df):
       """Fit the preprocessor to the training data"""
       categorical_data = df[self.categorical_columns]
       self.encoder.fit(categorical_data)
       self.encoded_feature_names = self.encoder.get_feature_names_out(self.categorical_columns)
       self.scaler.fit(df[['Child_Age']])
   
   def preprocess_data(self, df):
       """Preprocess the student data for the matching system"""
       df_processed = df.copy()
       
       # Convert availability and interest columns to binary
       availability_cols = [col for col in df.columns if col.startswith('Available_Time_')]
       interest_cols = [col for col in df.columns if col.startswith('Interest_')]
       
       for col in availability_cols + interest_cols:
           df_processed[col] = (df_processed[col].isin(['Available', 'Selected'])).astype(int)
       
       # One-hot encode categorical variables using fitted encoder
       categorical_data = df_processed[self.categorical_columns]
       encoded_data = self.encoder.transform(categorical_data)
       encoded_df = pd.DataFrame(
           encoded_data,
           columns=self.encoded_feature_names
       )
       
       # Scale numerical columns using fitted scaler
       df_processed['Child_Age'] = self.scaler.transform(
           df_processed[['Child_Age']]
       )
       
       # Map preference options to numeric values
       preference_mapping = {
           'Important': 1.0,
           'Neutral': 0.5,
           'Not Important': 0.0
       }
       
       preference_cols = [col for col in df.columns if col.startswith('Preference_')]
       for col in preference_cols:
           if col in self.categorical_columns:
               continue
           df_processed[col] = df_processed[col].map(preference_mapping)
       
       # Combine all features
       final_df = pd.concat([
           df_processed[['Child_Age']],
           encoded_df,
           df_processed[availability_cols],
           df_processed[interest_cols]
       ], axis=1)
       
       return final_df

   def get_feature_names(self):
       return self.encoded_feature_names.tolist() if self.encoded_feature_names is not None else None
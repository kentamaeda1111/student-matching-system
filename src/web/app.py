# src/web/app.py
from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
import sys

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.models.matching_system import StudentMatchingSystem
from src.data.data_generator import generate_sample_data

app = Flask(__name__)

def ensure_data_exists():
    """Ensure sample data exists and return the DataFrame"""
    data_dir = os.path.join(project_root, "data")
    os.makedirs(data_dir, exist_ok=True)
    
    data_file = os.path.join(data_dir, "student_data.csv")
    if not os.path.exists(data_file):
        print("Generating new sample data...")
        df = generate_sample_data(n_samples=300, save_path=data_file)
        print(f"Sample data saved to {data_file}")
    else:
        print("Loading existing sample data...")
        df = pd.read_csv(data_file)
    return df

# Initialize data and matching system
df = ensure_data_exists()
matching_system = StudentMatchingSystem()
matching_system.fit(df)

@app.route('/')
def index():
    age_range = range(3, 14)  # Ages from 3 to 13
    return render_template('index.html', age_range=age_range)

@app.route('/match', methods=['POST'])
def match():
    student_data = request.json
    student_data['Child_Age'] = int(student_data['Child_Age'])
    matches = matching_system.find_matches(student_data, top_n=5)
    return jsonify(matches)

if __name__ == '__main__':
    app.run(debug=True) 
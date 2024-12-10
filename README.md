# Student Matching System with Autoencoder 

## Overview 
This project is a student matching system that uses an autoencoder-based deep learning approach to find compatible study partners. The system considers multiple factors including interests, availability, age, and preferences to generate optimal matches.

## Key Features 
* Deep learning-based matching using autoencoder
* Web interface for student registration and matching
* Real-time matching results
* Customizable preference settings

## Technical Architecture 

### Autoencoder Architecture
The system uses a neural network-based autoencoder for dimensionality reduction and feature learning. Here's how it works:

1. **Input Layer**
   * Takes preprocessed student data (interests, availability, preferences, etc.)

2. **Encoder**
   * First dense layer: 64 neurons with ReLU activation
   * Second dense layer (bottleneck): 32 neurons with ReLU activation

3. **Decoder**
   * First dense layer: 64 neurons with ReLU activation
   * Output layer: Reconstructs input dimensions with sigmoid activation

4. **Training**
   * Loss function: Mean Squared Error (MSE)
   * Optimizer: Adam
   * Validation split: 20%

The autoencoder learns to compress student data into a 32-dimensional latent space, capturing essential patterns and relationships between different features. This compressed representation is then used for finding similar students through cosine similarity.

### Matching Algorithm
The matching process involves:

1. Feature encoding using the trained autoencoder
2. Base similarity calculation using cosine similarity
3. Penalty system based on preferences (age, gender, time overlap)
4. Final score adjustment and ranking

## Setup Instructions 

### Prerequisites
* Python 3.8 or higher
* pip (Python package manager)
* Virtual environment (recommended)

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/kentamaeda1111/student-matching-system.git
   cd student-matching-system
   ```

2. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the Flask application:
   ```bash
   python src/web/app.py
   ```
   Note: Sample data will be automatically generated on first startup.

5. Access the application:
   ```
   http://localhost:5000
   ```

## Project Structure 
```
student-matching-system/
├── .gitignore
├── data/
│   └── student_data.csv
├── src/
│   ├── data/
│   │   ├── __init__.py
│   │   └── data_generator.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── autoencoder.py
│   │   └── matching_system.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── preprocessing.py
│   └── web/
│       ├── __init__.py
│       ├── app.py
│       ├── static/
│       │   ├── style.css
│       │   └── script.js
│       └── templates/
│           └── index.html
├── LICENSE
├── requirements.txt
└── README.md
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact 📧
Your Name - Kenta Maeda
Project Link: https://github.com/kentamaeda1111/student-matching-system
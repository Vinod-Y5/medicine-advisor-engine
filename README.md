# Medicine-Advisor-Engine
AI-based Symptom Checker and Medicine Recommendation System using Machine Learning and Streamlit

Live App: https://medicine-advisor-engine-hwxs6w2z36u7hng6di4ysx.streamlit.app/

## Overview
Medicine Advisor Engine is an end-to-end Machine Learning application that predicts possible diseases based on user-entered symptoms and provides medical guidance through an interactive web interface.

The project demonstrates how raw medical datasets can be transformed into a complete, real-world style application by combining data preprocessing, machine learning, database management, AI-generated reports, and a user-facing UI.

This is not just a model — it is a full pipeline from data to deployment-style usage.

## Key Features
- User registration and login system
- Symptom-based disease prediction using a trained ML model
- AI-generated health reports in simple, human-readable language (LLM-powered)
- Disease description, precautions, and recommended next steps
- Emergency alert functionality for critical conditions
- User profile management (medical history, allergies)
- Persistent storage using SQLite database
- Interactive and clean UI built with Streamlit

## Machine Learning Workflow
1. Data Collection
   - Multiple CSV datasets containing symptoms, disease descriptions, precautions, and symptom severity

2. Data Preprocessing
   - Cleaning and standardizing symptom data
   - Mapping symptoms into structured input format
   - Preparing data for supervised learning

3. Model Training
   - Supervised classification model trained on symptom–disease relationships
   - Model evaluation and validation
   - Final trained model saved using joblib for reuse

4. Prediction Pipeline
   - User symptoms converted into model-readable input
   - Model predicts the most probable disease
   - Related medical information is retrieved and displayed

## Application Flow
1. User registers or logs in
2. User enters symptoms via the UI
3. Machine Learning model predicts the disease
4. System displays:
   - Predicted disease
   - AI-generated health report
   - Precautions and guidance
5. Emergency alert option appears for critical diseases
6. User profile data is stored and can be updated

## Tech Stack
- Programming Language: Python
- Machine Learning: Scikit-learn
- Data Processing: Pandas, NumPy
- Web Framework: Streamlit
- Database: SQLite
- Model Serialization: Joblib
- Notebook Environment: Jupyter Notebook
- Version Control: Git, GitHub

## Project Structure
medicine-advisor-engine/
├── app.py                       # Main Streamlit application
├── update_database.py           # Database update utility
├── requirements.txt
├── README.md
├── data/
│   ├── dataset.csv
│   ├── symptom_precaution.csv
│   ├── symptom_severity.csv
│   └── symptom_description.csv
├── model/
│   └── disease_prediction_model.joblib
├── notebooks/
│   └── EDA_and_model_building.ipynb
├── docs/
│   └── Medicine_advisor_engine_report.pdf
├── screenshots/
│   ├── 01_login.png
│   ├── 02_symptom_input.png
│   ├── 03_prediction.png
│   ├── 04_ai_report.png
│
└── .gitignore

## How to Run Locally
1. Clone the repository
   git clone https://github.com/your-username/medicine-advisor-engine.git

2. Navigate to the project directory
   cd medicine-advisor-engine

3. Install dependencies
   pip install -r requirements.txt

4. Run the application
   streamlit run app.py

5. Open the browser and use the application

## Screenshots
Screenshots of the application UI are available in the screenshots/ folder, showing:
- Login and registration
- Symptom input
- Disease prediction result
- AI-generated health report

## Notes
- The SQLite database file is excluded from the repository for security reasons
- This project is intended for educational and demonstration purposes only
- It does not replace professional medical advice
- AI-generated health reports are powered via OpenRouter using free-tier models; availability may vary
- The emergency alert functionality is implemented in the application logic; a screenshot is not included due to runtime constraints

## Author
Built as a hands-on Machine Learning and Data Science project to demonstrate real-world application development.

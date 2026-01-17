import streamlit as st
import os
import sqlite3
import joblib
import smtplib
from email.mime.text import MIMEText
from openai import OpenAI
import requests
# Load the trained ML model
model = joblib.load("model/disease_prediction_model.joblib")

# Openai API setup
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# Generate AI health report
def generate_report(symptoms_list, predicted_disease):
    prompt = f"""A patient has entered the following symptoms: {', '.join(symptoms_list)}.
They were diagnosed with: {predicted_disease}.

Please provide a health report in clear, friendly language that explains:
- Possible causes of this diagnosis
- Recommended next steps
- Tips for management and when to seek help
- A positive, reassuring tone
"""
    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "https://yourdomain.com",
            "X-Title": "Symptom Checker"
        },
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content.strip()

# Emergency alert function

def send_emergency_alert(username, disease):
    try:
        sender_email = "youremail"
        receiver_email = "senderemail"

        # Get current location via IP
        location = requests.get("https://ipinfo.io").json()
        loc_text = f"Location: {location.get('city')}, {location.get('region')}, {location.get('country')} - {location.get('loc')}"

        msg = MIMEText(f"""
        Emergency Alert!\n
        User: {username}\n
        Diagnosis: {disease}\n
        {loc_text}
        """)
        msg['Subject'] = "Medical Emergency Alert"
        msg['From'] = sender_email
        msg['To'] = receiver_email

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login("sender mail", "app_password")
            server.sendmail(sender_email, receiver_email, msg.as_string())
        st.success("Emergency alert sent!")
    except Exception as e:
        st.error(f"Failed to send alert: {e}")
        
        
        


# Database setup
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    name TEXT,
    age INTEGER
)
""")
c.execute("""
CREATE TABLE IF NOT EXISTS profiles (
    username TEXT UNIQUE,
    medical_history TEXT,
    allergies TEXT
)
""")
conn.commit()

# Diagnosis function
def diagnose(symptoms_list):
    input_text = " ".join(symptoms_list).replace("_", " ").strip().lower()
    prediction = model.predict([input_text])[0]
    return prediction

# Login/Register Page
def login_page():
    st.title("Login or Register")
    choice = st.selectbox("Select Action", ["Login", "Register"])

    if choice == "Register":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=0, step=1)
        if st.button("Register"):
            try:
                c.execute("INSERT INTO users (username, password, name, age) VALUES (?, ?, ?, ?)",
                          (username, password, name, age))
                c.execute("INSERT INTO profiles (username, medical_history, allergies) VALUES (?, '', '')", (username,))
                conn.commit()
                st.success("User registered successfully. Please login.")
            except:
                st.error("Username already exists!")

    if choice == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = c.fetchone()
            if user:
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.success("Login successful!")
            else:
                st.error("Invalid credentials")

# Symptom Diagnostic Page
def symptom_diagnostic_page():
    st.title("Symptom Diagnostic Tool")
    symptoms = st.text_area("Enter your symptoms separated by spaces (e.g., itching skin_rash nodal_skin_eruptions)")

    if st.button("Diagnose"):
        symptoms_list = [s.strip().lower() for s in symptoms.split()]
        result = diagnose(symptoms_list)
        st.session_state['symptoms_list'] = symptoms_list
        st.session_state['diagnosis_result'] = result
        st.success(f"You may have: {result}")

    if 'diagnosis_result' in st.session_state and 'symptoms_list' in st.session_state:
        result = st.session_state['diagnosis_result']
        symptoms_list = st.session_state['symptoms_list']
        st.info(f"Diagnosis Result: {result}")

        if result.lower() in ["heart attack", "dengue", "malaria","pneumonia", "bronchial asthma"]: # emergency cases::
            if st.button("Emergency Alert"):
                send_emergency_alert(st.session_state['username'], result)

        if st.button("Generate Report"):
            with st.spinner("Generating report..."):
                report = generate_report(symptoms_list, result)
                st.markdown("### 📝 Health Report")
                st.info(report)
    st.markdown("""
---
### 🌎 Emergency Contacts in India
- **Medical Emergency (Ambulance):** 102
- **Police Emergency:** 100
- **Disaster Management:** 108
- **Women Helpline:** 1091
- **Senior Citizen Helpline:** 14567

_Note: Your location will be attached in emergency alerts for faster assistance._
""")
# Profile Page
def profile_page():
    st.title("User Profile")
    username = st.session_state['username']
    c.execute("SELECT medical_history, allergies FROM profiles WHERE username=?", (username,))
    profile = c.fetchone()

    if profile:
        medical_history = st.text_area("Medical History", profile[0])
        allergies = st.text_area("Allergies", profile[1])
        if st.button("Update Profile"):
            c.execute("UPDATE profiles SET medical_history=?, allergies=? WHERE username=?",
                      (medical_history, allergies, username))
            conn.commit()
            st.success("Profile updated successfully!")
    else:
        st.error("Profile not found")
    st.markdown("""
---
### 🌎 Emergency Contacts in India
- **Medical Emergency (Ambulance):** 102
- **Police Emergency:** 100
- **Disaster Management:** 108
- **Women Helpline:** 1091
- **Senior Citizen Helpline:** 14567

_Note: Your location will be attached in emergency alerts for faster assistance._
""")
# Main application logic
def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        login_page()
    else:
        page = st.sidebar.selectbox("Navigate", ["Symptom Diagnostic", "Profile", "Logout"])
        if page == "Symptom Diagnostic":
            symptom_diagnostic_page()
        elif page == "Profile":
            profile_page()
        elif page == "Logout":
            st.session_state['logged_in'] = False
            st.session_state.pop('username', None)
            st.session_state.pop('symptoms_list', None)
            st.session_state.pop('diagnosis_result', None)
            st.success("Logged out successfully!")

if __name__ == "__main__":
    main()



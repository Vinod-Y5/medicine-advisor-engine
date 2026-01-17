import streamlit as st
import sqlite3
import joblib
import smtplib
import os
import requests
import openai
from email.mime.text import MIMEText

# =========================
# OpenRouter Configuration
# =========================
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"
openai.api_headers = {
    "HTTP-Referer": "https://medicine-advisor-engine.streamlit.app",
    "X-Title": "Medicine Advisor Engine"
}

# =========================
# Load ML Model
# =========================
model = joblib.load("model/disease_prediction_model.joblib")

# =========================
# AI Health Report
# =========================
def generate_report(symptoms_list, predicted_disease):
    prompt = f"""
A patient has entered the following symptoms: {', '.join(symptoms_list)}.
They were diagnosed with: {predicted_disease}.

Please provide a health report in clear, friendly language that explains:
- Possible causes of this diagnosis
- Recommended next steps
- Tips for management and when to seek help
- A positive, reassuring tone
"""

    response = openai.ChatCompletion.create(
        model="openai/gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["choices"][0]["message"]["content"]

# =========================
# Emergency Alert (Optional)
# =========================
def send_emergency_alert(username, disease):
    try:
        sender_email = "youremail"
        receiver_email = "receiveremail"

        location = requests.get("https://ipinfo.io").json()
        loc_text = f"{location.get('city')}, {location.get('region')}, {location.get('country')}"

        msg = MIMEText(f"""
Emergency Alert!
User: {username}
Diagnosis: {disease}
Location: {loc_text}
""")
        msg["Subject"] = "Medical Emergency Alert"
        msg["From"] = sender_email
        msg["To"] = receiver_email

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("sender_email", "app_password")
            server.sendmail(sender_email, receiver_email, msg.as_string())

        st.success("Emergency alert sent!")

    except:
        st.warning("Emergency alert feature available but disabled in deployment.")

# =========================
# Database Setup
# =========================
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

# =========================
# Disease Prediction
# =========================
def diagnose(symptoms_list):
    text = " ".join(symptoms_list).replace("_", " ").lower()
    return model.predict([text])[0]

# =========================
# Login / Register
# =========================
def login_page():
    st.title("Login or Register")
    action = st.selectbox("Select Action", ["Login", "Register"])

    if action == "Register":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=0, step=1)

        if st.button("Register"):
            try:
                c.execute(
                    "INSERT INTO users VALUES (NULL, ?, ?, ?, ?)",
                    (username, password, name, age)
                )
                c.execute(
                    "INSERT INTO profiles VALUES (?, '', '')",
                    (username,)
                )
                conn.commit()
                st.success("Registered successfully. Please login.")
            except:
                st.error("Username already exists.")

    if action == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            c.execute(
                "SELECT * FROM users WHERE username=? AND password=?",
                (username, password)
            )
            if c.fetchone():
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.success("Login successful!")
            else:
                st.error("Invalid credentials.")

# =========================
# Symptom Diagnostic Page
# =========================
def symptom_diagnostic_page():
    st.title("Symptom Diagnostic Tool")

    symptoms = st.text_area("Enter symptoms separated by spaces")

    if st.button("Diagnose"):
        symptoms_list = symptoms.lower().split()
        result = diagnose(symptoms_list)
        st.session_state["symptoms"] = symptoms_list
        st.session_state["result"] = result
        st.success(f"Predicted Disease: {result}")

    if "result" in st.session_state:
        if st.button("Generate AI Health Report"):
            with st.spinner("Generating report..."):
                report = generate_report(
                    st.session_state["symptoms"],
                    st.session_state["result"]
                )
                st.info(report)

# =========================
# Profile Page
# =========================
def profile_page():
    st.title("User Profile")
    username = st.session_state["username"]

    c.execute("SELECT medical_history, allergies FROM profiles WHERE username=?", (username,))
    profile = c.fetchone()

    history = st.text_area("Medical History", profile[0])
    allergies = st.text_area("Allergies", profile[1])

    if st.button("Update Profile"):
        c.execute(
            "UPDATE profiles SET medical_history=?, allergies=? WHERE username=?",
            (history, allergies, username)
        )
        conn.commit()
        st.success("Profile updated.")

# =========================
# Main App
# =========================
def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        login_page()
    else:
        page = st.sidebar.selectbox(
            "Navigate",
            ["Symptom Diagnostic", "Profile", "Logout"]
        )

        if page == "Symptom Diagnostic":
            symptom_diagnostic_page()
        elif page == "Profile":
            profile_page()
        elif page == "Logout":
            st.session_state.clear()
            st.success("Logged out.")

if __name__ == "__main__":
    main()

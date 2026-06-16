import streamlit as st
from google import genai
import os

# Initialize the Gemini Client
# Best practice: Use st.secrets or set it directly for quick testing
client = genai.Client(api_key="AQ.Ab8RN6KmIXRuPLDYwBA9dqJ3GU7KvIv79-nXgF9UEv3acejfHw")

# Load external CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Language Dictionary for Multi-language Support
strings = {
    "English": {
        "title": "🎓 AI Final Year Project Guider",
        "login_hdr": "Student Login",
        "user": "Username",
        "pass": "Password",
        "login_btn": "Login",
        "welcome": "Welcome back, Student!",
        "select_dept": "Select your Engineering Department",
        "ask_placeholder": "e.g., Give me 3 innovative project ideas on Smart Grids with source code references...",
        "submit_btn": "Generate Project Guidance",
        "error_login": "Invalid Username or Password",
        "ai_response": "🤖 AI Guide Recommendations:"
    },
    "Hindi": {
        "title": "🎓 एआई फाइनल ईयर प्रोजेक्ट गाइड",
        "login_hdr": "छात्र लॉगिन",
        "user": "यूज़रनेम",
        "pass": "पासवर्ड",
        "login_btn": "लॉगिन करें",
        "welcome": "स्वागत है, छात्र!",
        "select_dept": "अपने इंजीनियरिंग विभाग का चयन करें",
        "ask_placeholder": "जैसे, मुझे स्मार्ट ग्रिड पर सोर्स कोड के साथ 3 इनोवेटिव प्रोजेक्ट आइडिया दें...",
        "submit_btn": "प्रोजेक्ट गाइडेंस जेनरेट करें",
        "error_login": "गलत यूज़रनेम या पासवर्ड",
        "ai_response": "🤖 एआई गाइड सुझाव:"
    },
    "Telugu": {
        "title": "🎓 AI ఫైనల్ ఇయర్ ప్రాజెక్ట్ గైడర్",
        "login_hdr": "విద్యార్థి లాగిన్",
        "user": "యూజర్ నేమ్",
        "pass": "పాస్‌వర్డ్",
        "login_btn": "లాగిన్ అవ్వండి",
        "welcome": "స్వాగతం, విద్యార్థి!",
        "select_dept": "మీ ఇంజనీరింగ్ విభాగాన్ని ఎంచుకోండి",
        "ask_placeholder": "ఉదాహరణకు, సోర్స్ కోడ్ రిఫరెన్స్‌లతో స్మార్ట్ గ్రిడ్‌లపై 3 వినూత్న ప్రాజెక్ట్ ఆలోచనలను ఇవ్వండి...",
        "submit_btn": "ప్రాజెక్ట్ గైడెన్స్ పొందండి",
        "error_login": "తప్పు యూజర్ నేమ్ లేదా పాస్‌వర్డ్",
        "ai_response": "🤖 AI గైడ్ సిఫార్సులు:"
    }
}

# 1. Language Selector Sidebar
lang = st.sidebar.selectbox("🌐 Choose Language / భాషను ఎంచుకోండి / भाषा चुनें", ["English", "Hindi", "Telugu"])
txt = strings[lang]

st.title(txt["title"])

# 2. Session State for Login Tracking
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# 3. Login Page Logic
if not st.session_state["logged_in"]:
    st.markdown(f'<div class="login-card"><h3>{txt["login_hdr"]}</h3></div>', unsafe_allow_html=True)
    username = st.text_input(txt["user"])
    password = st.text_input(txt["pass"], type="password")
    
    if st.button(txt["login_btn"]):
        # Simple mock credentials for testing (Change these as needed!)
        if username == "student" and password == "project2026":
            st.session_state["logged_in"] = True
            st.rerun()
        else:
            st.error(txt["error_login"])

# 4. Main Application Dashboard (Post-Login)
else:
    st.sidebar.success(txt["welcome"])
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.rerun()

    # Department Selection
    dept = st.selectbox(
        txt["select_dept"],
        ["CSE (Computer Science)", "IT (Information Technology)", "ECE (Electronics & Communication)", 
         "EEE (Electrical & Electronics)", "Civil Engineering", "Mechanical Engineering"]
    )

    # User input query for the AI Agent
    user_query = st.text_area("💡 What kind of project help do you need?", placeholder=txt["ask_placeholder"])

    if st.button(txt["submit_btn"]):
        if user_query:
            with st.spinner("Processing your project details..."):
                try:
                    # Construct system prompt keeping language and department in context
                    prompt_context = f"You are an expert engineering college professor and final year project guide. \
                    The student belongs to the {dept} department. \
                    Provide detailed project ideas, modules, technologies to use, and step-by-step execution guidance. \
                    Strictly reply in the language requested: {lang}."
                    
                    # Call Gemini API
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=f"{prompt_context}\n\nStudent Request: {user_query}"
                    )
                    
                    st.write("---")
                    st.subheader(txt["ai_response"])
                    st.write(response.text)
                    
                except Exception as e:
                    st.error(f"Error connecting to AI Agent: {e}")
        else:
            st.warning("Please type a query or topic first!")
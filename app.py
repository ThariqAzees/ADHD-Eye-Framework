import streamlit as st

# Set page config at the entry point of the multi-page application
st.set_page_config(
    page_title="ADHD Eye Framework",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply global custom styles for the premium dark theme
st.markdown("""
    <style>
        /* Base styles */
        .reportview-container {
            background: #0E1117;
        }
        .sidebar .sidebar-content {
            background: #161B22;
        }
        
        /* Glassmorphism custom cards */
        .custom-card {
            background: #161B22;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        
        /* Accent elements */
        .accent-text {
            color: #00E5FF;
            font-weight: bold;
        }
        
        /* Header styling */
        h1, h2, h3 {
            color: #FFFFFF !important;
            font-family: 'Outfit', 'Inter', sans-serif;
        }
        
        /* Styled disclaimers */
        .disclaimer-box {
            background-color: rgba(210, 153, 34, 0.1);
            border-left: 4px solid #D29922;
            padding: 16px;
            border-radius: 4px;
            margin: 16px 0;
            color: #C9D1D9;
        }
    </style>
""", unsafe_allow_html=True)

# Programmatically redirect to the Home page
st.switch_page("pages/Home.py")

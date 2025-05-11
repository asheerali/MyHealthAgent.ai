import streamlit as st
from meal_planner import show_meal_planner_page
from exercise_planner import show_exercise_planner_page
from bmi_calculator import show_bmi_calculator_page

# ---------------------------- Styling ----------------------------
st.set_page_config(page_title="MyHealthAgent.ai", layout="centered")
st.markdown("""
    <style>
        .stTextInput > div > input, .stNumberInput input {
            background-color: #f4f6fa;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 10px;  /* Added margin below inputs */
        }
        .stRadio > div {
            display: flex;
            gap: 20px;  /* Increased gap between radio options */
            margin: 10px 0;  /* Added margin above and below */
        }
        .stForm {
            padding: 20px;  /* Added padding inside forms */
            margin-bottom: 20px;  /* Added margin below forms */
        }
        .stForm button {
            background-color: #6c63ff;
            color: white;
            font-weight: bold;
            padding: 0.5rem 1rem;
            border-radius: 10px;
            margin-top: 20px;  /* Added margin above buttons */
        }
        .stForm button:hover {
            background-color: #4e47d0;
        }
        div[data-testid="stHorizontalBlock"] {
            gap: 20px !important;  /* Added important to ensure this gap applies */
            margin: 10px 0;  /* Added margin above and below */
        }
        /* Styling for main tabs */
        .main-tabs {
            display: flex;
            gap: 20px;  /* Added gap between main tab buttons */
            margin-bottom: 30px;  /* Added margin below tabs */
        }
        /* Add space between sections */
        .section-divider {
            margin: 30px 0;  /* Increased margin for section dividers */
        }
        /* Form container styling */
        .form-container {
            background-color: #f8f9fa;
            padding: 25px;
            border-radius: 10px;
            margin: 20px 0;
            border: 1px solid #e9ecef;
        }
        /* Header styling */
        h1, h2, h3 {
            margin-bottom: 20px !important;  /* Added important to ensure this margin applies */
        }
        /* Add space below selectbox elements */
        .stSelectbox {
            margin-bottom: 15px;
        }
        /* Space out multi-column layouts */
        .row-widget.stRadio > div {
            padding: 10px 0;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------- Title ----------------------------
st.markdown(
    "<h1 style='text-align: center; margin-bottom: 30px;'> <span style='color:#6c63ff;'>MyHealthAgent.ai</span></h1>",
    unsafe_allow_html=True
)

# ---------------------------- Tab Selection ----------------------------
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "Meal Planner"

# Add 'main-tabs' class to the container for proper spacing
st.markdown('<div class="main-tabs">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🍽️ Meal Planner", key="meal_tab", 
                use_container_width=True, 
                type="primary" if st.session_state.current_tab == "Meal Planner" else "secondary"):
        st.session_state.current_tab = "Meal Planner"
        st.rerun()

with col2:
    if st.button("💪 Exercise Planner", key="exercise_tab", 
                use_container_width=True,
                type="primary" if st.session_state.current_tab == "Exercise Planner" else "secondary"):
        st.session_state.current_tab = "Exercise Planner"
        st.rerun()

with col3:
    if st.button("📊 BMI Calculator", key="bmi_tab", 
                use_container_width=True,
                type="primary" if st.session_state.current_tab == "BMI Calculator" else "secondary"):
        st.session_state.current_tab = "BMI Calculator"
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# More visible divider
st.markdown("<div class='section-divider'><hr style='height: 2px; background-color: #e9ecef;'></div>", unsafe_allow_html=True)

# ---------------------------- Page Routing ----------------------------
# Add form-container class around the content
st.markdown("<div class='form-container'>", unsafe_allow_html=True)
if st.session_state.current_tab == "Meal Planner":
    show_meal_planner_page()
elif st.session_state.current_tab == "Exercise Planner":
    show_exercise_planner_page()
elif st.session_state.current_tab == "BMI Calculator":
    show_bmi_calculator_page()
st.markdown("</div>", unsafe_allow_html=True)
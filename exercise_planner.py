import streamlit as st
from tools.exercise_planner import generate_exercise_plan
from tools.email_sender import send_email
import os

def show_exercise_planner_page():
    """Display and handle the exercise planner page functionality"""
    
    st.markdown("### Exercise Plan Generator")
    
    with st.form("exercise_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # weight = st.number_input("Your Weight (kg)", min_value=30, max_value=250, value=70)
            weight = st.text_input("Your Weight (kg)", value=70)
            fitness_level = st.radio("Fitness Level", ["Beginner", "Intermediate", "Advanced"], index=0)
        
        with col2:
            body_goal = st.selectbox(
                "Body Goal", 
                ["Weight Loss", "Muscle Gain", "Toning", "Endurance", "General Fitness"]
            )
            days_per_week = st.slider("Days per Week", min_value=1, max_value=7, value=3)
        
        additional_info = st.text_area("Additional Information", 
            placeholder="Any injuries, preferences, or specific areas to focus on?")
        
        user_email = st.text_input("Email for Plan", placeholder="Please enter your email")
        email = user_email if user_email else os.getenv("RECEIVER_EMAIL", "")
        
        submitted = st.form_submit_button("🏋️ Generate Exercise Plan")
    
    if submitted:
        with st.spinner("Generating your personalized exercise plan..."):
            plan_response = generate_exercise_plan.invoke({
                "weight": weight,
                "fitness_level": fitness_level,
                "body_goal": body_goal,
                "days_per_week": days_per_week,
                "additional_info": additional_info
            })
            
            st.markdown("## Your Personalized Exercise Plan")
            st.markdown(plan_response)
            
            send_email.invoke({
                "subject": f"Your {body_goal} Exercise Plan 💪",
                "body": plan_response,
                "recipient_override": email
            })
            
            st.success("✅ Exercise plan sent via email!")
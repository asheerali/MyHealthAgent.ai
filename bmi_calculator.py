import streamlit as st
from tools.email_sender import send_email
import os

def calculate_bmi(weight, height):
    """Calculate BMI using weight (kg) and height (cm)"""
    # Convert height from cm to meters
    height_m = height / 100
    # BMI formula: weight (kg) / (height (m))^2
    bmi = weight / (height_m ** 2)
    return round(bmi, 1)

def get_bmi_category(bmi):
    """Return BMI category based on BMI value"""
    if bmi < 18.5:
        return "Underweight", "Your BMI suggests you are underweight. This could indicate nutritional deficiencies or other health issues. Consider focusing on nutrient-dense foods to gain weight in a healthy way."
    elif 18.5 <= bmi < 25:
        return "Normal weight", "Your BMI falls within the normal range. This is generally associated with good health. Focus on maintaining your weight through balanced nutrition and regular physical activity."
    elif 25 <= bmi < 30:
        return "Overweight", "Your BMI suggests you are overweight. This may increase your risk for certain health conditions. Consider adjusting your diet and increasing physical activity to achieve a healthier weight."
    elif 30 <= bmi < 35:
        return "Obesity (Class 1)", "Your BMI indicates Class 1 obesity. This increases your risk for health conditions like heart disease and diabetes. A healthy eating plan and regular exercise can help you lose weight gradually."
    elif 35 <= bmi < 40:
        return "Obesity (Class 2)", "Your BMI indicates Class 2 obesity. This significantly increases health risks. Consider consulting a healthcare provider for personalized weight management strategies."
    else:
        return "Obesity (Class 3)", "Your BMI indicates Class 3 obesity, which is associated with serious health risks. It's important to work with healthcare professionals to develop a comprehensive weight management plan."

def get_recommended_calorie_intake(weight, height, age, gender, activity_level):
    """Calculate recommended daily calorie intake based on person's stats"""
    # Calculate BMR (Basal Metabolic Rate) using the Mifflin-St Jeor Equation
    if gender.lower() == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    
    # Apply activity multiplier
    activity_multipliers = {
        "Sedentary (little or no exercise)": 1.2,
        "Lightly active (light exercise 1-3 days/week)": 1.375,
        "Moderately active (moderate exercise 3-5 days/week)": 1.55,
        "Very active (hard exercise 6-7 days/week)": 1.725,
        "Super active (very hard exercise & physical job)": 1.9
    }
    
    maintenance_calories = round(bmr * activity_multipliers[activity_level])
    
    return maintenance_calories

def generate_bmi_analysis(name, weight, height, age, gender, activity_level):
    """Generate a comprehensive BMI analysis report"""
    bmi = calculate_bmi(weight, height)
    category, description = get_bmi_category(bmi)
    maintenance_calories = get_recommended_calorie_intake(weight, height, age, gender, activity_level)
    
    weight_loss_calories = maintenance_calories - 500
    weight_gain_calories = maintenance_calories + 500
    
    analysis = f"""# BMI Analysis for {name}

## BMI Results
**Your BMI**: {bmi}
**Category**: {category}

{description}

## Body Statistics
- **Weight**: {weight} kg
- **Height**: {height} cm
- **Age**: {age} years
- **Gender**: {gender}
- **Activity Level**: {activity_level}

## Calorie Recommendations
- **Maintenance**: {maintenance_calories} calories/day (to maintain current weight)
- **Weight Loss**: {weight_loss_calories} calories/day (for healthy weight loss of ~0.5kg/week)
- **Weight Gain**: {weight_gain_calories} calories/day (for healthy weight gain of ~0.5kg/week)

## Health Recommendations
"""
    
    # Add specific recommendations based on BMI category
    if bmi < 18.5:
        analysis += """
1. **Increase calorie intake** with nutrient-dense foods like nuts, avocados, and whole grains
2. **Incorporate strength training** to build muscle mass
3. **Eat frequent, smaller meals** if you struggle with large portions
4. **Consider protein supplements** if you have difficulty meeting protein needs
5. **Monitor your progress** with regular weight checks and health assessments
"""
    elif 18.5 <= bmi < 25:
        analysis += """
1. **Maintain balanced nutrition** with plenty of fruits, vegetables, whole grains, and lean proteins
2. **Stay physically active** with a mix of cardio and strength training exercises
3. **Practice portion control** to maintain your healthy weight
4. **Stay hydrated** by drinking plenty of water throughout the day
5. **Continue regular health check-ups** to monitor your overall health
"""
    else:  # BMI >= 25
        analysis += """
1. **Focus on portion control** and mindful eating practices
2. **Increase physical activity** gradually, aiming for at least 150 minutes of moderate activity per week
3. **Choose nutrient-dense foods** over calorie-dense options
4. **Monitor and reduce added sugar and processed foods** in your diet
5. **Consider consulting a healthcare provider** for personalized guidance
6. **Set realistic goals** for gradual, sustainable weight loss (0.5-1kg per week)
"""
    
    return analysis

def show_bmi_calculator_page():
    """Display and handle the BMI calculator page functionality"""
    
    st.markdown("### BMI Calculator & Health Analysis")
    
    # Add some space
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    with st.form("bmi_form"):
        name = st.text_input("Your Name", placeholder="Enter your name")
        
        # Add spacing between rows
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        
        # Use columns with more spacing
        col1, spacer1, col2 = st.columns([5, 1, 5])
        with col1:
            # weight = st.number_input("Weight (kg)", min_value=30.0, max_value=250.0, value=70.0, step=0.1)
            weight = st.text_input("Weight (kg)", value=70.0)
            weight = float(weight)
            # print("this is the weight ",weight)
            st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
            # height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=170.0, step=0.1)
            height = st.text_input("Height (cm)", value=170.0)
            height = float(height)
            st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
            # age = st.number_input("Age", min_value=18, max_value=100, value=30)
            age = st.text_input("Age", value=30)
            age = int(age)
        
        with col2:
            st.markdown("<div style='margin-bottom: 10px;'><b>Gender</b></div>", unsafe_allow_html=True)
            gender = st.radio("Gender", ["Male", "Female"], index=0, label_visibility="collapsed")
            
            st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
            
            st.markdown("<div style='margin-bottom: 10px;'><b>Activity Level</b></div>", unsafe_allow_html=True)
            activity_level = st.selectbox(
                "Activity Level", 
                [
                    "Sedentary (little or no exercise)",
                    "Lightly active (light exercise 1-3 days/week)",
                    "Moderately active (moderate exercise 3-5 days/week)",
                    "Very active (hard exercise 6-7 days/week)",
                    "Super active (very hard exercise & physical job)"
                ],
                index=1,
                label_visibility="collapsed"
            )
        
        # Add some space
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        
        user_email = st.text_input("Email for BMI Report", placeholder="Please enter your email")
        
        # Add some space before button
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        submitted = st.form_submit_button("📊 Calculate & Send BMI Analysis")
    
    if submitted:
        with st.spinner("Analyzing your BMI and health metrics..."):
            email = user_email if user_email else os.getenv("RECEIVER_EMAIL", "")
            bmi = calculate_bmi(weight, height)
            category, _ = get_bmi_category(bmi)
            
            # Add space
            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
            
            st.markdown(f"## Your BMI Results")
            
            # Create a colored box for the BMI result
            color = ""
            if bmi < 18.5:
                color = "#3a86ff"  # Blue
            elif 18.5 <= bmi < 25:
                color = "#2ecc71"  # Green
            elif 25 <= bmi < 30:
                color = "#f39c12"  # Orange
            else:
                color = "#e74c3c"  # Red
                
            st.markdown(
                f"""
                <div style="padding: 20px; border-radius: 10px; background-color: {color}; color: white; margin: 20px 0;">
                    <h3 style="margin: 0;">BMI: {bmi}</h3>
                    <p style="margin: 10px 0 0 0; font-size: 16px;">Category: {category}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Generate the full analysis
            full_analysis = generate_bmi_analysis(name, weight, height, age, gender, activity_level)
            st.markdown(full_analysis)
            
            # Send email with the analysis
            send_email.invoke({
                "subject": f"Your BMI Analysis and Health Recommendations",
                "body": full_analysis,
                "recipient_override": email
            })
            
            # Success message with better styling
            st.markdown(
                """
                <div style="padding: 15px; background-color: #d4edda; color: #155724; border-radius: 5px; margin: 20px 0;">
                    <p style="margin: 0; font-weight: bold;">✅ BMI Analysis sent via email!</p>
                </div>
                """,
                unsafe_allow_html=True
            )
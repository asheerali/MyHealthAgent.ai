import os
import google.generativeai as genai
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@tool
def generate_exercise_plan(weight: int, fitness_level: str, body_goal: str, days_per_week: int, additional_info: str = "") -> str:
    """Generates a personalized exercise plan based on user information using Gemini."""
    
    prompt = f"""
    Create a detailed {days_per_week}-day exercise plan for someone with the following profile:
    - Weight: {weight} kg
    - Fitness level: {fitness_level}
    - Goal: {body_goal}
    - Days available for exercise per week: {days_per_week}
    
    Additional information: {additional_info}
    
    Format the exercise plan with:
    1. A brief overview of the plan and why it's suitable for this profile
    2. Days of the week with specific workouts
    3. For each exercise include:
       - Name of exercise
       - Number of sets and reps
       - Rest periods
       - Brief form instructions
    4. A section with progressive overload recommendations
    5. Recovery and nutrition tips specific to this goal
    
    Make the plan challenging but realistic for someone at a {fitness_level.lower()} level.
    Use markdown formatting to make the plan easy to read.
    """
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    print("Exercise plan generated.")
    return response.text
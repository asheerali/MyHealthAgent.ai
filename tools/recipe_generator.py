import os
import google.generativeai as genai
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@tool
def generate_recipe(meal: str, mode: str, custom_prompt: str = "") -> str:
    """Generates a clearly structured recipe for a given meal and diet mode using Gemini."""
    base_prompt = (
        f"Suggest a {meal} recipe for {'someone dieting' if mode == 'dieting' else 'someone not dieting'}."
    )

    if custom_prompt:
        base_prompt += f" The user wants: {custom_prompt}."

    base_prompt += (
        " Return your response in the following exact format:\n\n"
        "Name: <Recipe Name>\n"
        "Ingredients:\n- item 1\n- item 2\n...\n"
        "Recipe:\nStep-by-step cooking instructions.\n\n"
        "Video Tutorials:\n"
        "- Suggest one best YouTube tutorial links with titles. Format each as 'Title: [YouTube URL]'\n"
        "- These should be relevant tutorials for this exact recipe or very similar dishes\n"
        "- Use real YouTube URLs in the format https://www.youtube.com/watch?v=XXXXXXXXXXX\n\n"
        "Make sure the name does NOT include calories.\n"
        "Do NOT use markdown or bold formatting.\n"
    )

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(base_prompt)
    print("response:", response.text)
    return response.text
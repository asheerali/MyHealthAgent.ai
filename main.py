import os
import re
from dotenv import load_dotenv
from tools.recipe_generator import generate_recipe
from tools.email_sender import send_email

load_dotenv()

# def parse_recipe(raw_text: str):
#     """Parses recipe text in strict 'Name/Ingredients/Recipe' format."""
#     name_match = re.search(r'Name:\s*(.*)', raw_text)
#     ingredients_match = re.search(r'Ingredients:\s*([\s\S]*?)Recipe:', raw_text)
#     recipe_match = re.search(r'Recipe:\s*([\s\S]*)', raw_text)

#     name = name_match.group(1).strip() if name_match else "Unknown Recipe"
#     ingredients = ingredients_match.group(1).strip() if ingredients_match else "Not provided"
#     recipe = recipe_match.group(1).strip() if recipe_match else "Not provided"

#     return name, ingredients, recipe


def parse_recipe(raw_text: str):
    """Parses recipe text in strict 'Name/Ingredients/Recipe/Video Tutorials' format."""
    name_match = re.search(r'Name:\s*(.*)', raw_text)
    ingredients_match = re.search(r'Ingredients:\s*([\s\S]*?)Recipe:', raw_text)
    recipe_match = re.search(r'Recipe:\s*([\s\S]*?)(?:Video Tutorials:|$)', raw_text)
    tutorials_match = re.search(r'Video Tutorials:\s*([\s\S]*?)(?:$)', raw_text)

    name = name_match.group(1).strip() if name_match else "Unknown Recipe"
    ingredients = ingredients_match.group(1).strip() if ingredients_match else "Not provided"
    recipe = recipe_match.group(1).strip() if recipe_match else "Not provided"
    tutorials = tutorials_match.group(1).strip() if tutorials_match else ""

    return name, ingredients, recipe, tutorials


def run_daily_recipes():
    mode = input("Are you dieting? (yes/no) [default: yes]: ").strip().lower()
    mode = "dieting" if mode in ["", "yes", "y"] else "not dieting"

    default_email = os.getenv("RECEIVER_EMAIL")
    recipient = input(f"Enter recipient email [default: {default_email}]: ").strip()
    recipient = recipient if recipient else default_email

    custom_prompt = input("What kind of meal would you like? (e.g., high protein, vegan pasta): ").strip()

    calories_breakfast = input("Calories for breakfast? (e.g., 300): ").strip()
    calories_lunch = input("Calories for lunch? (e.g., 500): ").strip()
    calories_dinner = input("Calories for dinner? (e.g., 600): ").strip()

    calories_breakfast = calories_breakfast if calories_breakfast.isdigit() else "300"
    calories_lunch = calories_lunch if calories_lunch.isdigit() else "500"
    calories_dinner = calories_dinner if calories_dinner.isdigit() else "600"

    calorie_dict = {
        "breakfast": calories_breakfast,
        "lunch": calories_lunch,
        "dinner": calories_dinner,
    }

    meals = ["breakfast", "lunch", "dinner"]
    recipes = []

    for meal in meals:
        prompt = f"{custom_prompt} for {meal}, around {calorie_dict[meal]} calories. Dieting: {mode == 'dieting'}"
        raw_response = generate_recipe.invoke({
            "meal": meal,
            "mode": mode,
            "custom_prompt": prompt
        })

        name, ingredients, recipe_steps = parse_recipe(raw_response)

        formatted_recipe = (
            f"{meal.capitalize()} ({calorie_dict[meal]} calories)\n"
            # f"name: {name} ({calorie_dict[meal]} calories)\n\n"
            f"Name: {name} ({calorie_dict[meal]} calories)\n\n"
            f"Ingredients:\n{ingredients}\n\n"
            f"Recipe:\n{recipe_steps}\n"
        )

        recipes.append(formatted_recipe)

    full_email_body = "\n\n".join(recipes)

    send_email.invoke({
        "subject": f"Your {mode.capitalize()} Recipes for Today 🍽️",
        "body": full_email_body,
        "recipient_override": recipient
    })

if __name__ == "__main__":
    run_daily_recipes()

import streamlit as st
from tools.recipe_generator import generate_recipe
from tools.email_sender import send_email
from main import parse_recipe
import os
import re

def show_meal_planner_page():
    """Display and handle the meal planner page functionality"""

    st.markdown("### Meal Planner")

    # Global custom style (CSS)
    st.markdown(
        """
        <style>
            .youtube-link {
                text-decoration: none;
                color: #007bff;
            }
            .youtube-link:hover {
                text-decoration: underline;
            }
            .success-message {
                padding: 15px;
                background-color: #d4edda;
                color: #155724;
                border-radius: 5px;
                margin: 20px 0;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Spacing
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # ---------------------------- Form ----------------------------
    with st.form("recipe_form"):
        st.markdown("<p style='font-size: 18px; font-weight: bold; margin-bottom: 15px;'>Preferences</p>", unsafe_allow_html=True)

        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("<div style='margin-bottom: 10px;'><b>Diet Mode:</b></div>", unsafe_allow_html=True)
            mode = st.radio("Are you dieting?", ["Yes", "No"], index=0, horizontal=True, label_visibility="collapsed")
        with col2:
            custom_prompt = st.text_input("Meal Preference", placeholder="e.g., High protein vegan pasta")

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        user_email = st.text_input("Recipient Email", placeholder="Please enter your email")
        email = user_email if user_email else os.getenv("RECEIVER_EMAIL", "")

        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

        st.markdown("<p style='font-size: 18px; font-weight: bold; margin-bottom: 15px;'>🔥 Calories</p>", unsafe_allow_html=True)
        c1, _, c2, _, c3 = st.columns([3, 0.5, 3, 0.5, 3])
        with c1:
            calories_breakfast = st.text_input("Breakfast", value="300")
        with c2:
            calories_lunch = st.text_input("Lunch", value="500")
        with c3:
            calories_dinner = st.text_input("Dinner", value="600")

        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🍳 Generate & Send Recipes")

    # ---------------------------- Recipe Generation ----------------------------
    if submitted:
        mode_flag = "dieting" if mode.lower() == "yes" else "not dieting"
        calorie_dict = {
            "breakfast": calories_breakfast,
            "lunch": calories_lunch,
            "dinner": calories_dinner,
        }

        meals = ["breakfast", "lunch", "dinner"]
        recipes = []

        with st.spinner("Generating recipes..."):
            for meal in meals:
                prompt = f"{custom_prompt} for {meal}, around {calorie_dict[meal]} calories. Dieting: {mode_flag == 'dieting'}"
                raw_response = generate_recipe.invoke({
                    "meal": meal,
                    "mode": mode_flag,
                    "custom_prompt": prompt
                })

                name, ingredients, recipe, tutorials = parse_recipe(raw_response)

                # Extract YouTube links
                tutorial_links_html = ""
                if tutorials:
                    tutorial_links_html = "<div class='tutorial-section'><h4>📹 Video Tutorials:</h4>"
                    youtube_links = re.findall(r'(.*?):\s*(https://www\.youtube\.com/watch\?v=[\w-]+)', tutorials)
                    if youtube_links:
                        for title, url in youtube_links:
                            clean_title = title.strip('- ').strip()
                            tutorial_links_html += f'<a href="{url}" target="_blank" class="youtube-link">▶️ {clean_title}</a><br>'
                    else:
                        tutorial_links_html += f"<p>{tutorials}</p>"
                    tutorial_links_html += "</div>"

                # HTML card
                st.markdown(
                    f"""
                    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #e9ecef;">
                        <h3>{meal.capitalize()} ({calorie_dict[meal]} calories)</h3>
                        <h4>Name: {name}</h4>
                        <p><strong>Ingredients:</strong><br>{ingredients.replace('- ', '• ')}</p>
                        <p><strong>Recipe:</strong><br>{recipe}</p>
                        <p><strong>Video Tutorials:</strong><br>{tutorial_links_html}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                recipes.append(f"### {meal.capitalize()} ({calorie_dict[meal]} calories)\n"
                               f"**Name:** {name}\n\n"
                               f"**Ingredients:**\n{ingredients}\n\n"
                               f"**Recipe:**\n{recipe}\n\n"
                               f"**Video Tutorials:**\n{tutorials}")

        full_body = "\n\n".join(recipes)

        send_email.invoke({
            "subject": f"Your {mode_flag.capitalize()} Recipes for Today",
            "body": full_body,
            "recipient_override": email
        })

        # Confirmation
        st.markdown(
            '<div class="success-message">✅ Recipes sent via email!</div>',
            unsafe_allow_html=True
        )

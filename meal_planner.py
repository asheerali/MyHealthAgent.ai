import streamlit as st
from tools.recipe_generator import generate_recipe
from tools.email_sender import send_email
from main import parse_recipe
import os
import re

def show_meal_planner_page():
    """Display and handle the meal planner page functionality"""
    
    st.markdown("### Meal Planner")
    
    # Add some space
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # ---------------------------- Form ----------------------------
    with st.form("recipe_form"):
        st.markdown("<p style='font-size: 18px; font-weight: bold; margin-bottom: 15px;'>Preferences</p>", unsafe_allow_html=True)

        # Add space between sections
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("<div style='margin-bottom: 10px;'><b>Diet Mode:</b></div>", unsafe_allow_html=True)
            mode = st.radio("Are you dieting?", ["Yes", "No"], index=0, horizontal=True, label_visibility="collapsed")
        with col2:
            custom_prompt = st.text_input("Meal Preference", placeholder="e.g., High protein vegan pasta")

        # Add spacing
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        user_email = st.text_input("Recipient Email", placeholder="Please enter your email")
        email = user_email if user_email else os.getenv("RECEIVER_EMAIL", "")

        # Add spacing
        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
        
        st.markdown("<p style='font-size: 18px; font-weight: bold; margin-bottom: 15px;'>🔥 Calories</p>", unsafe_allow_html=True)
        c1, spacer1, c2, spacer2, c3 = st.columns([3, 0.5, 3, 0.5, 3])
        with c1:
            # st.markdown("<div style='text-align: center;'><b>Breakfast</b></div>", unsafe_allow_html=True)
            # calories_breakfast = st.number_input("Breakfast", value=300, step=50, label_visibility="collapsed")
            calories_breakfast = st.text_input("Breakfast", value= 300 )
        with c2:
            # st.markdown("<div style='text-align: center;'><b>Lunch</b></div>", unsafe_allow_html=True)
            # calories_lunch = st.number_input("Lunch", value=500, step=50, label_visibility="collapsed")
            calories_lunch = st.text_input("Lunch", value= 500 )
        with c3:
            # st.markdown("<div style='text-align: center;'><b>Dinner</b></div>", unsafe_allow_html=True)
            # calories_dinner = st.number_input("Dinner", value=600, step=50, label_visibility="collapsed")
            calories_dinner = st.text_input("Dinner", value= 600 )

        # Add spacing before button
        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
        
        submitted = st.form_submit_button("🍳 Generate & Send Recipes")

    # ---------------------------- Recipe Generation ----------------------------
    if submitted:
        mode_flag = "dieting" if mode.lower() == "yes" else "not dieting"
        calorie_dict = {
            "breakfast": str(calories_breakfast),
            "lunch": str(calories_lunch),
            "dinner": str(calories_dinner),
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
                print("tutorials", tutorials[1], "tutorial2 ", tutorials[2])
                print("DEBUG - Raw tutorials:", repr(tutorials))  # Shows exact content with special chars
                print("DEBUG - Tutorial type:", type(tutorials))  # Shows if it's a string, list, etc.
                print("DEBUG - Tutorial length:", len(tutorials) if tutorials else "Empty")

# Process the tutorials to extract links
                tutorial_links_html = ""
                if tutorials:
                    tutorial_links_html = "<div class='tutorial-section'><h4>📹 Video Tutorials:</h4>"
                    
                    # Use regex to find YouTube links
                    youtube_links = re.findall(r'(.*?):\s*(https://www\.youtube\.com/watch\?v=[a-zA-Z0-9_-]+)', tutorials)
                    
                    if youtube_links:
                        for title, url in youtube_links:
                            clean_title = title.strip('- ').strip()
                            tutorial_links_html += f"""
                            <a href="{url}" target="_blank" class="youtube-link">
                                <i>▶️</i> {clean_title}
                            </a><br>
                            """
                    else:
                        # If no links were found with the expected format, just display the raw text
                        tutorial_links_html += f"<p>{tutorials}</p>"
                    
                    tutorial_links_html += "</div>"

                formatted = (
                    f"### {meal.capitalize()} ({calorie_dict[meal]} calories)\n"
                    f"**Name:** {name}\n\n"
                    f"**Ingredients:**\n{ingredients}\n\n"
                    f"**Recipe:**\n{recipe}"
                      f"**Video Tutorials:**\n{tutorials}"
                  
                )
                
                # Add styled recipe card
                st.markdown(
                    f"""
                    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid #e9ecef;">
                        <h3>{meal.capitalize()} ({calorie_dict[meal]} calories)</h3>
                        <h4>Name: {name}</h4>
                        <p><strong>Ingredients:</strong><br>{ingredients.replace('- ', '• ')}</p>
                        <p><strong>Recipe:</strong><br>{recipe}</p>
                        <p><strong>Video Tutorials:</strong><br>{tutorial_links_html}</p>
                        
                        <style>
                            .youtube-link {{
                                text-decoration: none;
                                color: #007bff;
                            }}
                            .youtube-link:hover {{
                                text-decoration: underline;
                            }}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                recipes.append(formatted)

        full_body = "\n\n".join(recipes)

        send_email.invoke({
            "subject": f"Your {mode_flag.capitalize()} Recipes for Today 🍽️",
            "body": full_body,
            "recipient_override": email
        })

        # Success message with better styling
        st.markdown(
            """
            <div style="padding: 15px; background-color: #d4edda; color: #155724; border-radius: 5px; margin: 20px 0;">
                <p style="margin: 0; font-weight: bold;">✅ Recipes sent via email!</p>
            </div>
            """,
            unsafe_allow_html=True
        )
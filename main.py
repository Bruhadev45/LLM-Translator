# A simple Streamlit app to translate text into various Indian languages using OpenAI.

import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Fire up the environment variables from the .env file.
load_dotenv()

# Basic page setup. This should be the first Streamlit command.
st.set_page_config(
    page_title="Indian Language Translator",
    page_icon="🇮🇳",
    layout="wide"
)

# This is our core translation logic.
# We cache the results so we don't waste API calls (and money!) on the same translation.
@st.cache_data
def get_translation(api_key, text_to_translate, target_language, model="gpt-4o"):
    """Pings the OpenAI API to get the translation."""

    # Don't bother calling the API if the user hasn't typed anything.
    if not text_to_translate.strip():
        st.info("Start by typing something in the text box.")
        return ""

    # A good practice to wrap API calls in a try-except block to handle network issues or API errors gracefully.
    try:
        client = OpenAI(api_key=api_key)

        # Here, we're crafting the prompt. A good prompt is key to getting good results.
        # The system message sets the 'personality' of the AI.
        system_prompt = {
            "role": "system",
            "content": "You are a skilled translator for Indian languages. Your translations should be accurate, natural, and culturally fitting."
        }
        # The user message gives the actual instruction.
        user_prompt = {
            "role": "user",
            "content": f"Please translate the following text into {target_language}:\n\n---\n{text_to_translate}\n---"
        }

        # Let the user know something is happening in the background.
        with st.spinner(f"Translating to {target_language}..."):
            # The actual API call.
            response = client.chat.completions.create(
                model=model,
                messages=[system_prompt, user_prompt],
                temperature=0.3, # Lower temp makes the model more predictable.
                max_tokens=2000
            )
        
        # Dig out the translated text from the API response.
        return response.choices[0].message.content.strip()

    except Exception as e:
        # Let the user know if their API key is bad or if something else went wrong.
        if "Incorrect API key" in str(e):
            st.error("Your OpenAI API key in the .env file seems to be incorrect. Please check it.")
        else:
            st.error(f"An unexpected error occurred: {e}")
        return ""

# --- App's Main Interface ---

# Fetch the API key from environment variables.
API_KEY = os.getenv("OPENAI_API_KEY")

st.title("🇮🇳 Indian Language Translator")
st.markdown("Translate text into major Indian languages with OpenAI.")

# We need session_state to remember what the user has typed, even when the app reruns.
# Initialize our text fields if they don't already exist.
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "translation_result" not in st.session_state:
    st.session_state.translation_result = "Your translation will appear here..."

# A simple function to reset the text fields back to their original state.
def clear_text_fields():
    """This is a callback function for the 'Clear All' button."""
    st.session_state.user_input = ""
    st.session_state.translation_result = "Your translation will appear here..."

# A list of languages for the dropdown menu.
indian_languages = [
    "Hindi", "Bengali", "Telugu", "Marathi", "Tamil", "Urdu",
    "Gujarati", "Kannada", "Odia", "Malayalam", "Punjabi", "Assamese"
]

# Set up a two-column layout for a clean look.
left_column, right_column = st.columns(2, gap="large")

# --- Left Column (User Input) ---
with left_column:
    st.header("Enter Your Text")

    language_choice = st.selectbox(
        "Translate to which language?",
        options=indian_languages
    )
    
    # This text area is linked to our session state.
    st.text_area(
        "Text to translate:",
        height=250,
        placeholder="Type or paste your text here...",
        key="user_input" 
    )
    
    # The 'Clear All' button calls our reset function when clicked.
    st.button("Clear All 🗑️", on_click=clear_text_fields, use_container_width=True)

# --- Right Column (Translation Output) ---
with right_column:
    st.header("Translation Result")
    
    # The translate button should be disabled if the API key is missing.
    is_button_disabled = not API_KEY
    if is_button_disabled:
        st.error("OpenAI API key not found. Please follow the setup instructions below.")

    # When the user clicks this button...
    if st.button(f"Translate to {language_choice}!", use_container_width=True, type="primary", disabled=is_button_disabled):
        # ...we call our translation function and update the result in the session state.
        st.session_state.translation_result = get_translation(
            API_KEY,
            st.session_state.user_input,
            language_choice
        )

    # This text area just displays the result stored in our session state.
    # It's disabled so the user can't edit the translation.
    st.text_area(
        "Result:",
        value=st.session_state.translation_result,
        height=300,
        disabled=True
    )
import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Indian Language Translator",
    page_icon="🇮🇳",
    layout="wide"
)

# Caches translation results to reduce API calls
@st.cache_data
def get_translation(api_key, text, target_lang, model="gpt-4o"):
    if not text.strip():
        return ""

    try:
        client = OpenAI(api_key=api_key)

        messages = [
            {
                "role": "system",
                "content": "You are an expert Indian language translator. Provide accurate and culturally appropriate translations."
            },
            {
                "role": "user",
                "content": f"Translate this into {target_lang}:\n\n{text}"
            }
        ]

        with st.spinner(f"Translating to {target_lang}..."):
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.3,
                max_tokens=2000
            )
        return response.choices[0].message.content.strip()

    except Exception as e:
        if "Incorrect API key" in str(e):
            st.error("Invalid OpenAI API key.")
        else:
            st.error(f"Error: {e}")
        return ""

API_KEY = os.getenv("OPENAI_API_KEY")

st.title("🇮🇳 Indian Language Translator")
st.markdown("Translate text into major Indian languages using OpenAI.")

if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "translation_result" not in st.session_state:
    st.session_state.translation_result = "Your translation will appear here..."

def reset_fields():
    st.session_state.user_input = ""
    st.session_state.translation_result = "Your translation will appear here..."

languages = [
    "Hindi", "Bengali", "Telugu", "Marathi", "Tamil", "Urdu",
    "Gujarati", "Kannada", "Odia", "Malayalam", "Punjabi", "Assamese"
]

left, right = st.columns(2, gap="large")

with left:
    st.header("Input")

    lang = st.selectbox("Target Language:", options=languages)

    st.text_area(
        "Text:",
        height=250,
        placeholder="Enter text to translate...",
        key="user_input"
    )

    st.button("Clear All 🗑️", on_click=reset_fields, use_container_width=True)

with right:
    st.header("Translation")

    if not API_KEY:
        st.error("Missing OpenAI API key. Please check your .env file.")
    else:
        if st.button(f"Translate to {lang}", use_container_width=True, type="primary"):
            st.session_state.translation_result = get_translation(
                API_KEY,
                st.session_state.user_input,
                lang
            )

    st.text_area(
        "Result:",
        value=st.session_state.translation_result,
        height=300,
        disabled=True
    )

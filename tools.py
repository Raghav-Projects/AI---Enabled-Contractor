import streamlit as st
import os
import time
from google import genai
from google.genai import types
from streamlit_mic_recorder import mic_recorder
from PIL import Image

# --- 1. SETTINGS & CLIENT ---
st.set_page_config(page_title="AI Contractor", page_icon="🏗️", layout="wide")

# Best free-tier model for 2026 (Highest quota, lowest errors)
MODEL_ID = "gemini-2.5-flash-lite" 

# Replace with your key or set as environment variable
API_KEY = "AIzaSyCTpcoi0g0dppFTCmzev5tIoI0uzgmtFyY" 

try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error("Invalid API Key. Please check your setup.")
    st.stop()

# --- 2. THE AGENT BRAIN ---
SYSTEM_PROMPT = """
You are an Autonomous AI General Contractor. Handle these 5 roles:
1. MANAGER: Coordinate flow.
2. ARCHITECT: Analyze blueprints/images.
3. ESTIMATOR: Use Google Search for live material prices.
4. COMPLIANCE: Use Google Search for building codes/sanctions.
5. LOGISTICS: Suggest transport/availability.

When images are provided, analyze them for dimensions.
Always use Google Search for prices—do not guess.
"""

# --- 3. SESSION STATE (Memory) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. THE UI ---
st.title("🏗️ AI Site Manager (End-to-End)")
st.markdown("---")

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "image" in msg and msg["image"]:
            st.image(msg["image"], width=300)

# --- 5. INPUT SECTION (Guarded against NoneType errors) ---
with st.sidebar:
    st.header("Upload Tools")
    uploaded_file = st.file_uploader("Upload Blueprint", type=["jpg", "jpeg", "png"])
    
    st.write("Voice Input:")
    # The key feature: Voice Search
    voice_record = mic_recorder(
        start_prompt="🎙️ Start Speaking", 
        stop_prompt="⏹️ Stop & Send", 
        key='my_mic'
    )

user_text = st.chat_input("Ask about materials, budget, or local rules...")

# --- 6. PROCESSING LOGIC ---
if user_text or voice_record or uploaded_file:
    payload = []
    active_img = None

    # A. Handle Image
    if uploaded_file is not None:
        active_img = Image.open(uploaded_file)
        payload.append(active_img)

    # B. Handle Voice (This is where the 'NoneType' error was)
    if voice_record is not None:
        # Check if bytes exist before accessing
        if 'bytes' in voice_record:
            audio_part = types.Part.from_bytes(
                data=voice_record['bytes'], 
                mime_type="audio/wav"
            )
            payload.append(audio_part)
            payload.append("I have sent a voice message. Please listen and answer.")

    # C. Handle Text
    if user_text:
        payload.append(user_text)

    # Final Guard: Only proceed if payload is not empty
    if payload:
        # Update UI with User Message
        st.session_state.messages.append({
            "role": "user", 
            "content": user_text if user_text else "Sent a voice/image command.",
            "image": active_img
        })
        
        with st.chat_message("user"):
            if user_text: st.markdown(user_text)
            if active_img: st.image(active_img, width=300)

        # Generate AI Response
        with st.chat_message("assistant"):
            with st.spinner("👷 Contractor is analyzing site data..."):
                try:
                    # Config with Google Search Grounding
                    config = types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        tools=[types.Tool(google_search=types.GoogleSearch())],
                        temperature=1.0
                    )
                    
                    response = client.models.generate_content(
                        model=MODEL_ID,
                        contents=payload,
                        config=config
                    )
                    
                    ai_response = response.text
                    st.markdown(ai_response)
                    
                    # Store response
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
                except Exception as e:
                    if "429" in str(e):
                        st.error("Quota Exhausted! Please wait 60 seconds or switch to a Paid Plan.")
                    else:
                        st.error(f"Error: {e}")

# --- FOOTER ---
st.markdown("---")
st.caption("Powered by Gemini 2.5 Flash-Lite & Grounded by Google Search.")
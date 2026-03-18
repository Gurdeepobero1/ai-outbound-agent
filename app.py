import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# UI Configuration
st.set_page_config(page_title="AI Outbound Agent", page_icon="🚀", layout="centered")

st.title("🚀 Supercharged Outbound Agent")
st.caption("Paste what you sell and who you're targeting. The AI handles the strategy and copy.")

# --- 1. MINIMIZED INPUTS ---
product = st.text_area(
    "📦 What are you selling?", 
    placeholder="e.g., We build AI voice agents for dental clinics to automate appointment bookings...", 
    height=80
)

lead_context = st.text_area(
    "🎯 Lead Details (Paste whatever you have)", 
    placeholder="Paste their LinkedIn bio, a recent post they made, or just type 'John Doe, VP of Sales at TechCorp'...", 
    height=80
)

# --- 2. PLATFORM & TONE CONTROLS ---
col1, col2 = st.columns(2)
with col1:
    platform = st.selectbox("📫 Delivery Platform", ["LinkedIn DM", "Cold Email", "Twitter / X DM"])
with col2:
    tone = st.selectbox("🎭 Tone", ["Conversational & Crisp", "Professional & Direct", "Provocative / Pattern-Interrupt"])

# Button
if st.button("✨ Generate Best-in-Class Outreach", use_container_width=True):
    if not product or not lead_context:
        st.warning("Please provide both your product description and lead details.")
    else:
        with st.spinner("Analyzing lead and crafting the perfect hook..."):
            
            # --- 3. DYNAMIC PLATFORM CONSTRAINTS ---
            if platform == "LinkedIn DM":
                constraints = """
                - Length: STRICTLY UNDER 50 words.
                - Format: No subject line. Short, punchy sentences.
                - Style: Highly casual, zero fluff. DO NOT use greetings like 'I hope this finds you well' or 'Dear'.
                - Goal: Start a conversation, not pitch immediately. 1 soft question at the end.
                """
            elif platform == "Cold Email":
                constraints = """
                - Subject Line: Create a catchy, 2-4 word subject line (lowercase often works best).
                - Length: STRICTLY UNDER 80 words.
                - Format: Spaced out paragraphs (1-2 sentences each maximum) for readability.
                - Style: Professional but concise. Clear Value Proposition.
                """
            else: # Twitter/X
                constraints = """
                - Length: STRICTLY UNDER 40 words.
                - Format: Extremely punchy, casual, text-message style. No line breaks needed.
                - Style: High energy, direct to the point.
                """

            # --- 4. EXPERT SDR PROMPT ---
            prompt = f"""
            You are an elite top-1% B2B Sales Development Representative (SDR) and copywriter known for booking meetings with Fortune 500 execs.

            CONTEXT:
            - My Product/Offer: {product}
            - Target Lead Profile: {lead_context}

            REQUIREMENTS:
            - Platform: {platform}
            - Tone: {tone}
            {constraints}

            OUTPUT EXACTLY IN THIS FORMAT:
            ### 🧠 The Strategy
            (1 sentence explaining the psychological angle/pain point you chose based on their profile)

            ### ✍️ The Message
            (Write the actual message here. If Email, include "Subject: ")

            ### 🔄 Follow-up Message
            (1 very short follow-up to send 3 days later if they ghost you)
            """

            try:
                # Adding temperature for better creative copywriting
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7 
                )

                output = response.choices[0].message.content

                st.divider()
                st.write(output)

            except Exception as e:
                st.error(f"Error: {str(e)}")

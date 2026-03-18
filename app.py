import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
api_key = os.getenv("GROQ_API_KEY") or st.secrets["GROQ_API_KEY"] 
client = Groq(api_key=api_key)

# UI
st.set_page_config(page_title="AI Outbound Agent", layout="centered")

st.title("🚀 AI Outbound Intelligence Agent")
st.caption("Generate high-converting personalized outreach in seconds")

# Inputs
product = st.text_area("Describe your product")
icp = st.text_input("Target Audience (ICP)")
name = st.text_input("Lead Name")
role = st.text_input("Role")
company = st.text_input("Company")
tone = st.selectbox("Tone", ["Formal", "Casual", "Persuasive"])

# Button
if st.button("Generate Message"):
    if not product or not icp or not name:
        st.warning("Please fill required fields")
    else:
        with st.spinner("Generating..."):
            prompt = f"""
            You are an expert AI sales strategist.

            Product: {product}
            ICP: {icp}
            Lead: {name}, {role} at {company}
            Tone: {tone}

            Tasks:
            1. Identify likely pain point
            2. Write a highly personalized cold message (max 80 words)
            3. Add 1 follow-up message
            4. Explain in 1 line why it works
            """

            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}]
                )

                output = response.choices[0].message.content

                st.subheader("📩 Generated Output")
                st.write(output)

            except Exception as e:
                st.error(f"Error: {str(e)}")

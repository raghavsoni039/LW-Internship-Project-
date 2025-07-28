from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from credentials import Gemini_API
import streamlit as st


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=Gemini_API,
    convert_system_message_to_human=True
)

@tool
def refine_idea(input: str) -> str:
    '''refines a vague startup idea into a clear problem-solution statement'''
    prompt = f"""
Refine the following startup idea into a clear and professional problem-solution statement.

**Startup Idea:**  
{input}

**Format:**  
Problem: ...  
Solution: ...
"""
    return llm.invoke(prompt)

@tool
def market_research(input: str) -> str:
    '''performs basic market research for a startup idea'''
    prompt = f"""
Conduct basic market research for the startup idea below.

**Startup Idea:**  
{input}

Include:
- Market size
- Target audience
- Trends
- Competitors
"""
    return llm.invoke(prompt)

@tool
def business_model(input: str) -> str:
    '''Generate a Business model Canvas for the start up idea'''
    prompt = f"""
Generate a Business Model Canvas for the startup:

{input}

Include:
- Key Partners, Activities
- Value Proposition
- Customer Segments
- Revenue Streams
- Cost Structure
"""
    return llm.invoke(prompt)

@tool
def pitch_deck(input: str) -> str:
    '''Create a pitch deck outline from the business idea'''
    prompt = f"""
Create a pitch deck outline with 8 slides for the startup idea:

{input}

Slides:
1. Title
2. Problem
3. Solution
4. Market
5. Business Model
6. Roadmap
7. Team
8. Ask
"""
    return llm.invoke(prompt)

@tool
def elevator_pitch(input: str) -> str:
    '''Write a short persuasive elevator pitch which can be pitched in 15 seconds '''
    prompt = f"""
Write a compelling 15-second elevator pitch for:

{input}
"""
    return llm.invoke(prompt)

def startup_builder():
    st.subheader("🚀 AI-Powered Startup Builder")
    idea = st.text_area("💡 Enter your startup idea:")

    if st.button("Generate Startup Plan"):
        with st.spinner("Generating responses..."):
            refined = refine_idea.invoke(idea).content
            research = market_research.invoke(idea).content
            model = business_model.invoke(idea).content
            deck = pitch_deck.invoke(idea).content
            pitch = elevator_pitch.invoke(idea).content

        st.markdown("### 🔍 Refined Idea")
        st.markdown(refined)

        st.markdown("### 📊 Market Research")
        st.markdown(research)

        st.markdown("### 📦 Business Model Canvas")
        st.markdown(model)

        st.markdown("### 🖼️ Pitch Deck Outline")
        st.markdown(deck)

        st.markdown("### 🎙️ Elevator Pitch")
        st.markdown(pitch)

import streamlit as st
from agent import create_agent

st.set_page_config(page_title="AI Trip Planner", layout="wide")

st.title("🌍 AI Trip Planner Agent")
st.write("Plan trips using LLM reasoning + real-time data")

agent = create_agent()

user_prompt = st.text_input(
    "Enter your trip request",
    placeholder="Plan a 3-day trip to Tokyo in May"
)

if st.button("Generate Trip Plan"):
    if not user_prompt:
        st.warning("Please enter a prompt")
    else:
        with st.spinner("Planning your trip..."):
            response = agent.run(
                f"""
                Create a travel plan with:
                1. Cultural & historical overview (1 paragraph)
                2. Current weather and forecast
                3. Travel dates (assume mid-month)
                4. Flight options
                5. Hotel options
                6. Day-wise itinerary

                User request: {user_prompt}
                """
            )

        st.subheader("✈️ Your Trip Plan")
        st.write(response)

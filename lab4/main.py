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
            response = agent.invoke({
                "input": f"""
            Plan a trip for the following request:

            {user_prompt}

            Instructions:
            - Use tools for weather, flights, and hotels when needed
            - Provide a detailed itinerary
            - Do NOT return JSON
            - Respond in plain text
            """
            })




        st.subheader("✈️ Your Trip Plan")
        # st.write(response["output"])
        st.markdown(response["output"])


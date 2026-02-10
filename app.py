import streamlit as st
from data_loader import load_data
from logic import find_assignment
from urgent import urgent_reassign

st.title("🛩️ Drone Operations Coordinator AI")

pilots, drones, missions = load_data()

user_input = st.text_input("Ask me about pilots, drones, or missions")

if user_input:
    msg = user_input.lower()

    if "urgent" in msg:
        mission = missions.iloc[0]
        options = urgent_reassign(mission, pilots)
        st.warning("Urgent reassignment required")
        for score, pilot in options:
            st.write(f"Pilot: {pilot} | Score: {score}")

    elif "assign" in msg:
        mission = missions.iloc[0]
        matches = find_assignment(mission, pilots, drones)

        if matches:
            st.success("Possible assignments found:")
            for m in matches:
                st.write(m)
        else:
            st.error("No valid assignments found due to conflicts")

    elif "available" in msg:
        available = pilots[pilots["status"] == "available"]
        st.write(available[["name", "location", "certifications"]])

    else:
        st.info("Try: assign mission / urgent reassignment / available pilots")

import streamlit as st
from data_loader import load_data
from logic import find_assignment
from urgent import urgent_reassign

st.title("🛩️ Drone Operations Coordinator AI")

# Load data
pilots, drones, missions = load_data()

user_input = st.text_input("Ask me about pilots, drones, or missions")

if user_input:
    msg = user_input.lower()

    # -------- URGENT REASSIGNMENT --------
    if "urgent" in msg:
        if missions.empty:
           st.error("No missions available")
           st.stop()

        mission = missions.iloc[0]
        options = urgent_reassign(mission, pilots)

        st.warning("⚠️ Urgent reassignment required")

        if options:
            for opt in options:
                st.write(
                    f"Pilot: {opt['pilot']} | "
                    f"Score: {opt['score']} | "
                    f"Location: {opt['location']}"
                )
        else:
            st.error("No available pilots found for urgent reassignment")

    # -------- NORMAL ASSIGNMENT --------
    elif "assign" in msg:
        mission = missions.iloc[0]
        matches = find_assignment(mission, pilots, drones)

        if matches:
            st.success("✅ Possible assignments found:")
            for m in matches:
                st.write(m)
        else:
            st.error("❌ No valid assignments found due to conflicts")

    # -------- AVAILABILITY QUERY --------
    elif "available" in msg:
        available = pilots[pilots["status"] == "available"]
        st.subheader("Available Pilots")
        st.write(available[["name", "location", "certifications"]])

    # -------- HELP --------
    else:
        st.info("Try: `assign mission` / `urgent reassignment` / `available pilots`")

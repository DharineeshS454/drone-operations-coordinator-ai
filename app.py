import streamlit as st
from urgent import detect_urgent, urgent_reassign

from data_loader import load_data
from logic import find_assignment
from urgent import urgent_reassign
from roster import (
    get_available_pilots,
    get_pilots_by_location,
    get_pilots_by_certification
)
from sheets_service import update_pilot_status
from drone_inventory import (
    get_available_drones,
    get_drones_by_capability,
    get_drones_under_maintenance
)
from sheets_service import update_drone_status

from sheets_service import (
    assign_pilot,
    assign_drone,
    clear_pilot_assignment,
    clear_drone_assignment
)

st.title("🛩️ Drone Operations Coordinator AI")

# Load data
pilots, drones, missions = load_data()

user_input = st.text_input("Ask me about pilots, drones, or missions")

if user_input:
    msg = user_input.lower().strip()

    # -------- PHASE 3: ROSTER MANAGEMENT --------

    if msg == "available pilots":
        result = get_available_pilots(pilots)
        st.subheader("🧑‍✈️ Available Pilots")
        st.write(result[["name", "location", "certifications"]])

    elif msg.startswith("pilots in"):
        location = msg.replace("pilots in", "").strip()
        result = get_pilots_by_location(pilots, location)

        st.subheader(f"🧑‍✈️ Pilots in {location.title()}")
        st.write(result[["name", "status", "certifications"]])

    elif msg.startswith("pilots with"):
        cert = msg.replace("pilots with", "").strip()
        result = get_pilots_by_certification(pilots, cert)

        st.subheader(f"🧑‍✈️ Pilots with {cert}")
        st.write(result[["name", "location", "status"]])
    elif msg == "available drones":
         result = get_available_drones(drones)
         st.subheader("🚁 Available Drones")
         st.write(result[["drone_id", "model", "capabilities", "location"]])
    elif msg.startswith("drones with"):
         capability = msg.replace("drones with", "").strip()
         result = get_drones_by_capability(drones, capability)

         st.subheader(f"🚁 Drones with {capability}")
         st.write(result[["drone_id", "model", "status", "location"]])
    elif msg == "drones under maintenance":
         result = get_drones_under_maintenance(drones)
         st.subheader("🛠️ Drones Under Maintenance")
         st.write(result[["drone_id", "model", "location"]])
    elif "mark drone" in msg and "under maintenance" in msg:
        drone_id = (
        msg.replace("mark drone", "")
           .replace("as under maintenance", "")
           .strip()
           .upper()
    )

        success = update_drone_status(drone_id, "under maintenance")

        if success:
            st.success(f"✅ Drone {drone_id} marked as Under Maintenance")
            pilots, drones, missions = load_data()  # refresh state
        else:
            st.error(f"❌ Drone {drone_id} not found")

    elif "mark pilot" in msg and "on leave" in msg:
        name = msg.replace("mark pilot", "").replace("on leave", "").strip()
        success = update_pilot_status(name, "on leave")

        if success:
            st.success(f"✅ Pilot {name} marked as On Leave")
            pilots, drones, missions = load_data()  # refresh
        else:
            st.error(f"❌ Pilot {name} not found")

    # -------- URGENT REASSIGNMENT --------

    elif "urgent" in msg:
       if missions.empty:
           st.error("No missions available")
           st.stop()
 
       mission = missions.iloc[0]
       options = urgent_reassign(mission, pilots)

       st.warning("⚠️ Urgent reassignment required")
       st.info("Urgent mode → relaxed constraints applied")

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
       mission = missions.iloc[0]  # demo scope: first mission
       matches, reasons = find_assignment(mission, pilots, drones)

       if matches:
        # Pick first valid assignment (rule-based, deterministic)
           choice = matches[0]

           pilot_name = choice["pilot"]
           drone_id = choice["drone"]
           mission_id = mission["mission_id"]

        # ---- PHASE 6: WRITE STATE ----
           assign_pilot(pilot_name, mission_id)
           assign_drone(drone_id, mission_id)

           st.success(
            f"✅ Assigned Pilot {pilot_name} and Drone {drone_id} "
            f"to mission {mission_id}"
        )

        # Refresh data from source of truth
           pilots, drones, missions = load_data()

       else:
           st.error("❌ No valid assignments found")
           st.write("Reasons:")
           for r in reasons:
               st.write(f"- {r}")

    # -------- HELP --------

    else:
        st.info(
            "Try:\n"
            "- available pilots\n"
            "- pilots in <location>\n"
            "- pilots with <certification>\n"
            "- mark pilot <name> on leave\n"
            "- assign mission\n"
            "- urgent reassignment"
        )

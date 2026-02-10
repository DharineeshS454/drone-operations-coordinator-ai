from datetime import datetime


def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d")



def dates_overlap(start1, end1, start2, end2):
    """
    Returns True if two date ranges overlap.
    """
    return start1 <= end2 and start2 <= end1




def check_pilot_conflicts(mission, pilots):
    conflicts = []

    mission_start = parse_date(mission["start_date"])

    for _, pilot in pilots.iterrows():

        # 1️⃣ Pilot already assigned
        if pilot["status"].lower() == "assigned":
            conflicts.append(
                f"Pilot {pilot['name']} is already assigned "
                f"to mission {pilot['current_assignment']}"
            )
            continue

        # 2️⃣ Pilot not available yet
        if pilot.get("available_from"):
            available_from = parse_date(pilot["available_from"])
            if mission_start < available_from:
                conflicts.append(
                    f"Pilot {pilot['name']} is available only from "
                    f"{available_from.date()}"
                )

    return conflicts

def check_drone_conflicts(mission, drones):
    conflicts = []

    mission_start = parse_date(mission["start_date"])

    for _, drone in drones.iterrows():

        if drone["status"].lower() == "assigned":
            conflicts.append(
                f"Drone {drone['drone_id']} is already assigned "
                f"to mission {drone['current_assignment']}"
            )

        if drone.get("available_from"):
            available_from = parse_date(drone["available_from"])
            if mission_start < available_from:
                conflicts.append(
                    f"Drone {drone['drone_id']} is available only from "
                    f"{available_from.date()}"
                )

    return conflicts


def detect_conflicts(mission, pilots, drones):
    reasons = []
    reasons.extend(check_pilot_conflicts(mission, pilots))
    reasons.extend(check_drone_conflicts(mission, drones))
    return reasons


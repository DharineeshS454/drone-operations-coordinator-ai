def pilot_conflicts(pilot, mission):
    issues = []

    if pilot["status"] != "available":
        issues.append("Pilot not available")

    if mission["required_certification"] not in pilot["certifications"]:
        issues.append("Certification mismatch")

    if pilot["location"] != mission["location"]:
        issues.append("Pilot location mismatch")

    return issues


def drone_conflicts(drone, mission):
    issues = []

    if drone["status"] != "available":
        issues.append("Drone not available or under maintenance")

    if mission["required_capability"] not in drone["capabilities"]:
        issues.append("Drone capability mismatch")

    if drone["location"] != mission["location"]:
        issues.append("Drone location mismatch")

    return issues


def find_assignment(mission, pilots, drones):
    matches = []

    for _, pilot in pilots.iterrows():
        if pilot_conflicts(pilot, mission):
            continue

        for _, drone in drones.iterrows():
            if drone_conflicts(drone, mission):
                continue

            matches.append({
                "pilot": pilot["name"],
                "drone": drone["drone_id"],
                "location": mission["location"]
            })

    return matches

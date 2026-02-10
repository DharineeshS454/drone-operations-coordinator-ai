def pilot_conflicts(pilot, mission):
    issues = []

    if pilot["status"] != "available":
        issues.append("Pilot not available")

    # FIXED: required_certs is a list
    if not set(mission["required_certs"]).issubset(set(pilot["certifications"])):
        issues.append("Certification mismatch")

    if pilot["location"] != mission["location"]:
        issues.append("Pilot location mismatch")

    return issues


def drone_conflicts(drone, mission):
    issues = []

    if drone["status"] != "available":
        issues.append("Drone not available or under maintenance")

    # FIXED: required_skills vs capabilities
    if not set(mission["required_skills"]).issubset(set(drone["capabilities"])):
        issues.append("Drone capability mismatch")

    if drone["location"] != mission["location"]:
        issues.append("Drone location mismatch")

    return issues


def find_assignment(mission, pilots, drones):
    matches = []

    for _, pilot in pilots.iterrows():
        pilot_issues = pilot_conflicts(pilot, mission)

        for _, drone in drones.iterrows():
            drone_issues = drone_conflicts(drone, mission)

            if pilot_issues or drone_issues:
                print("❌ Rejected combination:")
                print("Pilot:", pilot["name"])
                print("Pilot issues:", pilot_issues)
                print("Drone:", drone["drone_id"])
                print("Drone issues:", drone_issues)
                print("-" * 40)
                continue

            matches.append({
                "pilot": pilot["name"],
                "drone": drone["drone_id"],
                "location": mission["location"]
            })

    return matches


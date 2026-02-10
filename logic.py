from conflicts import detect_conflicts


def pilot_conflicts(pilot, mission):
    issues = []

    if pilot["status"] != "available":
        issues.append("Pilot not available")

    if not set(mission["required_certs"]).issubset(
        set(pilot["certifications"])
    ):
        issues.append("Pilot certification mismatch")

    if pilot["location"] != mission["location"]:
        issues.append("Pilot location mismatch")

    return issues


def drone_conflicts(drone, mission):
    issues = []

    if drone["status"] != "available":
        issues.append("Drone not available or under maintenance")

    if not set(mission["required_skills"]).issubset(
        set(drone["capabilities"])
    ):
        issues.append("Drone capability mismatch")

    if drone["location"] != mission["location"]:
        issues.append("Drone location mismatch")

    return issues


def find_assignment(mission, pilots, drones):
    matches = []
    rejection_reasons = set()

    # STEP 1: Global conflicts (date overlap)
    conflict_reasons = detect_conflicts(mission, pilots, drones)
    if conflict_reasons:
        return [], conflict_reasons

    # STEP 2: Pilot + Drone compatibility checks
    for _, pilot in pilots.iterrows():
        pilot_issues = pilot_conflicts(pilot, mission)

        for _, drone in drones.iterrows():
            drone_issues = drone_conflicts(drone, mission)

            if pilot_issues or drone_issues:
                for issue in pilot_issues + drone_issues:
                    rejection_reasons.add(issue)
                continue

            matches.append({
                "pilot": pilot["name"],
                "drone": drone["drone_id"],
                "location": mission["location"]
            })

    # STEP 3: Return results
    if matches:
        return matches, []

    return [], list(rejection_reasons)

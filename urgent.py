def urgent_reassign(mission, pilots):
    ranked = []

    for _, pilot in pilots.iterrows():
        if pilot["status"] != "available":
            continue

        score = 0
        if pilot["location"] == mission["location"]:
            score += 2
        if mission["required_certification"] in pilot["certifications"]:
            score += 3

        ranked.append((score, pilot["name"]))

    ranked.sort(reverse=True)
    return ranked[:3]

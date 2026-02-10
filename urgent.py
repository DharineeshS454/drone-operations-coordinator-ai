def urgent_reassign(mission, pilots):
    ranked = []

    for _, pilot in pilots.iterrows():
        # Skip unavailable pilots
        if pilot["status"] != "available":
            continue

        score = 0

        # Location preference (not mandatory)
        if pilot["location"] == mission["location"]:
            score += 2

        # FIX ✅: required_certs is a LIST
        if set(mission["required_certs"]).intersection(set(pilot["certifications"])):
            score += 3

        ranked.append({
            "pilot": pilot["name"],
            "score": score,
            "location": pilot["location"]
        })

    # Highest score first
    ranked.sort(key=lambda x: x["score"], reverse=True)
    return ranked

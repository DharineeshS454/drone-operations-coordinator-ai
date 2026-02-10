URGENT_KEYWORDS = [
    "urgent",
    "immediately",
    "tomorrow",
    "pilot unavailable"
]


def detect_urgent(msg):
    msg = msg.lower()
    return any(word in msg for word in URGENT_KEYWORDS)


def score_pilot_urgent(pilot, mission):
    """
    Higher score = better fallback pilot
    """
    score = 0

    # 1️⃣ Availability (mandatory)
    if pilot["status"].lower() == "available":
        score += 5
    else:
        return 0  # hard reject

    # 2️⃣ Certification match (mission["required_certs"] is a LIST)
    cert_match = len(
        set(mission["required_certs"]) &
        set(pilot["certifications"])
    )
    score += cert_match * 3

    # 3️⃣ Location bonus (not mandatory)
    if pilot["location"] == mission["location"]:
        score += 2

    return score


def urgent_reassign(mission, pilots, top_n=3):
    ranked = []

    for _, pilot in pilots.iterrows():
        score = score_pilot_urgent(pilot, mission)

        if score > 0:
            ranked.append({
                "pilot": pilot["name"],
                "score": score,
                "location": pilot["location"],
                "certifications": pilot["certifications"]
            })

    ranked.sort(key=lambda x: x["score"], reverse=True)
    return ranked[:top_n]

import pandas as pd

def load_data():
    pilots = pd.read_csv("pilot_roster.csv")
    drones = pd.read_csv("drone_fleet.csv")
    missions = pd.read_csv("missions.csv")

    # Normalize status
    pilots["status"] = pilots["status"].str.lower()
    drones["status"] = drones["status"].str.lower()

    # Convert lists
    pilots["certifications"] = pilots["certifications"].fillna("").apply(
        lambda x: [c.strip() for c in x.split(",")]
    )

    drones["capabilities"] = drones["capabilities"].fillna("").apply(
        lambda x: [c.strip() for c in x.split(",")]
    )

    missions["required_certs"] = missions["required_certs"].fillna("").apply(
        lambda x: [c.strip() for c in x.split(",")]
    )

    missions["required_skills"] = missions["required_skills"].fillna("").apply(
        lambda x: [c.strip() for c in x.split(",")]
    )

    return pilots, drones, missions

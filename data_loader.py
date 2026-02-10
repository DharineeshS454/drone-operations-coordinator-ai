import pandas as pd

from sheets_service import (
    read_pilots,
    read_drones,
    read_missions
)

def load_data():
    # 🔹 SOURCE CHANGED (Sheets instead of CSV)
    pilots = read_pilots()
    drones = read_drones()
    missions = read_missions()

    # 🔹 NORMALIZATION (KEEP THIS)
    pilots["status"] = pilots["status"].str.strip().str.lower()
    drones["status"] = drones["status"].str.lower()

    # 🔹 LIST CONVERSIONS (KEEP THIS)
    pilots["certifications"] = pilots["certifications"].fillna("").apply(
        lambda x: [c.strip() for c in x.split(",") if c.strip()]
    )

    drones["capabilities"] = drones["capabilities"].fillna("").apply(
        lambda x: [c.strip() for c in x.split(",") if c.strip()]
    )

    missions["required_certs"] = missions["required_certs"].fillna("").apply(
        lambda x: [c.strip() for c in x.split(",") if c.strip()]
    )

    missions["required_skills"] = missions["required_skills"].fillna("").apply(
        lambda x: [c.strip() for c in x.split(",") if c.strip()]
    )

    return pilots, drones, missions

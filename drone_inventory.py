def get_available_drones(drones):
    return drones[drones["status"].str.lower() == "available"]


def get_drones_by_capability(drones, capability):
    return drones[
        drones["capabilities"].apply(
            lambda caps: capability.lower() in
            [c.strip().lower() for c in caps]
        )
    ]


def get_drones_under_maintenance(drones):
    return drones[drones["status"].str.lower() == "under maintenance"]

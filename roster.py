def get_available_pilots(pilots):
    return pilots[pilots["status"] == "available"]


def get_pilots_by_location(pilots, location):
    return pilots[pilots["location"].str.lower() == location.lower()]


def get_pilots_by_certification(pilots, certification):
    return pilots[
        pilots["certifications"]
        .apply(lambda certs: certification.lower() in [c.lower() for c in certs])
    ]

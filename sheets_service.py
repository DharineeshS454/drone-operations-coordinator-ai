import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

CREDS_FILE = "drone-ops-ai-43253546c101.json"
SPREADSHEET_NAME = "Drone Operations Data"


def get_client():
    creds = Credentials.from_service_account_file(
        CREDS_FILE, scopes=SCOPES
    )
    return gspread.authorize(creds)


def read_sheet(sheet_name):
    client = get_client()
    sheet = client.open(SPREADSHEET_NAME).worksheet(sheet_name)
    data = sheet.get_all_records()
    return pd.DataFrame(data)


# -------- READ FUNCTIONS --------

def read_pilots():
    return read_sheet("Pilot_Roster")


def read_drones():
    return read_sheet("Drone_Fleet")


def read_missions():
    return read_sheet("Missions")


# -------- UPDATE FUNCTIONS --------

def update_pilot_status(pilot_name, new_status):
    client = get_client()
    sheet = client.open(SPREADSHEET_NAME).worksheet("Pilot_Roster")

    records = sheet.get_all_records()

    for idx, row in enumerate(records, start=2):  # start=2 (skip header)
        if row["name"] == pilot_name:
            sheet.update_cell(idx, 3, new_status)  # column 3 = status
            return True

    return False


def update_drone_status(drone_id, new_status):
    client = get_client()
    sheet = client.open(SPREADSHEET_NAME).worksheet("Drone_Fleet")

    records = sheet.get_all_records()

    for idx, row in enumerate(records, start=2):
        if row["drone_id"] == drone_id:
            sheet.update_cell(idx, 3, new_status)
            return True

    return False

import os
import json
import pandas as pd

import gspread
from google.oauth2.service_account import Credentials
import streamlit as st

SPREADSHEET_ID = "1OK8ZAASHHSf_VGmIJBhJnLdHuNyQxJySjE0asPTCHME
"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_client():
    creds = Credentials.from_service_account_info(
        st.secrets["GOOGLE_SERVICE_ACCOUNT"],
        scopes=SCOPES
    )
    return gspread.authorize(creds)




def read_sheet(sheet_name):
    client = get_client()
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(sheet_name)
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
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet("Pilot_Roster")

    records = sheet.get_all_records()
    headers = sheet.row_values(1)

    name_col = headers.index("name") + 1
    status_col = headers.index("status") + 1

    for idx, row in enumerate(records, start=2):
        sheet_name = row["name"].strip().lower()
        input_name = pilot_name.strip().lower()

        if input_name == sheet_name:
            sheet.update_cell(idx, status_col, new_status)
            return True

    return False



def update_drone_status(drone_id, new_status):
    client = get_client()
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet("Drone_Fleet")

    records = sheet.get_all_records()

    for idx, row in enumerate(records, start=2):
        if row["drone_id"] == drone_id:
            sheet.update_cell(idx, 3, new_status)
            return True

    return False

def assign_pilot(pilot_name, mission_id):
    client = get_client()
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet("Pilot_Roster")

    records = sheet.get_all_records()
    headers = sheet.row_values(1)

    name_col = headers.index("name") + 1
    status_col = headers.index("status") + 1
    assignment_col = headers.index("current_assignment") + 1

    for idx, row in enumerate(records, start=2):
        if row["name"].strip().lower() == pilot_name.strip().lower():
            sheet.update_cell(idx, status_col, "assigned")
            sheet.update_cell(idx, assignment_col, mission_id)
            return True

    return False


def assign_drone(drone_id, mission_id):
    client = get_client()
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet("Drone_Fleet")

    records = sheet.get_all_records()
    headers = sheet.row_values(1)

    id_col = headers.index("drone_id") + 1
    status_col = headers.index("status") + 1
    assignment_col = headers.index("current_assignment") + 1

    for idx, row in enumerate(records, start=2):
        if row["drone_id"].strip().upper() == drone_id.strip().upper():
            sheet.update_cell(idx, status_col, "assigned")
            sheet.update_cell(idx, assignment_col, mission_id)
            return True

    return False

def clear_pilot_assignment(pilot_name):
    client = get_client()
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet("Pilot_Roster")

    records = sheet.get_all_records()
    headers = sheet.row_values(1)

    name_col = headers.index("name") + 1
    status_col = headers.index("status") + 1
    assignment_col = headers.index("current_assignment") + 1

    for idx, row in enumerate(records, start=2):
        if row["name"].strip().lower() == pilot_name.strip().lower():
            sheet.update_cell(idx, status_col, "available")
            sheet.update_cell(idx, assignment_col, "")
            return True

    return False


def clear_drone_assignment(drone_id):
    client = get_client()
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet("Drone_Fleet")

    records = sheet.get_all_records()
    headers = sheet.row_values(1)

    id_col = headers.index("drone_id") + 1
    status_col = headers.index("status") + 1
    assignment_col = headers.index("current_assignment") + 1

    for idx, row in enumerate(records, start=2):
        if row["drone_id"].strip().upper() == drone_id.strip().upper():
            sheet.update_cell(idx, status_col, "available")
            sheet.update_cell(idx, assignment_col, "")
            return True

    return False

import sys
import os
import base64
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime

# Get input parameters from GitHub Actions
problem_number = sys.argv[1]
problem_name = sys.argv[2]
solution_link = sys.argv[3]
notes = sys.argv[4] if len(sys.argv) > 4 else ""

# Decode the base64-encoded service account credentials stored as an environment variable
base64_credentials = os.getenv('GOOGLE_CREDENTIALS_BASE64')
if not base64_credentials:
    raise ValueError(
        "GOOGLE_CREDENTIALS_BASE64 environment variable is missing")

# Decode and write the service account JSON to a file
credentials_json = base64.b64decode(base64_credentials).decode('utf-8')
with open('service_account.json', 'w') as f:
    f.write(credentials_json)

# Load the credentials from the file
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'service_account.json'

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID of the spreadsheet (replace with your actual Google Sheets ID)
SPREADSHEET_ID = os.getenv("SHEET_ID")

service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# Prepare the row to append
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
row = [timestamp, problem_number, problem_name, solution_link, notes]

# Append the row to the Google Sheet
request = sheet.values().append(
    spreadsheetId=SPREADSHEET_ID,
    range='Sheet1!A:E',
    valueInputOption='RAW',
    insertDataOption='INSERT_ROWS',
    body={'values': [row]}
).execute()

print(f"Updated sheet with problem {problem_number}-{problem_name}")

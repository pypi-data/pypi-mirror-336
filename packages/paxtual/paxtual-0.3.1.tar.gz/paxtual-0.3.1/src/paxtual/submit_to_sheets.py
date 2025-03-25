import gspread
from google.oauth2 import service_account
import os
import pandas as pd
import numpy as np

SERVICE_ACCOUNT_FILE = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
SHEET_NAME = 'new'
WORKSHEET_NAME = 'Sheet1'
SHEET_KEY = "1g25m-ZEtkk_gsAevSdLtq-m7JqLK15jZS52ZbpvsESM" #added sheet key.

def format_dataframe(records: dict):
    df = pd.DataFrame(records)
    df = df.replace({np.nan: None}) # Replace NaN with None

    return df.to_dict(orient='records')  # Return list of dicts

def add_production_data(data: list): #data is now a list of dictionaries.
    if not SERVICE_ACCOUNT_FILE:
        print("Error: GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
        return

    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        gc = gspread.Client(auth=credentials)
        sheet = gc.open_by_key(SHEET_KEY) #use sheet key.
        worksheet = sheet.worksheet(WORKSHEET_NAME)

        # Get existing headers from the sheet
        existing_headers = worksheet.row_values(1)

        # Get headers from the data
        if data: #only run if there is data.
            data_headers = list(data[0].keys())

            # Check for missing headers and add them
            for header in data_headers:
                if header not in existing_headers:
                    existing_headers.append(header)
                    worksheet.update('A1', [existing_headers])

            # Reorder data headers to match sheet headers
            ordered_data = []
            for row_dict in data:
                ordered_row = []
                for header in existing_headers:
                    ordered_row.append(row_dict.get(header, '')) #get value, or empty string.
                ordered_data.append(ordered_row)

            # Find the next available row and add data
            next_row = len(worksheet.get_all_values()) + 1
            worksheet.append_rows(ordered_data, value_input_option='USER_ENTERED', table_range=f'A{next_row}')

            print(f"Data added to worksheet '{WORKSHEET_NAME}' successfully.")
        else:
            print("No data to add.")

    except FileNotFoundError:
        print(f"Error: Service account file not found at {SERVICE_ACCOUNT_FILE}")
    except Exception as e:
        print(f"An error occurred: {e}")


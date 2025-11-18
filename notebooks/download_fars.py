import os
import requests
import zipfile
import io

# SCRIPT FOR DOWNLOADING ALL ACCIDENT.CSV DATA IMMEDIATELY INSIDE THE data/data_accidents/<YEAR> folders
START_YEAR = 1975
END_YEAR = 2023

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
base_folder = os.path.join(project_root, "data/data_accidents")
os.makedirs(base_folder, exist_ok=True)

def download_fars_year(year):
    print(f"\n=== YEAR {year} ===")

    zip_url = f"https://static.nhtsa.gov/nhtsa/downloads/FARS/{year}/National/FARS{year}NationalCSV.zip"
    print(f"Downloading: {zip_url}")

    response = requests.get(zip_url)

    if response.status_code != 200:
        print(f"ZIP not found for {year}. Skipping.")
        return

    zip_bytes = io.BytesIO(response.content)
    year_folder = os.path.join(base_folder, str(year))
    os.makedirs(year_folder, exist_ok=True)

    try:
        with zipfile.ZipFile(zip_bytes) as z:
            files = z.namelist()
            accident_files = [f for f in files if f.lower().endswith("accident.csv")]

            if not accident_files:
                print(f"No ACCIDENT.csv found in {year} ZIP.")
                return

            accident_name = accident_files[0]
            print(f"Extracting: {accident_name}")

            extract_path = os.path.join(year_folder, "accident.csv")
            with z.open(accident_name) as src, open(extract_path, "wb") as dst:
                dst.write(src.read())

            print(f"Saved: {extract_path}")

    except Exception as e:
        print(f"Error extracting {year}: {e}")

if __name__ == "__main__":
    print("Starting FARS automated download...\n")

    for year in range(START_YEAR, END_YEAR + 1):
        download_fars_year(year)

    print("\nDONE! All ACCIDENT.csv files downloaded into data_accidents/")
import sqlite3
import pandas as pd
import json
import glob
import os
import time

# Define the common and extra columns
common_columns = [
    'country', 'year', 'amount', 'currency', 'recipient_name', 'currency_original', 'pk',
    'recipient_address', 'recipient_id', 'recipient_country', 'amount_original',
    'recipient_fingerprint', 'scheme', 'scheme_id'
]

extra_columns = [
    'nuts1', 'nuts3', 'nuts2', 'recipient_location', 'scheme_1', 'scheme_code',
    'recipient_postcode', 'scheme_name', 'recipient_county', 'recipient_url', 'scheme_description'
]

def get_all_files(years):
    """
    Retrieve all CSV file paths for the given years.

    Args:
        years (list): List of years to process.

    Returns:
        list: List of file paths.
    """
    csv_files = []
    for year in years:
        print(f"Processing year: {year}")
        # Folder containing your CSV files
        data_folder = f"./data_raw/farm_subsidy/{year}"
        # Get all CSV file paths
        csv_files.extend(glob.glob(os.path.join(data_folder, "*.csv")))

    print(f"Found {len(csv_files)} CSV files across all years.")
    return csv_files

def clean_amount(value):
    """
    Clean and standardize the amount value.

    Args:
        value: The value to clean.

    Returns:
        float or None: Cleaned numeric value or None if invalid.
    """
    if pd.isna(value):
        return None

    value = str(value).replace("€", "").replace(" ", "")

    # Handle European format (comma as decimal separator)
    if "," in value and "." not in value:
        value = value.replace(",", ".")
    else:
        value = value.replace(",", "")

    try:
        return float(value)
    except ValueError:
        return None

def process_file(file, conn):
    """
    Processes a single CSV file and inserts its data into the SQLite database.

    Args:
        file (str): Path to the CSV file to process.
        conn (sqlite3.Connection): SQLite database connection object.
    """
    print(f"Processing file: {file}")

    # Time the operation
    start_time = time.time()
    # Read the CSV file in chunks to handle large files efficiently
    for chunk in pd.read_csv(file, chunksize=10000):
        # Ensure all required columns exist in the chunk
        for col in common_columns:
            if col not in chunk.columns:
                chunk[col] = None  # Add missing columns with default value None

        # Clean numerical columns
        chunk['amount'] = chunk['amount'].apply(clean_amount)
        chunk['amount_original'] = chunk['amount_original'].apply(clean_amount)
        chunk['year'] = chunk['year'].apply(lambda x: int(x) if pd.notna(x) else None)

        # Prepare rows for insertion
        rows_to_insert = []
        for _, row in chunk.iterrows():
            core_data = [row.get(col, None) for col in common_columns]
            extra_data = {
                col: row[col]
                for col in chunk.columns
                if col not in common_columns and pd.notna(row[col])
            }
            rows_to_insert.append((*core_data, json.dumps(extra_data)))

        # Insert rows into the database
        placeholders = ",".join(["?"] * (len(common_columns) + 1))  # +1 for `extra_data`
        insert_query = f"""
            INSERT INTO subsidies ({','.join(common_columns)}, extra_data)
            VALUES ({placeholders})
        """

        try:
            conn.executemany(insert_query, rows_to_insert)
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error inserting data from file {file}: {e}")
            conn.rollback()
    end_time = time.time()

    print(f"Finished processing file: {file} in {end_time - start_time:.4f} s = {(end_time - start_time) / 60:.2f} m")

if __name__ == "__main__":
    column_types = {
        "amount": "REAL",          # Numeric
        "year": "INTEGER",         # Year
        "amount_original": "REAL", # Numeric
        # Everything else defaults to TEXT
    }

    # Filepath
    file_path = "./data_raw/databases/"
    os.makedirs(file_path, exist_ok=True)

    # Create database
    conn = sqlite3.connect(os.path.join(file_path, "subsidies.db"))
    cursor = conn.cursor()

    # Build CREATE TABLE dynamically
    columns_sql = ", ".join([
        f"{col} {column_types.get(col, 'TEXT')}"
        for col in common_columns
    ])

    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS subsidies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        {columns_sql},
        extra_data TEXT
    )
    """)

    conn.commit()

    # Process files for the specified years
    # years = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024][:1]  # Adjust this list as needed
    # years_done = [2016,2017, 2018,2019,2020,2021,2022,2023,2024]
    years = []
    csv_files = get_all_files(years)

    # For each file get the size and order them by size
    csv_files = sorted(csv_files, key=lambda x: os.path.getsize(x), reverse=True)

    start_time = time.time()
    for i , file in enumerate(csv_files):
        print(f'File {i+1}/{len(csv_files)}')
        process_file(file, conn)
    end_time = time.time()
    print(f"Finished processing all files in {end_time - start_time:.4f} s = {(end_time - start_time) / 60:.2f} m")

    conn.close()

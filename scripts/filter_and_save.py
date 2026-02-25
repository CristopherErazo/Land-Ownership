import pandas as pd
from pathlib import Path
import numpy as np

from land_ownership.utils import countries , clean_dataframe, get_scheme_columns



def main():

    # Years to analyze
    years = [2023,2024]

    # Loop through each country and year
    for year in years:
        for abbr , country in zip(countries['abbreviations'], countries['names']):
            print(f"Processing data for {country} in {year}...")
            # Define filepath and filename
            dir_path = f'./data_raw/farm_subsidy_polished/{year}/'
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            file_path = dir_path + f'{country}.csv'
            # Check if the polished file already exists and skip if it does
            if Path(file_path).is_file():
                print(f"File {file_path} already exists. Skipping {country} for {year}.")
                continue

            # Load the dataset for the current country and year
            file = f'./data_raw/farm_subsidy/{year}/{abbr}.csv'
            
            # Check if the file exists            
            if not Path(file).is_file():
                print(f"File {file} does not exist. Skipping {country} for {year}.")
                continue
            df = pd.read_csv(file)

            # Search for valid scheme columns and keep only those with no NaN values
            valid_scheme_columns = get_scheme_columns(df)
            
            # Clean the dataframe and keep only the relevant columns
            cols = df.columns.to_list()
            # check the adress/location columns
            loc_col = 'recipient_adreess'
            if loc_col not in cols:
                loc_col = 'recipient_location'

            df = clean_dataframe(df, columns_to_keep=['recipient_name','amount',loc_col,*valid_scheme_columns ])

            # Add contry to recipient adress column
            df['address'] = df[loc_col] # + ', ' + country

            # Add extra column with recipient_name_fixed by cleaning the recipient_name column 
            # (removing leading/trailing spaces and converting to lowercase)
            df['recipient_name_fixed'] = df['recipient_name'].str.strip().str.lower()

            # Sort by amount in descending order
            df = df.sort_values(by='amount', ascending=False).reset_index(drop=True)

            # Group by recipients, summing the amounts and concatenating the schemes
            agg_opperations = {sch : lambda x: ' _&_ '.join(x.unique()) for sch in valid_scheme_columns}
            agg_opperations['amount'] = 'sum'
            agg_opperations['recipient_name'] = 'count'
            agg_opperations['address'] = 'first'

            df_grouped = df.groupby('recipient_name_fixed').agg(agg_opperations).reset_index()
            df_grouped = df_grouped.rename(columns={'recipient_name': 'counts',
                                                    'recipient_name_fixed': 'recipient_name'})
            
            # Sort by amount in descending order again
            df_grouped = df_grouped.sort_values(by='amount', ascending=False).reset_index(drop=True)
            
            # Save the polished dataframe to a new CSV file           
            df_grouped.to_csv(file_path, index=False)

            print(f'N entries = {df.shape[0]}, N recipients = {df_grouped.shape[0]}')
            # break

if __name__ == "__main__":
    main()







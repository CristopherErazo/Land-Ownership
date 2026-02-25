import pandas as pd
from pathlib import Path
import numpy as np

from land_ownership.utils import countries 


def main():

    # Years to analyze
    years = [2023,2024]

    results = {
        'country': [],
        'year': [],
        'scheme': [],
        'amount': [] 
    }

    # Loop through each country and year
    for year in years:
        for abbr , country in zip(countries['abbreviations'], countries['names']):
            print(f"Processing data for {country} in {year}...")
            
            # Load the dataset for the current country and year
            file = f'./data_raw/farm_subsidy/{year}/{abbr}.csv'
            
            # Check if the file exists            
            if not Path(file).is_file():
                print(f"File {file} does not exist. Skipping {country} for {year}.")
                continue
            df = pd.read_csv(file)
            df = df.dropna(axis=1, how='all')

            if 'scheme_1' not in df.columns:
                print(f"No scheme columns found for {country} in {year}. Skipping.")
                continue

            df = df[['scheme_1','amount']]
            df = df.groupby('scheme_1')['amount'].sum().reset_index()
            
            # Append results to the dictionary
            for _, row in df.iterrows():
                results['country'].append(country)
                results['year'].append(year)
                results['scheme'].append(row['scheme_1'])
                results['amount'].append(row['amount'])

    # Convert results to a DataFrame
    results_df = pd.DataFrame(results)
    print(results_df.head())
    # Save the results to a CSV file
    save_dir_path = './data/global_analysis/'
    Path(save_dir_path).mkdir(parents=True, exist_ok=True)
    file_path = save_dir_path + 'aggregated_schemes.csv'
    results_df.to_csv(file_path, index=False)

if __name__ == "__main__":
    main()







import pandas as pd
from pathlib import Path
import numpy as np

from land_ownership.utils import countries , clean_dataframe
from land_ownership.measures import compute_gini


def main():

    # Years to analyze
    years = [2024,2023]

    # Share percentages
    percentages = [1, 5, 10]
    results = {f'Top {p}%': [] for p in percentages}
    results['country'] = []
    results['year'] = []
    results['total'] = []
    results['count'] = []
    results['mean'] = []
    results['max'] = []
    results['gini'] = []

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

            # Clean the dataframe and keep only the relevant columns
            df = clean_dataframe(df, columns_to_keep=['recipient_name','amount'])

            # Add extra column with recipient_name_fixed by cleaning the recipient_name column 
            # (removing leading/trailing spaces and converting to lowercase)
            df['recipient_name_fixed'] = df['recipient_name'].str.strip().str.lower()

            # Group by recipient_name and calculate the total amount for each recipient
            df_recipients = df.groupby("recipient_name_fixed", as_index=False).agg({"amount": "sum"})

            # Sort descending
            df_sorted = df_recipients.sort_values("amount", ascending=False)

            # Total subsidy
            total_subsidy = df_sorted["amount"].sum()
            counts = df_sorted.shape[0]

            # Top p% shares
            for p in percentages:
                top_n = int(np.ceil(p * counts / 100))
                share = df_sorted.iloc[:top_n]["amount"].sum() / total_subsidy # Share is between 0 and 1
                results[f'Top {p}%'].append(share)
            
            # Gini coefficient
            gini_value = compute_gini(df_sorted["amount"])

            # Append the results 
            results['country'].append(country)
            results['year'].append(year)
            results['total'].append(total_subsidy)
            results['count'].append(df_sorted.shape[0])
            results['mean'].append(df_sorted['amount'].mean())
            results['max'].append(df_sorted['amount'].max())
            results['gini'].append(gini_value)


    # Convert results to a DataFrame
    results_df = pd.DataFrame(results)
    
    # Save the results to a CSV file
    dir_path = './data/global_analysis/'
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    file_path = dir_path + 'summary_statistics_per_country.csv'
    results_df.to_csv(file_path, index=False)


if __name__ == "__main__":
    main()







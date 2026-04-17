import pandas as pd
from pathlib import Path
import numpy as np
import sqlite3

from land_ownership.utils import countries , clean_dataframe
from land_ownership.measures import compute_gini


def main():

    # Years to analyze
    years = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

    # Share percentages
    percentages = [1, 5, 10]
    results = {f'Top {p}%': [] for p in percentages}
    results['country'] = []
    results['year'] = []
    results['total'] = []
    results['count'] = []
    results['mean'] = []
    results['std'] = []
    results['max'] = []
    results['min'] = []
    results['gini'] = []

    # Include quantiles
    quantiles = [0.25, 0.5, 0.75]
    for q in quantiles:
        results[f'q_{int(q*100)}%'] = []

    # Path to the database
    db_path = "./data_raw/databases/subsidies.db"
    table_name = "subsidies"

    # Connect to the database
    conn = sqlite3.connect(db_path)
    print(f"Connected to database: {db_path}")

    # Loop through each country and year
    for year in years:
        for abbr , country in zip(countries['abbreviations'], countries['names']):
            print(f"Processing data for {country} in {year}...")
            # Load the dataset for the current country and year aggregated by recipient_name
            query = f"""
                    SELECT 
                            recipient_name,
                            SUM(amount) AS total_amount
                    FROM 
                            {table_name}
                    WHERE 
                            year = {year} AND country = '{abbr.upper()}'
                    GROUP BY 
                            recipient_name
                    ORDER BY 
                            total_amount DESC
                    """
            df_recipients = pd.read_sql_query(query, conn)
            print(f'Loaded {len(df_recipients)} records for {country} in {year}.')
            # Filter out rows with non-positive amounts (if any) and nan values
            df_recipients = df_recipients[df_recipients['total_amount'] > 0.1].dropna(subset=['total_amount'])

            # Check if there are any valid entries after filtering           
            if len(df_recipients) == 0:
                print(f"No data found for {country} in {year}. Skipping.")
                continue

            # Total subsidy
            total_subsidy = df_recipients["total_amount"].sum()
            counts = len(df_recipients)

            # Top p% shares
            for p in percentages:
                top_n = int(np.ceil(p * counts / 100))
                share = df_recipients.iloc[:top_n]["total_amount"].sum() / total_subsidy # Share is between 0 and 1
                results[f'Top {p}%'].append(share)

            # Gini coefficient
            gini_value = compute_gini(df_recipients["total_amount"])

            # Compute quantiles
            for q in quantiles:
                quantile_value = df_recipients["total_amount"].quantile(q)
                results[f'q_{int(q*100)}%'].append(quantile_value)

            # Append the results 
            results['country'].append(country)
            results['year'].append(year)
            results['total'].append(total_subsidy)
            results['count'].append(df_recipients.shape[0])
            results['mean'].append(df_recipients['total_amount'].mean())
            results['std'].append(df_recipients['total_amount'].std())
            results['max'].append(df_recipients['total_amount'].max())
            results['min'].append(df_recipients['total_amount'].min())
            results['gini'].append(gini_value)

    conn.close()

    # Convert results to a DataFrame
    results_df = pd.DataFrame(results)

    # Save the results to a CSV file
    dir_path = './data/global_analysis/'
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    file_path = dir_path + 'summary_statistics_per_country.csv'
    results_df.to_csv(file_path, index=False)


if __name__ == "__main__": 
    main()







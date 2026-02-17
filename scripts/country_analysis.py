import pandas as pd
from pathlib import Path

from land_ownership.utils import countries , clean_dataframe

years = [2024,2023]



def main():

    # Create empty dict to store results
    results = {
        'country': [],
        'year': [],
        'count': [],
        'mean': [],
        'std': [],
        'min': [],
        '25%': [],
        '50%': [],
        '75%': [],
        'max': []
    }

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
            df_group = df.groupby("recipient_name_fixed", as_index=False).agg({"amount": "sum"})

            # Generate summary statistics for the amount column
            summary_df = df_group.describe()
            print(f'Total amont: {summary_df.loc['count', 'amount']}, Mean: {summary_df.loc['mean', 'amount']}, Std: {summary_df.loc['std', 'amount']}, Min: {summary_df.loc['min', 'amount']}, 25%: {summary_df.loc['25%', 'amount']}, 50%: {summary_df.loc['50%', 'amount']}, 75%: {summary_df.loc['75%', 'amount']}, Max: {summary_df.loc['max', 'amount']}\n')
            
            # Append the results 
            results['country'].append(country)
            results['year'].append(year)
            results['count'].append(summary_df.loc['count', 'amount'])
            results['mean'].append(summary_df.loc['mean', 'amount'])    
            results['std'].append(summary_df.loc['std', 'amount'])
            results['min'].append(summary_df.loc['min', 'amount'])
            results['25%'].append(summary_df.loc['25%', 'amount'])
            results['50%'].append(summary_df.loc['50%', 'amount'])
            results['75%'].append(summary_df.loc['75%', 'amount'])
            results['max'].append(summary_df.loc['max', 'amount'])
            # break

    # Convert results to a DataFrame
    results_df = pd.DataFrame(results)
    
    # Save the results to a CSV file
    dir_path = './data/global_analysis/'
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    file_path = dir_path + 'summary_statistics.csv'
    results_df.to_csv(file_path, index=False)


if __name__ == "__main__":
    main()







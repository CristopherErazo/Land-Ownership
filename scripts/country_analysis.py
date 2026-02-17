import pandas as pd

# year = 2023
# country = 'hr'
# file = f'../data/farm_subsidy/{year}/{country}.csv'
# print(f"Loading data from: {file}")

years = [2022,2023]


def main():
    # Load the dataset
    df = pd.read_csv('data/country_data.csv')

    # Perform analysis (example: calculate average GDP per capita)
    avg_gdp_per_capita = df['GDP_per_capita'].mean()
    print(f'Average GDP per capita: {avg_gdp_per_capita}')

    # Additional analysis can be added here

if __name__ == "__main__":
    main()
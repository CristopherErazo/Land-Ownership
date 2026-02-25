import pandas as pd
from pathlib import Path
import numpy as np
# from geopy.geocoders import Nominatim
# from geopy.extra.rate_limiter import RateLimiter

from land_ownership.utils import countries , clean_dataframe, get_scheme_columns



def main():
    # geolocator = Nominatim(user_agent="myGeocoder")
    # geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.3)
    


    # Years to analyze
    years = [2023,2024]
    k = 20
    # L = 2 # Top entries to get locations for

    # Loop through each country and year
    for year in years:
        for abbr , country in zip(countries['abbreviations'], countries['names']):
            print(f"Processing data for {country} in {year}...")
            # Check if file already exist and skip if it does
            dir_path = f'./data/farm_subsidy_top_bottom/{year}/'
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            file_save = dir_path + f'{country.lower().replace(' ','_')}.csv'
            # if Path(file_save).is_file():
            #     print(f"File {file_save} already exists. Skipping {country} for {year}.")
            #     continue


            # Define filepath and filename
            file_load = f'./data_raw/farm_subsidy_polished/{year}/{country}.csv'
                        
            # Check if the file exists            
            if not Path(file_load).is_file():
                print(f"File {file_load} does not exist. Skipping {country} for {year}.")
                continue
            df = pd.read_csv(file_load)
            
            # Filter out negative amounts
            df = df[df['amount'] > 0]

            total_amount = df['amount'].sum()
            df['rank'] = np.arange(len(df)) + 1

            # Make new df with just the top and bottom k recipients by amount
            df_top = df.head(k)
            df_bottom = df.tail(k)
            df_new = pd.concat([df_top, df_bottom], ignore_index=True)

            # Add fraction column
            df_new['fraction'] = df_new['amount'] / total_amount 

            # Order columns: recipient_name, amount, then the rest
            first_columns = ["rank","recipient_name", "amount","fraction","address"]
            cols = first_columns + [c for c in df_new.columns if c not in first_columns]
            df_new = df_new[cols]
            # Add country to adress
            # df_new["address"] = df_new["address"] + ', ' + country
        

            # Add 2 columns with latitude and longitude and empty values for now
            df_new['latitude'] = np.nan
            df_new['longitude'] = np.nan

            # For top L entries compute location with geopy
            # for l in range(L):
            #     address = str(df_new['address'].iloc[l])
            #     print(l,address,type(address))
            #     # location = geocode(address)
            #     # df_new['latitude'].iloc[l] = location.latitude
            #     # df_new['longitude'].iloc[l] = location.longitude
       
            # Save
            df_new.to_csv(file_save, index=False)


            # break

if __name__ == "__main__":
    main()







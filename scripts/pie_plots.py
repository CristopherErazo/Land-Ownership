import pandas as pd
import plotly.express as px
from pathlib import Path


def create_pies(dataframe: pd.DataFrame, year:int, settings:dict):
    # Make pie chart with dropdown for countries
    df = dataframe.copy()
    df = df[df['year'] == year]
    countries_list = df['country'].unique()

    # Create initial figure with first country
    first_country = countries_list[0]
    initial_data = df[df['country'] == first_country]

    fig = px.pie(initial_data, values='amount', names='scheme', 
                title=f'Year {year}')
    fig.update_traces(textposition='inside', textinfo='percent+label')

    # Create buttons for dropdown
    buttons = []
    for country in countries_list:
        data = df[df['country'] == country]
        buttons.append(
            dict(
                label=country,
                method='update',
                args=[{'values': [data['amount']], 
                       'labels': [data['scheme']]}]
            )
        )

    # Add dropdown menu
    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=buttons,
                x=0.0,
                xanchor="left",
                y=1.15,
                yanchor="top"
            )
        ],
        height=settings['width'] * settings['height_proportion'],
        width=settings['width'],
        showlegend=False
    )

    return fig

if __name__ == "__main__":

    # Load dataframe
    filename = './data/global_analysis/aggregated_schemes.csv'
    agg_schemes = pd.read_csv(filename)
    
    # Configure settings
    settings = {
        'width': 400,
        'height_proportion': 1.
    }
    years = [2023,2024]

    for year in years:
        print(f"Creating pie plot for year {year}...")
        fig = create_pies(agg_schemes, year, settings)

        dir_path = "./docs/_static/plots/"
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        file_path = Path(dir_path) / f"pie_plot_{year}.html"

        fig.write_html(file_path, include_plotlyjs="cdn")  
        print(f"Saved pie plot for year {year} at {file_path}")
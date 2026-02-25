import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

from land_ownership.utils import countries, fmt_fraction, fmt_amount



def define_figure_layout(year,width=600, height_proportion=1.2):

    title = dict(
                text=f'Year {year}', #
                x=0.5,              # Position at center (0 to 1)
                y=0.92,              # Position near the top
                xanchor='center',    # Anchor point is center
                font=dict(family='Computer Modern',size=30)
                )   
    
    layout = go.Layout(
        title=title,
        height=width*height_proportion,
        width=width,
        showlegend=False
    )

    return layout



def create_table(dataframe: pd.DataFrame, settings:dict):
    """
    Create a table from dataframe
    
    Args:
        dataframe: DataFrame with summary statistics (mean, std, min, max, percentiles)
        settings: dict with settings for the table (column width, fill colors, alignments)
    """

    dataframe = dataframe.copy()
    dataframe['recipient_name'] = dataframe['recipient_name'].str.title()
    dataframe['address'] = dataframe['address'].str.title()

    df_plot = dataframe[['rank','recipient_name', 'amount','fraction','address']]
    df_plot['fraction'] *= 100
    df_plot['fraction'] = df_plot['fraction'].apply(fmt_fraction)
    df_plot['amount'] = df_plot['amount'].apply(fmt_amount)
    df_plot['rank'] = df_plot['rank'].astype(str)

    k=20
    # At row 20 insert a row with '...' in all columns
    df_plot.loc[k] = ['...']*len(df_plot.columns)

    df_plot = df_plot.rename(columns={
                                    'rank':'Rank',
                                    'recipient_name': 'Recipient Name',
                                    'amount': 'Amount [€]',
                                    'fraction': "% of Total",
                                    'address': 'Address'
                                    })

    table = go.Table(
                    columnwidth = settings['col_w'],
                    header=dict(values=list(df_plot.columns),
                                fill_color=settings['fill_color_header'],
                                align='center',
                                font=dict(color='white', size=14)),
                    cells=dict(values=[df_plot[key] for key in df_plot.columns],
                            fill_color=settings['fill_color_cells'],
                            align=settings['aligns'],
                            font=dict(color='black', size=12)))



    return table



def create_figure_with_dropdown(year: int, countries: list, settings:dict):
    """Create a figure with dropdown to switch between variables"""


    
    # Get layout from your existing function
    layout = define_figure_layout(year=year, width=settings['width'], height_proportion=settings['height_proportion'])
    
    # Create initial map with first variable
    first_country = countries[0]
    dir_path = f'./data/farm_subsidy_top_bottom/{year}/{first_country.lower().replace(' ','_')}.csv'
    dataframe = pd.read_csv(dir_path)
    initial_table = create_table(dataframe,settings)
    
    # Create the figure
    fig = go.Figure(data=[initial_table], layout=layout)
    
    # Create buttons for the dropdown
    buttons = []
    for country in countries:
        # load data for the country and year and create the table
        dir_path = f'./data/farm_subsidy_top_bottom/{year}/{country.lower().replace(' ','_')}.csv'
        if not Path(dir_path).exists():
            print(f"Data file for {country} in {year} not found at {dir_path}. Skipping.")
            continue
        dataframe = pd.read_csv(dir_path)
        table = create_table(dataframe, settings)
        
        buttons.append(
            dict(
                label = country,
                method="update",
                args=[{"cells.values": [table.cells.values]}]
            )
        )
    
    # Add dropdown menu to the figure
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=buttons,
                direction="down",
                pad={"r": 5, "t": 5},
                showactive=True,
                x=0.76,
                xanchor="left",
                y=1.2,
                yanchor="top"
            )
        ]
    )
    
    return fig




if __name__ == "__main__":

    
    countries_list = countries['names']
    # countries = ['Italy', 'Germany', 'France', 'Spain']
    print(countries_list)


    settings = { }

    settings['width'] = 900 # width of the map in pixels
    settings['height_proportion'] = 0.5
    settings['col_w'] = [0.5,1,0.6,0.5,0.5]
    settings['fill_color_header'] = 'olivedrab'
    settings['fill_color_cells'] = 'gainsboro'
    settings['aligns'] = ['center','left','center','center','left']  

    # Create figures for both years
    years = [2023, 2024]

    for year in years:
        print(f"Creating box plot for year {year}...")
        fig = create_figure_with_dropdown(year, countries_list, settings)
        print(f"Saving box plot for year {year}...")

        dir_path = "./docs/_static/plots/"
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        file_path = Path(dir_path) / f"table_plot_{year}.html"

        fig.write_html(file_path, include_plotlyjs="cdn")  
        
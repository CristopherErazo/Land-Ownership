import pandas as pd
import plotly.graph_objects as go
from pathlib import Path



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
        yaxis_title='Subsidy Amount (EUR)',
        yaxis_type='log',
        height=width*height_proportion,
        width=width,
        showlegend=False,
        hovermode='closest' # options: 'x', 'y', 'closest'
    )

    return layout



def create_box_plot(dataframe: pd.DataFrame, country: str, year: int, settings:dict):
    """
    Create a box plot from summary statistics
    
    Args:
        dataframe: DataFrame with summary statistics (mean, std, min, max, percentiles)
        country: Country name to filter
        year: Year to filter
    """
    
    # Filter data for the specific country and year
    data = dataframe[(dataframe['country'] == country) & (dataframe['year'] == year)]
    
    if data.empty:
        print(f"No data found for {country} in {year}")
        return None
    
    row = data.iloc[0]
    
    # Extract quartile values
    q1 = row['q_25%']
    median = row['q_50%']
    q3 = row['q_75%']
    min_val = row['min']
    max_val = row['max']
    mean_val = row['mean']
    
    # Create box plot using proper Plotly parameters
    box = go.Box(
        q1=[q1],           # Box starts here
        median=[median],   # Line in the middle
        q3=[q3],          # Box ends here
        lowerfence=[min_val],  # Lower whisker
        upperfence=[max_val],  # Upper whisker
        mean=[mean_val],        # Show mean as well
        name=country,
        boxmean=True,     # Display the mean
        marker_color='lightgreen',
        line_color='darkgreen',
        whiskerwidth=0.2,
        orientation='v',
        width=0.3,
        boxpoints=False,

    )

    return box



def create_figure_with_dropdown(dataframe: pd.DataFrame, year: int, countries: list, settings:dict):
    """Create a figure with dropdown to switch between variables"""


    
    # Get layout from your existing function
    layout = define_figure_layout(year=year, width=settings['width'], height_proportion=settings['height_proportion'])
    
    # Create initial map with first variable
    first_country = countries[0]
    initial_box = create_box_plot(dataframe, first_country, year,settings)
    
    # Create the figure
    fig = go.Figure(data=[initial_box], layout=layout)
    
    # Create buttons for the dropdown
    buttons = []
    for country in countries:
        # Filter data for the specific country and year
        data = dataframe[(dataframe['country'] == country) & (dataframe['year'] == year)]
        # If no data, skip
        if data.empty:
            print(f"No data found for {country} in {year}. Skipping.")
            continue
        row = data.iloc[0]
        
        # Extract quartile values
        q1 = row['q_25%']
        median = row['q_50%']
        q3 = row['q_75%']
        min_val = row['min']
        max_val = row['max']
        mean_val = row['mean']    

        
        buttons.append(
            dict(
                label = country,
                method="update",
                args=[
                    {
                        "q1": [[q1]],
                        "median": [[median]],
                        "q3": [[q3]],
                        "lowerfence": [[min_val]],
                        "upperfence": [[max_val]],
                        "mean": [[mean_val]]
                    }
                ]
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
                y=1.08,
                yanchor="top"
            )
        ]
    )
    
    return fig




if __name__ == "__main__":

    # Load the data and the shapefile
    df = pd.read_csv('./data/global_analysis/summary_statistics_per_country.csv')

    countries = df['country'].unique().tolist()
    # countries = ['Italy', 'Germany', 'France', 'Spain']
    print(countries)


    settings = { }

    settings['width'] = 400 # width of the map in pixels
    settings['height_proportion'] = 1.2

    # Create figures for both years
    years = [2023, 2024]

    for year in years:
        print(f"Creating box plot for year {year}...")
        fig = create_figure_with_dropdown(df, year, countries, settings)
        print(f"Saving box plot for year {year}...")

        dir_path = "./docs/_static/plots/"
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        file_path = Path(dir_path) / f"box_plot_{year}.html"

        fig.write_html(file_path, include_plotlyjs="cdn")  
        
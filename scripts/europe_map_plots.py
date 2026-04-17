import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go
from pathlib import Path

def create_map_plot(dataframe: pd.DataFrame, variable: str, year: int, settings: dict, color_scale: str = 'Greens'):
    """Create a choropleth map for a specific variable and year."""
    # Filter the DataFrame for the specified year
    dataframe = dataframe[dataframe['year'] == year]

    # Calculate variable range for color scaling
    var_min = dataframe[variable].dropna().min() * settings[variable]['amin']
    if variable in ['Top 1%', 'Top 5%', 'Top 10%', 'gini']:
        var_max = dataframe[variable].dropna().max()
    else:
        second_largest = dataframe[variable].dropna().nlargest(2).iloc[-1]
        var_max = second_largest * settings[variable]['amax']

    # Create the choropleth map
    map = go.Choropleth(
        locations=dataframe['ISO_A3'],
        z=dataframe[variable],
        colorscale=color_scale,
        colorbar=dict(
            title=dict(
                text=settings[variable]['label'],
                side="bottom"
            ),
            thickness=15,
            len=1.07,
            orientation='h',
            x=0.5,
            y=-0.15,
        ),
        zmin=var_min,
        zmax=var_max,
    )

    return map

def define_figure_layout(settings: dict):
    """Define the layout for the figure."""
    layout = go.Layout(
        title=dict(
            text='Farm Subsidies in Europe',
            x=0.5,
            y=0.92,
            xanchor='center',
            font=dict(family='Computer Modern', size=30)
        ),
        geo=dict(
            scope='europe',
            projection_type='mercator',
            showframe=True,
            framecolor='black',
            framewidth=2,
            bgcolor='gainsboro',
            showland=True,
            landcolor='rgb(243, 243, 243)',
            lonaxis=dict(range=[-12, 30]),
            lataxis=dict(range=[37, 67]),
        ),
        height=settings['width'] * settings['height_proportion'],
        width=settings['width'],
    )
    return layout

def create_interactive_figure(dataframe: pd.DataFrame, years: list, variables: list, settings: dict):
    """Create an interactive figure with a year slider and variable dropdown."""
    # Get layout
    layout = define_figure_layout(settings)

    # Create initial map with the first year and variable
    initial_year = years[0]
    initial_variable = variables[0]
    initial_map = create_map_plot(dataframe, initial_variable, initial_year, settings, settings['color_scale'])

    # Create the figure
    fig = go.Figure(data=[initial_map], layout=layout)

    # Define global min and max values for each variable across all years for consistent color scaling
    min_max_values = {'min': {}, 'max': {}}
    for variable in variables:
        var_min = dataframe[variable].dropna().min() 
        var_max = dataframe[variable].dropna().max()
        min_max_values['min'][variable] = var_min
        min_max_values['max'][variable] = var_max

    # Create frames for each year and variable combination
    frames = []
    for year in years:
        for variable in variables:
            filtered_data = dataframe[dataframe['year'] == year]
            var_min = filtered_data[variable].dropna().min() * settings[variable]['amin']
            if variable in ['Top 1%', 'Top 5%', 'Top 10%', 'gini']:
                var_max = filtered_data[variable].dropna().max()
            else:
                second_largest = filtered_data[variable].dropna().nlargest(2).iloc[-1]
                var_max = second_largest * settings[variable]['amax']

            frames.append(
                go.Frame(
                    data=[
                        go.Choropleth(
                            locations=filtered_data['ISO_A3'],
                            z=filtered_data[variable],
                            colorscale=settings['color_scale'],
                            zmin=min_max_values['min'][variable] * settings[variable]['amin'],
                            zmax=min_max_values['max'][variable] * settings[variable]['amax'],
                            colorbar=dict(
                                title=dict(
                                    text=settings[variable]['label'],  # Update label dynamically
                                    side="bottom"
                                ),
                                thickness=15,
                                len=1.07,
                                orientation='h',
                                x=0.5,
                                y=-0.15,
                            )
                        )
                    ],
                    name=f"{year}-{variable}"
                )
            )

    fig.frames = frames

    # Add slider for years
    sliders = [
        dict(
            active=0,
            currentvalue={"prefix": "Year: ", "font": {"size": 20}},
            pad={"t": 60},
            steps=[
                dict(
                    label=str(year),
                    method="animate",
                    args=[
                        [f"{year}-{initial_variable}"],
                        {"frame": None, "transition": None, "mode": "immediate"}  # Disable automatic evolution
                    ]
                ) for year in years
            ],
            transition=dict(duration=0),  # Disable transition animation
        )
    ]
    

    # Add dropdown for variables
    dropdown = [
        dict(
            buttons=[
                dict(
                    label=var.replace('_', ' ').capitalize(),
                    method="animate",
                    args=[
                        [f"{year}-{var}" for year in years],
                        {"frame": None, "transition": None, "mode": "immediate"}  # Disable animation
                    ]
                ) for var in variables
            ],
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.76,
            xanchor="left",
            y=1.08,
            yanchor="top"
        )
    ]

    # Disable autoplay of animation
    fig.update_layout(updatemenus=dropdown, sliders=sliders)

    return fig

if __name__ == "__main__":
    # Load the data and the shapefile
    df = pd.read_csv('./data/global_analysis/summary_statistics_per_country.csv')

    dir_path = './data/maps/europe/'
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    file_path = dir_path + 'europe_map.shp'
    europe = gpd.read_file(file_path)

    # Merge the DataFrame with the GeoDataFrame on the country name
    merged_df = europe.merge(df, left_on='SOVEREIGNT', right_on='country', how='left')

    # Add column with total subsidy per hectare (total subsidies divided by country area in hectares)
    merged_df['tot_per_h'] = merged_df['total'] / merged_df['area_h']

    # For 'Top *' columns, convert from fraction to percentage
    for col in merged_df.columns:
        if col.startswith('Top '):
            merged_df[col] = merged_df[col] * 100

    # Configuration for the dropdown menu and color scale
    total_variables = ['total', 'mean', 'max', 'count', 'Top 1%', 'Top 5%', 'Top 10%', 'gini', 'tot_per_h']

    settings = {var: {
        'amin': 1.0,
        'amax': 1.0,
        'label': var.capitalize(),
    } for var in total_variables}

    settings['total']['label'] = 'Total Subsidies (EUR)'
    settings['mean']['label'] = 'Average Subsidy Per Recipients (EUR)'
    settings['max']['label'] = 'Maximum Subsidy Received by one Recipient (EUR)'
    settings['gini']['label'] = 'Gini Coefficient'
    settings['tot_per_h']['label'] = 'Total Subsidies per Country Area (EUR/ha)'
    settings['count']['label'] = 'Number of Subsidy Recipients'

    for key in settings.keys():
        if key in ['Top 1%', 'Top 5%', 'Top 10%']:
            settings[key]['label'] = f'Percentage of Total Subsidy Gone to {key} recipients'

    # Settings for figure layout
    settings['color_scale'] = 'Greens'
    settings['width'] = 800  # width of the map in pixels
    settings['height_proportion'] = 1.2

    # Create figure for years 2016–2024
    years = list(range(2016, 2025))
    fig = create_interactive_figure(merged_df, years, total_variables, settings)

    # Save the figure as an HTML file
    output_dir = "./docs/_static/plots/"
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    output_file = Path(output_dir) / "interactive_map_subsidies.html"
    fig.write_html(output_file, include_plotlyjs="cdn")

import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go
from pathlib import Path
def create_map_plot(dataframe: pd.DataFrame, variable: str, year: int,color_scale: str = 'Greens',amin: float = 1.0, amax: float = 0.5):
    
    # Filter the DataFrame for the specified year
    dataframe = dataframe[dataframe['year'] == year]
    var_min = dataframe[variable].dropna().min() * amin
    var_max = dataframe[variable].dropna().max() * amax

    colorbar = dict(
                title=dict(
                text=f'{variable} (EUR)',
                side="bottom"  # Use 'side' inside the title object
                ),
                thickness=15,
                len=1.,
                orientation='h', # put colorbar horizontally below the map
                x = 0.5, # center the colorbar
                y = -0.15, # position it below the map
                
                )
    

   

    map = go.Choropleth(locations = dataframe['ISO_A3'],
                    z = dataframe[variable],colorscale = color_scale,colorbar=colorbar,
                    zmin=var_min, zmax=var_max,)

    return map

def define_figure_layout():
    layout = go.Layout(title = dict(
                        text=f'Farm Subsidies in Europe',
                        x=0.5,              # Position at center (0 to 1)
                        y=0.95,              # Position near the top
                        xanchor='center',    # Anchor point is center
                        font=dict(family='Computer Modern',size=30)
                        
                    ),
                    geo = dict(
                            scope='europe',
                            projection_type='mercator',
                            showframe=True,
                            framecolor='black',          # Color of the frame (if visible)
                            framewidth=2,                # Width of the frame
                            bgcolor='gray',         # Background color of map area
                            showland=True,
                            landcolor='rgb(243, 243, 243)',
                            # center = dict(lon=10, lat=52),  # Center point (longitude, latitude)
                            # projection_scale = 1.0, # Adjust the scale of the projection (zoom)
                            lonaxis=dict(range=[-12, 30]),  # Longitude bounds
                            lataxis=dict(range=[37, 67]),   # Latitude bounds
                            ),

                    height = 700,
                    width = 600,
                   )
    return layout

def create_figure_with_dropdown(dataframe: pd.DataFrame, year: int, variables: list, color_scale: str = 'Greens',amin: float = 1.0, amax: float = 0.5):
    """Create a figure with dropdown to switch between variables"""
    # Filter dataframe for the year
    df_filtered = dataframe[dataframe['year'] == year]
    
    # Get layout from your existing function
    layout = define_figure_layout()
    
    # Create initial map with first variable
    first_var = variables[0]
    initial_map = create_map_plot(dataframe, first_var, year, color_scale, amin, amax)
    
    # Create the figure
    fig = go.Figure(data=[initial_map], layout=layout)
    
    # Create buttons for the dropdown
    buttons = []
    for var in variables:
        # Get the data for this variable
        var_data = df_filtered[var]
        var_min = var_data.dropna().min() * amin
        var_max = var_data.dropna().max() * amax
        
        buttons.append(
            dict(
                label=f'{var} data',
                method="update",
                args=[
                    {
                        "z": [var_data],
                        "zmin": var_min,              # Update min color scale
                        "zmax": var_max,              # Update max color scale
                        "colorbar.title.text": f'{var} (EUR)'
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
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.74,
                xanchor="left",
                y=1.03,
                yanchor="top"
            )
        ]
    )
    
    return fig


if __name__ == "__main__":

    df = pd.read_csv('./data/global_analysis/summary_statistics.csv')
    # Add column with 'total' values multiplien mean by count
    df['total'] = df['mean'] * df['count']  # Convert to millions

    dir_path = './data/maps/europe/'
    file_path = dir_path + 'europe_map.shp'

    europe = gpd.read_file(file_path)

    # Merge the DataFrame with the GeoDataFrame on the country name
    merged_df = europe.merge(df, left_on='SOVEREIGNT', right_on='country', how='left')

    
    # Create the figure with dropdown
    year = 2023
    variables = ['total','mean','std']

    fig = create_figure_with_dropdown(merged_df, year, variables,amax=0.3)

    dir_path = "./docs/_static/plots/"
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    file_path = Path(dir_path) / "map_subsidies.html"

    fig.write_html(file_path, include_plotlyjs="cdn")

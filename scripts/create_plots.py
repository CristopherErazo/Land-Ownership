import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go
from pathlib import Path

def create_map_plot(dataframe: pd.DataFrame, variable: str, year: int, settings:dict, color_scale: str = 'Greens'):
    
    var_min = dataframe[variable].dropna().min() * settings[variable]['amin']
    if variable in ['Top 1%', 'Top 5%', 'Top 10%', 'gini']:
        var_max = dataframe[variable].dropna().max() #* settings[variable]['amax']
    else:
        second_largest = dataframe[variable].dropna().nlargest(2).iloc[-1]
        var_max = second_largest * settings[variable]['amax']

    # Filter the DataFrame for the specified year
    dataframe = dataframe[dataframe['year'] == year]
    colorbar = dict(
                title=dict(
                text=settings[variable]['label'],
                side="bottom"  # Use 'side' inside the title object
                ),
                thickness=15,
                len=1.07,
                orientation='h', # put colorbar horizontally below the map
                x = 0.5, # center the colorbar
                y = -0.15, # position it below the map
                
                )
    

   

    map = go.Choropleth(locations = dataframe['ISO_A3'],
                    z = dataframe[variable],colorscale = color_scale,colorbar=colorbar,
                    zmin=var_min, zmax=var_max,)

    return map

def define_figure_layout(year,width=600, height_proportion=1.2):
    title = dict(
                text=f'Year {year}',#f'Farm Subsidies in Europe <br><sup>Data for {year}</sup>',
                x=0.5,              # Position at center (0 to 1)
                y=0.92,              # Position near the top
                xanchor='center',    # Anchor point is center
                font=dict(family='Computer Modern',size=30)
                )   
    layout = go.Layout(title = title,
                    geo = dict(
                            scope='europe',
                            projection_type='mercator',
                            showframe=True,
                            framecolor='black',          # Color of the frame (if visible)
                            framewidth=2,                # Width of the frame
                            bgcolor='gainsboro',         # Background color of map area
                            showland=True,
                            landcolor='rgb(243, 243, 243)',
                            # center = dict(lon=10, lat=52),  # Center point (longitude, latitude)
                            # projection_scale = 1.0, # Adjust the scale of the projection (zoom)
                            lonaxis=dict(range=[-12, 30]),  # Longitude bounds
                            lataxis=dict(range=[37, 67]),   # Latitude bounds
                            ),

                    height = width * height_proportion,
                    width = width,
                   )
    return layout

def create_figure_with_dropdown(dataframe: pd.DataFrame, year: int, variables: list, settings:dict):
    """Create a figure with dropdown to switch between variables"""
    # Filter dataframe for the year
    df_filtered = dataframe[dataframe['year'] == year]
    
    # Get layout from your existing function
    layout = define_figure_layout(year=year, width=settings['width'], height_proportion=settings['height_proportion'])
    
    # Create initial map with first variable
    first_var = variables[0]
    initial_map = create_map_plot(dataframe, first_var, year,settings, settings['color_scale'])
    
    # Create the figure
    fig = go.Figure(data=[initial_map], layout=layout)
    
    # Create buttons for the dropdown
    buttons = []
    for var in variables:
        # Get the data for this variable
        var_data = dataframe[var]
        var_min = var_data.dropna().min() * settings[var]['amin']
        if var in ['Top 1%', 'Top 5%', 'Top 10%', 'gini']:
            var_max = var_data.dropna().max() #* settings[var]['amax']
        else:
            second_largest = var_data.dropna().nlargest(2).iloc[-1]
            var_max = second_largest * settings[var]['amax']
        var_data = df_filtered[var]
        
        buttons.append(
            dict(
                # Capitalize and replace _ for spaces in the label
                label = var.replace('_', ' ').capitalize(),
                method="update",
                args=[
                    {
                        "z": [var_data],
                        "zmin": var_min,              # Update min color scale
                        "zmax": var_max,              # Update max color scale
                        "colorbar.title.text": settings[var]['label']
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
    total_variables = ['total', 'mean','max','count','Top 1%', 'Top 5%', 'Top 10%','gini','tot_per_h']

    settings = { var: {
        'amin':1.0,
        'amax':1.1,
        'label': var.capitalize(),
    } for var in total_variables }

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
    settings['width'] = 470 # width of the map in pixels
    settings['height_proportion'] = 1.2

    # Create figures for both years
    years = [2023, 2024]

    for year in years:
        fig = create_figure_with_dropdown(merged_df, year, total_variables, settings)

        dir_path = "./docs/_static/plots/"
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        file_path = Path(dir_path) / f"map_subsidies_{year}.html"

        fig.write_html(file_path, include_plotlyjs="cdn")  
        
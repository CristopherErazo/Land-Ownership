import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go
from pathlib import Path


# -------------------------
# CREATE MAP TRACE
# -------------------------
def create_choropleth(df, variable, var_min, var_max,settings,x=0.5, y=-0.1):


    return go.Choropleth(
        locations=df['ISO_A3'],
        z=df[variable],
        colorscale=settings['color_scale'],
        zmin=var_min,
        zmax=var_max,
        colorbar=dict(
            # title=dict(text=settings[variable]['label'], side="bottom"),
            thickness=15,
            len=1.0,
            orientation='h',
            x=x,
            y=y,
        ),
    )


# -------------------------
# LAYOUT
# -------------------------
def define_layout(settings, variable):

    return go.Layout(
        title=dict(
            text=settings[variable]['label'],
            x=0.5,
            y=0.95,
            xanchor='center',
            font=dict(family='Computer Modern', size=28)
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


# -------------------------
# CREATE FIGURE (ONE VARIABLE)
# -------------------------
def create_figure_for_variable(df, years, variable, settings,padt=60):

    var_min = df[variable].dropna().min() * settings[variable]['amin']
    
    second_largest = df[variable].dropna().nlargest(2).iloc[-1]
    var_max = second_largest * settings[variable]['amax']

    initial_year = years[0]
    df_initial = df[df['year'] == initial_year]

    fig = go.Figure(
        data=[create_choropleth(df_initial, variable,var_min,var_max, settings)],
        layout=define_layout(settings, variable)
    )

    # -------------------------
    # FRAMES (YEARS ONLY)
    # -------------------------
    frames = []
    for year in years:
        df_year = df[df['year'] == year]

        frames.append(
            go.Frame(
                data=[create_choropleth(df_year, variable,var_min,var_max, settings)],
                name=str(year)
            )
        )

    fig.frames = frames

    # -------------------------
    # SLIDER
    # -------------------------
    sliders = [
        dict(
            active=0,
            currentvalue={"prefix": "Year: ", "font": {"size": 20}},
            pad={"t": padt},
            steps=[
                dict(
                    label=str(year),
                    method="animate",
                    args=[
                        [str(year)],
                        {
                            "mode": "immediate",
                            "frame": {"duration": 0, "redraw": True},
                            "transition": {"duration": 0}
                        }
                    ],
                )
                for year in years
            ],
        )
    ]

    fig.update_layout(sliders=sliders)

    return fig


# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":

    # Load data
    df = pd.read_csv('./data/global_analysis/summary_statistics_per_country.csv')
    europe = gpd.read_file('./data/maps/europe/europe_map.shp')

    merged_df = europe.merge(df, left_on='SOVEREIGNT', right_on='country', how='left')

    # Derived variable
    merged_df['tot_per_h'] = merged_df['total'] / merged_df['area_h']

    # Convert Top % columns
    for col in merged_df.columns:
        if col.startswith('Top '):
            merged_df[col] *= 100

    # Variables
    variables = [
        'total', 'mean', 'max', 'count',
        'Top 1%', 'Top 5%', 'Top 10%',
        'gini', 'tot_per_h'
    ]

    # Settings
    settings = {
        var: {'amin': 1.0, 'amax': 1.0, 'label': var}
        for var in variables
    }

    settings['total']['label'] = 'Total Subsidies (EUR)'
    settings['mean']['label'] = 'Average Subsidy (EUR)'
    settings['max']['label'] = 'Maximum Subsidy (EUR)'
    settings['count']['label'] = 'Number of Recipients'
    settings['gini']['label'] = 'Gini Coefficient'
    settings['tot_per_h']['label'] = 'Subsidies per Hectare (EUR/ha)'

    for key in ['Top 1%', 'Top 5%', 'Top 10%']:
        settings[key]['label'] = f'% of Subsidy to {key}'

    settings['color_scale'] = 'Greens'
    settings['width'] = 550
    settings['height_proportion'] = 1.2

    # Years
    years = list(range(2016, 2025))

    # Output directory
    output_dir = Path("./docs/_static/plots/")
    output_dir.mkdir(parents=True, exist_ok=True)

    # -------------------------
    # GENERATE ALL MAPS
    # -------------------------
    for var in variables:
        print(f"Creating map for: {var}")

        fig = create_figure_for_variable(merged_df, years, var, settings)

        safe_var_name = var.lower().replace(" ", "_").replace("%", "pct")

        output_file = output_dir / f"interactive_map_{safe_var_name}.html"

        fig.write_html(
            output_file,
            include_plotlyjs="cdn",
            auto_play=False
        )

    print("✅ All maps generated successfully.")
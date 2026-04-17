import pickle
import matplotlib.pyplot as plt
import numpy as np

from land_ownership.utils import countries
from configurations import set_font_sizes, create_fig, apply_general_styles, save_fig
apply_general_styles()


def plot_country(country, years, kde_results):
    colors = plt.get_cmap('Greens')(np.linspace(0.4, 1, len(years)))

    xtk = [1,2,3,4,5,6,7,8,9][::2]
    xlb = [r'$10$',r'$100$',r'$1\;k$',r'$10\;k$',r'$100\;k$',r'$1\;M$',r'$10\;M$',r'$100\;M$',r'$1\;B$'][::2]
    xlb = [lb+" €" for lb in xlb]

    # Figure
    fig , axes = create_fig(nrows=len(years), ncols=1, w=1,h=1,size='single',sharex=False)


    for i , year in enumerate(years):
        ax = axes[i]
        ax.spines['left'].set_visible(False)
        ax.set_yticks([])
        ax.set_xlim(0,9)
        ax.text(0.,0.5,rf"${year}$", transform=ax.transAxes,color=colors[i], fontsize=12, fontweight='bold')
        if i != len(years)-1:
            ax.spines['bottom'].set_visible(False)
            ax.set_xticks([])

        try:
            x , y = kde_results[year][country]
        except KeyError:
            print(f"No KDE results for {country} in {year}")
            continue
        ax.plot(x, y, linewidth=1.5,color=colors[i])
        ax.hlines(0,x.min(),x.max(),color=colors[i], linewidth=1.5)
        ax.fill_between(x, y, color=colors[i], alpha=0.5)
        
    # Change color also of x-axis line
    ax.spines['bottom'].set_color(colors[-1])
    ax.set_xticks(xtk)
    ax.set_xticklabels(xlb,color=colors[-1], fontsize=10)
    fig.suptitle(country,color=colors[0], fontsize=14)#, fontweight='bold')

    return fig , axes 

def main():
    # Load KDE results from the pickle file
    with open('./data/global_analysis/kde_results.pkl', 'rb') as f:
        kde_results = pickle.load(f)
    years = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
    for country in countries['names']:
        print(f"Plotting KDE for {country}...")
        fig , axes = plot_country(country, years=years, kde_results=kde_results)
        save_fig(fig, f'kde_{country}', base_dir='./docs/_static/plots')
    

if __name__ == "__main__":
    main()
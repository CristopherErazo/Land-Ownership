.. contents::
   :local:
   :depth: 2

Preliminary Analysis
====================

The first step of the project is to visualize the data and create some preliminary plots to understand the distribution of land ownership and farm subsidies in Europe. The following sections show some of the plots created during this phase of the project.

.. _subsidies:

Subsidies 
---------

The following section shows the results obtained by analizing the dataset of subsidies in the european countries for the years 2023 and 2024. The data was obtained from *(source)*.

For each **Year** and **Country** (among the ones included in the dataset) we have a list of list of subsidy transactions, each one containing the following information (mainly):

- **Recipient Name**: The recipient of the subsidy.
- **Recipient Adress**: The address of the recipient.
- **Amount**: The amount of the subsidy.
- **Scheme**: The scheme under which the subsidy was given (for now ignored).

among other information (also for now ignored).

Since many transactions are given to the same recipient, we agregated the data by recipient to procede with the analysis. 

.. _summary-statistics:

Summary Statistics
~~~~~~~~~~~~~~~~~~

To get a first insight of the data, we created two plots showing several summary statistics of the distribution of subsidies in the european countries for the years 2023 and 2024. The variables shown in the plots are the following:

- **Total**: The total amount of subsidies given to each country.
- **Mean**: The mean amount of subsidies given to each recipient.
- **Max**: The maximum amount of subsidies given to a single recipient in each country.
- **Count**: The total number of subsidy recipients in each country.
- **Top 1, 5, 10%**: The percentage of the total amount of subsidies given to the top 1, 5 and 10% of recipients in each country.
- **Gini**: The Gini coefficient of the distribution of subsidies in each country.
- **Tot per h**: The total amount of subsidies given to each country per hectare of country area in hectares.

*In the datasets there were some times entries with negative values. For this analysis we filtered them out.*

.. raw:: html

    <h2 style="text-align: center; margin-bottom: 5px;">Farm Subsidies Summary Statistics</h2>
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; max-width: 1600px; margin: 0 auto;">
        
        <!-- Left Column -->
        <div style="width: 100%;">
            <div style="position: relative; width: 100%; padding-bottom: 116.67%; height: 0;">
                <iframe src="_static/plots/map_subsidies_2023.html"
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;">
                </iframe>
            </div>
        </div>
        
        <!-- Right Column -->
        <div style="width: 100%;">
            <div style="position: relative; width: 100%; padding-bottom: 116.67%; height: 0;">
                <iframe src="_static/plots/map_subsidies_2024.html"
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;">
                </iframe>
            </div>
        </div>
        
    </div>
    

.. _box-plots:

Box Plots
~~~~~~~~~~~~~~~~~~

To get a better understanding of the distribution of subsidies in each country, we created box plots for each country and year. The box plots show the at a high level the distribution of subsidies per recipient in each country, showing the mean, minimum, first quartile, median, third quartile, and maximum of the distribution. You can hover over the box plots to see the exact values of these statistics, as well.

Since the distribution of subsidies is highly skewed, we used a logarithmic scale for amount of subsidy to better visualize the data. 

.. raw:: html

    <h2 style="text-align: center; margin-bottom: 5px;">Box Plots</h2>
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; max-width: 1600px; margin: 0 auto;">
        
        <!-- Left Column -->
        <div style="width: 100%;">
            <div style="position: relative; width: 100%; padding-bottom: 116.67%; height: 0;">
                <iframe src="_static/plots/box_plot_2023.html"
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;">
                </iframe>
            </div>
        </div>
        
        <!-- Right Column -->
        <div style="width: 100%;">
            <div style="position: relative; width: 100%; padding-bottom: 116.67%; height: 0;">
                <iframe src="_static/plots/box_plot_2024.html"
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;">
                </iframe>
            </div>
        </div>
        
    </div>
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


*New plot with all data.*

.. raw:: html
    <h2 style="text-align: center; margin-bottom: 5px;">Top and Bottom Recipients</h2>
    
    <div style="display: grid; grid-template-columns: 1fr; gap: 10px; max-width: 800px; margin: 0 auto;">
       
        <select id="mapSelector" onchange="showMap()">
            <option value="total">Total Subsidies</option>
            <option value="mean">Average</option>
            <option value="max">Max</option>
            <option value="count">Count</option>
            <option value="top1%">Top 1%</option>
            <option value="top5%">Top 5%</option>
            <option value="top10%">Top 10%</option>
            <option value="gini">Gini</option>
            <option value="tot_per_h">Total per hectare</option>
        </select>

        <div id="map-total" style="display: block; height: 700px;">
            <iframe src="_static/plots/interactive_map_total.html" width="600" height="700" style="border: 0;"></iframe>
        </div>

        <div id="map-mean" style="display: none; height: 700px;">
            <iframe src="_static/plots/interactive_map_mean.html" width="600" height="700" style="border: 0;"></iframe>
        </div>

        <div id="map-gini" style="display: none; height: 700px;">
            <iframe src="_static/plots/interactive_map_gini.html" width="600" height="700" style="border: 0;"></iframe>
        </div>

        <div id="map-max" style="display: none; height: 700px;">
            <iframe src="_static/plots/interactive_map_max.html" width="600" height="700" style="border: 0;"></iframe>
        </div>

        <div id="map-count" style="display: none; height: 700px;">
            <iframe src="_static/plots/interactive_map_count.html" width="600" height="700" style="border: 0;"></iframe>   
        </div>  

        <div id="map-top1%" style="display: none; height: 700px;">
            <iframe src="_static/plots/interactive_map_top_1pct.html" width="600" height="700" style="border: 0;"></iframe>    
        </div>

        <div id="map-top5%" style="display: none; height: 700px;">
            <iframe src="_static/plots/interactive_map_top_5pct.html" width="600" height="700" style="border: 0;"></iframe>    
        </div>
        
        <div id="map-top10%" style="display: none; height: 700px;">
            <iframe src="_static/plots/interactive_map_top_10pct.html" width="600" height="700" style="border: 0;"></iframe>   
        </div>
        
        <div id="map-tot_per_h" style="display: none; height: 700px;">
            <iframe src="_static/plots/interactive_map_tot_per_h.html" width="600" height="700" style="border: 0;"></iframe>   
        </div>
        
    </div>


    <script>
    function showMap() {
        const value = document.getElementById("mapSelector").value;

        document.querySelectorAll("[id^='map-']").forEach(div => {
            div.style.display = "none";
        });

        document.getElementById("map-" + value).style.display = "block";
    }
    </script>


Distributions
~~~~~~~~~~~~~~~~~~


.. raw:: html
    <h2 style="text-align: center; margin-bottom: 5px;">Subsidy Distribution</h2>
    
    <div style="display: grid; grid-template-columns: 1fr; gap: 10px; max-width: 800px; margin: 0 auto;">
       
        <select id="countrySelector" onchange="showMap()">
            <option value="austria">Austria</option>
            <option value="belgium">Belgium</option>
            <option value="bulgaria">Bulgaria</option>
            <option value="croatia">Croatia</option>
            <option value="czechia">Czechia</option>
            <option value="denmark">Denmark</option>
            <option value="estonia">Estonia</option>
            <option value="finland">Finland</option>
            <option value="france">France</option>
            <option value="germany">Germany</option>
            <option value="greece">Greece</option>
            <option value="hungary">Hungary</option>
            <option value="ireland">Ireland</option>
            <option value="italy">Italy</option>
            <option value="latvia">Latvia</option>
            <option value="lithuania">Lithuania</option>
            <option value="luxembourg">Luxembourg</option>
            <option value="netherlands">Netherlands</option>
            <option value="poland">Poland</option>
            <option value="portugal">Portugal</option>
            <option value="romania">Romania</option>
            <option value="slovakia">Slovakia</option>
            <option value="spain">Spain</option>
            <option value="sweden">Sweden</option>
            <option value="uk">United Kingdom</option>
            
        </select>

        <div id="kde-austria" style="display: block; height: 800px;">
            <iframe src="_static/plots/kde_Austria.png" width="750" height="750" style="border: 0;"></iframe>
        </div>

        <div id="kde-belgium" style="display: none; height: 800px;">
            <iframe src="_static/plots/kde_Belgium.png" width="750" height="750" style="border: 0;"></iframe>
        </div>

        <div id="kde-bulgaria" style="display: none; height: 800px;">
            <iframe src="_static/plots/kde_Bulgaria.png" width="750" height="750" style="border: 0;"></iframe>
        </div>

        <div id="kde-croatia" style="display: none; height: 800px;">
            <iframe src="_static/plots/kde_Croatia.png" width="750" height="750" style="border: 0;"></iframe>   
        </div>

        <div id="kde-czechia" style="display: none; height: 800px;">
            <iframe src="_static/plots/kde_Czechia.png" width="750" height="750" style="border: 0;"></iframe>
        </div>

        <div id="kde-denmark" style="display: none; height: 800px;">
            <iframe src="_static/plots/kde_Denmark.png" width="750" height="750" style="border: 0;"></iframe>
        </div>

        <div id="kde-estonia" style="display: none; height: 800px;">
            <iframe src="_static/plots/kde_Estonia.png" width="750" height="750" style="border: 0;"></iframe>
        </div>

        <div id="kde-finland" style="display: none; height: 800px;">
            <iframe src="_static/plots/kde_Finland.png" width="750" height="750" style="border: 0;"></iframe>
        </div>

        <div id="kde-france" style="display: none; height: 800px;">
            <iframe src="_static/plots/kde_France.png" width="750" height="750" style="border: 0;"></iframe>
        </div>

        <div id="kde-germany" style="display: none; height: 800px;">
            <iframe src="_static/plots/kde_Germany.png" width="750" height="750" style="border: 0;"></iframe>
        </div>

        <div id="kde-greece" style="display: none; height: 800px;">
            <iframe src="_static/plots/kde_Greece.png" width="750" height="750" style="border: 0;"></iframe>
        </div>

        <div id="kde-hungary" style="display: none; height: 800px;">
            <iframe src="_static/plots/kde_Hungary.png" width="750" height="750" style="border: 0;"></iframe>
        </div>

        <div id="kde-ireland" style="display: none; height: 800px;">
            <iframe src="_static/plots/kde_Ireland.png" width="750" height="750" style="border: 0;"></iframe>
        </div>

        <div id="kde-italy" style="display: none; height: 800px;">
            <iframe src="_static/plots/kde_Italy.png" width="750" height="750" style="border: 0;"></iframe>
        </div>

        <div id="kde-latvia" style="display: none; height: 800px;">
            <iframe src="_static/plots/kde_Latvia.png" width="750" height="750" style="border: 0;"></iframe>
        </div>

        <div id="kde-lithuania" style="display: none; height: 800px;">
            <iframe src="_static/plots/kde_Lithuania.png" width="750" height="750" style="border: 0;"></iframe>
        </div>

        <div id="kde-luxembourg" style="display: none; height: 800px;">
            <iframe src="_static/plots/kde_Luxembourg.png" width="750" height="750" style="border: 0;"></iframe>
        </div>

        <div id="kde-netherlands" style="display: none; height: 800px;">
            <iframe src="_static/plots/kde_Netherlands.png" width="750" height="750" style="border: 0;"></iframe>
        </div>

        <div id="kde-poland" style="display: none; height: 800px;">
            <iframe src="_static/plots/kde_Poland.png" width="750" height="750" style="border: 0;"></iframe>
        </div>

        <div id="kde-portugal" style="display: none; height: 800px;">
            <iframe src="_static/plots/kde_Portugal.png" width="750" height="750" style="border: 0;"></iframe>
        </div>

        <div id="kde-romania" style="display: none; height: 800px;">
            <iframe src="_static/plots/kde_Romania.png" width="750" height="750" style="border: 0;"></iframe>
        </div>

        <div id="kde-slovakia" style="display: none; height: 800px;">
            <iframe src="_static/plots/kde_Slovakia.png" width="750" height="750" style="border: 0;"></iframe>
        </div>

        <div id="kde-spain" style="display: none; height: 800px;">
            <iframe src="_static/plots/kde_Spain.png" width="750" height="750" style="border: 0;"></iframe>
        </div>

        <div id="kde-sweden" style="display: none; height: 800px;">
            <iframe src="_static/plots/kde_Sweden.png" width="750" height="750" style="border: 0;"></iframe>
        </div>

        <div id="kde-uk" style="display: none; height: 800px;">
            <iframe src="_static/plots/kde_UK.png" width="750" height="750" style="border: 0;"></iframe>        
        </div>

        
    </div>


    <script>
    function showMap() {
        const value = document.getElementById("countrySelector").value;

        document.querySelectorAll("[id^='kde-']").forEach(div => {
            div.style.display = "none";
        });

        document.getElementById("kde-" + value).style.display = "block";
    }
    </script>

some extra text

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

Tables
~~~~~~~~~~~~~~~~~~

To get a more detailed view of the distribution of subsidies in each country, we created tables showing the top and bottom 20 recipients of subsidies in each country for the years 2023 and 2024. The tables show the name of the recipient, the total amount of subsidies received, the percentage of the total amount of subsidies received by each recipient, and the adress.

.. raw:: html

    <h2 style="text-align: center; margin-bottom: 5px;">Top and Bottom Recipients</h2>
    
    <div style="display: grid; grid-template-columns: 1fr; gap: 10px; max-width: 1600px; margin: 0 auto;">
        
        <!-- 2023 Table -->
        <div style="width: 100%;">
            <div style="position: relative; width: 100%; padding-bottom: 53%; height: 0;">
                <iframe src="_static/plots/table_plot_2023.html"
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;">
                </iframe>
            </div>
        </div>
        
        <!-- 2024 Table -->
        <div style="width: 100%;">
            <div style="position: relative; width: 100%; padding-bottom: 53%; height: 0;">
                <iframe src="_static/plots/table_plot_2024.html"
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;">
                </iframe>
            </div>
        </div>
        
    </div>

test after adding some text to test spaces

shomething else
 


Pie Plots
~~~~~~~~~~~~~~~~~~

To get a better understanding of the distribution of subsidies in each country, we created pie plots for each country and year. The pie plots show the percentage of the total amount of subsidies given to each scheme in each country. You can hover over the pie plots to see the exact values of these percentages, as well.

.. raw:: html

    <h2 style="text-align: center; margin-bottom: 5px;">Distribution of Schemes</h2>
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; max-width: 1600px; margin: 0 auto;">
        
        <!-- Left Column -->
        <div style="width: 100%;">
            <div style="position: relative; width: 100%; padding-bottom: 116.67%; height: 0;">
                <iframe src="_static/plots/pie_plot_2023.html"
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;">
                </iframe>
            </div>
        </div>
        
        <!-- Right Column -->
        <div style="width: 100%;">
            <div style="position: relative; width: 100%; padding-bottom: 116.67%; height: 0;">
                <iframe src="_static/plots/pie_plot_2024.html"
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;">
                </iframe>
            </div>
        </div>
        
    </div>
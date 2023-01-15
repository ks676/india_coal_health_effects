# Plotting 64 units linked to 25% of cumulative mortality

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gdf
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import matplotlib

def main():

    # import states shapefile
    states = gdf.read_file("/Users/kiratsingh/Desktop/research/india_coal/health/input/maps/Indian_States.shp")

    # import unit data
    units = gdf.read_file("/Users/kiratsingh/Desktop/research/india_coal/health/output/visualization_tables/top_25_mort.csv",
                          index_col=False)
    units.crs = 'epsg:4326'
    units.geometry = gdf.points_from_xy(units.longitude, units.latitude)
    units["sum_mean_delta_M_ij"] = units["sum_mean_delta_M_ij"].astype(float)
    print(units.columns)

    india_map = states.plot()
    units.plot(ax=india_map,
                   column=units["sum_mean_delta_M_ij"],
                   markersize=units["sum_mean_delta_M_ij"]*0.5,
                   cmap="inferno_r",
                   legend=True)

    #plt.title('Annual Attributable Premature Mortality per Unit (deaths/year)', fontsize=10)
    #plt.xlabel("Longitude (°E)")
    #plt.ylabel("Latitude (°N)")
    plt.xticks([])
    plt.yticks([])
    plt.savefig("/Users/kiratsingh/Documents/coal_health_effects/visualizations/plots/top_25_mort_by_gen.png",
                dpi=300)

    plt.show()

main()
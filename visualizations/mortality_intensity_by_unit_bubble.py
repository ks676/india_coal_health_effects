# Goal: take as input the unit_mortality_and_ef file and render a map showing bubbles
# for per-unit mortality intensity

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gdf
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import matplotlib

def main():

    # import dataset containing mortality by unit
    unit_mort = gdf.read_file("/Users/kiratsingh/Desktop/research/india_coal/health/output/visualization_tables/unit_mortality_and_ef.csv")
    unit_mort.crs = 'epsg:4326'
    unit_mort.geometry = gdf.points_from_xy(unit_mort.longitude, unit_mort.latitude)
    unit_mort["sum_mean_delta_M_ij"] = unit_mort["sum_mean_delta_M_ij"].astype(float)
    unit_mort["annual_unit_gen_GWh"] = unit_mort["annual_unit_gen_GWh"].astype(float)
    unit_mort["mort_intensity"] = unit_mort["sum_mean_delta_M_ij"]/unit_mort["annual_unit_gen_GWh"]

    # import states shapefile
    states = gdf.read_file("/Users/kiratsingh/Desktop/research/india_coal/health/input/maps/2011_states.shp")

    india_map = states.plot()
    unit_mort.plot(ax=india_map,
                   column=unit_mort["mort_intensity"],
                   markersize= unit_mort["mort_intensity"]*30,
                   cmap="inferno_r",
                   legend=True)

    #plt.title('Premature Mortality Intensity per Unit (deaths/GWh)', fontsize=10)
    #plt.xlabel("Longitude (°E)")
    #plt.ylabel("Latitude (°N)")
    plt.xticks([])
    plt.yticks([])
    plt.savefig("/Users/kiratsingh/Documents/coal_health_effects/visualizations/plots/unit_bubble_mort_intensity.png",
                dpi=300)

    plt.show()


main()


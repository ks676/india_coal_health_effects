# Goal: take as input the unit_mortality_and_ef file and render a map showing bubbles
# for per-unit mortality intensity

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gdf
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import matplotlib

KG_TONNES = 0.001

def main():

    # import dataset containing mortality by unit
    unit_mort = gdf.read_file("/Users/kiratsingh/Desktop/research/india_coal/health/output/visualization_tables/unit_mortality_and_ef.csv")
    unit_mort.crs = 'epsg:4326'
    unit_mort.geometry = gdf.points_from_xy(unit_mort.longitude, unit_mort.latitude)
    unit_mort["annual_plant_CO2_kg"] = unit_mort["annual_plant_CO2_kg"].astype(float)
    unit_mort["annual_unit_gen_GWh"] = unit_mort["annual_unit_gen_GWh"].astype(float)
    unit_mort["carbon_intensity"] = (unit_mort["annual_plant_CO2_kg"]/unit_mort["annual_unit_gen_GWh"])* KG_TONNES

    # import states shapefile
    states = gdf.read_file("/Users/kiratsingh/Desktop/research/india_coal/health/input/maps/2011_states.shp")

    india_map = states.plot()
    unit_mort.plot(ax=india_map,
                   column=unit_mort["carbon_intensity"],
                   markersize= unit_mort["carbon_intensity"]*0.05,
                   cmap="inferno_r",
                   legend=True)

    #plt.title('Carbon Dioxide Emissions Intensity per Unit (tonnesCO2/GWh)', fontsize=10)
    plt.xlabel("Longitude (°E)")
    plt.ylabel("Latitude (°N)")
    plt.savefig("/Users/kiratsingh/Documents/coal_health_effects/visualizations/plots/unit_bubble_carbon_intensity.png",
                dpi=2400)

    plt.show()


main()


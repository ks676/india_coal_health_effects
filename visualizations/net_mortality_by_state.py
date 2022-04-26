# Goal: Create chloropleth map showing net mortality by state (source minus receptor).

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gdf
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import matplotlib

def main():

    # import states shapefile
    states = gdf.read_file("/Users/kiratsingh/Desktop/research/india_coal/health/input/maps/2011_states.shp")

    # import source csv
    source = pd.read_csv(
        "/Users/kiratsingh/Desktop/research/india_coal/health/output/visualization_tables/state_source.csv")

    # import receptor csv
    receptor = pd.read_csv(
        "/Users/kiratsingh/Desktop/research/india_coal/health/output/visualization_tables/state_receptor.csv")

    net = pd.merge(source, receptor,
                      how="left",
                      left_on=["state"],
                      right_on=["state"])

    net['receptor_mort'] = net['receptor_mort'].fillna(0)

    net["export_mort"] = net['source_mort'] - net['receptor_mort']

    # merge exported mortality into shapefile
    states = pd.merge(states, net,
                      how="left",
                      left_on=["NAME"],
                      right_on=["state"])

    # plot chloropleth
    states.plot(column='export_mort',
                cmap="inferno_r",
                legend=True)

    plt.title('Annual Premature Mortality Exported by State', fontsize=10)
    plt.xlabel("Longitude (°E)")
    plt.ylabel("Latitude (°N)")

    plt.show()
main()
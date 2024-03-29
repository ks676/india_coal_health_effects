# Goal: Create chloropleth map showing receptor mortality by state (i.e. map showing
# how many attributable premature deaths are occuring in each state regardless
# of where the responsible emissions occurred.

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gdf
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import matplotlib

def main():

    # import states shapefile as geopandas df
    states = gdf.read_file("/Users/kiratsingh/Desktop/research/india_coal/health/input/maps/Indian_States.shp")

    # import by-unit-and-state dataset
    mort_by_state = pd.read_csv("/Users/kiratsingh/Desktop/research/india_coal/health/output/unit_level/csv/aggregations/fleet/by_unit_and_state.csv")

    # aggregate receptor mortality by state
    mort_by_state = mort_by_state.groupby(['state'], as_index=False).agg({'mean_Delta_M_i_j': 'sum'})

    # join in mort_by_state onto states to create chloropleth map
    states = pd.merge(states, mort_by_state,
                    how="left",
                    left_on=["st_nm"],
                    right_on=["state"])

    states['mean_Delta_M_i_j'] = states['mean_Delta_M_i_j'].fillna(0)

    # plot chloropleth
    states.plot(column='mean_Delta_M_i_j',
                cmap="inferno_r",
                legend=True)

    plt.title('Annual Premature Mortality Borne by State', fontsize=10)
    plt.xlabel("Longitude (°E)")
    plt.ylabel("Latitude (°N)")

    plt.show()

    # rename columns
    states = states.rename(columns={"mean_Delta_M_i_j": "receptor_mort"})

    # select cols
    states = states[["state", "receptor_mort"]]

    # export as csv
    states.to_csv(
        "/Users/kiratsingh/Desktop/research/india_coal/health/output/visualization_tables/state_receptor.csv",
        index=False)

main()
# Goal: Create chloropleth map showing source mortality by state (i.e. map showing
# how many attributable premature deaths are occuring nationwide as a result of
# emissions occuring in each state

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

    states = states[["st_nm", "geometry"]]

    states = states.to_crs(4326)

    # import unit mortality and ef file - this contains mortality per source unit
    mort_by_unit = pd.read_csv(
        "/Users/kiratsingh/Desktop/research/india_coal/health/output/visualization_tables/unit_mortality_and_ef.csv")

    # convert mort_by_unit df to geodataframe
    mort_by_unit = gdf.GeoDataFrame(mort_by_unit, geometry=gdf.points_from_xy(mort_by_unit["longitude"],
                                                                              mort_by_unit["latitude"]),
                                    crs=4326)

    # spatial join to map each unit based on its lat and lon to a state
    mort_by_unit = mort_by_unit.sjoin(states, how="left", predicate='intersects')

    # aggregate source mortality by state
    mort_by_unit = mort_by_unit.groupby(['st_nm'], as_index=False).agg({'sum_mean_delta_M_ij': 'sum'})



    # join back into states file for plotting
    states = pd.merge(states, mort_by_unit,
                      how="left",
                      left_on=["st_nm"],
                      right_on=["st_nm"])

    states['sum_mean_delta_M_ij'] = states['sum_mean_delta_M_ij'].fillna(0)



    # plot chloropleth
    states.plot(column='sum_mean_delta_M_ij',
                cmap="inferno_r",
                legend=True)

    plt.title('Annual Premature Mortality Sourced in State', fontsize=10)
    plt.xlabel("Longitude (°E)")
    plt.ylabel("Latitude (°N)")

    plt.show()

    # rename columns
    states = states.rename(columns={"sum_mean_delta_M_ij": "source_mort",
                                    "st_nm": "state"})

    # select cols
    states = states[["state", "source_mort"]]

    # export as csv
    states.to_csv(
        "/Users/kiratsingh/Desktop/research/india_coal/health/output/visualization_tables/state_source.csv",
        index=False)


main()
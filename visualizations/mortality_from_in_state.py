# Goal: Create chloropleth map showing, for each state, the amount of mortality that occurs in that
# state as a result of emissions occurring inside that state

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
    states = states[["NAME", "geometry"]]
    states = states.to_crs(4326)

    # import unit mortality and ef file - this contains mortality per source unit
    mort_by_unit = pd.read_csv(
        "/Users/kiratsingh/Desktop/research/india_coal/health/output/visualization_tables/unit_mortality_and_ef.csv")

    # import csv containing unit-attributable mortality by receptor state
    mort_by_unit_and_state = pd.read_csv(
        "/Users/kiratsingh/Desktop/research/india_coal/health/output/unit_level/csv/aggregations/fleet/by_unit_and_state.csv")

    # convert mort_by_unit df to geodataframe
    mort_by_unit = gdf.GeoDataFrame(mort_by_unit, geometry=gdf.points_from_xy(mort_by_unit["longitude"],
                                                                              mort_by_unit["latitude"]),
                                    crs=4326)

    # spatial join to map each unit based on its lat and lon to a state
    mort_by_unit = mort_by_unit.sjoin(states, how="left", predicate='intersects')

    unit_state = mort_by_unit[["unit", "NAME"]]

    # join in unit_state onto mort_by_unit_state to get source state column
    mort_by_unit_and_state = pd.merge(mort_by_unit_and_state, unit_state,
                      how="left",
                      left_on=["unit"],
                      right_on=["unit"])

    mort_by_unit_and_state = mort_by_unit_and_state.rename(columns={"state": "receptor_state",
                                    "NAME": "source_state"})

    mort_by_unit_and_state = mort_by_unit_and_state[
        mort_by_unit_and_state["receptor_state"] == mort_by_unit_and_state["source_state"]]

    mort_by_receptor_state = mort_by_unit_and_state.groupby(['receptor_state'],
                                                            as_index=False).agg({'Delta_M_i_j': 'sum'})

    states = pd.merge(states, mort_by_receptor_state,
                      how="left",
                      left_on=["NAME"],
                      right_on=["receptor_state"])

    states = states.rename(columns={'Delta_M_i_j': "mort_from_in_state"})

    states = states[["NAME", "mort_from_in_state", "geometry"]]

    states['mort_from_in_state'] = states['mort_from_in_state'].fillna(0)

    # plot chloropleth
    states.plot(column='mort_from_in_state',
                cmap="inferno_r",
                legend=True)

    plt.title('Annual Premature Mortality from in-State Sources', fontsize=10)
    plt.xlabel("Longitude (°E)")
    plt.ylabel("Latitude (°N)")

    plt.show()

main()
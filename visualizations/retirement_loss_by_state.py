# Goal: For units that are being proposed for retirement, estimate how much capacity they constitute of their
# home state, in absolute value and as percentage of total installed capacity in that state

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

    # import file containing units proposed for retirement
    mort_by_unit = pd.read_csv(
        "/Users/kiratsingh/Desktop/research/india_coal/health/output/visualization_tables/top_25_mort.csv")



    # convert mort_by_unit df to geodataframe
    mort_by_unit = gdf.GeoDataFrame(mort_by_unit, geometry=gdf.points_from_xy(mort_by_unit["longitude"],
                                                                              mort_by_unit["latitude"]),
                                    crs=4326)

    # spatial join to map each unit based on its lat and lon to a state
    mort_by_unit = mort_by_unit.sjoin(states, how="left", predicate='intersects')

    # get proposed retired capacity by state
    mort_by_unit = mort_by_unit.groupby(['st_nm'], as_index=False).agg({'unit_capacity': 'sum'})

    # import dataset containing mortality by unit for all units
    unit_cap = pd.read_csv(
        "/Users/kiratsingh/Desktop/research/india_coal/health/output/visualization_tables/unit_mortality_and_ef.csv")

    # convert unit_cap df to geodataframe
    unit_cap = gdf.GeoDataFrame(unit_cap, geometry=gdf.points_from_xy(unit_cap["longitude"],
                                                                              unit_cap["latitude"]),
                                    crs=4326)

    # filter out retired units
    unit_cap = unit_cap[unit_cap["status"] != "retired"]

    # spatial join to map each unit based on its lat and lon to a state
    cap_by_state = unit_cap.sjoin(states, how="left", predicate='intersects')

    # get total capacity by state
    cap_by_state = cap_by_state.groupby(['st_nm'], as_index=False).agg({'unit_capacity': 'sum'})

    # join both tables together
    cap_loss = pd.merge(mort_by_unit, cap_by_state,
                      how="left",
                      left_on=["st_nm"],
                      right_on=["st_nm"])

    cap_loss = cap_loss.rename(columns={"unit_capacity_x": "proposed_for_retirement",
                                    "unit_capacity_y": "total_across_units"})

    cap_loss["percentage_loss"] = (cap_loss["proposed_for_retirement"]/ cap_loss["total_across_units"])*100

    print(cap_loss)

main()
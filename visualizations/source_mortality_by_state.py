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
    states = gdf.read_file("/Users/kiratsingh/Desktop/research/india_coal/health/input/maps/2011_states.shp")

    states = states[["NAME", "geometry"]]

    states = states.to_crs(4326)

    # import unit mortality and ef file - this contains mortality per source
    mort_by_unit = pd.read_csv(
        "/Users/kiratsingh/Desktop/research/india_coal/health/output/visualization_tables/unit_mortality_and_ef.csv")

    # convert mort_by_unit df to geodataframe
    mort_by_unit = gdf.GeoDataFrame(mort_by_unit, geometry=gdf.points_from_xy(mort_by_unit["longitude"],
                                                                              mort_by_unit["latitude"]),
                                    crs=4326)

    # spatial join to map each unit based on its lat and lon to a state
    mort_by_unit = mort_by_unit.sjoin(states, how="left", predicate='intersects')

    # aggregate source mortality by state
    mort_by_unit = mort_by_unit.groupby(['NAME'], as_index=False).agg({'sum_delta_M_ij': 'sum'})



    # join back into states file for plotting
    states = pd.merge(states, mort_by_unit,
                      how="left",
                      left_on=["NAME"],
                      right_on=["NAME"])

    states['sum_delta_M_ij'] = states['sum_delta_M_ij'].fillna(0)



    # plot chloropleth
    states.plot(column='sum_delta_M_ij',
                cmap="inferno_r",
                legend=True)

    plt.show()

    # rename columns
    states = states.rename(columns={"sum_delta_M_ij": "source_mort",
                                    "NAME": "state"})

    # select cols
    states = states[["state", "source_mort"]]

    # export as csv
    states.to_csv(
        "/Users/kiratsingh/Desktop/research/india_coal/health/output/visualization_tables/state_source.csv",
        index=False)


main()
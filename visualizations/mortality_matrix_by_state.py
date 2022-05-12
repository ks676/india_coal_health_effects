# Goal: create a matrix showing source-receptor mortality transfers
# across all states

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

    # aggregate by source-receptor pairs
    mort_by_source_receptor = mort_by_unit_and_state.groupby(
        ['receptor_state', 'source_state'], as_index=False).agg({'Delta_M_i_j': 'sum'})

    # rename for clarity
    mort_by_source_receptor = mort_by_source_receptor.rename(columns={"Delta_M_i_j": "mort"})
    mort_by_source_receptor = mort_by_source_receptor[mort_by_source_receptor['receptor_state'] != "Tamilnadu"]

    receptor_states = mort_by_source_receptor["receptor_state"].unique()
    source_states = mort_by_source_receptor["source_state"].unique()

    print(len(receptor_states))

    # initialise matrix
    mort_matrix = np.zeros((32,32))

    # i will track sources, j will track receptors
    # using len(receptor states) even for sources  because that is more comprehensive
    for i in range(len(receptor_states)):
        # filter mort_by_source_receptor to rows where the source is i, if available
        source_i = receptor_states[i]
        for j in range(len(receptor_states)):
            receptor_j = receptor_states[j]
            # filter mort_by_source_receptor to rows where source_i is the source state
            # and receptor_i is the receptor state
            mort_ij = mort_by_source_receptor[
                (mort_by_source_receptor["source_state"] == source_i) & (mort_by_source_receptor["receptor_state"] == receptor_j)]
            val_ij = np.array(mort_ij["mort"])
            # if this pairing doesn't exist, then the mortality transfer from source to receptor is 0
            if len(val_ij) == 0:
                val_ij = 0
            else:
                val_ij = val_ij[0]
            # store val_ij in position ij in matrix
            mort_matrix[i,j] = val_ij

    cmap = matplotlib.colors.ListedColormap(["white", "rosybrown",
                                             "lightcoral", "indianred",
                                             "brown", "firebrick",
                                             "maroon", "grey",
                                             "dimgrey", "black"])
    norm = matplotlib.colors.BoundaryNorm(np.arange(-0.5, 4), cmap.N)

    plt.imshow(mort_matrix, cmap=cmap)
    plt.colorbar(fraction=0.046)
    plt.title("Mortality Transfers from Source to Receptor States (deaths/year)",
              fontsize=10)
    plt.xlabel("Receptor States")
    plt.ylabel("Source States")
    plt.xticks(range(len(receptor_states)), receptor_states,
               fontsize=6,
               rotation=90)
    plt.yticks(range(len(receptor_states)), receptor_states,
               fontsize=6)
    plt.tight_layout()
    plt.savefig("/Users/kiratsingh/Documents/coal_health_effects/visualizations/plots/mort_matrix_by_state.png",
                dpi=2400)
    plt.show()


main()
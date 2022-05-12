# Goal: This script creates four maps, aligned in a grid, that show total receptor mortality by state,
# mortality in state from in-state emissions, mortality outside state from in-state emissions, and
# net mortality in each state (source - receptor)

# Goal: Create choropleth map showing, for each state, the amount of mortality that occurs in that
# state as a result of emissions occurring inside that state

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gdf
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import matplotlib

def main():

    print("x")

    # import states shapefile
    states = gdf.read_file("/Users/kiratsingh/Desktop/research/india_coal/health/input/maps/2011_states.shp")
    states = states[["NAME", "geometry"]]
    states = states.to_crs(4326)

    ##################################################################################################################
    #                   Prepare dataset for plot 1: Receptor mortality by state                                      #
    ##################################################################################################################

    # import by-unit-and-state dataset
    mort_by_state = pd.read_csv(
        "/Users/kiratsingh/Desktop/research/india_coal/health/output/unit_level/csv/aggregations/fleet/by_unit_and_state.csv")

    # aggregate receptor mortality by state
    mort_by_state = mort_by_state.groupby(['state'], as_index=False).agg({'Delta_M_i_j': 'sum'})

    # join in mort_by_state onto states to create chloropleth map
    plot_1 = pd.merge(states, mort_by_state,
                      how="left",
                      left_on=["NAME"],
                      right_on=["state"])

    plot_1['Delta_M_i_j'] = plot_1['Delta_M_i_j'].fillna(0)



    ##################################################################################################################
    #            Prepare dataset for plot 2: In-state mortality from in-state emissions                              #
    ##################################################################################################################

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

    plot_2 = pd.merge(states, mort_by_receptor_state,
                      how="left",
                      left_on=["NAME"],
                      right_on=["receptor_state"])

    plot_2 = plot_2.rename(columns={'Delta_M_i_j': "mort_from_in_state"})

    plot_2 = plot_2[["NAME", "mort_from_in_state", "geometry"]]

    plot_2['mort_from_in_state'] = plot_2['mort_from_in_state'].fillna(0)


    ##################################################################################################################
    #            Prepare dataset for plot 3: Out-of-state mortality from out-of-state emissions                      #
    ##################################################################################################################

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
        mort_by_unit_and_state["receptor_state"] != mort_by_unit_and_state["source_state"]]

    mort_by_receptor_state = mort_by_unit_and_state.groupby(['source_state'],
                                                            as_index=False).agg({'Delta_M_i_j': 'sum'})

    plot_3 = pd.merge(states, mort_by_receptor_state,
                      how="left",
                      left_on=["NAME"],
                      right_on=["source_state"])

    plot_3 = plot_3.rename(columns={'Delta_M_i_j': "out_mort_from_in_state"})

    plot_3 = plot_3[["NAME", "out_mort_from_in_state", "geometry"]]

    plot_3['out_mort_from_in_state'] = plot_3['out_mort_from_in_state'].fillna(0)

    ##################################################################################################################
    #                           Prepare dataset for plot 4: Net mortality by state                                   #
    ##################################################################################################################

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
    plot_4 = pd.merge(states, net,
                      how="left",
                      left_on=["NAME"],
                      right_on=["state"])

    print(plot_4[["NAME", "export_mort"]])
    ##################################################################################################################
    #                                               Plot Maps                                                        #
    ##################################################################################################################

    fig, axs = plt.subplots(2,2)

    plot_1.plot(column='Delta_M_i_j',
                cmap="inferno_r",
                legend=True, ax=axs[0,0])

    plot_2.plot(column='mort_from_in_state',
                cmap="inferno_r",
                legend=True, ax=axs[0,1])

    plot_3.plot(column='out_mort_from_in_state',
                cmap="inferno_r",
                legend=True, ax=axs[1, 0])

    plot_4.plot(column='export_mort',
                cmap="inferno_r",
                legend=True, ax=axs[1, 1])

    # set titles
    axs[0,0].set_title("(1) In-state Mortality from all EGUs", fontsize=9.5)
    axs[0,1].set_title("(2) In-state Mortality from in-state EGUs", fontsize=9.5)
    axs[1,0].set_title("(3) Exported Mortality from in-state EGUs", fontsize=9.5)
    axs[1,1].set_title("(4) Net Mortality (source - receptor) by State", fontsize=9.5)

    plt.rcParams.update({'font.size': 12})
    plt.suptitle("Mortality by State", fontsize=10, fontweight='bold')
    fig.supxlabel("Longitude (°E)", fontsize=10)
    fig.supylabel("Latitude (°N)", fontsize=10)
    plt.tight_layout()

    plt.savefig("/Users/kiratsingh/Documents/coal_health_effects/visualizations/plots/mort_by_state_combined.png",
                dpi=2400)
    plt.show()



main()
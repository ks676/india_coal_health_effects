# Goal: Produce correlation plot between annual output and absolute
# mortality intensity for each unit - for SI

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gdf
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import matplotlib

def main():



    # import dataset containing mortality by unit
    unit_mort = pd.read_csv(
        "/Users/kiratsingh/Desktop/research/india_coal/health/output/visualization_tables/unit_mortality_and_ef.csv")

    # plot mortality intensity against generation
    x = np.array(unit_mort["annual_unit_gen_GWh"])
    y = np.array(unit_mort["sum_mean_delta_M_ij"]/unit_mort["annual_unit_gen_GWh"])

    plt.scatter(x, y, c="blue")
    plt.xlabel("Total Generation in 2019 (GWh)")
    plt.ylabel("Mortality Intensity of Generation in 2019 (Deaths/GWh)")

    plt.savefig("/Users/kiratsingh/Documents/coal_health_effects/visualizations/plots/si/gen_v_mort_int_by_unit.png",
                dpi=300)

    plt.show()

    # plot mortality intensity against emission factors

    x = np.array(unit_mort["annual_plant_SO2_kg"]/(unit_mort["annual_unit_gen_GWh"]*1000))

    plt.scatter(x, y, c="blue")
    plt.xlabel("SO2 Emission Factor (tonnes/GWh)")
    plt.ylabel("Mortality Intensity of Generation in 2019 (Deaths/GWh)")

    plt.savefig("/Users/kiratsingh/Documents/coal_health_effects/visualizations/plots/si/so2_int_v_mort_int_by_unit.png",
                dpi=300)

    plt.show()

main()
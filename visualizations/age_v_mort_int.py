# Goal: Produce correlation plot between age and
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

    # plot mortality against generation
    x = np.array(2019 - unit_mort["unit_commissioning_year"])
    y = np.array(unit_mort["sum_mean_delta_M_ij"]/unit_mort["annual_unit_gen_GWh"])


    plt.scatter(x, y, c="blue")
    plt.xlabel("Age of Unit in 2019")
    plt.ylabel("Mortality Intensity of Generation in 2019 (Deaths/GWh)")

    plt.savefig("/Users/kiratsingh/Documents/coal_health_effects/visualizations/plots/si/age_v_mort_int_by_unit.png",
                dpi=300)

    plt.show()

main()
# Goal: Produce correlation plot between annual output and absolute
# annual attributable mortality for each unit - for SI

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
    x = np.array(unit_mort["annual_unit_gen_GWh"])
    y = np.array(unit_mort["sum_mean_delta_M_ij"])
    z = np.array(unit_mort["annual_plant_SO2_kg"]/1000000)

    plt.scatter(x, y, c=z)
    plt.xlabel("Total Generation in 2019 (GWh)")
    plt.ylabel("Total Attributable Mortality in 2019 (Deaths)")
    plt.colorbar(label='Total SO2 Emissions in 2019 (kt)')

    plt.savefig("/Users/kiratsingh/Documents/coal_health_effects/visualizations/plots/si/gen_v_abs_mort_by_unit.png",
                dpi=300)

    plt.show()

main()
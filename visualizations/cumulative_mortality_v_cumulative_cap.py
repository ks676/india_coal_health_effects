# Goal: Take the unit mortality table and plot cumulative mortality against cumulative capacity to illustrate
# the extent to which certain units disproportionately contribute to overall mortality

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gdf
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import matplotlib

def main():

    # import dataset containing mortality by unit
    unit_mort = pd.read_csv("/Users/kiratsingh/Desktop/research/india_coal/health/output/visualization_tables/unit_mortality_and_ef.csv")

    # create col to reflect mortality intensity
    unit_mort["sum_mean_delta_M_ij"] = unit_mort["sum_mean_delta_M_ij"].astype(float)
    unit_mort["mort_intensity"] = unit_mort["sum_mean_delta_M_ij"] / unit_mort["unit_capacity"]

    # sort in descending order of mortality intensity
    unit_mort = unit_mort.sort_values(by='mort_intensity', ascending=False)

    # calculate cumulative sums of mortality and generation
    unit_mort["cum_mort"] = unit_mort["sum_mean_delta_M_ij"].cumsum()
    unit_mort["cum_cap"] = unit_mort["unit_capacity"].cumsum()

    # calculate percentage of total mortality and generation
    total_mort = sum(unit_mort["sum_mean_delta_M_ij"])
    total_cap = sum(unit_mort["unit_capacity"])
    unit_mort["cum_mort_perc"] = (unit_mort["cum_mort"]/total_mort)*100
    unit_mort["cum_cap_perc"] = (unit_mort["cum_cap"] / total_cap) * 100

    # export cumulative totals
    unit_mort.to_csv(
        "/Users/kiratsingh/Desktop/research/india_coal/health/output/visualization_tables/cum_mort_cap.csv",
        index=False)

    # line chart of cumulative mortality against cumulative generation
    x = np.array(unit_mort["cum_cap_perc"])
    y = np.array(unit_mort["cum_mort_perc"])

    # overlays to highlight cut-offs
    mort_markers = [25.002, 50.068, 75.015]
    gen_markers = [4.466, 24.153, 53.896]


    plt.plot(x,y)
    plt.scatter(gen_markers, mort_markers, c="green")
    plt.annotate("25% of mortality from 4.46% of capacity", (7,23))
    plt.annotate("50.07%, 24.15%", (27, 47))
    plt.annotate("75.02%, 53.9%", (57, 72))
    plt.title("Cumulative Premature Mortality vs. Cumulative Capacity")
    plt.xlabel("Cumulative Capacity (% of total)")
    plt.ylabel("Cumulative Premature Mortality (% of total)")

    plt.savefig("/Users/kiratsingh/Documents/coal_health_effects/visualizations/plots/cum_mort_v_cum_cap.png",
                dpi=300)

    plt.show()





main()
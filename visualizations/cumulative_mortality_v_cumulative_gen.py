# Goal: Take the unit mortality table and plot cumulative mortality against cumulative generation to illustrate
# the extent to which certain units disproportionately contribute to overall mortality

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def main():

    # import dataset containing mortality by unit
    unit_mort = pd.read_csv("/Users/kiratsingh/Desktop/research/india_coal/health/output/visualization_tables/unit_mortality_and_ef.csv")

    print(len(unit_mort))

    # create col to reflect mortality intensity
    unit_mort["sum_mean_delta_M_ij"] = unit_mort["sum_mean_delta_M_ij"].astype(float)
    unit_mort["sum_min_delta_M_ij"] = unit_mort["sum_min_delta_M_ij"].astype(float)
    unit_mort["sum_max_delta_M_ij"] = unit_mort["sum_max_delta_M_ij"].astype(float)
    unit_mort["annual_unit_gen_GWh"] = unit_mort["annual_unit_gen_GWh"].astype(float)
    unit_mort["mean_mort_intensity"] = unit_mort["sum_mean_delta_M_ij"] / unit_mort["annual_unit_gen_GWh"]
    unit_mort["min_mort_intensity"] = unit_mort["sum_min_delta_M_ij"] / unit_mort["annual_unit_gen_GWh"]
    unit_mort["max_mort_intensity"] = unit_mort["sum_max_delta_M_ij"] / unit_mort["annual_unit_gen_GWh"]

    # sort in descending order of mortality intensity
    unit_mort = unit_mort.sort_values(by='mean_mort_intensity', ascending=False)

    # calculate cumulative sums of mortality and generation
    unit_mort["cum_mort"] = unit_mort["sum_mean_delta_M_ij"].cumsum()
    unit_mort["cum_gen"] = unit_mort["annual_unit_gen_GWh"].cumsum()

    # calculate percentage of total mortality and generation
    total_mort = sum(unit_mort["sum_mean_delta_M_ij"])
    total_gen = sum(unit_mort["annual_unit_gen_GWh"])
    unit_mort["cum_mort_perc"] = (unit_mort["cum_mort"]/total_mort)*100
    unit_mort["cum_gen_perc"] = (unit_mort["cum_gen"]/total_gen)*100

    # export cumulative totals
    unit_mort.to_csv(
        "/Users/kiratsingh/Desktop/research/india_coal/health/output/visualization_tables/cum_mort_gen.csv",
        index=False)

    # line chart of cumulative mortality against cumulative generation
    x = np.array(unit_mort["cum_gen_perc"])
    y = np.array(unit_mort["cum_mort_perc"])

    # overlays to highlight cut-offs
    mort_markers = [25.157, 50.035, 75.133]
    gen_markers = [4.506, 22.421, 52.373]


    plt.plot(x,y)
    plt.scatter(gen_markers, mort_markers, c="green")
    plt.annotate("25.15% of mortality from 4.50% of generation", (7,23))
    plt.annotate("50.03%, 22.42%%", (25, 47))
    plt.annotate("75.13%, 52.37%", (55, 72))
    plt.title("Cumulative Premature Mortality vs. Cumulative Generation")
    plt.xlabel("Cumulative Generation (% of total)")
    plt.ylabel("Cumulative Premature Mortality (% of total)")
    plt.savefig("/Users/kiratsingh/Documents/coal_health_effects/visualizations/plots/cum_mort_v_cum_gen.png",
                dpi=300)

    plt.show()


main()
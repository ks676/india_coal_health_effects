# Goal: Use the retirement_scenarios_for_plotting csv
# to create a bar chart showing reduced damages under
# different retirement scenarios, along with CIs to
# account for uncertainty in VSL and SCC

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

DOLLAR_BILLIONS = 1/1000000000

def main():

    # import csv
    damages = pd.read_csv(
        "/Users/kiratsingh/Desktop/research/india_coal/health/output/visualization_tables/retirement_scenarios_for_plotting.csv",
    index_col=False)

    # define variables used for chart
    min_mort_reduced_mort = damages["mort_min_mort_reduced_damages_mid"]*DOLLAR_BILLIONS
    min_mort_reduced_co2 = damages["mort_min_co2_reduced_damages_mid"]*DOLLAR_BILLIONS
    min_co2_reduced_mort = damages["co2_min_mort_reduced_damages_mid"]*DOLLAR_BILLIONS
    min_co2_reduced_co2 = damages["co2_min_co2_reduced_damages_mid"]*DOLLAR_BILLIONS

    # construct error vectors
    mort_min_lower_mort = (damages["mort_min_mort_reduced_damages_mid"] - damages["mort_min_mort_reduced_damages_low"])*DOLLAR_BILLIONS
    mort_min_upper_mort = (damages["mort_min_mort_reduced_damages_high"] - damages["mort_min_mort_reduced_damages_mid"])*DOLLAR_BILLIONS
    mort_min_mort_error = [mort_min_lower_mort, mort_min_upper_mort]

    mort_min_lower_co2 = (damages["mort_min_co2_reduced_damages_mid"] - damages[
        "mort_min_co2_reduced_damages_low"]) * DOLLAR_BILLIONS
    mort_min_upper_co2 = (damages["mort_min_co2_reduced_damages_high"] - damages[
        "mort_min_co2_reduced_damages_mid"]) * DOLLAR_BILLIONS
    mort_min_co2_error = [mort_min_lower_co2, mort_min_upper_co2]

    co2_min_lower_mort = (damages["co2_min_mort_reduced_damages_mid"] - damages[
        "co2_min_mort_reduced_damages_low"]) * DOLLAR_BILLIONS
    co2_min_upper_mort = (damages["co2_min_mort_reduced_damages_high"] - damages[
        "co2_min_mort_reduced_damages_mid"]) * DOLLAR_BILLIONS
    co2_min_mort_error = [co2_min_lower_mort, co2_min_upper_mort]

    co2_min_lower_co2 = (damages["co2_min_co2_reduced_damages_mid"] - damages[
        "co2_min_co2_reduced_damages_low"]) * DOLLAR_BILLIONS
    co2_min_upper_co2 = (damages["co2_min_co2_reduced_damages_high"] - damages[
        "co2_min_co2_reduced_damages_mid"]) * DOLLAR_BILLIONS
    co2_min_co2_error = [co2_min_lower_co2, co2_min_upper_co2]


    # spacing parameters
    barWidth = 0.2
    r1 = [0, 1, 2, 3]
    r2 = [0.2, 1.2, 2.2, 3.2]
    r3 = [0.5, 1.5, 2.5, 3.5]
    r4 = [0.7, 1.7, 2.7, 3.7]

    plt.bar(r1, min_mort_reduced_mort, width=barWidth,
            color='lightblue', edgecolor='lightblue', yerr= mort_min_mort_error,
            capsize=7, label='Mortality Minimization - Mortality Benefits')
    plt.bar(r2, min_mort_reduced_co2, width=barWidth,
            color='steelblue', edgecolor='steelblue',
            yerr=mort_min_co2_error, capsize=7,
            label='Mortality Minimization - Climate Benefits')
    plt.bar(r3, min_co2_reduced_mort, width=barWidth,
            color='limegreen', edgecolor='limegreen',
            yerr=co2_min_mort_error, capsize=7,
            label='CO2 Minimization - Mortality Benefits')
    plt.bar(r4, min_co2_reduced_co2, width=barWidth,
            color='green', edgecolor='green',
            yerr=co2_min_co2_error, capsize=7,
            label='CO2 Minimization - Climate Benefits')

    plt.xticks([0.2, 1.2, 2.2, 3.2], ['5%', '10%', '15%', '20%'])

    plt.xlabel("Generation Replaced (%)")
    plt.ylabel("Avoided Damages (US$ billions)")

    plt.legend()
    plt.tight_layout()

    plt.savefig("/Users/kiratsingh/Documents/coal_health_effects/visualizations/plots/reduced_damages_by_scenario.png",
                dpi=400)
    plt.show()

main()
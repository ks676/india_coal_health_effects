# Goal: Take as input the per-unit mortality figures unit_level_aggregations,
# and the top_50_units csv which contains unit-level metadata. Merge
# those two together and plot basic correlations: annual generation vs.
# annual attributable mortality, annual CO2 generation vs. annual
# attributable mortality, and climate change damages v. health damages
# (would look identical to the CO2 v. mortality but in monetary units).

import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

def main():

    # import csv containing unit-level data on annual generation, carbon dioxide emissions and other
    # criteria air pollutant emissions
    unit_meta = pd.read_csv("/Users/kiratsingh/Documents/india_thermal_ts/output/top_50_thermal_units.csv")
    unit_meta['unit'] = unit_meta['unit'].astype(str)

    # import csv containing unit-level mortality aggregates
    unit_mortality = pd.read_csv("/Users/kiratsingh/Desktop/research/india_coal/health/output/unit_level/csv/aggregations/fleet/by_unit.csv")
    # remove mundra_umtpp rows because it is at a different scale (plant level rather than unit level)
    unit_mortality = unit_mortality[unit_mortality['unit'] != 'MUNDRA_UMTPP']

    # create join keys
    unit_mortality['unit_num'] = unit_mortality['unit'].str.slice(start=-1)
    unit_mortality['unit'] = unit_mortality['unit'].str.slice_replace(-2, repl='')
    unit_mortality['unit'] = unit_mortality['unit'].str.replace('_', ' ')
    unit_mortality = unit_mortality.rename(columns={"unit": "plant",
                                                    "unit_num": "unit"})
    unit_mortality['unit'] = unit_mortality['unit'].astype(str)



    # merge the two tables
    unit = pd.merge(unit_mortality, unit_meta,
                    how="left",
                    left_on=["plant", "unit"],
                    right_on=["plant", "unit"])

    ###################################################################################################################
    #################################################### Plots ########################################################
    ###################################################################################################################

    # Annual Attributable Mortality vs. Annual Generation
    x = unit['annual_unit_gen_GWh']
    y = unit['sum_delta_M_ij']
    color = unit['annual_plant_CO2_kg']

    fig, ax = plt.subplots()
    ax.scatter(x, y, c=color)
    plt.xlabel("Total Generation in 2019 (GWh)")
    plt.ylabel("Attributable Premature Mortality in 2019 (Deaths)")

    #z = np.polyfit(x, y, 1)
    #p = np.poly1d(z)
    #plt.plot(x, p(x))

    plt.show()

    # Annual Attributable Mortality vs. Annual CO2 emissions
    x = unit['annual_plant_CO2_kg']/1000000
    y = unit['sum_delta_M_ij']

    fig, ax = plt.subplots()
    ax.scatter(x, y)
    plt.xlabel("Estimated CO2 emissions in 2019 ('000 tonnes)")
    plt.ylabel("Attributable Premature Mortality in 2019 (Deaths)")

    # z = np.polyfit(x, y, 1)
    # p = np.poly1d(z)
    # plt.plot(x, p(x))

    plt.show()

    # Annual Attributable Mortality Damages vs.
    # Annual Climate Damages using SCCO2
    x = (unit['annual_plant_CO2_kg'] / 1000)*(40/1000000)
    y = (unit['sum_delta_M_ij'])*0.5

    fig, ax = plt.subplots()
    ax.scatter(x, y)
    plt.xlabel("Climate Change Damages (@SCCO2 = $40/ton)")
    plt.ylabel("Health Damages (@VSL = $500,000)")
    plt.title("Per-unit Health vs. Climate Damages, USD millions")

    # z = np.polyfit(x, y, 1)
    # p = np.poly1d(z)
    # plt.plot(x, p(x))

    plt.show()


main()

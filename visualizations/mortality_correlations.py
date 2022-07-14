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

SCC = 50
VSL = 161000

def main():

    # import csv containing unit-level data on annual generation, carbon dioxide emissions and other
    # criteria air pollutant emissions
    unit_meta = pd.read_csv("/Users/kiratsingh/Documents/india_thermal_ts/output/all_thermal_units.csv")
    unit_meta['unit'] = unit_meta['unit'].astype(str)

    # import csv containing unit-level mortality aggregates
    unit_mortality = pd.read_csv("/Users/kiratsingh/Desktop/research/india_coal/health/output/unit_level/csv/aggregations/fleet/by_unit.csv")
    # remove mundra_umtpp rows because it is at a different scale (plant level rather than unit level)
    unit_mortality = unit_mortality[unit_mortality['unit'] != 'MUNDRA_UMTPP']

    # import csv containing capacities
    unit_capacity = pd.read_csv('/Users/kiratsingh/Documents/india_thermal_ts/output/all_thermal_units_metadata.csv')
    unit_capacity = unit_capacity[["unit", "unit_capacity", "unit_commissioning_year"]]
    # create join keys
    unit_meta['plant'] = unit_meta['plant'].str.replace(' ','_')
    unit_meta['unit'] = unit_meta['plant'] + "_" + unit_meta['unit']


    # merge unit mortality and unit meta
    unit = pd.merge(unit_mortality, unit_meta,
                    how="left",
                    left_on=["unit"],
                    right_on=["unit"])

    # merge in capacity
    unit = pd.merge(unit, unit_capacity,
                    how="left",
                    left_on=["unit"],
                    right_on=["unit"])


    # save merged table as csv
    unit.to_csv("/Users/kiratsingh/Desktop/research/india_coal/health/output/visualization_tables/unit_mortality_and_ef.csv", index=False)

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

    plt.show()

    # Annual Attributable Mortality vs. Annual CO2 emissions
    x = unit['annual_plant_CO2_kg']/1000000
    y = unit['sum_delta_M_ij']

    fig, ax = plt.subplots()
    ax.scatter(x, y)
    plt.xlabel("Estimated CO2 emissions in 2019 ('000 tonnes)")
    plt.ylabel("Attributable Premature Mortality in 2019 (Deaths)")

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

    lims = [
        np.min([ax.get_xlim(), ax.get_ylim()]),  # min of both axes
        np.max([ax.get_xlim(), ax.get_ylim()]),  # max of both axes
        ]

    ax.plot(lims, lims, 'k-', alpha=0.75, zorder=0)
    ax.set_aspect('equal')
    ax.set_xlim(lims)
    ax.set_ylim(lims)

    plt.show()


    # Mortality per GWh (deaths) vs. CO2 per GWh (kgs)
    x = unit['annual_plant_CO2_kg']/(unit['annual_unit_gen_GWh']*1000)
    y = unit['sum_delta_M_ij']/unit['annual_unit_gen_GWh']

    fig, ax = plt.subplots()
    ax.scatter(x, y)
    plt.xlabel("Estimated CO2 per GWh (tonnes)")
    plt.ylabel("Attributable Deaths per GWh (deaths)")

    # Mortality Damages per GWh ($) vs. Climate change damages per GWh ($)
    x = ((unit['annual_plant_CO2_kg'] / (unit['annual_unit_gen_GWh'] * 1000))*(SCC))/1000
    y = ((unit['sum_delta_M_ij'] / unit['annual_unit_gen_GWh'])*VSL)/1000

    # get median damages for plotting overlays
    median_mort_damage = y.median()
    print(median_mort_damage)
    median_co2_damage = x.median()
    print(median_co2_damage)
    # create vectors for plotting
    mort_vector = np.full((len(x),1),median_mort_damage)
    co2_vector = np.full((len(x),1),median_co2_damage)


    fig, ax = plt.subplots()
    ax.scatter(x, y, c="green")
    plt.xlabel("Estimated Climate Damages per GWh (US$ '000)")
    plt.ylabel("Estimated Mortality Damages per GWh (US$ '000)")
    plt.plot(x, mort_vector, label="Median Health Damages: $14k/GWh")
    plt.plot(co2_vector, y, label="Median Climate Damages: $46k/GWh")
    plt.legend(loc='upper right')

    plt.savefig("/Users/kiratsingh/Documents/coal_health_effects/visualizations/plots/mort_damages_v_carbon_damages.png",
                dpi=2400)

    plt.show()





main()

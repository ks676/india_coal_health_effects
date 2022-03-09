# Goal: This script takes as input the file containing all units' emission factor and plots the
# PM 2.5 emission factors

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Constants
kg_to_tonnes = 0.001
GWh_to_MWh = 1000


def main():

    factors = pd.read_csv("/Users/kiratsingh/Documents/india_thermal_ts/output/all_thermal_units.csv")
    factors["pm25_ef"] = (factors["annual_plant_PM25_kg"]*kg_to_tonnes)/(factors["annual_unit_gen_GWh"] * GWh_to_MWh)

    factors = factors[factors["pm25_ef"] > 0]

    sns.histplot(data=factors, x="pm25_ef")

    plt.xlabel("PM2.5 Emission Factor (tonnes/MWh)", size=12)
    plt.ylabel("Units", size=12)

    plt.axvline(x=factors["pm25_ef"].mean(),color='red')

    plt.show()



main()
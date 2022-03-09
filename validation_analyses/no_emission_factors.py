# Goal: This script takes as input the file containing all units' emission factor and plots the nitrous
# oxide emission factors

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Constants
kg_to_tonnes = 0.001
GWh_to_MWh = 1000


def main():

    factors = pd.read_csv("/Users/kiratsingh/Documents/india_thermal_ts/output/all_thermal_units.csv")
    factors["no_ef"] = (factors["annual_plant_NO_kg"]*kg_to_tonnes)/(factors["annual_unit_gen_GWh"] * GWh_to_MWh)

    factors = factors[factors["no_ef"] > 0]

    sns.histplot(data=factors, x="no_ef")

    plt.xlabel("NO Emission Factor (tonnes/MWh)", size=12)
    plt.ylabel("Units", size=12)

    plt.axvline(x=factors["no_ef"].mean(),color='red')

    plt.show()


main()
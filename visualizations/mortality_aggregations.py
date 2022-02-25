# Goal: This script uses matplotlib to create three simple charts - 1. A bar chart showing mortality by unit,
# 2. A bar chart showing mortality by endpoint, and 3. A bar chart showing mortality by state in which it occurs

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def main():

    # import unit-level mortality dataset
    by_unit = pd.read_csv("/Users/kiratsingh/Desktop/research/india_coal/health/output/unit_level/csv/aggregations/fleet/by_unit.csv")
    # remove mundra_umtpp rows because it is at a different scale (plant level rather than unit level)
    by_unit = by_unit[by_unit['unit'] != 'MUNDRA_UMTPP']
    by_unit = by_unit.sort_values(by='sum_delta_M_ij', ascending=False)



    # create np vectors
    x = by_unit["unit"].values
    y = by_unit["sum_delta_M_ij"].values

    # define bar chart
    fig, ax = plt.subplots()
    ax.bar(x, y, width=1, edgecolor="white", linewidth=0.7)
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.50)

    # show plot
    plt.show()

    # import fleet-wide, mortality-by-endpoint dataset
    by_endpoint = pd.read_csv("/Users/kiratsingh/Desktop/research/india_coal/health/output/unit_level/csv/aggregations/fleet/by_unit_and_endpoint.csv")
    # remove mundra_umtpp rows because it is at a different scale (plant level rather than unit level)
    by_endpoint = by_endpoint[by_endpoint['unit'] != 'MUNDRA_UMTPP']

    # aggregate dataframe by endpoint
    by_endpoint = by_endpoint.groupby(['endpoint'], as_index=False).agg({'Delta_M_i_j': 'sum'})
    by_endpoint = by_endpoint.sort_values(by='Delta_M_i_j', ascending=False)

    # create np vectors
    x = ["Heart Disease", "COPD", "Stroke",
         "LR Infection", "Lung Cancer", "T2 Diabetes"]
    y = by_endpoint["Delta_M_i_j"].values

    # define bar chart
    fig, ax = plt.subplots()
    ax.bar(x, y, width=1, edgecolor="white", linewidth=0.7)
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.50)

    # show plot
    plt.show()

    # import fleet-wide, mortality-by-state dataset
    by_state = pd.read_csv(
        "/Users/kiratsingh/Desktop/research/india_coal/health/output/unit_level/csv/aggregations/fleet/by_unit_and_state.csv")
    # remove mundra_umtpp rows because it is at a different scale (plant level rather than unit level)
    by_state = by_state[by_state['unit'] != 'MUNDRA_UMTPP']

    # aggregate dataframe by state
    by_state = by_state.groupby(['state'], as_index=False).agg({'Delta_M_i_j': 'sum'})
    by_state = by_state[by_state['Delta_M_i_j'] > 10]
    by_state = by_state.sort_values(by='Delta_M_i_j', ascending=False)

    # create np vectors
    y = by_state["state"].values
    y_pos = np.arange(len(y))
    x = by_state["Delta_M_i_j"].values

    # define bar chart
    fig, ax = plt.subplots()
    ax.barh(y_pos, x, align='center')
    ax.set_yticks(y_pos, labels=y)
    ax.invert_yaxis()
    #plt.xticks(rotation=90)
    plt.subplots_adjust(left=0.250)

    # show plot
    plt.show()


main()
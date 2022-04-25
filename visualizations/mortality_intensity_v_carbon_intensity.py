# Goal: Plot unit-level mortality intensity against carbon intensity

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gdf
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import matplotlib

KG_TONNES = 1/1000

def main():

    # import dataset containing mortality by unit
    unit_mort = pd.read_csv(
        "/Users/kiratsingh/Desktop/research/india_coal/health/output/visualization_tables/unit_mortality_and_ef.csv")

    # create col to reflect mortality intensity
    unit_mort["sum_delta_M_ij"] = unit_mort["sum_delta_M_ij"].astype(float)
    unit_mort["annual_unit_gen_GWh"] = unit_mort["annual_unit_gen_GWh"].astype(float)
    unit_mort["mort_intensity"] = unit_mort["sum_delta_M_ij"] / unit_mort["annual_unit_gen_GWh"]

    # create col to reflect carbon intensity
    unit_mort["annual_plant_CO2_kg"] = unit_mort["annual_plant_CO2_kg"].astype(float)
    unit_mort["carbon_intensity"] = (unit_mort["annual_plant_CO2_kg"] / unit_mort["annual_unit_gen_GWh"])*KG_TONNES

    # create vectors for scatterplot
    mort_vec = unit_mort["mort_intensity"]
    carbon_vec = unit_mort["carbon_intensity"]

    # get median intensities for plotting overlays
    unit_mort["mort_intensity_median"] = unit_mort["mort_intensity"].median()
    unit_mort["carbon_intensity_median"] = unit_mort["carbon_intensity"].median()

    # create vectors
    mort_med = unit_mort["mort_intensity_median"]
    carbon_med = unit_mort["carbon_intensity_median"]

    # scatter plot of mortality intensity against carbon intensity
    plt.scatter(carbon_vec, mort_vec, c="green")

    # line overlays for identifying quadrants
    plt.plot(carbon_med, mort_vec, label = "Median Carbon Intensity")
    plt.plot(carbon_vec, mort_med, label = "Median Mortality Intensity")
    plt.legend()

    # titles
    plt.title("Unit-level Mortality Intensity vs. Carbon Intensity")
    plt.xlabel("Carbon Intensity (tonneCO2/GWh)")
    plt.ylabel("Mortality Intensity (annual deaths/GWh)")

    plt.show()

main()
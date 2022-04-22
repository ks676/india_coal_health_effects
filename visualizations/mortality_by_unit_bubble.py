# Goal: take as input the unit_mortality_and_ef file and render a map showing bubbles
# for per-unit mortality

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

def main():

    mortality_by_unit = pd.read_csv("/Users/kiratsingh/Desktop/research/india_coal/health/output/visualization_tables/unit_mortality_and_ef.csv")
    mortality_by_unit["sum_delta_M_ij"] = round(mortality_by_unit["sum_delta_M_ij"])
    mortality_by_unit["latitude"] = mortality_by_unit["latitude"] + np.random.uniform(-0.01, 0.01, len(mortality_by_unit["latitude"]))
    mortality_by_unit["longitude"] = mortality_by_unit["longitude"] + np.random.uniform(-0.01, 0.01, len(mortality_by_unit["latitude"]))
    mortality_by_unit = mortality_by_unit.rename(columns={"sum_delta_M_ij": "deaths/year"})


    fig = px.scatter_geo(mortality_by_unit,
                            lat="latitude",
                            lon="longitude",
                            hover_name="unit",
                            color="deaths/year",
                            color_continuous_scale="inferno_r",
                            size="deaths/year",
                            #zoom=3,
                            height=600)
    #fig.update_layout(mapbox_style="carto-positron")
    #fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_geos(
        visible=False, resolution=50, scope="asia",
        showcountries=True, countrycolor="Black"
    )
    fig.update_layout(height=500, margin={"r": 0, "t": 0, "l": 100, "b": 0})
    fig.show()
main()


# Goal: Take as input the hammer_2019 shapefile, an inmap output concentration file (any is okay because
# we are just using it to get the inmap grid polygons), and the india_states_shapefile.
# Produce two output files - hammer and inmap clipped to the indian states map. This will
# make it easier to process the two files in subsequent scripts by reducing the size of the shapefiles.

import geopandas
from shapely.geometry import Polygon

def main():

    # import the hammer shapefile (POINT geometry)
    hammer = geopandas.read_file("/Users/kiratsingh/Desktop/research/india_coal/concentrations/hammer_et_al/2019/0.05_0.05_GWR/GL_PM25.shp")

    print("Hammer imported")
    print(hammer.head())

    # import the india states shapefile (POLYGON geometry)
    states = geopandas.read_file("/Users/kiratsingh/Desktop/research/india_coal/health/output/2011_states.shp")

    print("States imported")
    print(states.head())

    # clip hammer based on india states
    # "The object on which you call clip is the object that will be clipped. The object you
    # pass is the clip extent." - geopandas docs: https://geopandas.org/en/stable/gallery/plot_clip.html
    hammer = hammer.clip(states)

    print("Hammer clipped")
    print(hammer.head())

    # export clipped hammer
    hammer.to_file("/Users/kiratsingh/Desktop/research/india_coal/health/output/intermediate/hammer_clipped.shp")

    print("Clipped Hammer exported")

    # import the inmap concentration shapefile (POLYGON geometry)
    inmap_grid = geopandas.read_file("/Users/kiratsingh/Documents/mundra_umtpp_emissions.shp")

    print("InMAP imported")

    # clip inmap grid based on india states
    inmap_grid = inmap_grid.clip(states)

    print("InMAP clipped")

    # export clipped inmap_grid
    inmap_grid.to_file("/Users/kiratsingh/Desktop/research/india_coal/health/output/intermediate/inmap_grid_clipped.shp")

    print("Clipped InMAP exported")

main()
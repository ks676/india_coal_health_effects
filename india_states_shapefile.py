# Goal: Take as input the 2011 Indian states shapefile. Produce as output a shapefile which does not contain
# duplicate features as the original one seems to.

import geopandas

def main():

    # open downloaded Indian states file
    states = geopandas.read_file("/Users/kiratsingh/Desktop/research/india_coal/maps/states/STATE2011.shp")

    states = states.drop_duplicates(subset=['NAME'])

    # write back as shapefile for use in further analysis
    states.to_file("/Users/kiratsingh/Desktop/research/india_coal/health/output/2011_states.shp")



main()
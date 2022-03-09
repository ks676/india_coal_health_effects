# Goal: Take as input one of the inmap output files and check to see that
# the population totals are consistent with Census results

import geopandas

def main():

    inmap = geopandas.read_file("/Users/kiratsingh/Desktop/research/india_coal/health/output/intermediate/inmap_grid_clipped.shp")

    print(inmap)
    print(inmap.columns)

    print(sum(inmap["TotalPop"]))


main()
# Goal: take as input the hammer_aggregated_to_inmap file and the states shapefile and bring in the relevant states
# information to the hammer_aggregated_to_inmap shapefile

import geopandas

def main():

    hammer_aggregated = geopandas.read_file(
        "/Users/kiratsingh/Desktop/research/india_coal/health/output/intermediate/hammer_aggregated.shp")

    print(hammer_aggregated.shape[0])

    states = geopandas.read_file("/Users/kiratsingh/Desktop/research/india_coal/health/input/maps/2011_states.shp")

    states = states[['geometry', 'STATE_ID', 'NAME']]

    hammer_aggregated_with_states = hammer_aggregated.sjoin(states, how="left", predicate='intersects')

    # we now have a dataset where every grid cell is matched to its state
    # however, there are around 1000 grid cells that fall along the boundaries of states and therefore get assigned
    # to multiple states - causing the number of rows to grow from 27254 to 29508
    # for those grid cells, we want to just retain the state in which the largest portion of the grid cell is
    # located. to do so, we calculate a new column which contains the area of each polygon/multi-polygon
    # that dataset is dissolved on WKT down to the rows with the largest areas for each WKT.

    hammer_aggregated_with_states['area'] = hammer_aggregated_with_states.geometry.area

    hammer_aggregated_with_states = hammer_aggregated_with_states.dissolve(by='WKT', aggfunc='max')

    print(hammer_aggregated_with_states.shape[0])

    # export dataset as a shapefile
    hammer_aggregated_with_states.to_file(
        "/Users/kiratsingh/Desktop/research/india_coal/health/output/intermediate/hammer_aggregated_with_states.shp")





main()
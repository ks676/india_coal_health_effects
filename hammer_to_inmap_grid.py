# Goal: Take as input the hammer_2019 shapefile, an inmap output concentration file (any is okay because
# we are just using it to get the inmap grid polygons), and the india_states_shapefile.
# Produce as output a file that contains the inmap grid clipped to just India, containing hammer_2019
# concentrations for each grid cell.
# Since there are some grid cells that are too small to contain or intersect with a point object from the
# hammer_2019 shapefile, for those cells, rely on a 'nearest' match.


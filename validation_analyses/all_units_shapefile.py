# Goal: This script iterates through the directory of per-unit input shapefiles and produces a single output
# shapefile that includes annual average emissions from all the units

import os
import geopandas

def main():

    directory = "/Users/kiratsingh/Documents/india_thermal_ts/output/shapefiles"
    output_directory = "/Users/kiratsingh/Desktop/research/india_coal/health/input/fleet_level"

    i = 0
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        split = filename.split('.')
        ext = split[1]
        unit = split[0]


        # if the ext is .shp, it's a shapefile and we want to open and process it using geopandas
        if ext == "shp":

            unit_emissions = geopandas.read_file(filepath)

            if i == 0:

                all_emissions = unit_emissions

            else:

                all_emissions = all_emissions.append(unit_emissions)

            print(unit + " appended")

            i+=1

            # save as shapefile
            path_save = output_directory + "/" + "all_units_2019.shp"
            all_emissions.to_file(path_save)
            print(unit + " exported")



main()
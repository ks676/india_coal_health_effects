# Goal: This script iterates through the folder containing unit-level outputs from InMAP. For every unit, it combines
# the inmap output with the hammer_aggregated_to_inmap_with_states shapefile and produces a shapefile containing all
# the columns - appropriately named - necessary for the premature mortality calculation.

import os
import geopandas

def main():

    # load the hammer_aggregated_to_inmap_with_states shapefile
    hammer = geopandas.read_file("/Users/kiratsingh/Desktop/research/india_coal/health/output/intermediate/hammer_aggregated_with_states.shp")
    hammer['WKT'] = hammer['geometry']
    print("hammer loaded")

    # import the india states shapefile (POLYGON geometry)
    states = geopandas.read_file("/Users/kiratsingh/Desktop/research/india_coal/health/input/maps/2011_states.shp")
    print("states loaded")

    # assign input directory
    directory = "/Users/kiratsingh/Desktop/research/india_coal/health/input/unit_level"

    # assign output directory
    output_directory = "/Users/kiratsingh/Desktop/research/india_coal/health/output/unit_level"

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        split = filename.split('.')
        ext = split[1]
        unit = split[0]

        # if the ext is .shp, it's a shapefile and we want to open and process it using geopandas
        if ext == "shp":

            # open shapefile as geopandas dataframe
            unit_conc = geopandas.read_file(filepath)
            print("unit loaded")

            # clip the shapefile to just India
            unit_conc = unit_conc.clip(states)
            print("unit clipped")
            print(unit_conc.shape[0])

            # for every unit, we want to 'match' it to the hammer_aggregated_to_inmap_with_states shapefile
            # the match is an exact match (i.e. WKT == WKT)
            unit_conc['WKT'] = unit_conc['geometry']
            unit_conc = unit_conc.sjoin(hammer, how="inner", predicate='contains')
            print("unit and hammer merged")

            # select relevant columns
            unit_conc = unit_conc[['TotalPM25', 'TotalPop', 'PM2_5', 'STATE_ID', 'NAME', 'geometry']]

            # rename columns for next stage of the pipeline
            unit_conc = unit_conc.rename(columns={"TotalPM25": "delta_C_i",
                                                "TotalPop": "P_i",
                                                "STATE_ID": "state_code",
                                                "NAME": "state",
                                                "PM2_5": "C_star_i"})

            # create C_i column
            unit_conc['C_i'] = unit_conc['C_star_i'] - unit_conc['delta_C_i']

            print(unit_conc.shape[0])
            # remove rows where PM 2.5 is missing
            unit_conc = unit_conc[unit_conc.C_star_i.notnull()]
            unit_conc = unit_conc[unit_conc.C_i.notnull()]
            print(unit_conc.shape[0])

            # create filepath
            path_save = output_directory + "/" + unit + ".shp"

            # export
            unit_conc.to_file(path_save)
            print(unit + " exported")


main()


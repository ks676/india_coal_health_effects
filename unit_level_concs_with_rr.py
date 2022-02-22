#Goal: Iterate through the outputs/unit_level directory that contains unit-level shapefiles for C_i and C_star_i.
# Produce as output a set of csvs containing unit-level concentrations along with the corresponding relative risks
# for 6 endpoints. The relative risks match both levels of concentration - with the generator and without the generator.
# For each unit, the number of rows/features in the csv increases 6x vs. the original shapefile because each endpoint
# gets its own row at every level of PM2.5 concentration.

import pandas as pd
import os
import geopandas

def main():

    # assign directory containing inputs
    directory = "/Users/kiratsingh/Desktop/research/india_coal/health/output/unit_level/shapefiles"

    # assign output directory
    output_directory = "/Users/kiratsingh/Desktop/research/india_coal/health/output/unit_level/csv/concs_with_rr"

    # open rr_by_state_and_endpoint dataset
    rr = pd.read_csv('/Users/kiratsingh/Desktop/research/india_coal/health/output/rr_by_state_and_endpoint.csv',
                     index_col=False)

    # here the only rounding we need to do is to int for values >= 10
    round_none = rr[rr['conc'] < 10]

    round_0 = rr[rr['conc'] >= 10]
    round_0 = round_0.round({'conc': 0})

    # recombine
    rr = pd.concat([round_0, round_none], ignore_index=True)

    # convert conc to string
    rr['conc'] = rr['conc'].astype(str)

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        split = filename.split('.')
        ext = split[1]
        unit = split[0]

        # if the ext is .shp, it's a shapefile and we want to open and process it
        if ext == "shp":

            # load shapefile
            unit_conc = geopandas.read_file(filepath)

            # convert to pandas df
            conc = pd.DataFrame(unit_conc)

            # round C_i concentrations to the same levels as in the rr curves:
            # 1. if <=1, two decimal places
            # 2. if <=10, 1 decimal place
            # 3. if >10, 0 decimal places
            # 4. if > 100, nearest tens
            # 5. if > 1000, nearest hundreds

            round_2 = conc[conc['C_i'] < 1.001]
            round_2 = round_2.round({'C_i': 2})

            round_1 = conc[(conc['C_i'] < 10) & (conc['C_i'] >= 1.001)]
            round_1 = round_1.round({'C_i': 1})

            round_0 = conc[(conc['C_i'] < 100) & (conc['C_i'] >= 10)]
            round_0 = round_0.round({'C_i': 0})

            round_tens = conc[(conc['C_i'] < 1000) & (conc['C_i'] >= 100)]
            round_tens['C_i'] = round_tens['C_i'] * 0.1
            round_tens = round_tens.round({'C_i': 0})
            round_tens['C_i'] = round_tens['C_i'] * 10

            round_hundreds = conc[conc['C_i'] >= 1000]
            round_hundreds['C_i'] = round_hundreds['C_i'] * 0.01
            round_hundreds = round_hundreds.round({'C_i': 0})
            round_hundreds['C_i'] = round_hundreds['C_i'] * 100

            # recombine
            conc = pd.concat([round_0, round_1, round_2, round_tens, round_hundreds], ignore_index=True)

            # similarly round the C_star_i values (both will be mapped to rr data)

            round_2 = conc[conc['C_star_i'] < 1.001]
            round_2 = round_2.round({'C_star_i': 2})

            round_1 = conc[(conc['C_star_i'] < 10) & (conc['C_star_i'] >= 1.001)]
            round_1 = round_1.round({'C_star_i': 1})

            round_0 = conc[(conc['C_star_i'] < 100) & (conc['C_star_i'] >= 10)]
            round_0 = round_0.round({'C_star_i': 0})

            round_tens = conc[(conc['C_star_i'] < 1000) & (conc['C_star_i'] >= 100)]
            round_tens['C_star_i'] = round_tens['C_star_i'] * 0.1
            round_tens = round_tens.round({'C_star_i': 0})
            round_tens['C_star_i'] = round_tens['C_star_i'] * 10

            round_hundreds = conc[conc['C_star_i'] >= 1000]
            round_hundreds['C_star_i'] = round_hundreds['C_star_i'] * 0.01
            round_hundreds = round_hundreds.round({'C_star_i': 0})
            round_hundreds['C_star_i'] = round_hundreds['C_star_i'] * 100

            # recombine
            conc = pd.concat([round_0, round_1, round_2, round_tens, round_hundreds], ignore_index=True)

            # convert conc columns to string
            conc['C_star_i'] = conc['C_star_i'].astype(str)
            conc['C_i'] = conc['C_i'].astype(str)

            # join on state id and C_i
            conc = pd.merge(conc, rr[['endpoint',
                                      'mean_rr',
                                      "state_code",
                                      "conc"]],
                            how="left",
                            left_on=["state_code", "C_i"],
                            right_on=["state_code", "conc"])
            # rename mean_rr
            conc = conc.rename(columns={"mean_rr": "mean_rr_C_i",
                                        "endpoint": "endpoint_left"})

            # join on state id and C_i
            conc = pd.merge(conc, rr[['endpoint',
                                      'mean_rr',
                                      "state_code",
                                      "conc"]],
                            how="left",
                            left_on=["state_code", "C_star_i", "endpoint_left"],
                            right_on=["state_code", "conc", "endpoint"])

            # rename mean_rr
            conc = conc.rename(columns={"mean_rr": "mean_rr_C_star_i"})

            # drop extra columns
            conc = conc.drop(columns=['endpoint_left',
                                      'conc_x',
                                      'conc_y'])

            # create filepath
            path_save = output_directory + "/" + unit + ".csv"

            # export as csv for use in later scripts
            conc.to_csv(path_save,index=False)
            print(unit + " exported")



main()
# Goal: Iterate through the directory containing unit_level_concs_with_rr outputs, and combine each csv with
# base_mortality_by_state_and_endpoint, and pop_weighted_rr_by_state_and_endpoint. Produce as output a single i-indexed
# dataset for each unit that merges all three datasets so that we have all the terms needed to compute marginal changes
# in mortality in a single file

import pandas as pd
import os


PER_100k = 1/100000

def main():

    # assign directory containing inputs
    directory = "/Users/kiratsingh/Desktop/research/india_coal/health/output/unit_level/csv/concs_with_rr"

    # assign output directory
    output_directory = "/Users/kiratsingh/Desktop/research/india_coal/health/output/unit_level/csv/master"

    # load the datasets that will be merged with each of the unit-level concentration files
    baseline_mortality = pd.read_csv('/Users/kiratsingh/Desktop/research/india_coal/health/output/base_mortality_by_state_and_endpoint.csv',
        index_col=False)

    pop_weighted_rr = pd.read_csv('/Users/kiratsingh/Desktop/research/india_coal/health/output/pop_weighted_rr_by_state_and_endpoint_gbd.csv',
        index_col=False)

    # initialise tracker for progress monitoring
    i=1

    for filename in os.listdir(directory):
        print(i)
        i+=1
        filepath = os.path.join(directory, filename)
        split = filename.split('.')
        if filename.count('.') > 1:
            unit = split[0] + '.' + split[1]
        else:
            unit = split[0]

        print(filepath)

        # load csv
        conc = pd.read_csv(filepath, index_col=False)

        # bring in state and endpoint specific baseline mortality
        conc = pd.merge(conc, baseline_mortality[["baseline_mortality_rate",
                                                  "state_code",
                                                  "endpoint"]],
                        how="left",
                        left_on=["state_code", "endpoint"],
                        right_on=["state_code", "endpoint"])

        # bring in state and endpoint-specific pop-weighted rr
        conc = pd.merge(conc, pop_weighted_rr[["mean_rr_bar_j_k",
                                               "min_rr_bar_j_k",
                                               "max_rr_bar_j_k",
                                               "state",
                                               "endpoint"]],
                        how="left",
                        left_on=["state", "endpoint"],
                        right_on=["state", "endpoint"])

        conc["mean_I_hat_j_k"] = (conc["baseline_mortality_rate"] * PER_100k) / conc["mean_rr_bar_j_k"]
        conc["min_I_hat_j_k"] = (conc["baseline_mortality_rate"] * PER_100k) / conc["min_rr_bar_j_k"]
        conc["max_I_hat_j_k"] = (conc["baseline_mortality_rate"] * PER_100k) / conc["max_rr_bar_j_k"]

        # Need to create mean, min, max I_hat parameters

        conc["mean_Delta_M_i_j"] = conc["P_i"] * conc["mean_I_hat_j_k"] * (conc["mean_rr_C_star_i"] - conc["mean_rr_C_i"])

        conc["min_Delta_M_i_j"] = conc["P_i"] * conc["min_I_hat_j_k"] * (conc["min_rr_C_star_i"] - conc["min_rr_C_i"])

        conc["max_Delta_M_i_j"] = conc["P_i"] * conc["max_I_hat_j_k"] * (conc["max_rr_C_star_i"] - conc["max_rr_C_i"])

        # retain only needed columns for space management
        conc = conc[["geometry",
                     "state",
                     "P_i",
                     "endpoint",
                     "mean_Delta_M_i_j",
                     "min_Delta_M_i_j",
                     "max_Delta_M_i_j",
                     "mean_rr_C_star_i",
                     "mean_rr_C_i"]]

        # create filepath
        path_save = output_directory + "/" + unit + ".csv"

        # export as csv for use in later scripts
        conc.to_csv(path_save, index=False)
        print(unit + " exported")


main()
# Goal: Take as input test_generator_concentrations_and_rr, base_mortality_by_state_and_endpoint, and
# pop_weighted_rr_by_state_and_endpoint. Produce as output a single i-indexed dataset that merges all three
# datasets so that we have all the terms needed to compute marginal changes in mortality in a single file

import pandas as pd

PER_100k = 1/100000

def main():

    conc = pd.read_csv('/Users/kiratsingh/Desktop/research/india_coal/health/output/test_join.csv',
                       index_col=False)


    baseline_mortality = pd.read_csv('/Users/kiratsingh/Desktop/research/india_coal/health/output/base_mortality_by_state_and_endpoint.csv',
                       index_col=False)

    pop_weighted_rr = pd.read_csv('/Users/kiratsingh/Desktop/research/india_coal/health/output/pop_weighted_rr_by_state_and_endpoint.csv',
                       index_col=False)

    # bring in state and endpoint specific baseline mortality
    conc = pd.merge(conc, baseline_mortality[["baseline_mortality_rate",
                                              "state_code",
                                              "endpoint"]],
                    how="left",
                    left_on=["state_code", "endpoint"],
                    right_on=["state_code", "endpoint"])

    # bring in state and endpoint-specific pop-weighted rr
    conc = pd.merge(conc, pop_weighted_rr[["rr_bar_j_k",
                                              "state_code",
                                              "endpoint"]],
                    how="left",
                    left_on=["state_code", "endpoint"],
                    right_on=["state_code", "endpoint"])

    print(conc.columns)

    conc["I_hat_j_k"] = (conc["baseline_mortality_rate"] * PER_100k) / conc["rr_bar_j_k"]

    conc["Delta_M_i_j"] = conc["P_i"] * conc["I_hat_j_k"] * (conc["mean_rr_C_star_i"] - conc["mean_rr_C_i"])

    mortality_by_endpoint = conc.groupby(['endpoint'], as_index=False).agg({'Delta_M_i_j': 'sum'})

    mortality_by_state = conc.groupby(['state'], as_index=False).agg({'Delta_M_i_j': 'sum'})

    print(sum(conc['Delta_M_i_j']))

    # export as csvs for use in later scripts
    mortality_by_endpoint.to_csv('/Users/kiratsingh/Desktop/research/india_coal/health/output/test_mortality_by_endpoint.csv',
                index=False)

    mortality_by_state.to_csv(
        '/Users/kiratsingh/Desktop/research/india_coal/health/output/test_mortality_by_state.csv',
        index=False)

    conc.to_csv(
        '/Users/kiratsingh/Desktop/research/india_coal/health/output/test_master.csv',
        index=False)



main()
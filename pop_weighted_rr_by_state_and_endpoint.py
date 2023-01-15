# Goal: Take as input test_generator_concentrations_and_rr. Produce as output a dataset containing the average
# 'population-weighted relative risk for end point j within region k' (per Apte et al. 2015).

import pandas as pd

def main():

    df = pd.read_csv('/Users/kiratsingh/Desktop/research/india_coal/health/output/unit_level/csv/concs_with_rr/Dr_N_TATA_RAO_TPS_1.csv',
                       index_col=False)


    df['pop_times_mean_rr_C_i'] = df['P_i'] * df['mean_rr_C_star_i']
    df['pop_times_min_rr_C_i'] = df['P_i'] * df['min_rr_C_star_i']
    df['pop_times_max_rr_C_i'] = df['P_i'] * df['max_rr_C_star_i']

    df = df.groupby(['state',
                     'endpoint'], as_index=False).agg({'pop_times_mean_rr_C_i': 'sum',
                                                       'pop_times_min_rr_C_i': 'sum',
                                                       'pop_times_max_rr_C_i': 'sum',
                                                       'P_i' : 'sum'})

    df['mean_rr_bar_j_k'] = df['pop_times_mean_rr_C_i']/df['P_i']
    df['min_rr_bar_j_k'] = df['pop_times_min_rr_C_i'] / df['P_i']
    df['max_rr_bar_j_k'] = df['pop_times_max_rr_C_i'] / df['P_i']

    # export as csv for use in later scripts
    df.to_csv('/Users/kiratsingh/Desktop/research/india_coal/health/output/pop_weighted_rr_by_state_and_endpoint_gbd.csv',
                index=False)



main()
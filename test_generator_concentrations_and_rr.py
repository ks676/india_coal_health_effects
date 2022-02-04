# Goal: Take as input the test_generator_concentrations dataset and the rr_by_state_and_endpoint dataset.
# Produce as output a single dataset indexed by i and j, containing all the original columns as well as
# j-specific relative risks at both levels of C.

# This will be accomplished by taking test_generator_concentrations and joining in rr_by_state_and_endpoint twice:
# 1. First time on state id and baseline concentration
# 2. Second time on state id and with-generator concentration

# the number of rows in the dataset will grow 6x on the first join because every location will have 6 RR values but
# the number of rows should not increase after the second join if the join is correctly executed

import pandas as pd

def main():

    # open test_generator_concentrations dataset
    conc = pd.read_csv('/Users/kiratsingh/Desktop/research/india_coal/health/output/mundra_conc.csv',
                       index_col=False)

    # filter out empty rows
    conc = conc[conc['C_i'].notnull()]

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
    round_tens['C_i'] = round_tens['C_i'] / 10
    round_tens = round_tens.round({'C_i': 0})
    round_tens['C_i'] = round_tens['C_i'] * 10

    round_hundreds = conc[conc['C_i'] >= 1000]
    round_hundreds['C_i'] = round_hundreds['C_i']/100
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
    round_tens['C_star_i'] = round_tens['C_star_i']/10
    round_tens = round_tens.round({'C_star_i': 0})
    round_tens['C_star_i'] = round_tens['C_star_i']*10

    round_hundreds = conc[conc['C_star_i'] >= 1000]
    round_hundreds['C_star_i'] = round_hundreds['C_star_i']/100
    round_hundreds = round_hundreds.round({'C_star_i': 0})
    round_hundreds['C_star_i'] = round_hundreds['C_star_i'] * 100

    # recombine
    conc = pd.concat([round_0, round_1, round_2, round_tens, round_hundreds], ignore_index=True)

    # convert conc columns to string
    conc['C_star_i'] = conc['C_star_i'].astype(str)
    conc['C_i'] = conc['C_i'].astype(str)

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

    # export as csv for use in later scripts
    conc.to_csv('/Users/kiratsingh/Desktop/research/india_coal/health/output/test_join.csv',
                 index=False)

main()
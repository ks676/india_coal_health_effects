# Goal: Take as input the pop_by_age_and_state csv and the endpoint-specific relative risk curves.
# Produce a single dataset containing rr curves per state and endpoint.

# There are 6 endpoints accounted for here:
# 1. IHD - age-specific
# 2. Stroke - age-specific
# 3. Lower respiratory tract infection - single rate
# 4. Lung cancer - single rate
# 5. COPD - single rate
# 6. Type II diabetes - single rate

import pandas as pd
import os

def main():

    # dictionary to iterate through the list of states
    states = {'0': 'India',
              '1': 'Jammu & Kashmir and Ladakh',
              '2': 'Himachal Pradesh',
              '3': 'Punjab',
              '4': 'Other Union Territories',
              '5': 'Uttarakhand',
              '6': 'Haryana',
              '7': 'Delhi',
              '8': 'Rajasthan',
              '9': 'Uttar Pradesh',
              '10': 'Bihar',
              '11': 'Sikkim',
              '12': 'Arunachal Pradesh',
              '13': 'Nagaland',
              '14': 'Manipur',
              '15': 'Mizoram',
              '16': 'Tripura',
              '17': 'Meghalaya',
              '18': 'Assam',
              '19': 'West Bengal',
              '20': 'Jharkhand',
              '21': 'Odisha',
              '22': 'Chhattisgarh',
              '23': 'Madhya Pradesh',
              '24': 'Gujarat',
              '25': 'Other Union Territories',
              '26': 'Other Union Territories',
              '27': 'Maharashtra',
              '28': 'Andhra Pradesh',
              '29': 'Karnataka',
              '30': 'Goa',
              '31': 'Other Union Territories',
              '32': 'Kerala',
              '33': 'Tamil Nadu',
              '34': 'Other Union Territories',
              '35': 'Other Union Territories'}

    # setup empty dataframe that will be populated by state and endpoint-specific baseline mortality
    df = pd.DataFrame(columns=['state_code',
                               'state',
                               'endpoint',
                               'conc',
                               'mean_rr',
                               'min_rr',
                               'max_rr'])

    ###################################################################################################################
    ###################################################################################################################

    # create df from csv lri rr
    lri = pd.read_csv('/Users/kiratsingh/Desktop/research/india_coal/health/input/risk_curves/lri.csv')

    # change column names to reflect the names we want in the final dataset
    lri = lri.rename(columns={"label": "endpoint",
                              "mean": "mean_rr",
                              "min": "min_rr",
                              "max": "max_rr"})

    # iterate through the states dictionary - for each state, we create a state-specific lri df
    # that dataframe is then appended to the main dataframe


    for state in states:
        lri['state_code'] = state
        lri['state'] = states[state]
        # fix the order before appending
        lri = lri[["state_code", "state", "endpoint", "conc", "mean_rr", "min_rr", "max_rr"]]
        df = df.append(lri)
    ###################################################################################################################
    ###################################################################################################################

    # create df from csv containing lung cancer rr
    neo_lung = pd.read_csv('/Users/kiratsingh/Desktop/research/india_coal/health/input/risk_curves/neo_lung.csv')

    # change column names to reflect the names we want in the final dataset
    neo_lung = neo_lung.rename(columns={"label": "endpoint",
                              "mean": "mean_rr",
                              "min": "min_rr",
                              "max": "max_rr"})

    # iterate through the states dictionary - for each state, we create a state-specific neo_lung df
    # that dataframe is then appended to the main dataframe

    for state in states:
        neo_lung['state_code'] = state
        neo_lung['state'] = states[state]
        # fix the order before appending
        neo_lung = neo_lung[["state_code", "state", "endpoint", "conc", "mean_rr", "min_rr", "max_rr"]]
        df = df.append(neo_lung)

    ###################################################################################################################
    ###################################################################################################################

    # create df from csv containing copd rr
    res_copd = pd.read_csv('/Users/kiratsingh/Desktop/research/india_coal/health/input/risk_curves/resp_copd.csv')

    # change column names to reflect the names we want in the final dataset
    res_copd = res_copd.rename(columns={"label": "endpoint",
                              "mean": "mean_rr",
                              "min": "min_rr",
                              "max": "max_rr"})

    # iterate through the states dictionary - for each state, we create a state-specific res_copd df
    # that dataframe is then appended to the main dataframe

    for state in states:
        res_copd['state_code'] = state
        res_copd['state'] = states[state]
        # fix the order before appending
        res_copd = res_copd[["state_code", "state", "endpoint", "conc", "mean_rr", "min_rr", "max_rr"]]
        df = df.append(res_copd)

    ###################################################################################################################
    ###################################################################################################################

    # create df from csv containing t2_dm rr
    t2_dm = pd.read_csv('/Users/kiratsingh/Desktop/research/india_coal/health/input/risk_curves/t2_dm.csv')

    # change column names to reflect the names we want in the final dataset
    t2_dm = t2_dm.rename(columns={"label": "endpoint",
                              "mean": "mean_rr",
                              "min": "min_rr",
                              "max": "max_rr"})

    # iterate through the states dictionary - for each state, we create a state-specific t2_dm df
    # that dataframe is then appended to the main dataframe

    for state in states:
        t2_dm['state_code'] = state
        t2_dm['state'] = states[state]
        # fix the order before appending
        t2_dm = t2_dm[["state_code", "state", "endpoint", "conc", "mean_rr", "min_rr", "max_rr"]]
        df = df.append(t2_dm)


    ###################################################################################################################
    ###################################################################################################################


    # export as csv for use in other scripts
    df.to_csv('/Users/kiratsingh/Desktop/research/india_coal/health/output/rr_by_state_and_endpoint.csv',
            index=False)


main()
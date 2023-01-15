# Goal: Use the state-age fractions from 2019 GBD to construct state level RR curves for stroke
# instead of using age distributions from the 2011 Census, and explicitly account for <25s.

import pandas as pd
import os

def main():

    states = {#'0': 'India',
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

    age_splits = pd.read_csv('/Users/kiratsingh/Downloads/state_age_fractions.csv')

    # initialise new dataframe
    df_stroke = pd.DataFrame(columns=['state_code',
                                   'state',
                                   'endpoint',
                                   'conc',
                                   'mean_rr',
                                   'min_rr',
                                   'max_rr'])

    # iterate through all states
    for state in states:

        # initialise state level df
        df_stroke_state = pd.DataFrame(columns=['state_code',
                                   'state',
                                   'endpoint',
                                   'age_lower',
                                   'age_weight'
                                   'conc',
                                   'mean',
                                   'min',
                                   'max'])

        # filter age weights table to given state

        state_name = states[state]
        age_splits_state = age_splits[age_splits["states"] == state_name]
        state_under_25 = list(age_splits_state["under_25"])[0]

        # iterate through dictionary containing cvd ihd curves
        directory = "/Users/kiratsingh/Desktop/research/india_coal/health/input/risk_curves/interpolated/cvd_ihd"

        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            file = pd.read_csv(filepath)
            split = filename.split('_')
            file_age = split[2]
            file_age = file_age.split('.')[0]

            file["state"] = states[state]
            file["state_code"] = state
            file["endpoint"] = "cvd_stroke"

            age_weight = age_splits_state[file_age]
            age_weight = list(age_weight)[0]

            file["age_lower"] = file_age
            file["age_weight"] = age_weight

            # append file to state level df
            df_stroke_state = df_stroke_state.append(file)

        # at this point in the loop, for a given state we've iterated through the directory of age-specific RRs
        # and created a df containing the different age-specfic RRs + corresponding age-weights for each state

        # now we need to:
        # 1. calculated age-weighted RRs at each concentration level
        # 2. aggregate and sum so we have a single RR value at every exposure level
        # 3. add in the stable-relative risk for the under 25s

        df_stroke_state["mean_rr"] = df_stroke_state["mean"] * df_stroke_state["age_weight"]
        df_stroke_state["min_rr"] = df_stroke_state["min"] * df_stroke_state["age_weight"]
        df_stroke_state["max_rr"] = df_stroke_state["max"] * df_stroke_state["age_weight"]

        df_stroke_agg = df_stroke_state.groupby(['state_code',
                                     'state',
                                     'endpoint',
                                     'conc'], as_index=False).agg({'mean_rr': 'sum',
                                                                   'min_rr': 'sum',
                                                                   'max_rr': 'sum'})

        df_stroke_agg["mean_rr"] = df_stroke_agg["mean_rr"] + state_under_25
        df_stroke_agg["min_rr"] = df_stroke_agg["min_rr"] + state_under_25
        df_stroke_agg["max_rr"] = df_stroke_agg["max_rr"] + state_under_25
        print(df_stroke_agg)

        df_stroke = df_stroke.append(df_stroke_agg)

    print(df_stroke)

    df_stroke.to_csv('/Users/kiratsingh/Desktop/research/india_coal/health/output/rr_by_state_stroke_gbd.csv',
              index=False)


main()
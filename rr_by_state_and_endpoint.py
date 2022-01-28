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

    # to create the df from ihd, we need to account for the fact that there is a different distribution of
    # age groups in different states
    # for every state, we need to compute a weighted average of relative risk values at every level of
    # pm 2.5 exposure
    # to do so, we can:
    # 1. take pop_by_age_and_state and create an age_lower column
    # 2. remove under 25s from pop_by_age
    # 3. compute the weights of each age bucket
    #   i. compute the total population by state
    #   ii. join it back in on state
    #   iii. compute the weight of each age bracket as the pop/total
    # 4. left-join the corresponding rr files
    # 5. coalesce the rr columns into a single column
    # 6. aggregate the df, sum the column computed in 6. by state

    # create age_lower column in pop_by_age_and_state
    pop = pd.read_csv('/Users/kiratsingh/Desktop/research/india_coal/health/output/pop_by_age_and_state.csv')
    pop_by_age = pop
    pop_by_age[['age_lower', 'age_upper']] = pop_by_age['age'].str.split('-', expand=True)

    # remove under 25s and All ages from pop_by_age
    pop_by_age = pop_by_age[pop_by_age['age_lower'] != 'All ages']
    pop_by_age = pop_by_age[pop_by_age['age_lower'].astype(int) > 24]

    # weights of each age bucket
    pop_by_state = pop_by_age.groupby(['state_code', 'state'], as_index=False).agg({'pop': 'sum'})
    pop_by_state = pop_by_state.rename(columns={"pop": "total_population"})

    # merge (on state code) tot_pop_df into pop_by_age only bringing in the total population
    pop_by_age = pd.merge(pop_by_age, pop_by_state[['state_code', 'total_population']],
                          how="left",
                          left_on="state_code",
                          right_on="state_code")
    # calculate weight of each age bracket as pop/total_population
    pop_by_age['age_weight'] = pop_by_age['pop']/pop_by_age['total_population']

    # join the rr files

    # initialise dataframe to be populated
    df_ihd = pd.DataFrame(columns=['state_code',
                                   'state',
                                   'endpoint',
                                   'age_lower',
                                   'age_weight'
                                   'conc',
                                   'mean_rr',
                                   'min_rr',
                                   'max_rr'])


    # loop through the dictionary containing the rr curves

    # assign directory
    directory = "/Users/kiratsingh/Desktop/research/india_coal/health/input/risk_curves/cvd_ihd"

    # iterate over files in directory
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        file = pd.read_csv(filepath)
        split = filename.split('_')
        file_age = split[2]
        file_age = file_age.split('.')[0]
        # file_age points to the age_lower that this file contains the rr for
        # we filter pop_by_age to just the rows where age_lower = file_age
        # this gives us a subset consisting of 35 rows - one row per state since
        # we're only looking at one age group
        file_weights = pop_by_age[pop_by_age['age_lower'] == file_age]
        # add endpoint column
        file_weights['endpoint'] = 'cvd_ihd'
        # only keep columns we are interested in
        file_weights = file_weights[['state_code',
                                     'state',
                                     'endpoint',
                                     'age_lower',
                                     'age_weight']]
        # create key column in file for merge
        file['age_lower'] = file_age
        # with file_weights on the left, we merge in file from the right on age_lower
        file_weights = pd.merge(file_weights, file[['age_lower',
                                                    'conc',
                                                    'mean',
                                                    'min',
                                                    'max']],
                                how="left",
                                left_on="age_lower",
                                right_on="age_lower")
        # rename rr columns as needed
        file_weights = file_weights.rename(columns={"mean": "mean_rr",
                                                    "min": "min_rr",
                                                    "max": "max_rr",
                                                    "age_lower_x": "age_lower"})
        # reorder columns to make sure they reflect the column order of df_ihd
        file_weights = file_weights[['state_code',
                                     'state',
                                     'endpoint',
                                     'age_lower',
                                     'age_weight',
                                     'conc',
                                     'mean_rr',
                                     "min_rr",
                                     "max_rr"]]

        # calculate the weighted-rr per state and age group
        file_weights['weighted_mean_rr'] = file_weights['age_weight'].astype(float) * file_weights['mean_rr'].astype(float)
        file_weights['weighted_min_rr'] = file_weights['age_weight'].astype(float) * file_weights['min_rr'].astype(float)
        file_weights['weighted_max_rr'] = file_weights['age_weight'].astype(float) * file_weights['max_rr'].astype(float)

        df_ihd = df_ihd.append(file_weights)

    # group by state_code and state, sum rr values
    df_ihd_agg = df_ihd.groupby(['state_code',
                                 'state',
                                 'endpoint',
                                 'conc'], as_index=False).agg({'weighted_mean_rr': 'sum',
                                                               'weighted_min_rr': 'sum',
                                                               'weighted_max_rr': 'sum'})
    df_ihd_agg = df_ihd_agg.rename(columns={"weighted_mean_rr": "mean_rr",
                                            "weighted_min_rr": "min_rr",
                                            "weighted_max_rr": "max_rr"})

    df = df.append(df_ihd_agg)

    ###################################################################################################################
    ###################################################################################################################

    # export as csv for use in other scripts
    df.to_csv('/Users/kiratsingh/Desktop/research/india_coal/health/output/rr_by_state_and_endpoint.csv',
            index=False)


main()
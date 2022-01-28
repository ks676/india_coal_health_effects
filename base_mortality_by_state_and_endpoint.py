# Goal: Take as input the pop_by_age_and_state csv and the endpoint-specific baseline mortality rates. Produce
# a single dataset containing baseline mortality per state (rows) and per endpoint (cols)

# There are 6 endpoints accounted for here:
# 1. IHD - age-specific
# 2. Stroke - age-specific
# 3. Lower respiratory tract infection - single rate
# 4. Lung cancer - single rate
# 5. COPD - single rate
# 6. Type II diabetes - single rate

import pandas as pd
import os

PER_100k = 1/100000

def main():

    # setup empty dataframe that will be populated by state and endpoint-specific baseline mortality
    df = pd.DataFrame(columns = ['state_code',
                                 'state',
                                 'total_population',
                                 'endpoint',
                                 'baseline_mortality_rate',
                                 'baseline_mortality'])

    # create df from csv containing state and age-level populations
    pop = pd.read_csv('/Users/kiratsingh/Desktop/research/india_coal/health/output/pop_by_age_and_state.csv')

    ###################################################################################################################
    ###################################################################################################################

    # create df from csv containing lri mortality rates by state
    lri = pd.read_csv('/Users/kiratsingh/Desktop/research/india_coal/health/input/mortality_baseline/lri_state_baseline_2019.csv')

    # filter pop to "all ages" age bracket
    pop_all_ages = pop[pop['age'] == 'All ages']

    # create lri df
    df_lri = pd.DataFrame(columns = ['state_code',
                                 'state',
                                 'total_population',
                                 'endpoint',
                                 'baseline_mortality_rate',
                                 'baseline_mortality'])
    df_lri['state_code'] = pop_all_ages['state_code']
    df_lri['state'] = pop_all_ages['state']
    df_lri['total_population'] = pop_all_ages['pop']
    df_lri['endpoint'] = 'lri'

    # join in the lri data to get lri baseline mortality rates
    df_lri = pd.merge(df_lri, lri[['Location', 'Value']], how="left", left_on="state", right_on="Location")

    # fill in baseline mortality rate and baseline mortality columns
    df_lri['baseline_mortality_rate'] = df_lri['Value']
    df_lri['baseline_mortality'] = df_lri['baseline_mortality_rate'] * df_lri['total_population'] * PER_100k


    # clean up
    df_lri = df_lri.drop(columns=['Value', 'Location'])

    # append lri df to main df

    df = df.append(df_lri)


    ###################################################################################################################
    ###################################################################################################################

    # create df from csv containing lung cancer mortality rates by state
    neo_lung = pd.read_csv(
        '/Users/kiratsingh/Desktop/research/india_coal/health/input/mortality_baseline/neo_lung_state_baseline_2019.csv')

    # create lung cancer df
    df_neo_lung = pd.DataFrame(columns=['state_code',
                                   'state',
                                   'total_population',
                                   'endpoint',
                                   'baseline_mortality_rate',
                                   'baseline_mortality'])
    df_neo_lung['state_code'] = pop_all_ages['state_code']
    df_neo_lung['state'] = pop_all_ages['state']
    df_neo_lung['total_population'] = pop_all_ages['pop']
    df_neo_lung['endpoint'] = 'neo_lung'

    # join in the lung cancer data to get lung cancer baseline mortality rates
    df_neo_lung = pd.merge(df_neo_lung, neo_lung[['Location', 'Value']], how="left", left_on="state", right_on="Location")

    # fill in baseline mortality rate and baseline mortality columns
    df_neo_lung['baseline_mortality_rate'] = df_neo_lung['Value']
    df_neo_lung['baseline_mortality'] = df_neo_lung['baseline_mortality_rate'] * df_neo_lung['total_population'] * PER_100k

    # clean up
    df_neo_lung = df_neo_lung.drop(columns=['Value', 'Location'])

    # append lung cancer df to main df
    df = df.append(df_neo_lung)

    ###################################################################################################################
    ###################################################################################################################

    # create df from csv containing copd mortality rates by state
    res_copd = pd.read_csv(
        '/Users/kiratsingh/Desktop/research/india_coal/health/input/mortality_baseline/res_copd_state_baseline_2019.csv')

    # create copd df
    df_res_copd = pd.DataFrame(columns=['state_code',
                                        'state',
                                        'total_population',
                                        'endpoint',
                                        'baseline_mortality_rate',
                                        'baseline_mortality'])
    df_res_copd['state_code'] = pop_all_ages['state_code']
    df_res_copd['state'] = pop_all_ages['state']
    df_res_copd['total_population'] = pop_all_ages['pop']
    df_res_copd['endpoint'] = 'res_copd'

    # join in the copd data to get copd baseline mortality rates
    df_res_copd = pd.merge(df_res_copd, res_copd[['Location', 'Value']], how="left", left_on="state",
                           right_on="Location")

    # fill in baseline mortality rate and baseline mortality columns
    df_res_copd['baseline_mortality_rate'] = df_res_copd['Value']
    df_res_copd['baseline_mortality'] = df_res_copd['baseline_mortality_rate'] * df_res_copd[
        'total_population'] * PER_100k

    # clean up
    df_res_copd = df_res_copd.drop(columns=['Value', 'Location'])

    # append res_copd df to main df
    df = df.append(df_res_copd)

    ###################################################################################################################
    ###################################################################################################################

    # create df from csv containing type 2 diabetes mortality rates by state
    t2_dm = pd.read_csv(
        '/Users/kiratsingh/Desktop/research/india_coal/health/input/mortality_baseline/t2_dm_state_baseline_2019.csv')

    # create t2_dm df
    df_t2_dm = pd.DataFrame(columns=['state_code',
                                        'state',
                                        'total_population',
                                        'endpoint',
                                        'baseline_mortality_rate',
                                        'baseline_mortality'])
    df_t2_dm['state_code'] = pop_all_ages['state_code']
    df_t2_dm['state'] = pop_all_ages['state']
    df_t2_dm['total_population'] = pop_all_ages['pop']
    df_t2_dm['endpoint'] = 't2_dm'

    # join in the t2_dm data to get the t2_dm baseline mortality rates
    df_t2_dm = pd.merge(df_t2_dm, t2_dm[['Location', 'Value']], how="left", left_on="state",
                           right_on="Location")

    # fill in baseline mortality rate and baseline mortality columns
    df_t2_dm['baseline_mortality_rate'] = df_t2_dm['Value']
    df_t2_dm['baseline_mortality'] = df_t2_dm['baseline_mortality_rate'] * df_t2_dm[
        'total_population'] * PER_100k

    # clean up
    df_t2_dm = df_t2_dm.drop(columns=['Value', 'Location'])

    # append t2_dm df to main df
    df = df.append(df_t2_dm)

    ###################################################################################################################
    ###################################################################################################################

    pop_by_age = pop

    # split age column so that we can match with the correct DR curve
    pop_by_age[['age_lower', 'age_upper']] = pop_by_age['age'].str.split('-', expand=True)



    # iterate through the ihd files:
    # for each file, parse the file name to get the age group that the file contains data for
    # convert the contents of the file to a df with an additional column for age_lower
    # append that df to the main ihd dataframe so we get one df containing the curves for all age groups

    # initialise df to capture ihd dr curve from all age-specific files
    df_ihd_dr = pd.DataFrame(columns=['state',
                                   'endpoint',
                                   'baseline_mortality_rate',
                                      'age_lower'])

    # assign directory
    directory = "/Users/kiratsingh/Desktop/research/india_coal/health/input/mortality_baseline/ihd"

    # iterate over files in directory
    for filename in os.listdir(directory):
        split = filename.split('_')
        file_age = split[2]
        # filter pop_by_age to just this age group
        file_pop = pop_by_age[pop_by_age['age_lower'] == file_age]
        # get file path so we can open the file
        filepath = os.path.join(directory, filename)
        # iterate through the file - each row is a state
        file = pd.read_csv(filepath)
        file = file[file['Year'] == 2019]
        file = file.rename(columns={"Location": "state",
                             "Cause of death or injury": "endpoint",
                             "Value": "baseline_mortality_rate"})
        file = file.drop(columns=['Year', 'Age', 'Sex', 'Measure', 'Lower bound', 'Upper bound'])
        file['endpoint'] = 'cvd_ihd'
        file['age_lower'] = file_age
        df_ihd_dr = df_ihd_dr.append(file)


    # we now have a dataset the contains state and age-wise population, and a dataset that contains
    # state and age-wise mortality rates
    # we can left-join the latter onto the former to create a single dataset containing state, age-group,
    # population in that age group, cvd_ihd bmr for that age group, and cvd_ihd baseline mortality
    # for that age group
    df_ihd = pd.merge(pop_by_age, df_ihd_dr, how="inner", left_on=["state", "age_lower"],
                        right_on=["state", "age_lower"])
    df_ihd['baseline_mortality'] = df_ihd['baseline_mortality_rate'] * df_ihd['pop'] * PER_100k

    # aggregate to get state-level figures - specifically we want the total mortality across each state and the
    # pop-weighted average mortality rate
    df_ihd['bmr_times_pop'] = df_ihd['baseline_mortality_rate'] * df_ihd['pop']
    df_ihd_agg = df_ihd.groupby(['state_code','state', 'endpoint'], as_index=False).agg({'pop': 'sum',
                                                                      'bmr_times_pop': 'sum',
                                                                      'baseline_mortality': 'sum'}
                                                                      )
    df_ihd_agg['baseline_mortality_rate'] = df_ihd_agg['bmr_times_pop']/df_ihd_agg['pop']
    df_ihd_agg = df_ihd_agg.drop(columns=['bmr_times_pop'])
    df_ihd_agg = df_ihd_agg.rename(columns={"pop": "total_population"})
    df_ihd_agg = df_ihd_agg[["state_code",
                             "state",
                             "total_population",
                             "endpoint",
                             "baseline_mortality_rate",
                             "baseline_mortality"]]

    # append ihd df to main df
    df = df.append(df_ihd_agg)

    ###################################################################################################################
    ###################################################################################################################

    # iterate through the stroke files:
    # for each file, parse the file name to get the age group that the file contains data for
    # convert the contents of the file to a df with an additional column for age_lower
    # append that df to the main stroke dataframe so we get one df containing the curves for all age groups

    # initialise df to capture stroke dr curve from all age-specific files
    df_stroke_dr = pd.DataFrame(columns=['state',
                                      'endpoint',
                                      'baseline_mortality_rate',
                                      'age_lower'])

    # assign directory
    directory = "/Users/kiratsingh/Desktop/research/india_coal/health/input/mortality_baseline/stroke"

    # iterate over files in directory
    for filename in os.listdir(directory):
        split = filename.split('_')
        file_age = split[2]
        # filter pop_by_age to just this age group
        file_pop = pop_by_age[pop_by_age['age_lower'] == file_age]
        # get file path so we can open the file
        filepath = os.path.join(directory, filename)
        # iterate through the file - each row is a state
        file = pd.read_csv(filepath)
        file = file[file['Year'] == 2019]
        file = file.rename(columns={"Location": "state",
                                    "Cause of death or injury": "endpoint",
                                    "Value": "baseline_mortality_rate"})
        file = file.drop(columns=['Year', 'Age', 'Sex', 'Measure', 'Lower bound', 'Upper bound'])
        file['endpoint'] = 'cvd_stroke'
        file['age_lower'] = file_age
        df_stroke_dr = df_stroke_dr.append(file)

    # we now have a dataset the contains state and age-wise population, and a dataset that contains
    # state and age-wise mortality rates
    # we can left-join the latter onto the former to create a single dataset containing state, age-group,
    # population in that age group, cvd_stroke bmr for that age group, and cvd_stroke baseline mortality
    # for that age group
    df_stroke = pd.merge(pop_by_age, df_stroke_dr, how="inner", left_on=["state", "age_lower"],
                      right_on=["state", "age_lower"])
    df_stroke['baseline_mortality'] = df_stroke['baseline_mortality_rate'] * df_stroke['pop'] * PER_100k

    # aggregate to get state-level figures - specifically we want the total mortality across each state and the
    # pop-weighted average mortality rate
    df_stroke['bmr_times_pop'] = df_stroke['baseline_mortality_rate'] * df_stroke['pop']
    df_stroke_agg = df_stroke.groupby(['state_code', 'state', 'endpoint'], as_index=False).agg({'pop': 'sum',
                                                                                          'bmr_times_pop': 'sum',
                                                                                          'baseline_mortality': 'sum'}
                                                                                         )
    df_stroke_agg['baseline_mortality_rate'] = df_stroke_agg['bmr_times_pop'] / df_stroke_agg['pop']
    df_stroke_agg = df_stroke_agg.drop(columns=['bmr_times_pop'])
    df_stroke_agg = df_stroke_agg.rename(columns={"pop": "total_population"})
    df_stroke_agg = df_stroke_agg[["state_code",
                             "state",
                             "total_population",
                             "endpoint",
                             "baseline_mortality_rate",
                             "baseline_mortality"]]

    # append ihd df to main df
    df = df.append(df_stroke_agg)

    ###################################################################################################################
    ###################################################################################################################

    # export as csv for use in other scripts
    df.to_csv('/Users/kiratsingh/Desktop/research/india_coal/health/output/base_mortality_by_state_and_endpoint.csv', index=False)






main()
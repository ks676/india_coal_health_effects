# Goal: Iterate through the directory containing unit-level master csvs and create aggregated datasets for each unit -
# one that aggregates by state and one that aggregates by endpoint. In addition to the unit-level outputs, the script
# also creates fleet-wide aggregated tables: one that contains per-unit mortality for the full fleet, one that
# combines the per-unit, per-state mortality, and one that combines the per-unit, per-endpoint mortality


import pandas as pd
import os

def main():

    # initialise dataframes to capture fleet-wide totals
    fleet_mortality_by_unit = pd.DataFrame()
    fleet_mortality_by_endpoint = pd.DataFrame()
    fleet_mortality_by_state = pd.DataFrame()

    # assign directory containing inputs
    directory = "/Users/kiratsingh/Desktop/research/india_coal/health/output/unit_level/csv/master"

    # assign output directories
    output_dir_state = "/Users/kiratsingh/Desktop/research/india_coal/health/output/unit_level/csv/aggregations/state"
    output_dir_endpoint = "/Users/kiratsingh/Desktop/research/india_coal/health/output/unit_level/csv/aggregations/endpoint"
    output_dir_fleet = "/Users/kiratsingh/Desktop/research/india_coal/health/output/unit_level/csv/aggregations/fleet"

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        split = filename.split('.')
        unit = split[0]

        # load csv
        conc = pd.read_csv(filepath)

        # aggregate unit-attributable mortality by endpoint
        mortality_by_endpoint = conc.groupby(['endpoint'], as_index=False).agg({'Delta_M_i_j': 'sum'})

        # create filepath for endpoint csv
        path_save = output_dir_endpoint + "/" + unit + ".csv"

        # export csv
        mortality_by_endpoint.to_csv(path_save, index=False)
        print(unit + " endpoint agg exported")

        # add col for unit
        mortality_by_endpoint['unit'] = unit

        # append to fleet-wide by-endpoint df
        fleet_mortality_by_endpoint = pd.concat([fleet_mortality_by_endpoint, mortality_by_endpoint], ignore_index=True)

        # aggregate unit-attributable mortality by state
        mortality_by_state = conc.groupby(['state'], as_index=False).agg({'Delta_M_i_j': 'sum'})

        # create filepath for state csv
        path_save = output_dir_state + "/" + unit + ".csv"

        # export csv
        mortality_by_state.to_csv(path_save, index=False)
        print(unit + " state agg exported")

        # add col for unit
        mortality_by_state['unit'] = unit

        # append to fleet-wide by-endpoint df
        fleet_mortality_by_state = pd.concat([fleet_mortality_by_state, mortality_by_state], ignore_index=True)

        # calculate total mortality attributable to unit
        unit_mortality = sum(conc['Delta_M_i_j'])

        # create total mortality row to append to fleet-wide unit-level mortality df
        data = [[unit, unit_mortality]]
        unit_mortality_df = pd.DataFrame(data, columns = ['unit', 'sum_delta_M_ij'])

        # concatenate with fleet_wide mortality df
        fleet_mortality_by_unit = pd.concat([fleet_mortality_by_unit, unit_mortality_df], ignore_index=True)

        print(unit + " appended to fleet-wide tables")

    # save fleet-wide tables as csvs

    # create filepath for by-endpoint fleet-wide csv
    path_endpoint = output_dir_fleet + "/" + "by_unit_and_endpoint.csv"

    # export as csv
    fleet_mortality_by_endpoint.to_csv(path_endpoint, index=False)

    # create filepath for by-state fleet-wide csv
    path_state = output_dir_fleet + "/" + "by_unit_and_state.csv"

    # export as csv
    fleet_mortality_by_state.to_csv(path_state, index=False)

    # create filepath for fleet-wide by-unit mortality csv
    path_unit = output_dir_fleet + "/" + "by_unit.csv"

    # export as csv
    fleet_mortality_by_unit.to_csv(path_unit, index=False)

    print(unit + " exported to fleet tables")


main()
# Goal: Takes as input the csv generated in QGIS.
# Produces as output a cell-indexed (subscript 'i') dataset containing PM25 concentrations with and without Mundra.

import pandas as pd

def main():

    # import the QGIS-generated dataset
    gen_conc = pd.read_csv('/Users/kiratsingh/Desktop/research/india_coal/health/output/mundra_shp_export.csv')
    # This dataset contains two types of locations - most locations have an associated mean pm25 value, but some
    # do not. For the locations that don't have their own mean pm25, they are matched with their nearest mean PM25.
    # There can be multiple 'nearest' mean PM25s at the exact same distance from a cell (think all its immediate
    # neighbors) and each shows up as a separate row. We want a single row.

    # separate the values for which we have a direct pm25 mean
    exact_mean = gen_conc[gen_conc.PM2_5_mean.notnull()]
    # for this data, we can simply drop the 'nearest PM 25 mean' column and deduplicate what remains
    exact_mean = exact_mean.drop(columns=['nearestPM2_5_mean'])
    # deduplicate
    exact_mean = exact_mean.drop_duplicates()


    # get the rows for which we don't have a direct pm25 mean
    nearest_mean = gen_conc[gen_conc.PM2_5_mean.isnull()]
    # for this data, we want to compute mean pm25 as the mean of all the 'nearest' pm 25 values
    nearest_mean = nearest_mean.groupby(['WKT',
                                         'TotalPM25',
                                         'TotalPop',
                                         'STATE_ID',
                                         'NAME'], as_index=False).agg({'nearestPM2_5_mean': 'mean'})
    # rename the nearest mean aggregate column
    nearest_mean = nearest_mean.rename(columns={"nearestPM2_5_mean": "PM2_5_mean"})

    # recombine both to create a single dataset
    gen_conc = exact_mean.append(nearest_mean)

    # rename columns to align with rest of pipeline
    gen_conc = gen_conc.rename(columns={"TotalPM25" : "delta_C_i",
                                        "TotalPop" : "P_i",
                                        "STATE_ID" : "state_code",
                                        "NAME" : "state",
                                        "PM2_5_mean" : "C_star_i"})

    # create column reflecting concentrations without this generator
    gen_conc['C_i'] = gen_conc['C_star_i'] - gen_conc['delta_C_i']

    # round C_i concentrations to the same levels as in the rr curves:
    # 1. if <=1, two decimal places
    # 2. if <=10, 1 decimal place
    # 3. if >10, 0 decimal places

    round_2 = gen_conc[gen_conc['C_i'] < 1.001]
    round_2 = round_2.round({'C_i': 2})

    round_1 = gen_conc[(gen_conc['C_i'] < 10) & (gen_conc['delta_C_i'] >= 1.001)]
    round_1 = round_1.round({'C_i': 1})

    round_0 = gen_conc[gen_conc['C_i'] >= 10]
    round_0 = round_0.round({'C_i': 0})

    # recombine
    gen_conc = round_0.append(round_1).append(round_2)

    # similarly round the C_star_i values (both will be mapped to rr data)

    round_2 = gen_conc[gen_conc['C_star_i'] < 1.001]
    round_2 = round_2.round({'C_star_i': 2})

    round_1 = gen_conc[(gen_conc['C_star_i'] < 10) & (gen_conc['C_star_i'] >= 1.001)]
    round_1 = round_1.round({'C_star_i': 1})

    round_0 = gen_conc[gen_conc['C_star_i'] >= 10]
    round_0 = round_0.round({'C_star_i': 0})

    # recombine
    gen_conc = round_0.append(round_1).append(round_2)

    # export as csv for use in subsequent scripts
    gen_conc.to_csv('/Users/kiratsingh/Desktop/research/india_coal/health/output/mundra_conc.csv',
              index=False)


main()
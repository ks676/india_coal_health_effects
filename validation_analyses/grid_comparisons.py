# Goal: This script takes as input two InMAP outputs -
# concentrations for ANPARA TPS 2 using the global grid
# and using the south asia-only grid and compares the results

import geopandas
import numpy
from matplotlib import pyplot

def main():

    # import global grid output
    global_grid = geopandas.read_file("/Users/kiratsingh/Downloads/drive-download-20220330T234015Z-001/RIHAND_STPS_2.shp")


    # import south asia-only grid output
    sas_grid = geopandas.read_file("/Users/kiratsingh/Downloads/drive-download-20220331T003109Z-001/RIHAND_STPS_2_sas_grid.shp")


    # import states shapefile
    states = geopandas.read_file("/Users/kiratsingh/Desktop/research/india_coal/health/input/maps/2011_states.shp")
    states = states[['geometry', 'STATE_ID', 'NAME']]

    # trim both outputs to just India + add state names
    global_grid = global_grid.clip(states)
    sas_grid = sas_grid.clip(states)

    global_grid = global_grid.sjoin(states, how="left", predicate='intersects')
    sas_grid = sas_grid.sjoin(states, how="left", predicate='intersects')

    print(sas_grid.columns)

    # compare distributions of PM 2.5 in both outputs
    x = global_grid["TotalPM25"]
    y = sas_grid["TotalPM25"]
    bins = numpy.linspace(-0.01, 2.50, 50)

    pyplot.hist(x, bins, label='PM 2.5 - Global Grid')
    pyplot.hist(y, bins, label='PM 2.5 - South Asia Grid')
    pyplot.legend(loc='upper right')
    pyplot.show()

    # filter to just
    global_grid = global_grid[global_grid["NAME"].isin(['Chhattisgarh',
                                                        'Uttar Pradesh',
                                                        'Madhya Pradesh'])]
    sas_grid = sas_grid[sas_grid["NAME"].isin(['Chhattisgarh',
                                               'Uttar Pradesh',
                                               'Madhya Pradesh'])]

    x = global_grid["TotalPM25"]
    y = sas_grid["TotalPM25"]
    bins = numpy.linspace(-0.01, 2.50, 50)

    pyplot.hist(x, bins, alpha=0.4, label='PM 2.5 - Global Grid')
    pyplot.hist(y, bins, alpha=0.4, label='PM 2.5 - South Asia Grid')
    pyplot.legend(loc='upper right')
    pyplot.show()

    # calculate pop-weighted avg and compare
    global_pop_avg = sum(global_grid["TotalPM25"] * global_grid["TotalPop"])/sum(global_grid["TotalPop"])
    sas_pop_avg = sum(sas_grid["TotalPM25"] * sas_grid["TotalPop"]) / sum(sas_grid["TotalPop"])

    print(global_pop_avg)
    print(sas_pop_avg)

    data = [global_pop_avg, sas_pop_avg]
    pyplot.bar(["Global Grid (PWA)", "South Asia Grid (PWA)"], data)

    pyplot.show()

    # calculate simple avg and compare
    global_avg = sum(global_grid["TotalPM25"]) / len(global_grid["TotalPop"])
    sas_avg = sum(sas_grid["TotalPM25"]) / len(sas_grid["TotalPop"])

    print(global_avg)
    print(sas_avg)

    data = [global_avg, sas_avg]
    pyplot.bar(["Global Grid (SA)", "South Asia Grid (SA)"], data)

    pyplot.show()




main()
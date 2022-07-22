# Goal: use output data from EF sensitivity runs to create a spider plot
# showing the change in attributable mortality given various %-age
# changes in SOx, NOx and PM25 emission factors

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

def main():

    # dictionary of ef names
    ef = {"sox":"SOx", "nox": "NOx", "pm25": "PM2.5"}

    #dictionary of ef vectors
    ef_vals = {"sox":[], "nox":[], "pm25":[]}
    # assign input directory
    directory = "/Users/kiratsingh/Desktop/research/india_coal/health/output/visualization_tables/ef_sensitivity"

    for filename in os.listdir(directory):
        split = filename.split('.')
        var = split[0]
        print(var)
        filepath = os.path.join(directory, filename)

        # import csv
        data = pd.read_csv(filepath)

        # update ef_vals dict with values
        ef_vals[var] = data["diff_v_base_mean_perc"]

    # plot

    x = data["var"]
    y_sox = ef_vals["sox"]
    y_nox = ef_vals["nox"]
    y_pm25 = ef_vals["pm25"]
    print(y_pm25)

    plt.plot(x, y_sox, color="olive", label=ef["sox"])
    plt.plot(x, y_nox, color="steelblue", linestyle='dotted', lw='4', label=ef["nox"])
    plt.plot(x, y_pm25, linestyle='dashed', color="brown", label=ef["pm25"])

    plt.xticks(x)
    plt.legend()

    plt.xlabel("Change in Emission Factor (%)")
    plt.ylabel("Change in Attributal Mortality (%)")

    plt.savefig("/Users/kiratsingh/Documents/coal_health_effects/visualizations/plots/ef_spider.png",
                dpi=300)

    plt.show()


    print(x)


main()
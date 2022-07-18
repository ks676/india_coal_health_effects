# Goal: Plot sensitivity plots for stack features

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def main():

    # dictionary mapping variables to x-axis labels
    var_lab_dict = {'diam' : 'Stack Diameter (m)',
                    'height' : 'Stack Height (m)',
                    'temp' : 'Flue Gas Temperature (°K)',
                    'vel' : 'Flue Gas Velocity (m/s)'}


    var_unit_dict = {'diam' : 'm',
                    'height' : 'm',
                    'temp' : '°K',
                    'vel' : 'm/s'}

    # dictionary mapping variables to baseline values
    var_base_dict = {'diam': 7,
                    'height': 275,
                    'temp': 400,
                    'vel': 22}

    # assign input directory
    directory = "/Users/kiratsingh/Desktop/research/india_coal/health/output/visualization_tables/stack_sensitivity"

    for filename in os.listdir(directory):
        split = filename.split('.')
        var = split[0]
        filepath = os.path.join(directory, filename)

        # import csv
        data = pd.read_csv(filepath)

        # plot

        # trend data
        x = data["var"]
        y = data["diff_v_base_mean_perc"]

        # baseline data
        x_b = var_base_dict[var]

        # get x-axis label from dictionary
        x_lab = var_lab_dict[var]

        # get unit from dict
        x_unit = var_unit_dict[var]

        # construct path where the plot will be saved
        filepath_pre = "/Users/kiratsingh/Documents/coal_health_effects/visualizations/plots/"
        filepath_plot = var + ".png"
        save_filepath = filepath_pre + filepath_plot

        plt.scatter(x_b, 0, color="red")

        plt.plot(x, y)

        plt.xlabel(x_lab + ", Baseline = " + str(x_b) + " " + x_unit)
        plt.ylabel("Change vs. Baseline (%)")

        plt.savefig(save_filepath,
                    dpi=300)

        plt.show()






main()
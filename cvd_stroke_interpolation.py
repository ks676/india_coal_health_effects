# Goal: take as input the cvd_stroke RR file directory, produce as output a version that includes interpolated values
# between 10 and 200 that provide rr values for 0.1 ug/m3 changes in concentrations.

import pandas as pd
import os

def main():

    directory = "/Users/kiratsingh/Desktop/research/india_coal/health/input/risk_curves/cvd_stroke"
    output_directory = "/Users/kiratsingh/Desktop/research/india_coal/health/input/risk_curves/interpolated/cvd_stroke/"

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        split = filename.split('.')
        age_range = split[0]
        print(age_range)

        cvd_stroke = pd.read_csv(filepath)

        interpolation_vector = pd.read_csv("/Users/kiratsingh/Desktop/research/india_coal/health/input/risk_curves/interpolation_vector.csv",
                                       index_col=False)

        cvd_stroke = pd.merge(cvd_stroke, interpolation_vector,
                          how="right",
                          left_on="conc",
                          right_on="conc")

        cvd_stroke['label'] = age_range

        cvd_stroke = cvd_stroke.interpolate(method ='linear', limit_direction ='forward')

        save_path = output_directory + filename

        cvd_stroke.to_csv(save_path, index=False)


main()
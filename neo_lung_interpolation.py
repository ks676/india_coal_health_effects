# Goal: take as input the neo_lung RR file, produce as output a version that includes interpolated values between 10 and
# 200 that provide rr values for 0.1 ug/m3 changes in concentrations.

import pandas as pd

def main():

    neo_lung = pd.read_csv('/Users/kiratsingh/Desktop/research/india_coal/health/input/risk_curves/neo_lung.csv')

    interpolation_vector = pd.read_csv("/Users/kiratsingh/Desktop/research/india_coal/health/input/risk_curves/interpolation_vector.csv",
                                       index_col=False)

    neo_lung = pd.merge(neo_lung, interpolation_vector,
                          how="right",
                          left_on="conc",
                          right_on="conc")

    neo_lung['label'] = 'neo_lung'

    neo_lung = neo_lung.interpolate(method ='linear', limit_direction ='forward')

    neo_lung.to_csv("/Users/kiratsingh/Desktop/research/india_coal/health/input/risk_curves/interpolated/neo_lung.csv", index=False)



main()
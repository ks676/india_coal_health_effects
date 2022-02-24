# Goal: take as input the lri RR file, produce as output a version that includes interpolated values between 10 and
# 200 that provide rr values for 0.1 ug/m3 changes in concentrations.

import pandas as pd
import os

def main():

    lri = pd.read_csv('/Users/kiratsingh/Desktop/research/india_coal/health/input/risk_curves/lri.csv')

    interpolation_vector = pd.read_csv("/Users/kiratsingh/Desktop/research/india_coal/health/input/risk_curves/interpolation_vector.csv",
                                       index_col=False)

    lri = pd.merge(lri, interpolation_vector,
                          how="right",
                          left_on="conc",
                          right_on="conc")

    lri['label'] = 'lri'

    lri = lri.interpolate(method ='linear', limit_direction ='forward')

    lri.to_csv("/Users/kiratsingh/Desktop/research/india_coal/health/input/risk_curves/interpolated/lri.csv", index=False)




main()
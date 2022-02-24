# Goal: take as input the t2_dm RR file, produce as output a version that includes interpolated values between 10 and
# 200 that provide rr values for 0.1 ug/m3 changes in concentrations.

import pandas as pd

def main():

    t2_dm = pd.read_csv('/Users/kiratsingh/Desktop/research/india_coal/health/input/risk_curves/t2_dm.csv')

    interpolation_vector = pd.read_csv("/Users/kiratsingh/Desktop/research/india_coal/health/input/risk_curves/interpolation_vector.csv",
                                       index_col=False)

    t2_dm = pd.merge(t2_dm, interpolation_vector,
                          how="right",
                          left_on="conc",
                          right_on="conc")

    t2_dm['label'] = 't2_dm'

    t2_dm = t2_dm.interpolate(method ='linear', limit_direction ='forward')

    t2_dm.to_csv("/Users/kiratsingh/Desktop/research/india_coal/health/input/risk_curves/interpolated/t2_dm.csv", index=False)




main()
# Goal: take as input the resp_copd RR file, produce as output a version that includes interpolated values between
# 10 and 200 that provide rr values for 0.1 ug/m3 changes in concentrations.

import pandas as pd

def main():

    resp_copd = pd.read_csv('/Users/kiratsingh/Desktop/research/india_coal/health/input/risk_curves/resp_copd.csv')

    interpolation_vector = pd.read_csv("/Users/kiratsingh/Desktop/research/india_coal/health/input/risk_curves/interpolation_vector.csv",
                                       index_col=False)

    resp_copd = pd.merge(resp_copd, interpolation_vector,
                          how="right",
                          left_on="conc",
                          right_on="conc")

    resp_copd['label'] = 'resp_copd'

    resp_copd = resp_copd.interpolate(method ='linear', limit_direction ='forward')

    resp_copd.to_csv("/Users/kiratsingh/Desktop/research/india_coal/health/input/risk_curves/interpolated/resp_copd.csv", index=False)




main()
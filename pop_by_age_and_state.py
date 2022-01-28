# Goal: Take as input the .xls file containing pop by state and age bracket. Output a df containing only the
# necessary columns and cleaned state names

import pandas as pd

def main():

    file = pd.ExcelFile("/Users/kiratsingh/Desktop/research/india_coal/health/input/population/DDW-0000C-14.xls")
    # drop header rows
    df = file.parse('Sheet1', skiprows=7, index_col=None, na_values=['NA'])
    # drop unneeded columns
    df = df.iloc[:,[1,3,4,5]]
    # add column names
    df.columns = ['state_code', 'state_name_census', 'age', 'pop']
    # convert state code to string type for mapping
    df['state_code'] = df['state_code'].astype(str)

    # create dictionary mapping state codes to clean state names
    states = {'0': 'India',
              '1': 'Jammu & Kashmir and Ladakh',
              '2': 'Himachal Pradesh',
              '3': 'Punjab',
              '4': 'Other Union Territories',
              '5': 'Uttarakhand',
              '6': 'Haryana',
              '7': 'Delhi',
              '8': 'Rajasthan',
              '9': 'Uttar Pradesh',
              '10': 'Bihar',
              '11': 'Sikkim',
              '12': 'Arunachal Pradesh',
              '13': 'Nagaland',
              '14': 'Manipur',
              '15': 'Mizoram',
              '16': 'Tripura',
              '17': 'Meghalaya',
              '18': 'Assam',
              '19': 'West Bengal',
              '20': 'Jharkhand',
              '21': 'Odisha',
              '22': 'Chhattisgarh',
              '23': 'Madhya Pradesh',
              '24': 'Gujarat',
              '25': 'Other Union Territories',
              '26': 'Other Union Territories',
              '27': 'Maharashtra',
              '28': 'Andhra Pradesh',
              '29': 'Karnataka',
              '30': 'Goa',
              '31': 'Other Union Territories',
              '32': 'Kerala',
              '33': 'Tamil Nadu',
              '34': 'Other Union Territories',
              '35': 'Other Union Territories'}

    df['state'] = df['state_code'].map(states)

    # clean age column to remove + signs - useful in later steps
    df['age'] = df['age'].str.replace('+', '')

    # remove age groups not used for this analysis
    df = df[df['age'] != 'Age not stated']

    # remove all-India category since this is a state-level table
    df = df[df['state'] != 'India']


    # export as csv for use in other scripts
    df.to_csv('/Users/kiratsingh/Desktop/research/india_coal/health/output/pop_by_age_and_state.csv', index=False)



main()

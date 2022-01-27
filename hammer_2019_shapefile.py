import pandas as pd
import xarray as xr
import shapefile

# The goal of this script is to take as input a netCDF file, and produce as the final output a shapefile.
# This is accomplished by first converting the netCDF file to a dataframe, and then converting the
# table to a shapefile with point geometry.

def main():

    # take .nc file and convert to csv
    file = "/Users/kiratsingh/Desktop/research/india_coal/concentrations/hammer_et_al/2019/0.05_0.05_GWR/ACAG_PM25_GWR_V4GL03_201901_201912_0p05.nc"

    ds = xr.open_dataset(file)

    df = ds.to_dataframe()

    df.to_csv('/Users/kiratsingh/Desktop/research/india_coal/concentrations/hammer_et_al/2019/0.05_0.05_GWR/GL_PM25.csv')

    ### convert csv to a shapefile that can be used in QGIS for comparing with InMAP outputs ###

    # create projection file

    # create file
    prj = open("/Users/kiratsingh/Desktop/research/india_coal/concentrations/hammer_et_al/2019/0.05_0.05_GWR/GL_PM25.prj", "w")

    # define variable containing the file we want to copy here
    gcs = open("/Users/kiratsingh/Library/Mobile Documents/com~apple~CloudDocs/global_inmap/NOx_NATU.prj", "r")

    # process projection file
    gcs = gcs.read().replace(" ", "")
    gcs = gcs.replace("\n", "")

    # write projection file
    prj.write(gcs)
    prj.close()

    # create shapefile

    # create instance of Writer class and declare the geometry type (here POINT type)
    shp = shapefile.Writer("/Users/kiratsingh/Desktop/research/india_coal/concentrations/hammer_et_al/2019/0.05_0.05_GWR/GL_PM25.shp",
                                  shapeType=1)

    # ensure that every record has a corresponding geometry
    shp.autoBalance = 1

    ## add fields ##
    shp.field('PM2_5', 'N')

    # iterate through CSV to populate the shapefile

    # open csv in read mode

    file = open('/Users/kiratsingh/Desktop/research/india_coal/concentrations/hammer_et_al/2019/0.05_0.05_GWR/GL_PM25.csv',
                encoding='utf-8-sig')
    next(file)

    counter = 1

    for line in file:

        line = line.split(',')

        latitude = line[0].strip()
        longitude = line[1].strip()
        line_PM2_5 = line[2].strip()

        # create point geometry
        shp.point(float(longitude), float(latitude))

        # add attribute data
        shp.record(line_PM2_5)

        # track progress
        print(counter)
        counter += 1



main()

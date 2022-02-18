# Goal: Take as input the clipped hammer file and the clipped InMAP grid. Produce as output a shapefile containing
# the hammer point values aggregated to the level of the InMAP grid.

import geopandas

def main():

    # import the clipped hammer file
    hammer = geopandas.read_file("/Users/kiratsingh/Desktop/research/india_coal/health/output/intermediate/hammer_clipped.shp")

    # import the clipped InMAP file
    inmap = geopandas.read_file("/Users/kiratsingh/Desktop/research/india_coal/health/output/intermediate/inmap_grid_clipped.shp")

    print(len(inmap.geometry))

    # to get the aggregated dataset we want, we need to follow a two-step process
    # in the first step, we implement a spatial join, joining all points from hammer onto the inmap grid cells that
    # they intersect with. we then aggregate the resulting dataset, capturing the mean hammer value per grid cell.
    # the second step is necessary because there are some InMAP grid cells - small ones inside densely populated
    # cities, that do not intersect with any hammer observation. as a result, they have no 'mean' hammer value.
    # to get a reasonable estimate of the concentration here, we implement a nearest-join and pick the first match.

    # basic spatial join
    inmap_with_hammer = inmap.sjoin(hammer, how="left", predicate='intersects')

    # calculate mean value of hammer PM 2.5 per polygon where available
    inmap_with_hammer = inmap_with_hammer[['geometry', 'PM2_5']]

    # make column that allows for grouping by geometry
    inmap_with_hammer['WKT'] = inmap_with_hammer['geometry'].apply(lambda x:str(x))

    # dissolve by the new WKT column
    inmap_with_hammer = inmap_with_hammer.dissolve(by='WKT', aggfunc='mean')
    inmap_with_hammer = inmap_with_hammer[['geometry', 'PM2_5']]

    # we now have mean PM 2.5 values from hammer for the majority of InMAP grid cells; for the ones that we still
    # don't have values for, we use the nearest join
    hammer_nearest = geopandas.sjoin_nearest(inmap_with_hammer, inmap_with_hammer, how="left")
    hammer_nearest = hammer_nearest.reset_index()

    hammer_nearest = hammer_nearest.rename(columns={"PM2_5_left": "pm25_hammer_agg",
                                                          "PM2_5_right": "pm25_nearest"})

    nearest_pm25 = hammer_nearest[hammer_nearest['pm25_hammer_agg'].isnull()]
    nearest_pm25 = nearest_pm25[nearest_pm25['pm25_nearest'].notnull()]

    # make column that allows for grouping by geometry
    nearest_pm25['WKT'] = nearest_pm25['geometry'].apply(lambda x: str(x))

    # dissolve by the new WKT column
    nearest_pm25 = nearest_pm25.dissolve(by='WKT', aggfunc='mean')
    nearest_pm25 = nearest_pm25[['geometry', 'pm25_nearest']]
    nearest_pm25 = nearest_pm25.rename(columns={"pm25_nearest": 'PM2_5'})


    # combine the two subsets
    agg_pm25 = inmap_with_hammer[inmap_with_hammer['PM2_5'].notnull()]
    print(len(agg_pm25['PM2_5']))
    print(len(nearest_pm25['PM2_5']))
    inmap_with_hammer = agg_pm25.append(nearest_pm25)
    print(len(inmap_with_hammer['PM2_5']))


    # export dataset as shapefile
    inmap_with_hammer.to_file("/Users/kiratsingh/Desktop/research/india_coal/health/output/intermediate/hammer_aggregated.shp")




main()
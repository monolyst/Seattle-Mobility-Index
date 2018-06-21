## Seattle Universal Geocoder
# This universal geocoder performs a point in polygon inclusion test for commonly used City of Seattle geographies. The path vertices were generated in universal_geocoder_input.pynb by parsing various shapefiles.

# The data in universal_geocoder.py was organized in universal-geocoder-input.ipynb. Shapefile data are preprocessed and stored as key-value dictionaries where the key is the name of the geography and the value is a two dimensional list of vertices. There is a separate dictionary for each type of geography. The inclusion test is conducted using the path function from matplotlib.

# Zip code, blockgroup, and council district shapefiles can be downloaded at the county GIS portal: https://www5.kingcounty.gov/gisdataportal/ 
#Informal neighorhoods can be downloaded at: https://data.seattle.gov/dataset/Neighborhoods/2mbt-aqqx 
#Urban Villages can be downloaded at: #https://data.seattle.gov/dataset/Urban-Villages/ugw3-tp9e
                                
# The function geocode(float longtitude,float latitude) returns a list with the following values:

#    0 - Informal Neighborhood Short Name
#    1 - Informal Neighborhood Long Name
#    2 - Council District
#    3 - Zip Code
#    4 - Urban Village
#    5 - Block Group
#    6 - Geographical Area


import ast
import csv
import os
import sys

from matplotlib import path

maxInt = sys.maxsize
decrement = True

# increase size limit for large fields
while decrement:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.
    decrement = False
    try:
        csv.field_size_limit(maxInt)
    except OverflowError:
        maxInt = int(maxInt/10)
        decrement = True


## Load Data
my_path = os.getcwd()
data_path = os.path.join(my_path, '../seamo/data/raw')
    
GeographicalAreas = {}
for key, value in csv.reader(open(os.path.join(data_path, "zipcode.csv"))):
    GeographicalAreas[key] = value

def geocode(lat,long):
    
    NeighborhoodShort = "None"
    NeighborhoodLong = "None"
    CouncilDistrict = "None"
    ZipCode = "None"
    UrbanVillage = "None"
    BlockGroup = "None"
    GeographicalArea = "None"
    
    for key, value in csv.reader(open(os.path.join(data_path, "Neighborhoods-Short.csv"))):
        p = path.Path(ast.literal_eval(value))
        if p.contains_point((float(lat),float(long))) == True:
            NeighborhoodShort = key.split("--")[0]
            break

    for key, value in csv.reader(open(os.path.join(data_path, "Neighborhoods-Long.csv"))):
        p = path.Path(ast.literal_eval(value))
        if p.contains_point((float(lat),float(long))) == True:
            NeighborhoodLong = key.split("--")[0]
            break
            
    for key, value in csv.reader(open(os.path.join(data_path, "sccdst.csv"))):
        p = path.Path(ast.literal_eval(value))
        if p.contains_point((float(lat),float(long))) == True:
            CouncilDistrict = key.split("--")[0]
            break
            
    for key, value in csv.reader(open(os.path.join(data_path, "zipcode.csv"))):
        p = path.Path(ast.literal_eval(value))
        if p.contains_point((float(lat),float(long))) == True:
            ZipCode = key.split("--")[0]
            # GeographicalArea = GeographicalAreas[str(ZipCode)]            

            # Keys in GeographicalArea actually still have the dashes
            GeographicalArea = GeographicalAreas[str(key)]            
            break

    for key, value in csv.reader(open(os.path.join(data_path, "DPD_uvmfg_polygon.csv"))):
        p = path.Path(ast.literal_eval(value))
        if p.contains_point((float(lat),float(long))) == True:
            UrbanVillage = key.split("--")[0]
            break
            
    for key, value in csv.reader(open(os.path.join(data_path, "blkgrp10_shore.csv"))):
        p = path.Path(ast.literal_eval(value))
        if p.contains_point((float(lat),float(long))) == True:
            BlockGroup = key.split("--")[0]
            break
    
    return (NeighborhoodShort, NeighborhoodLong, CouncilDistrict, ZipCode, UrbanVillage, BlockGroup, GeographicalArea)

# The GeographicalArea is a huge list of coordinates. 
print(geocode(47.534185, -122.371273))

# coding: utf-8
"""
Basket Destination Calculator

This script constructs a market basket of destinations relevant to people
who travel in Seattle. The basket may nearby points of interest and activity
centers that are specific to each origin, and citywide destinations
that are the same for all starting points.

https://public.tableau.com/views/Basket_of_Destinations/Dashboard?:embed=y&:display_count=yes

This script accesses the Google Map Distance Matrix API and ranks each
possible origin-destination pair by their driving distance.
The basket definition is created by using parameters to filter each
class of destination.
"""
import json
import os
from urllib.request import Request, urlopen

import pandas as pd

import init
import constants as cn

from coordinate import Coordinate



origin_df = pd.read_csv(cn.ORIGIN_FP)
dest_df = pd.read_csv(cn.DEST_FP)


def origins_to_destinations(origin_df=origin_df, dest_df=dest_df,
                            method='haversine', threshold=True):
    """
    For every origin, store the distance to every destination in the
    full basket of destinations.
    Distance is calculated either with haversine or
    via the Google Distance Matrix API.

    Inputs: origin_df (dataframe)
            dest_df (dataframe)
            method (string)
            threshold (Boolean)
    Outputs: dist_df (dataframe)
  
    """
    cols = [cn.BLOCKGROUP, cn.PAIR, cn.DISTANCE, cn.CLASS,
            cn.GOOGLE_START_LAT, cn.GOOGLE_START_LON,
            cn.GOOGLE_END_LAT, cn.GOOGLE_END_LON]
   
    rows = []    
 
    for i, row in origin_df.iterrows():
        blockgroup = row[cn.BLOCKGROUP]
        origin_lat, origin_lon = row[cn.CENSUS_LAT], row[cn.CENSUS_LON]
        origin = Coordinate(origin_lat, origin_lon)
        distances = calculate_distances(origin, dest_df, method, threshold)
        for place_id, data in distances.items():
            distance = data[cn.DISTANCE]
            dest_class = data[cn.CLASS]
            end_lat = data[cn.GOOGLE_END_LAT]
            end_lon = data[cn.GOOGLE_END_LON]
            pair = "{0}-{1}".format(blockgroup, place_id)
            row = [blockgroup, pair, distance, dest_class,
                   origin_lat, origin_lon, end_lat, end_lon]
            rows.append(row)

    dist_df = pd.DataFrame(rows, columns=cols]
    
    return dist_df


def rank_destinations(dist_df):
    """
    For each blockgroup, rank destinations by class for proximity.

    Input: dataframe
    Output: dataframe with an added 'rank' column
    """
    # Group by blockgroup and destination class
    grouped = dist_df.groupby([cn.BLOCKGROUP, cn.CLASS])
    # Rank by proximity (closest is highest)
    dist_df[cn.RANK] = grouped[cn.DISTANCE].rank(
        ascending=True, method='first')
    return dist_df


def calculate_distance_API(origin, destination, api_key=None, reader=None):
    """
    Calculate the distance between an origin and destination pair.
    Calls Google Distance Matrix API.

    Input:  origin (Coordinate)
            destination (Coordinate)
    Output: distance in miles (int)
    """
    distance = 0

    url = cn.DIST_MATRIX_URL +\
          'units={0}'.format(cn.IMPERIAL_UNITS) +\
          '&mode={0}'.format(cn.DRIVING_MODE) +\
          '&origins={0}'.format(str(origin)) +\
          "&destinations={0}".format(str(destination)) +\
          "&departure_time={0}".format(cn.TIMESTAMP) +\
          "&key={0}".format(api_key)
    request = Request(url)
    try:
        if reader is None:
            response = urlopen(request).read()
        else:
            response = reader()
        data = json.loads(response)

        if data['status'] != 'OK':
            message = data['error_message']
            with open('API_error.log', 'a+') as outf:
                outf.write("{0} {1} {2}\n".format(origin, destination, message))
        else:
            elements = data['rows'][0]['elements']
            element = elements[0]
            if element['status'] == 'NOT_FOUND':
                # If the origin-destination pair is not found, should write to a log.
                message = 'Could not find the distance for this pair.'
                with open('API_error.log', 'a+') as outf:
                    outf.write("{0} {1} {2}\n".format(origin, destination, message))
            elif element['status'] == 'OK':
                distance = element['distance']['value']
    except:
        message = "URL open error."
        with open('API_error.log', 'a+') as outf:
            outf.write("{0} {1} {2}\n".format(origin, destination, message))

    return distance


def calculate_distance_haversine(origin, destination):
    """
    inputs: origin (Coordinate)
            destination (Coordinate)
    output: distance (float)
            Distance in miles.

    Calculate haversine distance between two points.
    Returns distance in miles.
    """
    distance = origin.haversine_distance(destination)
    return distance


def calculate_distances(origin, dest_df, method, threshold):
    """Calculate the distance (and travel time) to each destination
    and produce a CSV file of the data.
    If threshold is True, only store distances within a threshold in miles.
    Use Haversine or Google API

    Inputs:
        origin (Coordinate)
        dest_df (DataFrame)
        method (string)
        threshold (Boolean)
    Output:
        distances (dict)

    """
    distances = {}

    for index, row in dest_df.iterrows():
        end_lat, end_lon = row[cn.GOOGLE_PLACES_LAT], row[cn.GOOGLE_PLACES_LON]
        destination = Coordinate(end_lat, end_lon)
        dest_class = row[cn.CLASS]
        place_id = row[cn.PLACE_ID]

        if method == 'API':
            distance = calculate_distance_API(origin, destination)
        elif method == 'haversine':
            distance = calculate_distance_haversine(origin, destination)

        data = {cn.GOOGLE_END_LAT: end_lat,
                cn.GOOGLE_END_LON: end_lon,
                cn.DISTANCE: distance,
                cn.CLASS: dest_class}

        # If the distance is within the threshold (5 miles)
        # or if the destination is a citywide
        if threshold:
            if distance <= cn.PROXIMITY_THRESHOLD_MILES or dest_class == 'citywide':
                # Store the distance and the class of destination
                distances[place_id] = data
        else:
            distances[place_id] = data

    return distances


def create_basket(dist_df, basket_combination):
    """
    Given a list of integers denoting counts for basket categories
    and a dataframe of origin-destination pairs with each destination for
    each class ranked by proximity to the origin, create a basket of
    destinations for each blockgroup.

    Input: dist_df (dataframe), basket_combination (list)
    Output: dataframe
    """
    # A list to store intermediate dataframes organized by destination class
    dfs_by_class = []
   
    for i, category in enumerate(cn.BASKET_CATEGORIES):
        class_df = dist_df[(dist_df[cn.CLASS] == category) &
                    (dist_df[cn.RANK] <= basket_combination[i])]
        dfs_by_class.append(class_df)

    # Concatenate the intermediate dataframes
    basket_df = pd.concat(dfs_by_class)

    return basket_df

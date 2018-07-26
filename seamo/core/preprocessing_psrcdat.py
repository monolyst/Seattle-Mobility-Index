"""
This script preprocesses PSRD data; collapses personal level and
trip level data and merges to household level data.
"""

import numpy as np
import pandas as pd


# Household level attributes
HOUSEHOLD_ID = 'hhid'
HOUSEHOLD_SIZE = 'hhsize'
VEHICLE_COUNT = 'vehicle_count'
CHILDREN_COUNT = 'numchildren'
INCOME = 'hhincome_broad'
HOME_OWNERSHIP = 'home_ownership'
OFFSTREET_PARKING = 'offpark'
YEAR_RESIDENCE = 'year_residence'
WEIGHT = 'hh_wt_revised'

# Person-level attibutes
PERSON_ID = 'personid'
AGE = 'age'
RACE_WHITE = 'race_white'
RACE_BLACK = 'race_afam'
RACE_ASIAN = 'race_asian'
RACE_HISPANIC = 'race_hisp'
EDUCATION = 'education'
YEARS_AFTERHIGH = 'years_after_highschool'
EMPLOYED = 'employment'
STUDENT = 'student'

# Household-level attributes of Personal Information
MEAN_AGE = 'mean_age'
PROP_WHITE = 'proportion_white'
PROP_BLACK = 'proportion_black'
PROP_ASIAN = 'proportion_asian'
PROP_HISPANIC = 'proportion_hispanic'
YEAR_EDUCATION = 'mean_education_year'
PROP_EMPLOYED = 'proportion_employed'
PROP_STUDENT = 'proportion_student'
PERSON_COUNT = 'personid_count'

# Trip-level attributes
TRIP_ID = 'tripid'
DISTANCE = 'trip_path_distance'
ONE_DAY_IN_MINIUTES = 1440
DEPART_TIME = 'depart_time_mam'
DURATION = 'google_duration'
NUMBER_TRAVELERS = 'travelers_total'

## MODES and binary categories
MODES = 'mode_1'
DRIVING_ALONE = 'driving_alone'
DRIVING_WITH_OTHERS = 'driving_with_others'
TRANSIT = 'transit'
BIKING = 'biking'
WALKING = 'walking'

## PURPOSE for travel and binary categories
PURPOSE ='dest_purpose'
WENT_HOME = 'went_home'
WENT_WORK = 'went_work'
ERRANDS = 'errands'
SOCIAL = 'social'
GAVE_RIDE = 'gave_ride'

# Household-level attributes of trip information
MEAN_DISTANCE = 'mean_distance'
MEAN_DEPART_TIME = 'mean_depart_time'
MEAN_NUMBER_TRAVELERS = 'mean_num_travelers'
PROP_DRIVING_ALONE = 'prop_driving_alone'
PROP_DRIVING_WITH_OTHERS = 'prop_driving_with_others'
PROP_TRANSIT = 'prop_transit'
PROP_BIKING = 'prop_biking'
PROP_WALKING = 'prop_walking'
MEAN_DURATION = 'mean_duration'
PROP_WENT_HOME = 'prop_went_home'
PROP_WENT_WORK = 'prop_went_work'
PROP_ERRANDS = 'prop_errands'
PROP_SOCIAL = 'prop_social'
PROP_GAVE_RIDE = 'prop_gave_ride'
TRIP_COUNT = 'number_of_trips'

CLUSTER = 'cluster'

# One needs xlsx files with Seattle blockgroup information to preprocess
household = pd.read_excel('psrc/household.xlsx', header = 1)
person = pd.read_excel('psrc/person.xlsx', header = 1)
trip = pd.read_excel('psrc/trip.xlsx', header = 1)
blockgroup_mapping = pd.read_csv('SeattleCensusBlockGroups.csv', index_col=0, dtype={'area': str})

# The study only focuses on those with households residing in Seattle, identified by blockgroups
household = household.loc[household['final_home_bg'].isin(blockgroup_mapping['geoid'])]

def preprocess_household(household_dat):
    
    """
    <Household-level features and categories>

    a. INCOME:
        1: Under $25,000
        2: $25,000-$49,999
        3: $50,000-$74,999
        4: $75,000-$99,999
        5:$100,000 or more
        NaN: missing

    b. HOUSEHOLD SIZE: in this data, there is no household with size 8 or greater 
        1: 1 person
        2: 2 people
        3: 3 people
        4: 4 people
        5: 5 people
        6: 6 people
        7: 7 people
        8: 8 people
        9: 9 people
       10: 10 people
       11: 11 people
       12: 12 or more people
    
    c. VEHICLE_COUNT: in this data, there is no household with size 8 or greater 
        0: 0 (no vehicles)
        1: 1 vehicle
        2: 2 vehicles
        3: 3
        4: 4
        5: 5
        6: 6
        7: 7
        8: 8
        9: 9
       10: 10 or more vehicles
   
    d. CHILDREN_COUNT: unique values {0, 1, 2, 3, 4, 5}

    e. HOME_OWNERSHIP:
        0: Not own
        1: Own/paying mortgage

    f. OFFSTREET_PARKING: all values exist in this data
        0: 0 (no spaces available)
        1: 1
        2: 2
        3: 3
        4: 4
        5: 5
        6: 6
        7: 7
        8: 8
        9: 9
       10: 10 or more

    g. YEAR_RESIDENCE:
        1 -> 1: Less than a year
        2 -> 2: Between 1 and 2 years
        3 -> 3: Between 2 and 3 years
        4 -> 5: Between 3 and 5 years
        5 -> 10: Between 5 and 10 years
     6, 7 -> 20: 10+ years

    h. WEIGHT: survey weight
    """
    hh = household_dat[[HOUSEHOLD_ID, CHILDREN_COUNT, WEIGHT]].copy()
    hh[INCOME] = household[INCOME].replace(6, np.nan)
    hh[HOUSEHOLD_SIZE] = household[HOUSEHOLD_SIZE]
    hh[VEHICLE_COUNT] = household[VEHICLE_COUNT]
    hh[CHILDREN_COUNT] = household[CHILDREN_COUNT]
    hh[HOME_OWNERSHIP] = household['rent_own'].replace([1, 2, 3, 4, 5], [1, 0, 0, 0, np.nan])
    hh[OFFSTREET_PARKING] = household['offpark']
    hh[YEAR_RESIDENCE] = household['res_dur'].replace([2, 3, 4, 5, 6, 7], [2, 3, 5, 10, 20, 20])

    return(hh)



def preprocess_person(hh_dat, person_dat):

    """
    <Person-level features and categories>

    a. AGE: Each category was mapped using the middle point of the age range
        1 -> 2.0 (0-4 years old)
        2 -> 8.0 (5-11 years old)
        3 -> 13.5 (12-15 years)
        4 -> 16.5 (16-17 years)
        5 -> 21.0 (18-24 years)
        6 -> 29.5 (25-34 years)
        7 -> 39.5 (35-44 years)
        8 -> 49.5 (45-54 years)
        9 -> 59.5 (55-64 years)
       10 -> 69.5 (65-74 years)
       11 -> 79.5 (75-84 years)
       12 -> 89.5 (85 or years older)

    b. RACE_WHITE: only for 18+ olds
        0: Non-white
        1: White
        NaN: missing or N/A
    
    c. RACE_BLACK: only for 18+ olds
        0: Non-black
        1: Black
        NaN: missing or N/A
    
    d. RACE_ASIAN: only for 18+ olds
        0: Non-asian
        1: Asian
        NaN: missing or N/A
    
    e. RACE_HISPANIC: only for 18+ olds
        0: Non-hispanic
        1: Hispanic
        NaN: missing or N/A
    
    f. YEARS_AFTERHIGH: calculated from education categories using discretion
        1 -> 0.0 (Less than high school)
        2 -> 0.0 (High school graduate)
        3 -> 1.0 (Some college)
        4 -> 2.0 (Vocational/technical training)
        5 -> 2.0 (Associates degree)
        6 -> 4.0 (Bachelor degree)
        7 -> 6.0 (Graduate/post-graduate degree)
        NaN -> missing or N/A

    g. EMPLOYED: 
        0: Unemplyed (homemaker, retired, or not employed) 
        1: employed (full time, part time, self-employed, volunteer/intern)

    h. STUDENT:
        0: No
        1: Yes (full time or part time student)  
    """

    ps = person_dat[[HOUSEHOLD_ID, PERSON_ID]].copy()
    ps[AGE] = person[AGE].replace([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                  [2.0, 8.0, 13.5, 16.5, 21.0, 29.5, 39.5, 49.5, 59.5, 69.5, 79.5, 89.5])
    ps[RACE_WHITE] = person[RACE_WHITE]
    ps[RACE_BLACK] = person[RACE_BLACK]
    ps[RACE_ASIAN] = person[RACE_ASIAN]
    ps[RACE_HISPANIC] = person[RACE_HISPANIC]
    ps[YEARS_AFTERHIGH] = person[EDUCATION].replace([1, 2, 3, 4, 5, 6, 7], 
                                                    [0.0, 0.0, 1.0, 2.0, 2.0, 4.0, 6.0])
    ps[EMPLOYED] = person[EMPLOYED].replace([1, 2, 3, 4, 5, 6, 7], [1, 1, 1, 1, 0, 0, 0])
    ps[STUDENT] = person[STUDENT].replace([1, 2, 3], [0, 1, 1])

    # Summarize personal level data to household level, by calculating means of each features
    ps_household = ps.groupby([HOUSEHOLD_ID], as_index = False).agg(
        {AGE: 'mean', RACE_WHITE: 'mean', YEARS_AFTERHIGH: 'mean', 
         RACE_BLACK: 'mean', RACE_ASIAN: 'mean', RACE_HISPANIC: 'mean', 
         EMPLOYED: 'mean', STUDENT: 'mean'})
    
    # Rename the variables, as they are collapsed by averaging
    ps_household.rename(columns={AGE: MEAN_AGE, RACE_WHITE: PROP_WHITE, RACE_BLACK: PROP_BLACK,
                             RACE_ASIAN: PROP_ASIAN, RACE_HISPANIC: PROP_HISPANIC, 
                             YEARS_AFTERHIGH: YEAR_EDUCATION, EMPLOYED: PROP_EMPLOYED,
                             STUDENT: PROP_STUDENT, PERSON_ID: PERSON_COUNT}, inplace=True)

    # merge person level data with household level
    hh_plus_ps = pd.merge(left=hh_dat, right=ps_household, how='inner', 
                          left_on=HOUSEHOLD_ID, right_on = HOUSEHOLD_ID)


    return(hh_plus_ps)



def preprocess_trip(hhps_dat, trip_dat):


   """
   <Trip-level features and categories>

   a. DISTANCE: travel distance in miles estimated by Google

   b. DEPART_TIME: Departure time in minutes, 0 - 1440 (1 day = 1440 minutes).
                   If greater than 1440, divided by 1440 and used the remainder

   c. NUMBER_TRAVELERS: integer values from 1 - 9 (or NaN)

   d. MODES: five modes, dummy variable for each category was created after this
        - DRIVING_ALONE
        - DRIVING_WITH_OTHERS
        - TRANSIT
        - BIKING
        - WALKING

   e. DURATION: travel duration in minutes(?) estimated by Google

   f. PURPOSE: purpose of each trip, dummy variables created 
   (code 31 doesn't exist in codebook so changed to NaN)
       - WENT_HOME
       - WENT_WORK
       - ERRANDS
       - SOCIAL
       - GAVE_RIDE
   """
   # replace -9998 with nan   
   trip = trip_dat.replace(-9998, np.nan)  
   tr = trip[[HOUSEHOLD_ID, PERSON_ID, TRIP_ID]].copy()


   tr[DISTANCE] = pd.to_numeric(trip[DISTANCE], errors='coerce').fillna(0).astype(np.float)
   tr[DEPART_TIME] = trip[DEPART_TIME].replace([-5, 1440], np.nan)
   tr[DEPART_TIME] = tr[DEPART_TIME] % ONE_DAY_IN_MINIUTES
   tr[NUMBER_TRAVELERS] = trip[NUMBER_TRAVELERS]

   tr[MODES] = trip[MODES].replace([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 16, 17, 18, 21, 22, 
                                 23, 24, 26, 27, 28, 31, 32, 33, 34, 36, 37, 41, 42, 47, 52, 97], 
                                [WALKING, BIKING, DRIVING_ALONE, DRIVING_ALONE, DRIVING_ALONE, DRIVING_ALONE, DRIVING_ALONE, 
                                 DRIVING_ALONE, DRIVING_ALONE, DRIVING_ALONE, DRIVING_ALONE, DRIVING_ALONE, DRIVING_ALONE,
                                 DRIVING_ALONE, DRIVING_WITH_OTHERS, DRIVING_WITH_OTHERS, DRIVING_WITH_OTHERS,
                                TRANSIT, np.nan, np.nan, np.nan, np.nan, np.nan, TRANSIT, DRIVING_WITH_OTHERS, 
                                 DRIVING_WITH_OTHERS, np.nan, np.nan, TRANSIT, TRANSIT, np.nan, TRANSIT, np.nan])
   # modify values if number of travelers is 1; otherwise leave alone
   tr[MODES] = np.where( (tr[MODES] == DRIVING_WITH_OTHERS) & (tr[NUMBER_TRAVELERS] == 1), DRIVING_ALONE, tr[MODES])  
   # create dummy variables for modes
   dummy_modes = pd.get_dummies(tr[MODES])
   dummy_modes.loc[tr[MODES].isnull(), :] = np.nan
   tr = pd.concat([tr, dummy_modes], axis = 1)


   tr[DURATION] = pd.to_numeric(trip[DURATION], errors='coerce').fillna(0).astype(np.int64)

   tr[PURPOSE] = trip[PURPOSE].replace([1, 6, 9, 10, 11, 14, 30, 32, 33, 34, 50, 51, 52, 53, 54, 56, 60, 61, 62, 97, 31],
                                       [WENT_HOME, WENT_WORK, GAVE_RIDE, WENT_WORK, WENT_WORK, WENT_WORK, ERRANDS, ERRANDS, 
                                        ERRANDS, ERRANDS, SOCIAL, ERRANDS, SOCIAL, SOCIAL, SOCIAL, SOCIAL, np.nan, 
                                        ERRANDS, SOCIAL, np.nan, np.nan])
   dummy_purpose = pd.get_dummies(tr[PURPOSE])
   dummy_purpose.loc[tr[PURPOSE].isnull(), :] = np.nan
   tr = pd.concat([tr, dummy_purpose], axis = 1)

   # Summarize trip level data into household level, using mean

   tr_household = tr.groupby([HOUSEHOLD_ID], as_index = False).agg(
       {DISTANCE: 'mean', DEPART_TIME: 'mean', NUMBER_TRAVELERS: 'mean', DRIVING_ALONE: 'mean', DRIVING_WITH_OTHERS: 'mean',
        TRANSIT: 'mean', BIKING: 'mean', WALKING: 'mean', DURATION: 'mean', WENT_HOME: 'mean', WENT_WORK: 'mean', ERRANDS: 'mean',
        SOCIAL: 'mean', GAVE_RIDE: 'mean', TRIP_ID: 'count'
       })

   tr_household.rename(columns = {DISTANCE: MEAN_DISTANCE,
                                  DEPART_TIME: MEAN_DEPART_TIME,
                                  NUMBER_TRAVELERS: MEAN_NUMBER_TRAVELERS,
                                  DRIVING_ALONE: PROP_DRIVING_ALONE,
                                  DRIVING_WITH_OTHERS: PROP_DRIVING_WITH_OTHERS,
                                  TRANSIT: PROP_TRANSIT,
                                  BIKING: PROP_BIKING,
                                  WALKING: PROP_WALKING,
                                  DURATION: MEAN_DURATION,
                                  WENT_HOME: PROP_WENT_HOME,
                                  WENT_WORK: PROP_WENT_WORK,
                                  ERRANDS: PROP_ERRANDS,
                                  SOCIAL: PROP_SOCIAL,
                                  GAVE_RIDE: PROP_GAVE_RIDE,
                                  TRIP_ID: TRIP_COUNT}, inplace=True)


   # merge trip-level data with household level data (+ person-level data)
   hh_plus_ps_plus_tr = pd.merge(left=hhps_dat, right=tr_household, how='inner', 
                                 left_on=HOUSEHOLD_ID, right_on = HOUSEHOLD_ID)


   return(hh_plus_ps_plus_tr)


hh_result = preprocess_household(household)
hhps_result = preprocess_person(hh_result, person)
hhpstr_result = preprocess_trip(hhps_result, trip)

print(hhpstr_result.head())
# Save the result
print("data is ready to be saved!")
#result.to_csv('personas_processed_psrcdat.csv', index_label=False)

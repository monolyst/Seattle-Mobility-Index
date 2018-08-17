# Seattle Mobility Index


### Seattle Mobility Index

The Seattle Mobility Index Project measures transportation mode choice, affordability, and reliability at 481 Census Block Groups in Seattle. The project is a low-cost, granular approach to understanding, measuring and communicating mobility.

The Seattle Mobility Indices are based on the ability to reach a market basket of destinations derived from actual travel patterns, not solely on locations nearby. 

### Objectives/Goals

1. Market Basket of Destinations. We identified a market basket of destinations that include collections of trips to local destinations, nearby points of interest, and city-wide destination, activity centers that are specific to each origin. 

2. Mobility Indices. We analyze travel from each Census Block Group to the Block Group’s basket of destinations and developed algorithms that return the following indices:
   - Mode Choice: the number of modes available to reach the basket of destinations from each origin to reach the basket of travel destinations, within a duration threshold. 
   - Affordability: the average cost to reach the basket of travel destinations.
   - Reliability: the percentage of trips below the 85th percentile of travel duration. Travel time reliability algorithms will be applied to data that has been collected over a period of time.

3. Mode Share Predictions. We predict the probability a traveler will use a single occupancy vehicle and other modes given the Mode Choice and Affordability scores for their location.



### Seattle Mobility Index

The Seattle Mobility Index Project measures transportation mode choice, affordability, and reliability at 481 Census Block Groups in Seattle. The project is a low-cost, granular approach to understanding, measuring and communicating mobility.

The Seattle Mobility Indices are based on the ability to reach a market basket of destinations derived from actual travel patterns, not solely on locations nearby. 


### Organization of the project

The project has the following structure:

      |-seamo
      |  |-analysis
      |  |  |- ...
      |  |-core
      |  |  |- ...
      |  |-preproc
      |  |  |- ...
      |  |-support
      |  |  |- ...
      |  |-data
      |  |  |-processed
      |  |  |  |-csv_files
      |  |  |  |  |- ...
      |  |  |  |  |-weekday_7_25
      |  |  |  |  |-weekend_7_28
      |  |  |  |  |-weekend_8_5
      |  |  |  |-databases
      |  |  |  |-pickles
      |  |  |  |-shapefiles
      |  |  |  |-tableau
      |  |  |-raw
      |  |  |  |-census-demography
      |  |  |  |-dynamodb_out
      |  |  |  |  |-weekday_7_25
      |  |  |  |  |-weekend_7_28
      |  |  |  |  |-weekend_8_6
      |  |  |  |-shapefiles
      |  |  |-spring2017-travel-survey
      |  |  |-test
      |  |-tests
      |  |  |- ...
      |-notebooks
      |  |- ...





We used the [Shablona](https://github.com/uwescience/shablona) template for our repository structure.



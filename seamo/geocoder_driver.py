# import pdb; pdb.set_trace()
import init
import core.geocoder as geocoder
import core.parking_cost as parking_cost
import preproc.geography_processor as gp
import constants as cn

geo = geocoder.Geocoder()
decoded = geo.geocode_point((47.6145, -122.3210))
# print(decoded)
# print(geo.dataframe)
print(geo.dataframe)

pc = parking_cost.ParkingCost()
decoded = pc.geocode_point((47.6145, -122.3210))
# print(decoded)
# print(pc.dataframe)
print(pc.dataframe)

for rate in [cn.WEEKDAY_MORNING_RATE, cn.WEEKDAY_AFTERNOON_RATE, cn.WEEKDAY_EVENING_RATE,
			cn.WEEKEND_MORNING_RATE, cn.WEEKEND_AFTERNOON_RATE, cn.WEEKEND_EVENING_RATE]:
	print(decoded[rate])
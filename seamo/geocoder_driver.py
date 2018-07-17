# import pdb; pdb.set_trace()
import init
import core.geocoder as geocoder
import core.parking_cost as parking_cost
import preproc.geography_processor as gp

geo = geocoder.Geocoder()
decoded = geo.geocode_point((47.6145, -122.3210))
print(decoded)

pc = parking_cost.ParkingCost()
decoded = pc.geocode_point((47.6145, -122.3210))
print(decoded)
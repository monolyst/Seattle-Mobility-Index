# import pdb; pdb.set_trace()
import init
import core.geocoder as geo
import preproc.geography_processor as gp

decoded = geo.geocode_point((47.6145, -122.3210), reference_type='block_face')
print(decoded)
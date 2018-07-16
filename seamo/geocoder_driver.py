# import pdb; pdb.set_trace()
import init
import core.geocoder as geo
import preproc.geography_processor as gp

decoded = geo.geocode_point((47.57757113, -122.3397739), reference_type='block_face')
print(decoded)
import cProfile
import scripts.core.geopandas_geocoder as gg

cProfile.run('gg.geocode(47.8934, -122.4587)')
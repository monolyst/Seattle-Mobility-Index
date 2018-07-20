# import pdb; pdb.set_trace()
import init
import core.geocoder as geocoder
import core.parking_cost as parking_cost
import preproc.geography_processor as gp
import constants as cn

geo = geocoder.Geocoder()
decoded = geo.geocode_point((47.6145, -122.3210))
# decoded1 = decoded = geo.geocode_point((-122.3210, 47.6145))
print(decoded)
# print(decoded)
# print(geo.dataframe)
# print(geo.dataframe)

pc = parking_cost.ParkingCost()
decoded = pc.geocode_point((47.6145, -122.3210))
decoded1 = pc.geocode_point((-122.3210, 47.6145))
print(decoded1)
# print(pc.dataframe)
# print(pc.dataframe)

# for rate in [cn.WEEKDAY_MORNING_RATE, cn.WEEKDAY_AFTERNOON_RATE, cn.WEEKDAY_EVENING_RATE,
# 			cn.WEEKEND_MORNING_RATE, cn.WEEKEND_AFTERNOON_RATE, cn.WEEKEND_EVENING_RATE]:
# 	print(decoded[rate])


	   #  def main(argv):
    #     choice = str(sys.argv[1])
    #     output_file = str(sys.argv[3]) + '.csv'
    #     try:
    #         sys.argv[4]
    #     except:
    #         pickle_name = cn.REFERENCE_PICKLE
    #     else:
    #         pickle_name = str(sys.argv[4])
    #     if choice == "csv":
    #         # add directory where the file should be found
    #         input_file = os.path.join(PROCESSED_DIR, 'test/', str(sys.argv[2]) + '.csv')
    #         df = geocode_csv(input_file, pickle_name)
    #         write_to_csv(df, PROCESSED_DIR, output_file)
    #     elif choice == "point":
    #         coord = str(sys.argv[2])
    #         df = geocode_point(coord, pickle_name)
    #         write_to_csv(df, PROCESSED_DIR, output_file)
    #     else:
    #         raise "invalid input"


    # if __name__ == "__main__":
    #     main(sys.argv[1:])

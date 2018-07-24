import init
import constants as cn
from index_base_class import IndexBaseClass

class ModeChoiceCalculator(IndexBaseClass):
	"""
	"""

	def __init__(self):
		pass

	def is_viable(self, trip):
		viable = 0
		if trip.mode == cn.CAR and trip.duration < 60:
			viable = 1
		elif trip.mode == cn.BIKE and trip.duration < 60:
			viable = 1
		
		elif trip.mode == cn.TRANSIT and trip.duration < 60:
			viable = 1

		elif trip.mode == cn.WALK and trip.duration < 45:
			viable = 1

			#can we take into account proximity? thinking of nearby locations with bad connections
			# or disnant locations with good connections. Most relevant for bus.

		#Make threasholds constants
		
		return viable




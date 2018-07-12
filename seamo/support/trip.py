"""
Base Trip Class
"""
class Trip(object):
    def __init__(self, origin, destination, mode, distance, duration, category):
        self.origin = origin
        self.destination = destination
        self.mode = mode
        self.distance = distance
        self.duration = calculate_duration(duration)
        self.category = category
        self.persona = None
        self.time_of_day = None
        self.type_of_day = None
        self.cost = calculate_cost(mode)

    def set_persona(self, persona):
        self.persona = persona

    def calculate_cost(self):
        self.cost = 0

    def calculate_duration(duration):
        self.duration = duration

# geocode itself

class CarTrip(Trip):
    def __init__(self, origin, destination, mode, distance, category, duration_in_traffic):
        super().__init__(self, origin, destination, mode="car", distance, category)
        self.duration = calculate_duration(duration, duration_in_traffic)

    def calculate_cost(self, mile_rate, parking, toll_data=0):
        self.cost = self.distance * mile_rate + parking + toll_data

    def calculate_duration(duration, duration_in_traffic):
        # Not sure if this right
        self.duration = duration + duration_in_traffic



class TransitTrip(Trip):
    def __init__(self, origin, destination, mode, distance, category):
        super().__init__(self, origin, destination, mode="transit", distance, category)

    def calculate_cost(self, fare_value):
        self.cost = fare_value
    


class BikeTrip(Trip):
    def __init__(self, origin, destination, mode, distance, category):
        super().__init__(self, origin, destination, mode="bike", distance, category)

    

class WalkTrip(Trip):
    def __init__(self, origin, destination, mode, distance, category):
        super().__init__(self, origin, destination, mode="walk", distance, category)
    


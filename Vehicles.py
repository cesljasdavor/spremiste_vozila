class Vehicles:

    def __init__(self):
        self.vehicles_count = 0
        self.vehicles_list = []

    def add(self, vehicle):
        self.vehicles_count += 1
        self.vehicles_list.append(vehicle)

    def sort_by_departure_time_ascending(self):
        sorted_list = sorted(self.vehicles_list, key=lambda x: x.departure_time)
        return sorted_list

    def __str__(self):
        out = ""
        for vehicle in self.vehicles_list:
            out += str(vehicle)
            out += "\n\n"
        return out

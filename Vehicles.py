

class Vehicles:


	def __init__(self, vehicles_count=0, vehicles_list=[]):
		self.vehicles_count = vehicles_count
		self.vehicles_list = vehicles_list

	def add(self, vehicle):
		self.vehicles_count += 1
		self.vehicles_list.append(vehicle)

	def __str__(self):
		out = ""
		for vehicle in self.vehicles_list:
			out += str(vehicle)
			out += "\n"
		return out


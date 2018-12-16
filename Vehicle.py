
class Vehicle:

	def __init__(self, v_id=None, v_len=None, v_type=None, dep_time=None, sched_type=None, allowed_tracks=[]):
		self.vehicle_id = v_id
		self.vehicle_len = v_len
		self.vehicle_type = v_type
		self.departure_time = dep_time
		self.schedule_type = sched_type
		self.allowed_tracks = allowed_tracks

	def __str__(self):
		out = "Vehicle ID:" + str(self.vehicle_id) + "\n"
		out += "Vehicle length:" + str(self.vehicle_len) + "\n"
		out += "Vehicle type:" + str(self.vehicle_type) + "\n"
		out += "Departure time:" + str(self.departure_time) + "\n"
		out += "Schedule type:" + str(self.schedule_type) + "\n"
		out += "Allowed tracks:" + str(self.allowed_tracks) + "\n"
		return out



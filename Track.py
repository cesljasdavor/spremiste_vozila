

class Track:

	def __init__(self, t_len=None, veh_constraints=None, blocked_tracks=None, vehicles_list=[]):
		self.track_len = t_len
		self.vehicle_constraints = veh_constraints
		self.blocked_tracks = blocked_tracks
		self.vehicles_list = vehicles_list


	def __str__(self):
		out = "Track length:" + str(self.track_len) + "\n"
		out += "Vehicle constraints:" + str(self.vehicle_constraints) + "\n"
		out += "Blocks tracks:" + str(self.blocked_tracks) + "\n"
		out += "Vehicles list:" + str(self.vehicles_list)
		return out
import copy

EMPTY_SPACE = 0.5

class Track:

	def __init__(self, t_id, t_len=None, veh_constraints=None, tracks_blocked_by=None):
		self.track_id = t_id
		self.track_len = t_len
		self.vehicle_constraints = veh_constraints
		self.tracks_blocked_by = tracks_blocked_by
		self.vehicles_list = []
		self.vehicle_count = len(self.vehicles_list)

		self.assigned_type = None
		self.track_len_left = t_len
		self.vehicles_ids = []


	def __str__(self):
		out = "Track ID:" + str(self.track_id) + "\n"
		out += "Track length:" + str(self.track_len) + "\n"
		out += "Vehicle constraints:" + str(self.vehicle_constraints) + "\n"
		out += "Blocks tracks:" + str(self.tracks_blocked_by) + "\n"
		out += "Vehicles list:" + str(self.vehicles_list) + "\n"
		out += "Vehicle count:" + str(self.vehicle_count) + "\n"
		out += "Assigned vehicle type:" + str(self.assigned_type) + "\n"
		out += "Track length left:" + str(self.track_len_left) + "\n"
		out += "Vehicles IDs:" + str(self.vehicles_ids)		
		return out


	# Check if the vehicle type is the same as track type
	def checkType(self, vehicle):
		if self.assigned_type == None:
			return True
		elif self.assigned_type == vehicle.vehicle_type:
			return True
		else:
			print("Type mismatch, track type:" + str(self.assigned_type) + ", vehicle type:" + str(vehicle.vehicle_type))
			return False

	# Check if the track supports this type of vehicle by its ID
	def checkIdAllowed(self, vehicle):
		if vehicle.vehicle_id in self.vehicle_constraints:
			return True
		else:
			print("Vehicle with ID=" + str(vehicle.vehicle_id) + " is not allowed in this track")
			return False

	# Check if there is enough track length left for vehicle to put in
	def checkEnoughLen(self, vehicle):
		if self.vehicle_count == 0:
			if self.track_len_left >= vehicle.vehicle_len:
				return True
			else:
				print("Not enough lenth left in track")
				return False
		else:
			if self.track_len_left >= (vehicle.vehicle_len + EMPTY_SPACE):
				return True
			else:
				print("Not enough lenth left in track")
				return False

	def checkAlreadyExisting(self, vehicle):
		if vehicle in self.vehicles_list:
			return False
		return True

	# Check if the departure time of vehicle is after the departure time of the last vehicle in this track
	def checkTimings(self, vehicle):
		if self.vehicle_count == 0:
			return True
		last_vehicle_timing = self.vehicles_list[-1].departure_time
		if vehicle.departure_time >= last_vehicle_timing:
			return True
		return False

	# Check if vehicle's departure time is lower than the departure times of all the vehicles first in line in tracks that this track blocks
	# Da li ovo uopce treba??
	def checkBlockedTracks(self, vehicle, tracks):
		if self.tracks_blocked_by == None:
			return True
		for btrack in self.tracks_blocked_by:
			checked_track = tracks.getTrackById(btrack)
			if checked_track.vehicle_count == 0:
				continue
			first_vehicle_dtime = checked_track.vehicles_list[0].departure_time
			if vehicle.departure_time > first_vehicle_dtime:
				return False
		return False

	#TODO: Add BLOCKED-BY check when adding: sta ako se doda vozilo u traku koja blokira neke druge, a te druge su prazne, 
	# pa se tek nakon nekog vremena u te blokirane trake zeli dodati neko vozilo?

	# Perform checks and add vehicle to track
	def addVehicle(self, vehicle, tracks):
		if self.checkType(vehicle) and self.checkIdAllowed(vehicle) and self.checkEnoughLen(vehicle) and self.checkAlreadyExisting(vehicle) and self.checkTimings(vehicle) and self.checkBlockedTracks(vehicle, tracks):
			print("Adding vehicle with ID=" + str(vehicle.vehicle_id))
			self.vehicles_ids.append(vehicle.vehicle_id)
			self.vehicles_list.append(vehicle)

			if self.vehicle_count == 0:
				self.track_len_left = self.track_len_left - vehicle.vehicle_len
			else:
				self.track_len_left = self.track_len_left - vehicle.vehicle_len - EMPTY_SPACE

			self.vehicle_count += 1

			vehicle.assigned_track = self
			vehicle.assigned_position = self.vehicle_count # starts at 1
			if self.assigned_type == None:
				self.assigned_type = vehicle.vehicle_type
			return True
		else:
			print("Vehicle not added")
			return False


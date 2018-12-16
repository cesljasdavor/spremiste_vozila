import sys
from Vehicle import *
from Vehicles import *
from Track import *
from Tracks import *

class Problem:


	def __init__(self, input_file):
		self.problem_instance = input_file
		self.vehicles = None
		self.tracks = None
		self.vehicle_count = 0
		self.track_count = 0
		self.vehicle_lenghts = []
		self.vehicle_types = []
		self.track_specifics = []
		self.track_lenghts = []
		self.departure_times = []
		self.schedule_types = []
		self.blocked_tracks = []


	# Parses problem instance given from input file
	def parseProblem(self):
		print("Parsing problem...\n")
		with open(self.problem_instance, 'r') as f:

			# Vehicle count
			self.vehicle_count = int(f.readline().strip())
			print("Vehicle count:", self.vehicle_count)

			# Track count
			self.track_count = int(f.readline().strip())
			print("Track count:", self.track_count)

			# Empty space
			f.readline()

			# Vehicle lenghts
			self.vehicle_lenghts = f.readline().strip()
			self.vehicle_lenghts = self.vehicle_lenghts.split(' ')
			if len(self.vehicle_lenghts) != self.vehicle_count:
				sys.exit("vehicle_lenghts and vehicle count don't match")
			print("\nVehicle lenghts:")
			self.vehicle_lenghts = list(map(int, self.vehicle_lenghts))
			print(self.vehicle_lenghts)

			# Empty space
			f.readline()

			# Vehicle types
			self.vehicle_types = f.readline().strip().split(' ')
			if len(self.vehicle_types) != self.vehicle_count:
				sys.exit("vehicle_types and vehicle count don't match")
			print("\n Vehicle types:")
			print(self.vehicle_types)

			# Empty space
			f.readline()

			# Track specifics matrix
			for i in range(self.vehicle_count):
				veh_specifics = f.readline().strip().split(' ')
				veh_specifics = list(map(int, veh_specifics))
				self.track_specifics += [veh_specifics]
			print("\nTrack specifics:")
			print(self.track_specifics)

			# Empty space
			f.readline()

			# Track lenghts
			self.track_lenghts = f.readline().strip().split(' ')
			self.track_lenghts = list(map(int, self.track_lenghts))
			print("\nTrack lenghts:")
			print(self.track_lenghts)

			# Empty space
			f.readline()

			# Departure times
			self.departure_times = f.readline().strip().split(' ')
			self.departure_times = list(map(int, self.departure_times))
			print("\nDeparture times:")
			print(self.departure_times)

			# Empty space
			f.readline()

			# Schedule types
			self.schedule_types = f.readline().strip().split(' ')
			print("\nSchedule types:")
			print(self.schedule_types)

			# Empty space
			f.readline()

			# Blocked tracks
			for line in f.readlines():
				tmp_track = line.strip().split(' ')
				self.blocked_tracks += [tmp_track]
			print("\nBlocked tracks:")
			print(self.blocked_tracks)

		self.makeObjects()
			

	def makeObjects(self):

		# Make Vehicles
		print("\nCreating vehicles...\n")
		self.vehicles = Vehicles()
		for v in range(self.vehicle_count):
			vehicle = Vehicle((v + 1), self.vehicle_lenghts[v], self.vehicle_types[v], self.departure_times[v], self.schedule_types[v], self.track_specifics[v])
			self.vehicles.add(vehicle)
		print("Added vehicles:")
		print(self.vehicles)


		# Make Tracks
		print("Creating tracks...\n")
		self.tracks = Tracks()
		for t in range(self.track_count):

			allowed_vehicles = []
			for v in range(self.vehicle_count):
				if self.track_specifics[v][t] == 1:
					allowed_vehicles.append(v+1)

			if t < len(self.blocked_tracks):
				track = Track(self.track_lenghts[t], allowed_vehicles, self.blocked_tracks[t])
			else:
				track = Track(self.track_lenghts[t], allowed_vehicles)
			self.tracks.add(track)
		print("Added tracks:")
		print(self.tracks)


	# Implements solution to the problem instance
	def solve(self):
		pass

	# Output solution to file "outfile"
	def outputSolution(self, outfile):
		pass


def main():
	
	problem = Problem("./prob_instance_1")
	problem.parseProblem()

if __name__ == "__main__":
	main()
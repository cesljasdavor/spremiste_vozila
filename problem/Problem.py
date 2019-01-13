import sys
from random import shuffle

from problem.ProblemGrader import ProblemGrader
from models.Track import *
from models.Vehicle import *


class Problem:

    def __init__(self, input_file):
        self.problem_instance = input_file
        self.vehicles = None
        self.vehicle_count = 0
        self.vehicle_lengths = []
        self.vehicle_types = []
        self.departure_times = []
        self.schedule_types = []
        self.tracks = None
        self.track_count = 0
        self.track_specifics = []
        self.track_lengths = []
        self.tracks_blocked_by = {}
        self.blocking_tracks = {}
        self.best_gg1 = sys.maxsize
        self.best_gg2 = -sys.maxsize - 1
        self.best_tracks = None

    def make_objects(self):
        """
        Create iteration objects
        :return: void
        """

        self.vehicles = []
        for vehicle_index in range(self.vehicle_count):
            vehicle = Vehicle(
                vehicle_index + 1,
                self.vehicle_lengths[vehicle_index],
                self.vehicle_types[vehicle_index],
                self.departure_times[vehicle_index],
                self.schedule_types[vehicle_index],
                self.track_specifics[vehicle_index]
            )

            self.vehicles.append(vehicle)

        # Make Tracks
        track_id = 1
        self.tracks = []
        for track_index in range(self.track_count):
            allowed_vehicles = []
            for vehicle_index in range(self.vehicle_count):
                if self.track_specifics[vehicle_index][track_index] == 1:
                    allowed_vehicles.append(vehicle_index + 1)

            tracks_blocked_by = self.tracks_blocked_by[track_id] if track_id in self.tracks_blocked_by else None
            track = Track(track_id, self.track_lengths[track_index], allowed_vehicles, tracks_blocked_by)

            self.tracks.append(track)
            track_id += 1

    def solve(self):
        """
        Implements solution to the problem instance
        :return: void
        """

        vehicles_added = 0
        vehicles_sorted = sorted(self.vehicles, key=lambda x: x.departure_time)
        for vehicle in vehicles_sorted:
            shuffle(self.tracks)
            for track in self.tracks:
                if track.add_vehicle(vehicle, self.tracks):
                    vehicles_added += 1
                    break

        if vehicles_added == self.vehicle_count:
            grader = ProblemGrader(self)
            goal1 = grader.calculate_first_global_goal()
            goal2 = grader.calculate_second_global_goal()
            if goal1 < self.best_gg1 and goal2 > self.best_gg2:
                print("Success: ", goal1, goal2)
                self.best_gg1 = goal1
                self.best_gg2 = goal2
                self.best_tracks = self.tracks


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
        self.blocking_tracks = None
        self.non_blocking_tracks = None
        self.track_count = 0
        self.track_specifics = []
        self.track_lengths = []
        self.tracks_blocked_by_dict = {}
        self.blocking_tracks_dict = {}
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
            allowed_tracks_count = 0
            for track_index in range(self.track_count):
                allowed_tracks_count += self.track_specifics[vehicle_index][track_index]

            vehicle = Vehicle(
                vehicle_index + 1,
                self.vehicle_lengths[vehicle_index],
                self.vehicle_types[vehicle_index],
                self.departure_times[vehicle_index],
                self.schedule_types[vehicle_index],
                allowed_tracks_count,
                self.track_specifics[vehicle_index]
            )

            self.vehicles.append(vehicle)

        track_counter = 1
        self.tracks = []
        self.blocking_tracks = []
        self.non_blocking_tracks = []
        for track_index in range(self.track_count):
            allowed_vehicles = []
            for vehicle_index in range(self.vehicle_count):
                if self.track_specifics[vehicle_index][track_index] == 1:
                    allowed_vehicles.append(vehicle_index + 1)

            track_id = str(track_counter)
            tracks_blocked_by = self.tracks_blocked_by_dict[
                track_id] if track_id in self.tracks_blocked_by_dict else None
            blocking_tracks = self.blocking_tracks_dict[track_id] if track_id in self.blocking_tracks_dict else None
            track = Track(
                track_id,
                self.track_lengths[track_index],
                allowed_vehicles,
                tracks_blocked_by,
                blocking_tracks
            )

            self.tracks.append(track)
            if track_id in self.tracks_blocked_by_dict.keys():
                self.blocking_tracks.append(track)
            else:
                self.non_blocking_tracks.append(track)

            track_counter += 1

    def solve(self):
        """
        Implements solution to the problem instance
        :return: void
        """

        grader = ProblemGrader(self)
        # tracks_copy = self.tracks.copy()
        blocking_tracks_copy = self.blocking_tracks.copy()
        non_blocking_tracks_copy = self.non_blocking_tracks.copy()
        vehicles_sorted = sorted(self.vehicles, key=lambda x: x.departure_time)

        for vehicle in vehicles_sorted:
            best_ratio = - sys.maxsize - 1
            best_track = None
            shuffle(blocking_tracks_copy)
            for track in blocking_tracks_copy:
                if track.add_vehicle(vehicle, self.tracks):
                    grader.reinitialize_grader()
                    goal1 = grader.calculate_first_global_goal()
                    goal2 = grader.calculate_second_global_goal()
                    ratio = goal2 / goal1
                    if ratio > best_ratio:
                        best_ratio = ratio
                        best_track = track

                    track.remove_last()

            if best_track is not None:
                best_track.add_vehicle(vehicle, self.tracks)
                vehicles_sorted.remove(vehicle)
            else:
                break

        while len(vehicles_sorted) != 0:
            best_ratio = - sys.maxsize - 1
            best_track = None
            best_vehicle = None
            shuffle(non_blocking_tracks_copy)

            for vehicle in vehicles_sorted:
                for track in non_blocking_tracks_copy:
                    if track.add_vehicle(vehicle, self.tracks):
                        grader.reinitialize_grader()
                        goal1 = grader.calculate_first_global_goal()
                        goal2 = grader.calculate_second_global_goal()
                        ratio = goal2 / goal1
                        if ratio > best_ratio:
                            best_ratio = ratio
                            best_track = track
                            best_vehicle = vehicle

                        track.remove_last()

            if best_vehicle is not None and best_track is not None:
                best_track.add_vehicle(best_vehicle, self.tracks)
                vehicles_sorted.remove(best_vehicle)
            else:
                return False

        if len(vehicles_sorted) != 0:
            return False

        grader.reinitialize_grader()
        goal1 = grader.calculate_first_global_goal()
        goal2 = grader.calculate_second_global_goal()
        print("Success:", goal1, goal2)
        if goal1 < self.best_gg1 and goal2 > self.best_gg2:
            self.best_gg1 = goal1
            self.best_gg2 = goal2
            self.best_tracks = self.tracks

        return True

import time
from random import shuffle

from Track import *
from Tracks import *
from Vehicle import *
from Vehicles import *


class Problem:

    def __init__(self, input_file):
        self.problem_instance = input_file
        self.vehicles = None
        self.tracks = None
        self.vehicle_count = 0
        self.track_count = 0
        self.vehicle_lengths = []
        self.vehicle_types = []
        self.track_specifics = []
        self.track_lengths = []
        self.departure_times = []
        self.schedule_types = []
        self.tracks_blocked_by = {}
        self.blocking_tracks = {}
        self.best_g1 = sys.maxsize
        self.best_g2 = -sys.maxsize - 1
        self.best_tracks = None

    def parse_problem(self):
        """
        Parses problem instance given from input file
        :return: void
        """
        with open(self.problem_instance, 'r') as f:

            # Vehicle count
            self.vehicle_count = int(f.readline().strip())

            # Track count
            self.track_count = int(f.readline().strip())

            # Empty space
            f.readline()

            # Vehicle lenghts
            self.vehicle_lengths = f.readline().strip()
            self.vehicle_lengths = self.vehicle_lengths.split(' ')
            if len(self.vehicle_lengths) != self.vehicle_count:
                sys.exit("vehicle_lenghts and vehicle count don't match")
            self.vehicle_lengths = list(map(int, self.vehicle_lengths))

            # Empty space
            f.readline()

            # Vehicle types
            self.vehicle_types = f.readline().strip().split(' ')
            if len(self.vehicle_types) != self.vehicle_count:
                sys.exit("vehicle_types and vehicle count don't match")

            # Empty space
            f.readline()

            # Track specifics matrix
            for i in range(self.vehicle_count):
                veh_specifics = f.readline().strip().split(' ')
                veh_specifics = list(map(int, veh_specifics))
                self.track_specifics += [veh_specifics]

            # Empty space
            f.readline()

            # Track lengths
            self.track_lengths = f.readline().strip().split(' ')
            self.track_lengths = list(map(int, self.track_lengths))

            # Empty space
            f.readline()

            # Departure times
            self.departure_times = f.readline().strip().split(' ')
            self.departure_times = list(map(int, self.departure_times))

            # Empty space
            f.readline()

            # Schedule types
            self.schedule_types = f.readline().strip().split(' ')

            # Empty space
            f.readline()

            # Blocked tracks
            for line in f.readlines():
                tmp_track = line.strip().split(' ')
                self.tracks_blocked_by[tmp_track[0]] = tmp_track[1:]

                for track in tmp_track[1:]:
                    if track in self.blocking_tracks:
                        self.blocking_tracks[track].append(tmp_track[0])
                    else:
                        self.blocking_tracks[track] = [tmp_track[0]]

    def make_objects(self):

        # Make Vehicles
        self.vehicles = Vehicles()
        for v in range(self.vehicle_count):
            vehicle = Vehicle((v + 1), self.vehicle_lengths[v], self.vehicle_types[v], self.departure_times[v],
                              self.schedule_types[v], self.track_specifics[v])
            self.vehicles.add(vehicle)

        # Make Tracks
        t_id = 1
        self.tracks = Tracks()
        for t in range(self.track_count):
            track = None
            allowed_vehicles = []
            for v in range(self.vehicle_count):
                if self.track_specifics[v][t] == 1:
                    allowed_vehicles.append(v + 1)

            if t_id in self.tracks_blocked_by:
                track = Track(t_id, self.track_lengths[t], allowed_vehicles, self.tracks_blocked_by[t_id])
            else:
                track = Track(t_id, self.track_lengths[t], allowed_vehicles)
            self.tracks.add(track)
            t_id += 1

    def solve(self):
        """
        Implements solution to the problem instance
        :return: void
        """
        vehicles_added = 0
        for vehicle in self.vehicles.sortByDepartureTimeAscending():
            shuffle(self.tracks.tracks_list)
            for track in self.tracks.tracks_list:
                if track.addVehicle(vehicle, self.tracks) == True:
                    vehicles_added += 1
                    break

        if vehicles_added == self.vehicle_count:
            goal1 = self.first_global_goal_evaluate()
            goal2 = self.second_global_goal_evalute()
            if goal1 < self.best_g1 and goal2 > self.best_g2:
                print("Best: ", goal1, goal2)
                self.best_g1 = goal1
                self.best_g2 = goal2
                self.best_tracks = self.tracks
                print("Success: ", goal1, goal2)

    # Output solution to file "outfile"
    def output_solution(self, outfile):
        with open(outfile, "w") as f:
            count = 0
            for track in self.best_tracks.tracks_list:
                out = ""
                for vehicle in track.vehicles_list:
                    out += str(vehicle.vehicle_id) + " "
                f.write(out)
                count += 1
                if count < self.track_count:
                    f.write("\n")

    def first_global_goal_evaluate(self):
        used_count = 0
        for track in self.tracks.tracks_list:
            if track.vehicle_count > 0:
                used_count += 1
        p1 = 1 / (used_count - 1)

        assignes_types_list = []
        for track in self.tracks.tracks_list:
            if track.vehicle_count > 0:
                assignes_types_list.append(track.assigned_type)
        f1 = 0
        for first, second in zip(assignes_types_list, assignes_types_list[1:]):
            if first != second:
                f1 += 1

        p2 = 1 / (self.track_count)

        f2 = used_count

        p3 = 1 / (sum(self.track_lengths) - sum(self.vehicle_lengths))

        f3 = 0
        for track in self.tracks.tracks_list:
            if track.vehicle_count > 0:
                f3 += track.track_len_left

        return p1 * f1 + p2 * f2 + p3 * f3

    def second_global_goal_evalute(self):
        used_count = 0
        for track in self.tracks.tracks_list:
            if track.vehicle_count > 0:
                used_count += 1
        r1 = 1 / (self.vehicle_count - used_count)

        g1 = 0
        for track in self.tracks.tracks_list:
            if track.vehicle_count > 1:
                sched_type_count = 0
                for first, second in zip(track.vehicles_list, track.vehicles_list[1:]):
                    if first.schedule_type == second.schedule_type:
                        sched_type_count += 1
                g1 += sched_type_count

        r2 = 1 / (used_count - 1)

        g2 = 0
        used_tracks = []
        for track in self.tracks.tracks_list:
            if track.vehicle_count > 0:
                used_tracks.append(track)
        for first, second in zip(used_tracks, used_tracks[1:]):
            if first.vehicles_list[-1].schedule_type == second.vehicles_list[0].schedule_type:
                g2 += 1

        eval_pairs = 0
        g3 = 0
        for track in self.tracks.tracks_list:
            if track.vehicle_count > 1:
                for first, second in zip(track.vehicles_list, track.vehicles_list[1:]):
                    diff = second.departure_time - first.departure_time
                    eval_pairs += 1
                    if 10 <= diff <= 20:
                        g3 += 15
                    elif diff > 20:
                        g3 += 10
                    elif diff < 10:
                        g3 += -4 * (10 - diff)

        r3 = 1 / (15 * eval_pairs)

        return r1 * g1 + r2 * g2 + r3 * g3


def main():
    problem_file = sys.argv[1]
    minutes = int(sys.argv[2])

    problem = Problem(problem_file)
    problem.parse_problem()

    t_end = time.time() + 60 * minutes
    while time.time() < t_end:
        problem.make_objects()
        problem.solve()
    problem.output_solution("res-{0}m-{1}.txt".format(
        minutes if minutes == 1 or minutes == 5 else "n",
        problem_file.split(".")[0])
    )


if __name__ == "__main__":
    main()

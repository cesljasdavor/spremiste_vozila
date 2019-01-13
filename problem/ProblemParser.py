class ProblemParser(object):
    def __init__(self, problem):
        self.problem = problem

    def parse(self):
        """
        Parses problem instance given in problem's input file
        :return: void
        """

        with open(self.problem.problem_instance, 'r') as file:

            # Vehicle count
            self.problem.vehicle_count = int(file.readline().strip())

            # Track count
            self.problem.track_count = int(file.readline().strip())

            # Empty space
            file.readline()

            # Vehicle lengths
            self.problem.vehicle_lengths = file.readline().strip().split(' ')
            self.problem.vehicle_lengths = list(map(int, self.problem.vehicle_lengths))

            # Empty space
            file.readline()

            # Vehicle types
            self.problem.vehicle_types = file.readline().strip().split(' ')

            # Empty space
            file.readline()

            # Track specifics matrix
            for i in range(self.problem.vehicle_count):
                veh_specifics = file.readline().strip().split(' ')
                veh_specifics = list(map(int, veh_specifics))
                self.problem.track_specifics += [veh_specifics]

            # Empty space
            file.readline()

            # Track lengths
            self.problem.track_lengths = file.readline().strip().split(' ')
            self.problem.track_lengths = list(map(int, self.problem.track_lengths))

            # Empty space
            file.readline()

            # Departure times
            self.problem.departure_times = file.readline().strip().split(' ')
            self.problem.departure_times = list(map(int, self.problem.departure_times))

            # Empty space
            file.readline()

            # Schedule types
            self.problem.schedule_types = file.readline().strip().split(' ')

            # Empty space
            file.readline()

            # Blocked tracks
            for line in file.readlines():
                tmp_track = line.strip().split(' ')
                self.problem.tracks_blocked_by[tmp_track[0]] = tmp_track[1:]

                for track in tmp_track[1:]:
                    if track in self.problem.blocking_tracks:
                        self.problem.blocking_tracks[track].append(tmp_track[0])
                    else:
                        self.problem.blocking_tracks[track] = [tmp_track[0]]

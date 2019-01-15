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
                vehicle_specifics = file.readline().strip().split(' ')
                vehicle_specifics = list(map(int, vehicle_specifics))
                self.problem.track_specifics += [vehicle_specifics]

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
                track_data = line.strip().split(' ')
                self.problem.tracks_blocked_by_dict[track_data[0]] = track_data[1:]

                for track in track_data[1:]:
                    if track in self.problem.blocking_tracks_dict:
                        self.problem.blocking_tracks_dict[track].append(track_data[0])
                    else:
                        self.problem.blocking_tracks_dict[track] = [track_data[0]]

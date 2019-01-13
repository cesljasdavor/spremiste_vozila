class SolutionWriter(object):
    def __init__(self, problem):
        self.problem = problem

    def write(self, output_file_name):
        """
        Writes solution to file
        :param output_file_name: output file name
        :return: void
        """

        with open(output_file_name, "w") as f:
            count = 0
            for track in self.problem.best_tracks:
                out = ""
                for vehicle in track.vehicles:
                    out += str(vehicle.vehicle_id) + " "
                f.write(out)
                count += 1
                if count < self.problem.track_count:
                    f.write("\n")

class ProblemGrader(object):
    def __init__(self, problem):
        self.problem = problem
        self.used_count = self.get_used_count()

    def get_used_count(self):
        used_count = 0
        for track in self.problem.tracks:
            if track.vehicle_count() > 0:
                used_count += 1

        return used_count

    def calculate_first_global_goal(self):
        """
        Calculates first global goal
        :return: first global goal
        """

        return self.calculate_first_subgoal() + self.calculate_second_subgoal() + self.calculate_third_subgoal()

    def calculate_first_subgoal(self):
        """
        Calculates first subgoal of first global goal
        :return: first subgoal of first global goal
        """

        p1 = 1 / (self.used_count - 1)

        assignees_types_list = []
        for track in self.problem.tracks:
            if track.vehicle_count() > 0:
                assignees_types_list.append(track.assigned_type)
        f1 = 0
        for first, second in zip(assignees_types_list, assignees_types_list[1:]):
            if first != second:
                f1 += 1

        return p1 * f1

    def calculate_second_subgoal(self):
        """
        Calculates second subgoal of first global goal
        :return: second subgoal of first global goal
        """

        p2 = 1 / self.problem.track_count
        f2 = self.used_count

        return p2 * f2

    def calculate_third_subgoal(self):
        """
        Calculates third subgoal of first global goal
        :return: third subgoal of first global goal
        """

        p3 = 1 / (sum(self.problem.track_lengths) - sum(self.problem.vehicle_lengths))

        f3 = 0
        for track in self.problem.tracks:
            if track.vehicle_count() > 0:
                f3 += track.track_length_left

        return p3 * f3

    def calculate_second_global_goal(self):
        """
        Calculates second global goal
        :return: second global goal
        """

        return self.calculate_fourth_subgoal() + self.calculate_fifth_subgoal() + self.calculate_sixth_subgoal()

    def calculate_fourth_subgoal(self):
        """
        Calculates first subgoal of second global goal
        :return: first subgoal of second global goal
        """

        r1 = 1 / (self.problem.vehicle_count - self.used_count)

        g1 = 0
        for track in self.problem.tracks:
            if track.vehicle_count() > 1:
                sched_type_count = 0
                for first, second in zip(track.vehicles, track.vehicles[1:]):
                    if first.schedule_type == second.schedule_type:
                        sched_type_count += 1
                g1 += sched_type_count

        return r1 * g1

    def calculate_fifth_subgoal(self):
        """
        Calculates second subgoal of second global goal
        :return: second subgoal of second global goal
        """

        r2 = 1 / (self.used_count - 1)

        g2 = 0
        used_tracks = []
        for track in self.problem.tracks:
            if track.vehicle_count() > 0:
                used_tracks.append(track)
        for first, second in zip(used_tracks, used_tracks[1:]):
            if first.vehicles[-1].schedule_type == second.vehicles[0].schedule_type:
                g2 += 1

        return r2 * g2

    def calculate_sixth_subgoal(self):
        """
        Calculates third subgoal of second global goal
        :return: third subgoal of second global goal
        """

        eval_pairs = 0
        g3 = 0
        for track in self.problem.tracks:
            if track.vehicle_count() > 1:
                for first, second in zip(track.vehicles, track.vehicles[1:]):
                    diff = second.departure_time - first.departure_time
                    eval_pairs += 1
                    if 10 <= diff <= 20:
                        g3 += 15
                    elif diff > 20:
                        g3 += 10
                    elif diff < 10:
                        g3 += -4 * (10 - diff)

        r3 = 1 / (15 * eval_pairs)

        return r3 * g3

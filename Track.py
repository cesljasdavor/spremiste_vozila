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

    def check_type(self, vehicle):
        """
        Check if the vehicle type is the same as track type
        :param vehicle: vehicle object
        :return: boolean
        """

        if self.assigned_type is None:
            return True
        elif self.assigned_type == vehicle.vehicle_type:
            return True
        else:
            return False

    def check_id_allowed(self, vehicle):
        """
        Check if the track supports this type of vehicle by its ID
        :param vehicle: vehicle object
        :return: boolean
        """

        if vehicle.vehicle_id in self.vehicle_constraints:
            return True
        else:
            return False

    def check_enough_length(self, vehicle):
        """
        Check if there is enough track length left for vehicle to put in
        :param vehicle: vehicle object
        :return: boolean
        """

        if self.vehicle_count == 0:
            if self.track_len_left >= vehicle.vehicle_len:
                return True
            else:
                return False
        else:
            if self.track_len_left >= (vehicle.vehicle_len + EMPTY_SPACE):
                return True
            else:
                return False

    def check_already_existing(self, vehicle):
        """
        Check if vehicle already exists
        :param vehicle: vehicle object
        :return: boolean
        """

        if vehicle in self.vehicles_list:
            return False
        return True

    def check_timings(self, vehicle):
        """
        Check if the departure time of vehicle is after the departure time of the last vehicle in this track
        :param vehicle: vehicle object
        :return: boolean
        """

        if self.vehicle_count == 0:
            return True
        last_vehicle_timing = self.vehicles_list[-1].departure_time
        if vehicle.departure_time >= last_vehicle_timing:
            return True
        return False

    def check_blocked_tracks(self, vehicle, tracks):
        """
        Check if vehicle's departure time is lower than the departure times of
        all the vehicles first in line in tracks that this track blocks
        :param vehicle: vehicle object
        :param tracks: tracks object
        :return: boolean
        """

        if self.tracks_blocked_by is None:
            return True
        for bTrack in self.tracks_blocked_by:
            checked_track = tracks.get_track_by_id(bTrack)
            if checked_track.vehicle_count == 0:
                continue
            first_vehicle_dtime = checked_track.vehicles_list[0].departure_time
            if vehicle.departure_time > first_vehicle_dtime:
                return False
        return False

    def add_vehicle(self, vehicle, tracks):
        """
        Perform checks and add vehicle to track
        :param vehicle: vehicle object
        :param tracks: tracks object
        :return: boolean
        """

        if self.check_type(vehicle) and self.check_id_allowed(vehicle) and self.check_enough_length(
                vehicle) and self.check_already_existing(vehicle) and self.check_timings(vehicle) and self.check_blocked_tracks(vehicle, tracks):
            self.vehicles_ids.append(vehicle.vehicle_id)
            self.vehicles_list.append(vehicle)

            if self.vehicle_count == 0:
                self.track_len_left = self.track_len_left - vehicle.vehicle_len
            else:
                self.track_len_left = self.track_len_left - vehicle.vehicle_len - EMPTY_SPACE

            self.vehicle_count += 1

            vehicle.assigned_track = self
            vehicle.assigned_position = self.vehicle_count  # starts at 1
            if self.assigned_type is None:
                self.assigned_type = vehicle.vehicle_type
            return True
        else:
            return False

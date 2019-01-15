from utils.TrackUtils import find_track

EMPTY_SPACE = 0.5


class Track:

    def __init__(
            self,
            track_id,
            track_length=None,
            vehicle_constraints=None,
            tracks_blocked_by=None,
            blocking_tracks=None
    ):
        self.track_id = track_id
        self.track_length = track_length
        self.vehicle_constraints = vehicle_constraints
        self.tracks_blocked_by = tracks_blocked_by
        self.blocking_tracks = blocking_tracks
        self.vehicles_ids = []
        self.vehicles = []

        self.assigned_type = None
        self.track_length_left = track_length

    def check_vehicle(self, vehicle, tracks):
        """
        Check if vehicle can be added to this track
        :param vehicle: vehicle to check
        :param tracks: list of all tracks
        :return:
        """

        # Types match
        if self.assigned_type is not None and self.assigned_type != vehicle.vehicle_type:
            return False

        # Id allowed
        if vehicle.vehicle_id not in self.vehicle_constraints:
            return False

        # Enough length
        if self.vehicle_count() == 0:
            if self.track_length_left < vehicle.vehicle_length:
                return False
        else:
            if self.track_length_left < (vehicle.vehicle_length + EMPTY_SPACE):
                return False

        # Already existing
        if vehicle in self.vehicles:
            return False

        # Timings
        if self.vehicle_count() != 0:
            last_vehicle_timing = self.vehicles[-1].departure_time
            if vehicle.departure_time < last_vehicle_timing:
                return False

        # Blocked by
        if self.tracks_blocked_by is not None:
            for blocked_track_id in self.tracks_blocked_by:
                blocked_track = find_track(tracks, blocked_track_id)

                if blocked_track.vehicle_count() == 0:
                    continue

                first_vehicle_departure_time = blocked_track.vehicles[0].departure_time
                if vehicle.departure_time > first_vehicle_departure_time:
                    return False

        if self.blocking_tracks is not None:
            for blocking_track_id in self.blocking_tracks:
                blocking_track = find_track(tracks, blocking_track_id)

                if blocking_track.vehicle_count() == 0:
                    continue

                last_vehicle_departure_time = blocking_track.vehicles[-1].departure_time
                if vehicle.departure_time < last_vehicle_departure_time:
                    return False

        # If all passes
        return True

    def add_vehicle(self, vehicle, tracks):
        """
        Perform checks and add vehicle to track
        :param vehicle: vehicle object
        :param tracks: tracks object
        :return: boolean
        """

        if not self.check_vehicle(vehicle, tracks):
            return False

        if self.vehicle_count() == 0:
            self.track_length_left -= vehicle.vehicle_length
        else:
            self.track_length_left -= vehicle.vehicle_length + EMPTY_SPACE

        self.vehicles_ids.append(vehicle.vehicle_id)
        self.vehicles.append(vehicle)

        vehicle.assigned_track = self
        vehicle.assigned_position = self.vehicle_count()
        if self.assigned_type is None:
            self.assigned_type = vehicle.vehicle_type

        return True

    def remove_last(self):
        vehicle = self.vehicles[-1]

        self.vehicles_ids = self.vehicles_ids[:-1]
        self.vehicles = self.vehicles[:-1]

        vehicle.assigned_track = None
        vehicle.assigned_position = None

        if self.vehicle_count() == 0:
            self.track_length_left += vehicle.vehicle_length
        else:
            self.track_length_left += vehicle.vehicle_length + EMPTY_SPACE

        if self.vehicle_count() == 0:
            self.assigned_type = None

    def vehicle_count(self):
        """
        Gets vehicle count in track
        :return: vehicle count in track
        """

        return len(self.vehicles)

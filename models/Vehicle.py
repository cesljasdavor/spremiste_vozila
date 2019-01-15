class Vehicle:

    def __init__(
            self,
            vehicle_id=None,
            vehicle_length=None,
            vehicle_type=None,
            departure_time=None,
            schedule_type=None,
            allowed_tracks_count=None,
            allowed_tracks=[]
    ):
        self.vehicle_id = vehicle_id
        self.vehicle_length = vehicle_length
        self.vehicle_type = vehicle_type
        self.departure_time = departure_time
        self.schedule_type = schedule_type
        self.allowed_tracks = allowed_tracks
        self.allowed_tracks_count = allowed_tracks_count

        self.assigned_track = None
        self.assigned_position = None

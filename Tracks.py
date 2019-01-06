class Tracks:

    def __init__(self):
        self.tracks_count = 0
        self.tracks_list = []

    def add(self, track):
        self.tracks_count += 1
        self.tracks_list.append(track)

    def __str__(self):
        out = ""
        for track in self.tracks_list:
            out += str(track) + "\n\n"
        return out

    def getTrackById(self, tid):
        for track in self.tracks_list:
            if track.track_id == tid:
                return track

def find_track(tracks, track_id):
    """
    Finds track object by track id in list of tracks
    :param tracks: list of tracks
    :param track_id: track id
    :return:
    """

    for track in tracks:
        if track.track_id == track_id:
            return track

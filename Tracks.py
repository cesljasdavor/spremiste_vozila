

class Tracks:

	def __init__(self, tracks_count=0, tracks_list=[]):
		self.tracks_count = tracks_count
		self.tracks_list = tracks_list

	def add(self, track):
		self.tracks_count += 1
		self.tracks_list.append(track)

	def __str__(self):
		out = ""
		for track in self.tracks_list:
			out += str(track) + "\n\n"
		return out
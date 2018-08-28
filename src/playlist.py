class Playlist:

  def __init__(self, query, name=None):
    self.query = query
    if not name:
      self.name = query
    else:
      self.name = name
    self.tracks = []

  def add_track(self, track):
    return self.tracks.append(track)
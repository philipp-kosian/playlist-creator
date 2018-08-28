import os
from mutagen.id3 import ID3
from .parser import Parser


class PlaylistFiller:


  def __init__(self, config, playlists, tracks):
    self.config = config
    self.playlists = playlists
    self.tracks = tracks
    self.parser = Parser(config)


  # scan library and process every track with a function
  def run(self):
    if len(self.playlists) > 0:
      self.add_tracks_to_playlists()
    else:
      return


  # process a track from the library and decide which playlists it is added to
  def add_tracks_to_playlists(self):
    tr_amount = len(self.tracks)
    tr_count = 0
    pl_amount = len(self.playlists)

    for track in self.tracks:
      pl_count = 0
      for playlist in self.playlists:
        print(" Matching tracks to playlists... Track: {0}".format(tr_count) + "/" + str(tr_amount) + " Playlist: {0}".format(pl_count) + "/" + str(pl_amount), end="\r")
        if self.parser.parse(playlist.query, track):
          playlist.add_track(track)
        pl_count += 1
      tr_count += 1

    print(" Finished matching tracks to playlists. Track: " + str(tr_amount) + "/" + str(tr_amount) + " Playlist: " + str(pl_amount) + "/" + str(pl_amount))

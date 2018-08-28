from .playlist import Playlist
from .playlist_filler import PlaylistFiller
from .file_creator import FileCreator
from .parser import Parser
from .tag import Tag
from .track import Track
import os


class Main:

  def __init__(self, config, queries):
    print("Initializing...")

    self.config = config
    self.queries = queries
    self.tracks = []
    self.playlists = []
    self.errors = []


  def run(self):
    print("Running...")

    self.create_playlists()

    if self.check_errors():
      self.report_errors()
    else:
      self.scan_tracks()
      self.playlistFiller = PlaylistFiller(self.config, self.playlists, self.tracks)
      self.playlistFiller.run()
      self.fileCreator = FileCreator(self.config, self.playlists)
      self.fileCreator.run()
      print("Finished.")


  def scan_tracks(self):

    # iterate tracks in lib
    filenames = os.listdir(self.config['lib_path'])
    tr_amount = len(filenames)
    tr_count = 0

    for filename in filenames:
      print(" Scanning library... {0}".format(tr_count) + "/" + str(tr_amount), end="\r")
      if filename.endswith(self.config['filetype']):
        # create track and add it to track list
        self.tracks.append(Track(self.config, filename))
      tr_count += 1
    print(" Library scan complete: " + str(tr_amount) + "/" + str(tr_amount))


  def create_playlists(self):

    parser = Parser(self.config)

    pl_amount = len(self.queries)
    pl_counter = 0
    for query in self.queries:
      query_string = None
      query_name = None

      if len(query) == 1:
        query_name = query[0]
        query_string = query[0]
      if len(query) == 2:
        query_name = query[0]
        query_string = query[1]
      else:
        print("Following query seems to be configured incorrectly: " + str(query))
      
      if parser.check_query_validity(query_string):
        self.playlists.append(Playlist(query_string, query_name))
        print(" Initializing playlists and checking for validity: {0}".format(pl_counter) + "/" + str(pl_amount), end="\r")
      else:
        self.errors.append("  Following query is not valid: " + str(query))
    
    print(" Finished initializing playlists and checking for validity: " + str(pl_amount) + "/" + str(pl_amount))


  def check_errors(self):
    if self.errors:
      return True
    elif len(self.playlists) <= 1:
      return True


  def report_errors(self):
    if self.errors:
      print("\n!There have been errors: ")
      for error in self.errors:
        print(" "+error)
      print("\n")
    elif len(self.playlists) <= 1:
      print("\n!No playlists found.\n")

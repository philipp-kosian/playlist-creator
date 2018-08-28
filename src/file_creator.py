import os, sys

class FileCreator:

  def __init__(self, config, playlists):
    self.config = config
    self.playlists = playlists
    self.pl_counter = 0
    self.pl_amount = len(playlists)
    if self.config['mobile']:
      self.pl_amount *= 2

  def run(self):

    print(" Initializing directories...")
    self.initialize_dirs(self.config['out_path'])
    if self.config['mobile']:
      self.initialize_dirs(self.config['out_path_mobile'])

    print(" Creating playlist files...")
    for playlist in self.playlists:
      self.create_playlist(self.config['out_path'], self.config['lib_path'], playlist)
      self.pl_counter += 1
      if self.config['mobile']:
        self.create_playlist(self.config['out_path_mobile'], self.config['lib_path_mobile'], playlist)
        self.pl_counter += 1
    print("  Playlist files created: " + str(self.pl_amount) + "/" + str(self.pl_amount))


  def create_playlist(self, out_path, lib_path, playlist):
    file = open(out_path + playlist.name + self.config['playlist_filetype'], "w", encoding="utf-8")
    for track in playlist.tracks:
      filename = track.filename
      self.write_line(file, os.path.join(lib_path, filename))


  # Writes single filepath to playlist file, adjusts filepath to library path and optionally changes slashes
  def write_line(self, file, fp):
    # filename = fp.split("/")[-1]
    # if windows_backslashes:
      # file.write(library_path.replace("/", "\\") + filename + "\n")
    try:
      file.write(fp + "\n")
    except:
      print(fp + " could not be written to file.")


  # Create output directories if they're missing and clear them if option is set
  def initialize_dirs(self, dir_path):
    if not os.path.isdir(dir_path):
      os.makedirs(dir_path)
    if self.config['clear_directories']:
      self.clear_dir(dir_path)


  # Delete all files in a directory
  def clear_dir(self, path):
    file_list = os.listdir(path)
    for file_name in file_list:
      if not os.path.isdir(path + file_name):
        os.remove(path + file_name)
    print("   Directory cleared: " + path)
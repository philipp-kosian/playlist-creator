from mutagen.id3 import ID3
from .tag import Tag
import os

class Track:

  def __init__(self, config, filename):
    self.filename = filename
    self.filepath = os.path.join(config['lib_path'], filename)

    # scan tags
    if config['filetype'] == '.mp3':
      tag = Tag(config)
      id3_handle = ID3(self.filepath)
      self.artist = tag.get_artist(id3_handle)
      self.title = tag.get_title(id3_handle)
      self.album = tag.get_album(id3_handle)
      self.genre = tag.get_genre(id3_handle)
      self.mood = tag.get_mood(id3_handle)
      self.rating = tag.get_rating(id3_handle)
    else:
      print("Filetype not yet supported.")
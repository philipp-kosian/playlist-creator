import math

class Tag:

  def __init__(self, config):
    self.config = config


  def get_artist(self, tag_handle):
    artist = None
    if self.config['filetype'] == '.mp3':
      if tag_handle.getall(self.config["mp3_artist_frame"]):
        artist = tag_handle.getall(self.config["mp3_artist_frame"])[0].text[0]
    else:
      print("Artist function not completed for this filetype yet.")
    return artist


  def get_title(self, tag_handle):
    title = None
    if self.config['filetype'] == '.mp3':
      if tag_handle.getall(self.config["mp3_title_frame"]):
        title = tag_handle.getall(self.config["mp3_title_frame"])[0].text[0]
    else:
      print("Title function not completed for this filetype yet.")
    return title


  def get_album(self, tag_handle):
    album = None
    if self.config['filetype'] == '.mp3':
      if tag_handle.getall(self.config["mp3_album_frame"]):
        album = tag_handle.getall(self.config["mp3_album_frame"])[0].text[0]
    else:
      print("Album function not completed for this filetype yet.")
    return album


  def get_genre(self, tag_handle):
    genre = None
    if self.config['filetype'] == '.mp3':
      if tag_handle.getall(self.config["mp3_genre_frame"]):
        genre = tag_handle.getall(self.config["mp3_genre_frame"])[0].text[0]
    else:
      print("Rating function not completed for this filetype yet.")
    return genre


  def get_mood(self, tag_handle):
    mood = None
    if self.config['filetype'] == ".mp3":
      # get mood string from the ID3 Frame
      if tag_handle.getall(self.config["mp3_mood_frame"]):
        mood = tag_handle.getall(self.config["mp3_mood_frame"])[0].text[0]
    else:
      print("Mood function not completed for this filetype yet.")
    return mood


  def get_rating(self, tag_handle):
    rating = None
    if self.config['filetype'] == ".mp3":
      # Has rating tag
      if tag_handle.getall(self.config['mp3_rating_frame']):
        rating_raw = tag_handle.getall(self.config['mp3_rating_frame'])[0].rating
        rating = str(self.adjust_rating_format(rating_raw))
    else:
      print("Rating function not completed for this filetype yet.")
    return rating

  # This changes the raw rating format (255) into the max 5 pattern
  def adjust_rating_format(self, rating_raw):
    if self.config['filetype'] == ".mp3" and self.config['mp3_rating_stored_255']:
      return math.ceil(rating_raw / 255 * 5)


# Tag frames and storage types are configured for mp3
# Support for additional filetypes might require changes in the actual code

# End paths with /

config = {
  'filetype':             ".mp3",
  'playlist_filetype':    ".m3u8",

  'lib_path':             u"",    # Ex: "C:/Music/"
  'lib_path_mobile':      u"",    # Ex: "file:///storage/.../Music/"

  'mobile':               True,
  'out_path':             u"",    # Ex: "C:/Playlists/"
  'out_path_mobile':      u"",    # Ex: "C:/PlaylistsMobile/"

  'length_warning':       30,
  'debug':                False,
  'clear_directories':    True,

  # artist
  'mp3_artist_frame':     'TPE1',

  # title
  'mp3_title_frame':      'TIT2',

  # album
  'mp3_album_frame':      'TALB',

  # genre
  'mp3_genre_frame':      'TCON',

  # mood
  'mp3_mood_frame':       "TXXX:MOOD",
  'limit_moods_to_list':  True,
  'mood_list':            [], # Ex: ["Chilled", "Uplifting", ...] 

  # rating
  'mp3_rating_frame':     "POPM",
  'mp3_rating_stored_255': True  # In mp3s the rating is stored as int with max 255, 1 => 1, 2 => 64, 3 => 128
}

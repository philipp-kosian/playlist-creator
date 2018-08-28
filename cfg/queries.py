# Each Playlist is an array with name and search query
#  Name can contain only characters by system as filename
#  Search queries support (in exactly this spelling):
#   Tags: title, artist, album, genre, mood and rating
#   Operators: OR, AND, (, ), IS, HAS, GREATER, LESS

# Ex: ["Favorites", "rating IS 5"],
#     ["Relaxed", "mood HAS Chilled"],
#     ["Artist1", "artist HAS Artist1"],
#     ["Party", "rating GREATER 2 AND mood HAS Uplifting"]


queries = [
  ["name",  "query"],
]

class Parser:

  operator_or = ' OR '
  operator_and = ' AND '
  operator_not = 'NOT'
  bracket_open = '('
  bracket_close = ')'

  tag_operators = {
    ' IS ': 'is',
    ' HAS ': 'has',
    ' GREATER ': 'greater',
    ' LESS ': 'less'
  }


  def __init__(self, config):
    self.config = config
    self.tag_operator_functions = {
      'is':       self.is_compare,
      'has':      self.has_compare,
      'greater':  self.greater_compare,
      'less':     self.less_compare,
    }


  # TODO: add other tests
  def check_query_validity(self, query):
    if Parser.bracket_sum_zero(query):
      if self.config["limit_moods_to_list"]:
        # if self.check_moods(query)
        return True
      else:
        return True


  # recursively parses a query to see if it matches a track's tags
  def parse(self, query, track):

    if query and track:

      # remove any outer brackets because they are irrelevant
      # also remove any leading or trailing whitespace
      query = Parser.remove_outer_brackets(query).strip()

      # check for 'not (...)', parse rest of query and return inverted result
      if query[0:len(Parser.operator_not)] == Parser.operator_not:
        query_not = query[len(Parser.operator_not):].strip()
        if query_not:
          return not self.parse(query_not, track)


      # get 'or' subqueries
      subqueries = Parser.split_query_outer_layer_with_key(query, Parser.operator_or)

      # parse subqueries if available, combine with 'or' and return result
      if len(subqueries) >= 2:
        subquery_results = []
        for subquery in subqueries:
          subquery_results.append(self.parse(subquery, track))
        # combine subqueries as 'or'
        return any(res is True for res in subquery_results)

      # get 'and' subqueries
      else:

        subqueries = Parser.split_query_outer_layer_with_key(query, Parser.operator_and)

        # parse subqueries if available, combine with 'and' and return result
        if len(subqueries) >= 2:
          subquery_results = []
          for subquery in subqueries:
            subquery_results.append(self.parse(subquery, track))
          # print(subqueries, subquery_results)
          # combine subqueries as 'and'
          return all(res is True for res in subquery_results)

        # process query element
        else:
          return self.parse_query_element(query, track)


  # processes a query element, decides if track (id3_handle) matches the query
  def parse_query_element(self, el, track):
    result = False

    if el:

      op = None
      op_pos = None

      # find operator and check that there's only one operator
      for op_val in Parser.tag_operators:

        if op_pos is None:
          op_pos = el.find(op_val)

          # if not found, reset op_pos to None to make ifs simpler
          if op_pos == -1:
            op_pos = None

          # >= 0 means op_val was found,
          elif op_pos >= 0:

            # check that an operator wasn't already found and set op to op_val
            if op is not None:
              return False
            else:
              # set op to found op_val
              op = op_val


      # call corresponding tag compare function from dict
      if op:
        tag = el[0:op_pos]
        arg = el[op_pos+len(op):]

        # get the string of the tag that's going to be compared
        tag_val = None
        if tag == "artist":
          tag_val = track.artist
        elif tag == "title":
          tag_val = track.title
        elif tag == "album":
          tag_val = track.album
        elif tag == "genre":
          tag_val = track.genre
        elif tag == "mood":
          tag_val = track.mood
        elif tag == "rating":
          tag_val = track.rating
        else:
          print("Tag identifier not recognized: " + tag)

        # compare tag_val and arg with the compare-function corresponding to the operator
        result = self.tag_operator_functions[Parser.tag_operators[op]](tag_val, arg)

    # print(result)
    return result


  # Splits a query into subqueries on outer layer with a keyword
  @staticmethod
  def split_query_outer_layer_with_key(query, key):
    subqueries = []

    outer_layer_parts = Parser.get_outer_layer_parts(query)

    subquery_start = 0

    # search outer layer parts for key, split original query into the parts with indices
    for outer_layer_part_start, outer_layer_part in outer_layer_parts.items():

      search_index = 0

      # find all occurences of the key in this part and save subqueries
      while len(outer_layer_part)-1 > search_index:
        key_pos = outer_layer_part.find(key, search_index)

        # if key was found, calculate position of subquery in original query (from key position in an outer layer part) and save it
        if key_pos > -1:
          subquery_end = key_pos + outer_layer_part_start
          subqueries.append(query[subquery_start:subquery_end])
          subquery_start = subquery_end + len(key)
        else:
          break

        search_index += len(outer_layer_part)

    # add last subquery after last key
    subqueries.append(query[subquery_start:])

    return subqueries


  # Returns array of all query parts on the outer layer
  @staticmethod
  def get_outer_layer_parts(query):

    outer_layer_parts = {}
    layer = 0
    last_layer = -1
    outer_layer_part_start = 0

    # parse query char for char and collect outer layer parts
    for i, c in enumerate(query):

      # count layer up
      if c == Parser.bracket_open:
        layer += 1

      # mark start of outer layer and save index
      if layer == 0 and last_layer != 0:
        outer_layer_part_start = i

      # mark end of outer layer and save section with index of original start position
      if layer != 0 and last_layer == 0:
        outer_layer_parts[outer_layer_part_start] = query[outer_layer_part_start:i]
      if last_layer == 0 and i == len(query)-1:
        outer_layer_parts[outer_layer_part_start] = query[outer_layer_part_start:i+1]

      last_layer = layer

      # count layer down
      if c == Parser.bracket_close:
        layer -= 1

    return outer_layer_parts


  # Checks that amount of opening and closing brackets is the same
  @staticmethod
  def bracket_sum_zero(query):
    bracket_sum = 0
    for i, c in enumerate(query):
      if c == Parser.bracket_open:
        bracket_sum += 1
      if c == Parser.bracket_close:
        bracket_sum -= 1
      if bracket_sum == 0 and i == len(query)-1 and i != 0:
        return True
      elif i == len(query)-1 and i != 0:
        return False


  # Check that all moods in a query correspond to moods in defined list in config
  #   to prevent unnoticed spelling mistakes
  # TODO: Add support for multiple brackets
  def check_moods(self, query):

    mood_tag = "mood "
    space = " "

    i = 0
    while i < (len(query) - len(mood_tag)):
      # find if mood is somewhere in query
      i = query.find(mood_tag, i)

      if i > -1:
        # find next spaces
        start = query.find(space, i+len(mood_tag)) + 1
        end = query.find(space, start) # can be -1 if end of line
        
        if query[end-1] == ")":
          end = end-1

        mood_q = query[start:end]
        # if mood is last word (without bracket or anything)
        if end == -1 and query[-1:] != ")":
          mood_q = query[start:]

        i += len(mood_tag)

        if mood_q in self.config["mood_list"]:
          continue
        else:
          print("   Error in query! The mood "+ mood_q + " is not configured in config. (" + str(query) + ")")
          return False
      else:
        return True


  # Remove any outer brackets of a string
  @staticmethod
  def remove_outer_brackets(string):
    if string[0] is Parser.bracket_open and string[-1] is Parser.bracket_close:
      # could still be "(())(())"
      # count for each bracket: "(" => +1, ")" => -1, if 0 check position
      bracket_count = 1
      for i, c in enumerate(string[1:]):
        if c is Parser.bracket_open:
          bracket_count += 1
        if c is Parser.bracket_close:
          bracket_count -= 1
        if bracket_count is 0:
          if i is len(string)-2:
            # string has outer brackets, remove them and return
            string = string[1:-1]
    # return original or modified string
    return string


  # compares is-statement for a tag and an argument
  def is_compare(self, arg1, arg2):
    return arg1 == arg2

  # compares has-statement for a tag and an argument
  def has_compare(self, arg1, arg2):
    return arg2 in arg1

  # compares greater-statement for a tag and an argument
  def greater_compare(self, arg1, arg2):
    return arg1 > arg2

  # compares less-statement for a tag and an argument
  def less_compare(self, arg1, arg2):
    return arg1 < arg2

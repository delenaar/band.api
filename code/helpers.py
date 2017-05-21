from sqlalchemy.orm import class_mapper


def json(self):
  """Transforms a model into a dictionary which can be dumped to JSON."""
  # first we get the names of all the columns on your model
  columns = [c.key for c in class_mapper(self.__class__).columns]
  # then we return their values in a dict
  return dict((c, getattr(self, c)) for c in columns)

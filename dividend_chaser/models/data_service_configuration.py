class DataServiceConfiguration:
  # pylint: disable=R0903,W0102
  def __init__(self, params={}):
    self.params = params

  def is_skip_average_volume(self) -> bool:
    return self.params.get("skip_average_volume") or False

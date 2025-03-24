from ..terms import GoodTypes

class Good:
    def __init__(self, good_type):
        self._good_type = good_type

    @property
    def good_type(self):
        return self._good_type

    def as_string(self):
      return f"Good({self.good_type})"

    def __repr__(self):
        return self.good_type.value
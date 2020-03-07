import json
from solution import Solution


class SolEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, Solution):
            return o.__dict__
        else:
            super().default()

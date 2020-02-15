from utils.check_functions import check_values
from copy import deepcopy
from math import inf


class Normalize:
    def _check_values(self):
        check_values(self._data)

    def _find_values(self):
        for element in self._data["list"]:
            for i in element[1:len(element) - 1]:
                if i < self._min:
                    self._min = i

                if i > self._max:
                    self._max = i

        self._delta = self._max - self._min

    def _execute(self):
        for element in self._data["list"]:
            aux = deepcopy(element)

            for i in range(1, len(aux) - 1):
                aux[i] = (aux[i] - self._min) / self._delta

            self._normalized_data["list"].append(aux)

    def __init__(self, data):
        self._data = data
        self._check_values()

        self._normalized_data = {
            "identifiers": data["identifiers"],
            "list": []
        }
        self._min = inf
        self._max = -inf
        self._delta = None
        self._find_values()

        self._execute()

    def get_data(self):
        return deepcopy(self._normalized_data)

import csv
from copy import deepcopy

from utils.check_functions import check_type


class ReadData:
    def _check_values(self):
        check_type(self._path, str, "O campo path deve ser uma string que contem o caminho para o csv com os dados.")

    def _execute(self):
        with open(self._path) as file:
            reader = csv.reader(file, delimiter=",")

            for line in reader:
                aux = list(line)
                self._data["list"].append(aux)

            self._data["identifiers"] = self._data["list"][0]
            del self._data["list"][0]

            for line in self._data["list"]:
                line[0] = int(line[0])
                for i in range(1, len(line) - 1):
                    line[i] = float(line[i])

                if line[len(line) - 1] not in self._classifications:
                    self._classifications.append(line[len(line) - 1])

    def __init__(self, path):
        self._path = path
        self._check_values()
        self._classifications = []
        self._data = {
            "identifiers": None,
            "list": []
        }

        self._execute()

    def get_data(self):
        return deepcopy(self._data)

    def get_classifications(self):
        return deepcopy(self._classifications)

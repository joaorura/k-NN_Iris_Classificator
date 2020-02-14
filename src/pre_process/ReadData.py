import csv
from copy import deepcopy

from utils.check_functions import check_type


class ReadData:
    def _check_values(self):
        check_type(self._path, str, "O campo path deve ser uma string que contem o caminho para o csv com os dados.")
        check_type(self._amount, int, "O campo amount deve ser um inteiro.")

        if self._amount < -1 or self._amount == 0:
            raise RuntimeError("O campo amount deve ter valores maiores que 0.")

    def _execute(self):
        with open(self._path) as file:
            reader = csv.reader(file, delimiter=",")

            for line in reader:
                aux = list(line)
                self._data["list"].append(aux)

            self._data["identifiers"] = self._data["list"][0]
            del self._data["list"][0]

            aux = len(self._data["list"][0])
            if self._amount == -1:
                size = aux - 1
            else:
                size = self._amount
                if size > aux - 1:
                    raise RuntimeError(f"O valor do campo amount é muito grande, o mesmo deve ser menor que: "
                                       f"{aux}")

            for line in self._data["list"]:
                for i in range(0, size):
                    line[i] = float(line[i])

                i += 1
                if line[len(line) - 1] not in self._classifications:
                    self._classifications.append(line[len(line) - 1])

                while True:
                    if i >= len(line) - 1:
                        break
                    del line[i]

    def __init__(self, path, amount_metrics=-1):
        self._amount = amount_metrics
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

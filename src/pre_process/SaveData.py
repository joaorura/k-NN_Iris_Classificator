from utils.check_functions import check_values, check_type
from csv import writer


class SaveData:
    def _check_values(self):
        check_values(self._data)
        check_type(self._path, str, "O caminho precisa ser uma string.")

    def __init__(self, data, path):
        self._data = data
        self._path = path
        self._check_values()

    def execute(self):
        with open(self._path, 'w', newline='') as file:
            aux = writer(file)
            aux.writerow(self._data['identifiers'])

            for elements in self._data['list']:
                aux.writerow(elements)

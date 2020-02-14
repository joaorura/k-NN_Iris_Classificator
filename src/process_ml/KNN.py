from utils.check_functions import check_values, check_type
from math import inf


class KNN:
    def _check_values(self):
        check_values(self._data)

        if self._k < 1:
            raise RuntimeError("K deve ser maior que 1.")

        check_type(self._k, int, "K deve ser um inteiro.")
        check_type(self._classifications, list, "As classificacoes devem ser uma lista")

    def _zero_count_process(self):
        for i in self._classifications:
            self._count_process[i] = [0, None]

    def __init__(self, data, classifications, k=1):
        self._data = data
        self._k = k
        self._classifications = classifications
        self._check_values()

        self._count_process = {}
        self._zero_count_process()

        self._space_size = len(self._data["list"][0])

    def _check_consult_args(self, instance):
        check_type(instance, list, "A instancia deve ser uma lista")

        if len(instance) < self._space_size:
            raise RuntimeError(f"A instancia deve ter tamanho: {self._space_size}")

        check_type(instance[len(instance) - 1], str, "O ultimo elemento da lista deve ser uma string.")

        if instance[len(instance) - 1] not in self._classifications:
            raise RuntimeError(f"O ultimo elemento da lista deve possuir uma das classes.\n"
                               f"\tClasses: {self._classifications}")

        for i in instance[:len(instance) - 1]:
            if type(i) != float:
                raise RuntimeError(f"Os {self._space_size - 1} primeiros devem ser floats.")

    def consult(self, instance):
        self._check_consult_args(instance)

        results = []
        for element in self._data["list"]:
            aux = 0
            for i in range(0, self._space_size - 1):
                aux += (instance[i] - element[i]) ** 2

            aux_result = (aux, element)
            results.append(aux_result)

        results.sort()

        for i in range(0, self._k):
            classification = results[i][1][self._space_size - 1]
            self._count_process[classification][0] += 1
            self._count_process[classification][1] = results[i][1][:len(results[i][1]) - 1]
        aux = [-inf, None, None]

        for i in self._count_process:
            if aux[0] < self._count_process[i][0]:
                aux[0] = self._count_process[i][0]
                aux[1] = self._count_process[i][1]
                aux[2] = i

        self._zero_count_process()

        return tuple(aux)

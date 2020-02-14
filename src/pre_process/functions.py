from copy import deepcopy
from random import randint

from utils.check_functions import check_type


def reserve_data(percent, data):
    check_type(percent, float, "O campo percent deve ser float.")
    check_type(data, dict, "O campo data deve ser um dict.")

    if percent > 1 or percent < 0:
        raise RuntimeError("O valor percente deve está entre 0 e 1")

    if percent == 1:
        result = deepcopy(data)
        del data
        return result

    size = int(len(data["list"]) * percent)
    new_data = {
        "identifiers": data['identifiers'],
        "list": []
    }

    for i in range(0, size):
        aux = randint(0, len(data["list"]) - 1)
        new_tuple = deepcopy(data["list"][aux])
        del data["list"][aux]
        new_data['list'].append(new_tuple)

    return new_data

def check_type(value, the_type, message):
    if type(value) != the_type:
        raise RuntimeError(f"Error in type o variable!\n\t{message}")


def check_values(data):
    try:
        aux = data["identifiers"]
        check_type(aux, list, "O dicionário deve ter uma tupla, com identificador: 'identifiers'.")

        aux = data["list"]
        check_type(aux, list, "O dicionário deve ter uma lista, com identificador: 'list'.")
    except KeyError:
        raise RuntimeError("Problemas com o formato dos dados.")

from sys import argv
from pre_process.ReadData import ReadData
from pre_process.functions import reserve_data
from process_ml.KNN import KNN


def get_path():
    if len(argv) > 2 or len(argv) == 1:
        raise RuntimeError("Só é necessário como argumento o enedereco absoluto do arquivo.")
    if ".csv" not in argv[1]:
        raise RuntimeError("O argumento precisa ser um arquivo .csv.")

    return argv[1]


def main():
    path = get_path()
    read_data = ReadData(path)
    data = read_data.get_data()
    classifications = read_data.get_classifications()
    reserved_data = reserve_data(0.1, data)
    knn = KNN(data, classifications)

    for i in reserved_data['list']:
        aux = knn.consult(i)
        print(f"Element: {i[:len(i) - 1]} | Real: {i[len(i) - 1]}\n"
              f"\t Previsto: {aux[2]}\n  | Value: {aux[1]}\n\n")


if __name__ == "__main__":
    main()

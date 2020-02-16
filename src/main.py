from sys import argv

from pre_process.Normalize import Normalize
from pre_process.ReadData import ReadData
from pre_process.SaveData import SaveData
from pre_process.functions import reserve_data
from process_ml.KNN import KNN


def get_path():
    if len(argv) > 2 or len(argv) == 1:
        raise RuntimeError("Só é necessário como argumento o enedereco absoluto do arquivo.")
    if ".csv" not in argv[1]:
        raise RuntimeError("O argumento precisa ser um arquivo .csv.")

    return argv[1]


def get_data():
    path = get_path()
    read_data = ReadData(path)
    data = read_data.get_data()
    classifications = read_data.get_classifications()

    return read_data, data, classifications


def save_data(data, path):
    saved_data = SaveData(data, path)
    saved_data.execute()


def normalize_data(path):
    data_info = get_data()
    normalized_data = Normalize(data_info[1])
    normalized_data = normalized_data.get_data()
    save_data(normalized_data, path)


def mount_confusion_matrix(classification):
    matrix = []
    for i in range(0, len(classification)):
        line = []

        for j in range(0, len(classification)):
            line.append(0)

        matrix.append(line)

    return matrix


def process_confusion_matrix(matrix, size_classification):
    processed = []
    for i in range(0, size_classification):
        line = []

        for j in range(0, 4):
            line.append(0)

        processed.append(line)

    for i in range(0, size_classification):
        for j in range(0, size_classification):
            for k in range(0, size_classification):
                if j == i:
                    if k == i:
                        processed[i][0] += matrix[j][k]
                    else:
                        processed[i][3] += matrix[j][k]
                else:
                    if k == i:
                        processed[i][2] += matrix[j][k]
                    else:
                        processed[i][1] += matrix[j][k]

    return processed


def process_precision_recall(matrix, size):
    processed_precision = []
    processed_recall = []

    for i in range(0, size):
        try:
            precision = matrix[i][0] / (matrix[i][0] + matrix[i][2])
        except ZeroDivisionError:
            precision = 0.0

        try:
            recall = matrix[i][0] / (matrix[i][0] + matrix[i][3])
        except ZeroDivisionError:
            recall = 0.0

        processed_precision.append(precision)
        processed_recall.append(recall)

    return processed_recall, processed_precision


def print_matrix_confusion(confusion_matrix, classification):
    print('\n\n')
    aux_str = ''
    for i in range(0, len(classification[0])):
        aux_str += ' '

    print(aux_str, end="")

    for aux in classification:
        print(f"| {aux}", end="")

    print()

    j = 0
    for aux in classification:
        print(aux, end="")

        for element in confusion_matrix[j]:
            print(f" |   {element}", end="")

        j += 1
        print("|")


def print_process_data(processed_data, classification):
    print('\n\n')
    print("              |  TP  |  TN  |  FP  |  FN  |")

    for i in range(0, len(classification)):
        print(f' {classification[i]}    ', end="")

        for j in processed_data[i]:
            print(f"|  {j}  ", end="")

        print(" | ")


def print_precision_recall(precision_classes, recall_classes, classification):
    print('\n\n')
    print("       |  Precision  |  Recall  |")

    for i in range(0, len(classification)):
        print(f'{classification[i]} |   {precision_classes[i]}   |   {recall_classes[i]}  ', end="|\n")


def training():
    data_info = get_data()[0]
    classification = data_info.get_classifications()
    times = 50
    partition = 1 / times

    confusion_matrix = mount_confusion_matrix(classification)
    accuracy_rate = error_rate = 0

    for k in range(0, times):
        data = data_info.get_data()
        hit_count = 0
        reserved_data = reserve_data(partition, data)
        knn = KNN(data, classification, 7)

        # print(f"Avaliacão numéro: {k}")
        for i in reserved_data['list']:
            aux = knn.consult(i)
            real = classification.index(i[len(i) - 1])
            preview = classification.index(aux[2])

            confusion_matrix[real][preview] += 1
            if i[len(i) - 1] == aux[2]:
                hit_count += 1

            # print(f"\tElement: {i[:len(i) - 1]} | Real: {i[len(i) - 1]}\n"
            #       f"\t Previsto: {aux[2]}  | Value: {aux[1]}\n\n")

        accuracy_rate_moment = hit_count / len(reserved_data['list'])
        accuracy_rate += accuracy_rate_moment
        error_rate += 1 - accuracy_rate_moment

    accuracy_rate /= times
    error_rate /= times

    processed_data = process_confusion_matrix(confusion_matrix, len(classification))
    precision_classes = process_precision_recall(processed_data, len(classification))
    recall_classes = precision_classes[0]
    precision_classes = precision_classes[1]

    print(f"Accuracy: {accuracy_rate}\n"
          f"Error: {error_rate}\n")

    print_matrix_confusion(confusion_matrix, classification)
    print_process_data(processed_data, classification)
    print_precision_recall(precision_classes, recall_classes, classification)


if __name__ == "__main__":
    # normalize_data("C:\\Users\\jmess\\Workspace\\Python\\k-NN_Iris_Classificator\\data\\Iris_Normalized.csv")
    training()

import glob
import os.path
import string
import time

DATA_FOLDER = "PRE_02_mapreduce/data"
INPUT_FOLDER = "PRE_02_mapreduce/temp/input"
OUTPUT_FOLDER = "PRE_02_mapreduce/temp/output"

#
# Esta es la abstracción de la función hadoop que simula el comportamiento de un job de Hadoop.
#  
def hadoop(
    input_folder,
    output_folder,
    mapper_fn,
    reducer_fn,
):

    def read_records_from_input(folder):
        sequence = []
        files = glob.glob(f"{folder}/*")
        for file in files:
            with open(file, "r", encoding="utf-8") as f:
                for line in f:
                    sequence.append((file, line))
        return sequence

    def save_results_to_output(folder, result):
        with open(f"{folder}/part-00000", "w", encoding="utf-8") as f:
            for key, value in result:
                f.write(f"{key}\t{value}\n")

    def create_success_file(folder):
        with open(f"{folder}/_SUCCESS", "w", encoding="utf-8") as f:
            f.write("")

    def check_folder_exists(folder):
        if os.path.exists(folder):
            raise FileExistsError("La carpeta ya existe")

    check_folder_exists(output_folder)
    os.mkdir(output_folder)

    sequence = read_records_from_input(folder=input_folder)
    sequence = mapper_fn(sequence)
    sequence = sorted(sequence)
    sequence = reducer_fn(sequence)
    save_results_to_output(output_folder, sequence)
    create_success_file(output_folder)

    

#
# Este es el código especifico del experimento
#

def clear_folder(folder):
    if os.path.exists(folder):
        for file in glob.glob(f"{folder}/*"):
            os.remove(file)


def create_folder(input_folder):
    os.makedirs(input_folder)


def initialize_folder(input_folder):
    if os.path.exists(input_folder):
        clear_folder(input_folder)
    else:
        create_folder(input_folder)


def generate_file_copies(data_folder, input_folder, n):

    
    for file in glob.glob(f"{data_folder}/*"):
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()

        for i in range(1, n + 1):
            raw_filename_with_extension = os.path.basename(file)

            raw_filename_without_extension = os.path.splitext(raw_filename_with_extension)[
            0
        ]

            new_filename = f"{raw_filename_without_extension}_{i:05d}.txt"

            with open(f"{input_folder}/{new_filename}", "w", encoding="utf-8") as f2:
                f2.write(text)


def mapper(sequence):
    pairs_sequence = []
    for _, line in sequence:
        line = line.lower()
        line = line.translate(str.maketrans("", "", string.punctuation))
        line = line.replace("\n", "")
        words = line.split()
        pairs_sequence.extend([(word, 1) for word in words])
    return pairs_sequence


def reducer(pairs_sequence):
    result = []
    for key, value in pairs_sequence:
        if result and result[-1][0] == key:
            result[-1] = (key, result[-1][1] + value)
        else:
            result.append((key, value))
    return result

def delete_folder(folder):
    if os.path.exists(folder):
        for file in glob.glob(f"{folder}/*"):
            os.remove(file)
        os.rmdir(folder)

def main():

    n = 1000

    initialize_folder(INPUT_FOLDER)
    delete_folder(OUTPUT_FOLDER)
    generate_file_copies(DATA_FOLDER, INPUT_FOLDER, n)

    start_time = time.time()

    hadoop(
        input_folder=INPUT_FOLDER,
        output_folder=OUTPUT_FOLDER,
        mapper_fn=mapper,
        reducer_fn=reducer,
    )

    end_time = time.time()
    print(f"Tiempo de ejecución: {end_time - start_time:.2f} segundos")


if __name__ == "__main__":

    main()

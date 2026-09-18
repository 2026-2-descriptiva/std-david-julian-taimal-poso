# Importación de paquetes y declaración de constantes
# -----------------------------------------------------------------------------

import glob
import os.path
import string
import time

DATA_FOLDER = "PRE_02_mapreduce/data"
INPUT_FOLDER = "PRE_02_mapreduce/temp/input"
OUTPUT_FOLDER = "PRE_02_mapreduce/temp/output"

# Definición de funciones
# -----------------------------------------------------------------------------

def clear_folder(input_folder):
    if os.path.exists(input_folder):
        for file in glob.glob(f"{input_folder}/*"):
            os.remove(file)

def create_folder(input_folder):
    os.makedirs(input_folder)

def initialize_folder(input_folder):
    if os.path.exists(input_folder):
        clear_folder(input_folder)
    else:
        create_folder(input_folder)

def generate_file_copies(DATA_FOLDER, input_folder, n):
    for file in glob.glob(f"{DATA_FOLDER}/*"):
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

def read_records_from_input(input_folder):
    sequence = []
    files = glob.glob(f"{input_folder}/*")
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                sequence.append((file, line))
    return sequence

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

def save_results_to_output(output_folder, result):
    with open(f"{output_folder}/part-00000", "w", encoding="utf-8") as f:
        for key, value in result:
            f.write(f"{key}\t{value}\n")

def create_success_file(output_folder):
    with open(f"{output_folder}/_SUCCESS", "w", encoding="utf-8") as f:
        f.write("")

# La carpeta input/ debe existir y estar vacia.
# -----------------------------------------------------------------------------
# Genera copias de los archivos en raw
# -----------------------------------------------------------------------------
n = 1000
initialize_folder(INPUT_FOLDER)
generate_file_copies(DATA_FOLDER, INPUT_FOLDER, n)
# Lectura de los archivos
# -----------------------------------------------------------------------------
start_time = time.time()
sequence = read_records_from_input(INPUT_FOLDER)
# Mapper
# -----------------------------------------------------------------------------
pairs_sequence = mapper(sequence)
# Shuffle and sort
# -----------------------------------------------------------------------------
pairs_sequence = sorted(pairs_sequence)
# Reducer
# -----------------------------------------------------------------------------
result = reducer(pairs_sequence)
# La carpeta de salida debe estar vacia
# -----------------------------------------------------------------------------
initialize_folder(OUTPUT_FOLDER)
# Archivo con el conteo
# -----------------------------------------------------------------------------
save_results_to_output(OUTPUT_FOLDER, result)
# Marcador de éxito
# -----------------------------------------------------------------------------
create_success_file(OUTPUT_FOLDER)
# Reporte de tiempo de ejecución
# -----------------------------------------------------------------------------
end_time = time.time()
print(f"Tiempo de ejecución: {end_time - start_time:.2f} segundos")

import csv
import json

from nicegui import ui


def convert_csv_2_json(input_file):

    output_file = input_file.replace(".csv", ".json")
    output_file = output_file.replace("/data/", "/temp/")

    data = []

    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    ui.notify("The file was transformed successfully!")


def app():
    """Main function to run the app"""

    ui.label("CSV to JSON Converter").classes("text-4xl font-bold")
    ui.label("")

    filename = ui.input(
        label="CSV file to convert:",
        placeholder="filename",
    )

    ui.label("")

    ui.label("")
    ui.button("Convert", on_click=lambda: convert_csv_2_json(filename.value))
    ui.run(port=8081)


if __name__ in {"__main__", "__mp_main__"}:
    app()



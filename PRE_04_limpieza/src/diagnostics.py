import pandas as pd

OUTPUT_FILE = "PRE_04_limpieza/submission/ventas.csv"


def main():
    df = pd.read_csv(OUTPUT_FILE)

    series = df["amount"]

    # series = series.astype(str)
    # series = series[series.str.startswith("$")]

    series = series.sort_values()
    series = series.drop_duplicates()

    print(series)
    print(len(series))


if __name__ == "__main__":
    main()
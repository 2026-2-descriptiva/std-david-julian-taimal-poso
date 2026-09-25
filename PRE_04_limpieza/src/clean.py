import os

import pandas as pd

INPUT_FILE = "PRE_04_limpieza/data/ventas.csv"
OUTPUT_FILE = "PRE_04_limpieza/submission/ventas.csv"


SUPPLIER_REPLACEMENTS = {
    "Amazon Web Services Colombia": [
        "amazon web services colombia",
    ],
    "Bancolombia S.A.": [
        "BANCOLOMBIA S.A.",
    ],
    "Cementos Argos S.A.": [
        "Cementos Argos SA",
        "cementos argos s.a.",
    ],
    "Corona S.A.S.": [
        "Corona SAS",
    ],
    "Google Colombia Ltda.": [
        "GOOGLE COLOMBIA LTDA.",
    ],
    "IBM Colombia S.A.S.": [
        "IBM Colombia SAS.",
        "ibm colombia s.a.s.",
    ],
    "Microsoft Colombia Inc.": [
        "MICROSOFT COLOMBIA INC.",
    ],
    "Nutresa S.A.": [
        "Nutresa SA",
        "nutresa s.a.",
    ],
    "Oracle Colombia Ltda.": [
        "oracle colombia ltda.",
    ],
    "Postobón S.A.": [
        "POSTOBÓN S.A.",
        "Postobon S.A.",
    ],
    "SAP Colombia S.A.S.": [
        "SAP Colombia SAS",
    ],
    "Siemens S.A.S.": [
        "SIEMENS S.A.S.",
        "siemens s.a.s.",
    ],
}

COUNTRY_REPLACEMENTS = {
    "COL": [
        "Colombia",
        "CO",
        "COL",
        "COLOMBIA",
        "Colombia",
        "colombia",
    ]
}

CITY_REPLACEMENTS = {
    "Bogotá": [
        "BOGOTÁ",
        "bogotá",
    ],
    "Medellín": [
        "MEDELLÍN",
        "Medellin",
        "medellín",
    ],
}


PURCHASE_DATE_REPLACEMENTS = {
    r"^(\d{2})-(\d{2})-(\d{2})$": r"\1-\2-20\3",
}


def clean_column_names(series):
    series = strip_whitespace(series)
    series = to_lowercase(series)
    series = replace_space_with_underscore(series)
    return series


def strip_whitespace(series):
    return series.str.strip()


def normalize_whitespace(series):
    return series.str.replace(r"\s+", " ", regex=True)


def to_lowercase(series):
    return series.str.lower()


def replace_space_with_underscore(series):
    return series.str.replace(" ", "_")


def replace_date_separators(series):
    return series.str.replace(".", "-", regex=False).str.replace("/", "-", regex=False)


def make_date_replacements(series, replacements):
    for pattern, replacement in replacements.items():
        series = series.str.replace(pattern, replacement, regex=True)
    return series


def dd_mm_yyyy_2_yyyy_mm_dd(series):
    return series.str.replace(r"^(\d{2})-(\d{2})-(\d{4})$", r"\3-\2-\1", regex=True)


def yyyy_dd_mm_2_yyyy_mm_dd(series):
    def fn(text):
        if pd.isna(text):
            return text
        parts = text.split("-")
        year, p1, p2 = parts
        if int(p1) > 12:
            day, month = p1, p2
        else:
            day, month = p2, p1

        return f"{year}-{month}-{day}"

    return series.apply(fn)


def clean_supplier(series):
    series = strip_whitespace(series)
    series = normalize_whitespace(series)
    series = make_replacements(series, SUPPLIER_REPLACEMENTS)
    return series


def clean_country(series):
    series = strip_whitespace(series)
    series = normalize_whitespace(series)
    series = make_replacements(series, COUNTRY_REPLACEMENTS)
    return series


def clean_city(series):
    series = strip_whitespace(series)
    series = normalize_whitespace(series)
    series = make_replacements(series, CITY_REPLACEMENTS)
    return series


def clean_purchase_date_format(series):
    series = strip_whitespace(series)
    series = normalize_whitespace(series)
    series = make_date_replacements(series, PURCHASE_DATE_REPLACEMENTS)
    series = replace_date_separators(series)
    series = dd_mm_yyyy_2_yyyy_mm_dd(series)
    series = yyyy_dd_mm_2_yyyy_mm_dd(series)

    return series


def clean_amount(series):
    series = strip_whitespace(series)
    series = series.str.replace("COP ", "", regex=False)
    series = series.str.replace(r"\.00K$", "000", regex=True)
    series = series.str.replace("$", "", regex=False)
    series = series.str.replace(",", "", regex=False)
    series = series.str.replace(".", "", regex=False)
    return series


def clean_discount(series):
    series = strip_whitespace(series)
    series = series.str.replace("%", "", regex=False)
    series = series.apply(lambda x: float(x) / 100 if float(x) > 1 else float(x))
    return series


def clean_weight(series):

    def convert_weight(value):
        if pd.isna(value):
            return value
        value = value.lower().strip()
        if value.endswith(" kg"):
            return float(value.replace("kg", "").strip())
        elif value.endswith(" g"):
            return float(value.replace("g", "").strip()) / 1000
        elif value.endswith(" ton"):
            return float(value.replace("ton", "").strip()) * 1000

        else:
            return float(value)

    series = strip_whitespace(series)
    series = series.str.replace(",", ".", regex=False)
    series = series.apply(convert_weight)
    return series


def clean_unit_price(series):
    series = strip_whitespace(series)
    series = series.str.replace("$", "", regex=False)
    series = series.str.replace(r"\.00$", "", regex=True)
    series = series.str.replace(",", "", regex=False)
    series = series.str.replace(".", "", regex=False)
    return series


def make_replacements(series, replacements):
    for replacement, values in replacements.items():
        for value in values:
            series = series.replace(value, replacement)
    return series


def main():

    df = pd.read_csv(INPUT_FILE)

    df.columns = clean_column_names(df.columns)

    df["supplier"] = clean_supplier(df["supplier"])
    df["country"] = clean_country(df["country"])
    df["city"] = clean_city(df["city"])
    df["purchase_date"] = clean_purchase_date_format(df["purchase_date"])
    df["amount"] = clean_amount(df["amount"])
    df["discount"] = clean_discount(df["discount"])
    df["weight"] = clean_weight(df["weight"])
    df["unit_price"] = clean_unit_price(df["unit_price"])

    df.to_csv(OUTPUT_FILE, index=False)


if __name__ == "__main__":
    main()
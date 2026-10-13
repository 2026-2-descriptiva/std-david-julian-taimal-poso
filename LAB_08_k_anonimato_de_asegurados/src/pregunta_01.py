import json
from pathlib import Path
import pandas as pd


def pregunta_01():
    """
    Una aseguradora quiere publicar datos de sus afiliados para que un grupo
    de investigación estudie el costo de los seguros, sin que nadie pueda
    reconocer a una persona. El archivo `data/insurance.csv.gz` tiene una fila
    por afiliado con su edad (`age`), sexo (`sex`), índice de masa corporal
    (`bmi`), número de hijos (`children`), si fuma (`smoker`), región
    (`region`) y el costo de su seguro (`charges`).

    El archivo no tiene nombres ni documentos, pero eso no basta: la edad, el
    sexo, el índice de masa corporal, el número de hijos y la región son
    cuasi-identificadores, porque combinados pueden señalar a una persona.
    `smoker` es el atributo sensible que se quiere proteger.

    En este laboratorio usted va a medir el riesgo de reidentificación y a
    decidir qué publicar. Use estas definiciones:

    - Una clase de equivalencia es un grupo de registros con los mismos
      valores en todos los cuasi-identificadores. Un conjunto de datos cumple
      k-anonimato si toda clase tiene al menos k registros. Use k = 5.
    - `age_group`: `18-29`, `30-39`, `40-49` o `50-64`.
    - `bmi_group`: `bajo peso` (menos de 18.5), `normal` (desde 18.5 y menos
      de 25), `sobrepeso` (desde 25 y menos de 30) u `obesidad` (30 o más).
    - `children_group`: `0`, `1-2` o `3+`.

    Evalúe dos esquemas de generalización:

    - `with_children`: `age_group`, `sex`, `bmi_group`, `children_group` y
      `region`.
    - `without_children`: `age_group`, `sex`, `bmi_group` y `region`; el
      número de hijos no se publica.

    En cada esquema, suprima (no publique) los registros de las clases con
    menos de 5 registros. Luego, entre las clases publicadas, identifique las
    que no tienen diversidad en el atributo sensible, es decir, aquellas en
    las que todos los afiliados fuman o ninguno fuma: en esas clases, saber
    que alguien pertenece a ellas revela si fuma.

    Escriba `submission/privacy_report.json` con estas claves:

    - `original_k`: el menor tamaño de clase usando los cuasi-identificadores
      originales, sin generalizar.
    - `original_unique_records`: cuántos registros son los únicos de su clase
      con los cuasi-identificadores originales.
    - `schemes`: un diccionario con una entrada por esquema (`with_children` y
      `without_children`), cada una con las claves `quasi_identifiers` (la
      lista de columnas del esquema), `equivalence_classes` (clases antes de
      suprimir), `k_before_suppression`, `suppressed_records`,
      `published_records`, `published_classes`,
      `classes_without_smoker_diversity` y
      `records_without_smoker_diversity`.
    - `selected_scheme`: el esquema que suprime menos registros.
    - `mean_charges_original` y `mean_charges_published`: el costo promedio
      de todos los afiliados y el de los registros publicados con el esquema
      seleccionado.
    - `smoker_rate_original` y `smoker_rate_published`: la proporción de
      fumadores en ambos casos.

    Escriba también `submission/insurance_published.csv`, sin el índice de
    Pandas, con los registros publicados del esquema seleccionado, en el
    mismo orden del archivo original, y las columnas del esquema seguidas de
    `smoker` y `charges`.

    La función también debe retornar el reporte como un diccionario.
    """
    activity_dir = Path(__file__).resolve().parents[1]
    data_path = activity_dir / "data" / "insurance.csv.gz"
    submission_dir = activity_dir / "submission"
    submission_dir.mkdir(parents=True, exist_ok=True)
    report_file = submission_dir / "privacy_report.json"
    published_file = submission_dir / "insurance_published.csv"

    df = pd.read_csv(data_path)

    orig_qi = ["age", "sex", "bmi", "children", "region"]
    orig_counts = df.groupby(orig_qi).size()
    original_k = int(orig_counts.min())
    original_unique_records = int((orig_counts == 1).sum())

    def get_age_group(a):
        if a < 30:
            return "18-29"
        elif a < 40:
            return "30-39"
        elif a < 50:
            return "40-49"
        else:
            return "50-64"

    def get_bmi_group(b):
        if b < 18.5:
            return "bajo peso"
        elif b < 25.0:
            return "normal"
        elif b < 30.0:
            return "sobrepeso"
        else:
            return "obesidad"

    def get_children_group(c):
        if c == 0:
            return "0"
        elif c in (1, 2):
            return "1-2"
        else:
            return "3+"

    df["age_group"] = df["age"].apply(get_age_group)
    df["bmi_group"] = df["bmi"].apply(get_bmi_group)
    df["children_group"] = df["children"].apply(get_children_group)

    def eval_scheme(data, qi_cols):
        groups = data.groupby(qi_cols)
        eq_classes = len(groups)
        k_before = int(groups.size().min())

        sizes = data.groupby(qi_cols)["smoker"].transform("count")
        pub_df = data[sizes >= 5].copy()

        suppressed_recs = int(len(data) - len(pub_df))
        published_recs = int(len(pub_df))
        published_classes = int(len(pub_df.groupby(qi_cols)))

        pub_groups = pub_df.groupby(qi_cols)["smoker"]
        classes_no_div = 0
        records_no_div = 0
        for _, s in pub_groups:
            if s.nunique() == 1:
                classes_no_div += 1
                records_no_div += len(s)

        scheme_dict = {
            "quasi_identifiers": qi_cols,
            "equivalence_classes": eq_classes,
            "k_before_suppression": k_before,
            "suppressed_records": suppressed_recs,
            "published_records": published_recs,
            "published_classes": published_classes,
            "classes_without_smoker_diversity": classes_no_div,
            "records_without_smoker_diversity": records_no_div,
        }
        return scheme_dict, pub_df

    res_wc, pub_wc = eval_scheme(
        df, ["age_group", "sex", "bmi_group", "children_group", "region"]
    )
    res_woc, pub_woc = eval_scheme(
        df, ["age_group", "sex", "bmi_group", "region"]
    )

    if res_wc["suppressed_records"] <= res_woc["suppressed_records"]:
        selected_scheme = "with_children"
        selected_pub = pub_wc
    else:
        selected_scheme = "without_children"
        selected_pub = pub_woc

    mean_charges_original = float(df["charges"].mean())
    mean_charges_published = float(selected_pub["charges"].mean())
    smoker_rate_original = float((df["smoker"] == "yes").mean())
    smoker_rate_published = float((selected_pub["smoker"] == "yes").mean())

    report = {
        "original_k": original_k,
        "original_unique_records": original_unique_records,
        "schemes": {
            "with_children": res_wc,
            "without_children": res_woc,
        },
        "selected_scheme": selected_scheme,
        "mean_charges_original": mean_charges_original,
        "mean_charges_published": mean_charges_published,
        "smoker_rate_original": smoker_rate_original,
        "smoker_rate_published": smoker_rate_published,
    }

    report_file.write_text(json.dumps(report, indent=4), encoding="utf-8")

    pub_cols = report["schemes"][selected_scheme]["quasi_identifiers"] + [
        "smoker",
        "charges",
    ]
    selected_pub[pub_cols].to_csv(published_file, index=False)

    return report

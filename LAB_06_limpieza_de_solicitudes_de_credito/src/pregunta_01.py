from pathlib import Path
import re
import pandas as pd


def pregunta_01():
    """
    El archivo `data/solicitudes_de_credito.csv.gz` contiene las solicitudes de
    un programa de crédito, pero llegó sucio: tiene una columna de índice que
    no pertenece a los datos, registros duplicados, registros incompletos y
    valores que representan lo mismo escritos de formas distintas en los
    campos de texto, las fechas, el estrato y el monto.

    Su tarea es limpiarlo y guardar el resultado en
    `submission/solicitudes_de_credito.csv`, usando punto y coma (`;`) como
    separador y sin el índice de Pandas.

    El archivo limpio debe cumplir lo siguiente:

    - Contiene solamente las nueve columnas `sexo`, `tipo_de_emprendimiento`,
      `idea_negocio`, `barrio`, `estrato`, `comuna_ciudadano`,
      `fecha_de_beneficio`, `monto_del_credito` y `línea_credito`, en ese
      orden.
    - Los campos de texto están en minúsculas y sus palabras separadas por
      espacios.
    - `estrato` y `monto_del_credito` son números enteros, sin símbolos ni
      separadores de miles.
    - Todas las fechas de `fecha_de_beneficio` usan un mismo formato, por
      ejemplo `AAAA-MM-DD`.
    - No hay registros incompletos. La única excepción es
      `comuna_ciudadano`: sus valores faltantes son parte de los datos
      originales y deben conservarse.
    - No hay registros duplicados.

    Ejemplo del formato del archivo:

        sexo;tipo_de_emprendimiento;idea_negocio;barrio;estrato;...
        femenino;comercio;almacen de ropa en;los cerros el vergel;2;...
        ...
    """
    activity_dir = Path(__file__).resolve().parents[1]
    data_path = activity_dir / "data" / "solicitudes_de_credito.csv.gz"
    submission_dir = activity_dir / "submission"
    submission_dir.mkdir(parents=True, exist_ok=True)
    submission_file = submission_dir / "solicitudes_de_credito.csv"

    df = pd.read_csv(data_path, sep=";", index_col=0)

    # Renombrar columna de linea de credito si viene sin tilde o mal codificada
    col_mapping = {}
    for col in df.columns:
        if "nea_credito" in col:
            col_mapping[col] = "línea_credito"
    df = df.rename(columns=col_mapping)

    # Eliminar registros incompletos excepto en comuna_ciudadano
    subset_cols = [c for c in df.columns if c != "comuna_ciudadano"]
    df = df.dropna(subset=subset_cols)

    # Limpiar columnas de texto
    text_cols = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "línea_credito",
    ]
    for col in text_cols:
        df[col] = (
            df[col]
            .astype(str)
            .str.lower()
            .str.replace("-", " ")
            .str.replace("_", " ")
        )
        df[col] = df[col].apply(lambda x: " ".join(x.split()))

    # estrato a entero
    df["estrato"] = df["estrato"].astype(int)

    # monto_del_credito a entero
    df["monto_del_credito"] = (
        df["monto_del_credito"]
        .astype(str)
        .str.replace("$", "")
        .str.replace(",", "")
        .str.strip()
    )
    df["monto_del_credito"] = pd.to_numeric(df["monto_del_credito"]).astype(int)

    # fecha_de_beneficio a YYYY-MM-DD
    def fix_date(val):
        val = str(val).strip()
        parts = re.split(r"[-/]", val)
        if len(parts) == 3:
            if len(parts[0]) == 4:
                return f"{parts[0]}-{parts[1].zfill(2)}-{parts[2].zfill(2)}"
            elif len(parts[2]) == 4:
                return f"{parts[2]}-{parts[1].zfill(2)}-{parts[0].zfill(2)}"
        return val

    df["fecha_de_beneficio"] = df["fecha_de_beneficio"].apply(fix_date)

    # Asegurar orden exacto de columnas
    expected_cols = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "estrato",
        "comuna_ciudadano",
        "fecha_de_beneficio",
        "monto_del_credito",
        "línea_credito",
    ]
    df = df[expected_cols]

    # Eliminar duplicados
    df = df.drop_duplicates()

    df.to_csv(submission_file, sep=";", index=False)

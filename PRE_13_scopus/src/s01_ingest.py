from pathlib import Path

import pandas as pd

DATA_DIRECTORY = Path(__file__).resolve().parent.parent / "data"
SUBMISSION_DIRECTORY = DATA_DIRECTORY.parent / "submission"

INPUT_FILE = DATA_DIRECTORY / "scopus.csv.gz"
OUTPUT_FILE = SUBMISSION_DIRECTORY / "scopus.csv.gz"


COLUMN_RENAME_MAP = {
    "Abstract": "abstract",
    "Abbreviated Source Title": "source_title_abbr",
    "Art. No.": "article_number",
    "Affiliations": "affiliations",
    "Author full names": "author_full_names",
    "Author Keywords": "author_keywords",
    "Author(s) ID": "author_ids",
    "Authors": "author_names",
    "Authors with affiliations": "author_names_with_affiliations",
    "Cited by": "citation_count",
    "Document Type": "document_type",
    "DOI": "doi",
    "EID": "scopus_record_id",
    "Index Keywords": "index_keywords",
    "Issue": "issue_number",
    "Link": "scopus_url",
    "Open Access": "open_access_status",
    "Page count": "page_count",
    "Page end": "page_end",
    "Page start": "page_start",
    "Publication Stage": "publication_stage",
    "Source title": "source_title_full",
    "Source": "data_source",
    "Title": "publication_title",
    "Volume": "volume_number",
    "Year": "publication_year",
}


def s01_ingest() -> None:

    records = pd.read_csv(INPUT_FILE, compression="gzip")
    records = records.rename(columns=COLUMN_RENAME_MAP)
    records.to_csv(OUTPUT_FILE, index=False, compression="gzip")

    print(f"\nRenamed {len(records):,} records and saved them to {OUTPUT_FILE}\n")


if __name__ == "__main__":
    s01_ingest()
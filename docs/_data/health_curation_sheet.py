from pathlib import Path

import pandas as pd
import yaml

import bioregistry

HERE = Path(__file__).parent.resolve()
PATH = HERE.joinpath("health.yaml")
OUTPUT = HERE.joinpath("health_curation_sheet.xlsx")
OUTPUT_TSV = HERE.joinpath("health_curation_sheet.tsv")


def main():
    data = yaml.load(PATH.read_text(), Loader=yaml.FullLoader)
    results = data["runs"][0]["results"]
    rows = [
        (
            record["prefix"],
            bioregistry.get_name(record["prefix"]),
            bioregistry.get_homepage(record["prefix"]),
            record["url"],
            None,
            None,
            None,
        )
        for record in results
        if record["failed"]
    ]
    columns = ["prefix", "name", "homepage", "url", "call", "orcid", "date"]
    df = pd.DataFrame(rows, columns=columns)
    df.to_excel(OUTPUT, index=False)
    df.to_csv(OUTPUT_TSV, index=False, sep="\t")


if __name__ == "__main__":
    main()

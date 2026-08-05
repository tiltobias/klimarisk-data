import pandas as pd
import json


def getYearSheet(year: str):
    return f"KomRang_{year}"

def getIndicatorColumn(indicator: str, year: str):
    return f"{indicator}_{year}_0_100"


def buildDataObject(excel_file_path: str, dm: dict) -> dict:
    kommune_data = {
        "years": {}
    }

    for year in dm["years"]:
        df = pd.read_excel(excel_file_path, sheet_name=getYearSheet(year["key"]))

        kommune_data_year = {
            "byKommune": {},
            "byMetric": {},
        }
        for _, row in df.iterrows():
            iKomNr = str(row["iKomNr"]).zfill(4) # Ensure 4-digit kommune number

            kommune_data_year_byKommune = {
                "klimarisk_name": row["KomNavn"],
                "klimarisk_indicator_number": {},
            }
            for determinant in dm["determinants"]:
                for indicator in determinant["indicators"]:
                    indicator_value = row[getIndicatorColumn(indicator["key"], year["key"])]
                    if pd.isna(indicator_value):
                        continue

                    kommune_data_year_byKommune["klimarisk_indicator_number"][determinant["key"]] = kommune_data_year_byKommune["klimarisk_indicator_number"].get(determinant["key"], 0) + 1
                    kommune_data_year_byKommune[indicator["key"]] = indicator_value

                    # Add metric [] to byMetric dictionary if it doesnt exist
                    if indicator["key"] not in kommune_data_year["byMetric"]:
                        kommune_data_year["byMetric"][indicator["key"]] = [indicator_value]
                    else:
                        kommune_data_year["byMetric"][indicator["key"]].append(indicator_value)

            kommune_data_year["byKommune"][iKomNr] = kommune_data_year_byKommune

        # sort byMetric {} metrics
        for metric in kommune_data_year["byMetric"]:
            kommune_data_year["byMetric"][metric].sort()

        kommune_data["years"][year["key"]] = kommune_data_year
    return kommune_data


# Recreate the data model with only useful information for the frontend
def cleanDataModel(dm):
    return {
        "risk": {
            "name": dm["risk"]["name"],
            "description": dm["risk"]["description"],
        },

        "elements": [{
            "key": determinant["key"],
            "name": determinant["name"],
            **({"description": determinant["description"]} if "description" in determinant else {}),
            **({"invert": determinant["inverted"]} if "inverted" in determinant else {}),
            "metrics": [{
                "key": indicator["key"],
                "name": indicator["name"],
                **({"description": indicator["description"]} if "description" in indicator else {}),
                **({"url": indicator["url"]} if "url" in indicator else {}),
                **({"invert": indicator["invert"]} if "invert" in indicator else {}),
            } for indicator in determinant["indicators"]],
        } for determinant in dm["determinants"]],

        "years": [{
            "key": year["key"],
            "name": year["name"],
            "description": year["description"],
        } for year in dm["years"]],

        "documentation": [
            item for item in dm["documentation"]
        ],
    }


from pathlib import Path

if __name__ == "__main__":
    parent_folder = Path(__file__).resolve().parent
    in_path_excel = parent_folder / "input-files" / "source_data.xlsx"
    in_path_model = parent_folder / "input-files" / "source_data_model.json"

    root_folder = parent_folder.parent
    out_path = root_folder / "kommune_data.json"
    out_path_model = root_folder / "kommune_data_model.json"

    # Load data model
    dm = json.load(open(in_path_model, 'r', encoding='utf-8'))

    # Build data object and write to JSON
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(buildDataObject(in_path_excel, dm), f, ensure_ascii=False, indent=2)

    # Write cleaned data model to JSON
    with open(out_path_model, "w", encoding="utf-8") as f:
        json.dump(cleanDataModel(dm), f, ensure_ascii=False, indent=2)
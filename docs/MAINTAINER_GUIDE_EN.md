# Klimarisk data maintainer guide

This guide explains how to update the municipality climate-risk data used by the [Klimarisk dashboard](https://tiltobias.github.io/klimarisk/). Data updates are made in this repository and do not require changes to the dashboard frontend.

The dashboard supports:

- one or more years;
- one or more determinants;
- one or more indicators within each determinant; and
- changes to names, descriptions, ordering, and indicator composition.


The update workflow uses:

- `data-update/input-files/source_data.xlsx` as the source dataset;
- `data-update/input-files/source_data_model.json` as the source data model; and
- `data-update/prepare_data.py` to generate the dashboard files.

The script automatically reads these exact filenames and locations. You should not need to edit file paths in the Python code.

## Quick update workflow

For a normal data update:

1. Replace `data-update/input-files/source_data.xlsx`.
2. Update `source_data_model.json` if years, determinants, indicators, names, descriptions, URLs, or inversion settings have changed.
3. Run `prepare_data.py`.
4. Confirm that the generated root files have been updated.
5. Commit and push the changes to the `main` branch.
6. Check the live dashboard.

`kommune.geojson` normally remains unchanged. Replace it only when municipality boundaries or municipality identifiers change.

## 1. First-time Python setup

Install a current Python 3 version if Python is not already available.

Open a terminal in the repository's `data-update` folder:

```bash
cd data-update
```

Create a local virtual environment:

```bash
python -m venv .venv
```

On Windows, activate it with:

```bash
.venv\Scripts\activate
```

On macOS or Linux, activate it with:

```bash
source .venv/bin/activate
```

Install the required Python packages:

```bash
python -m pip install -r requirements.txt
```

The `.venv` folder is ignored by Git and exists only on your computer. This setup normally only needs to be repeated after cloning the repository on a new computer.

## 2. Update the source data model

Edit:

```text
data-update/input-files/source_data_model.json
```

This file controls the years, determinants, indicators, ordering, names, descriptions, links, and inversion settings shown in the dashboard.

Its root structure is:

```json
{
  "years": [],
  "risk": {},
  "determinants": []
}
```

Only use the properties described below.

### Root properties

| Property | Required | Description |
| --- | --- | --- |
| `years` | Yes | Array containing at least one year object. |
| `risk` | Yes | Metadata for the total climate-risk value. |
| `determinants` | Yes | Array containing at least one determinant object. |

### Year properties

| Property | Required | Description |
| --- | --- | --- |
| `key` | Yes | Unique string identifying the year or time period, such as `"2025"`. Also used in Excel sheet and column names. |
| `name` | Yes | Display name in every dashboard language. Currently `no` and `en`. |
| `description` | Recommended | Short description in every dashboard language. |

The order of the year objects controls their order in the dashboard. The last year in the array is selected by default when the dashboard opens.

Example:

```json
{
  "key": "2050",
  "name": {
    "no": "2050",
    "en": "2050"
  },
  "description": {
    "no": "Nær fremtid",
    "en": "Near future"
  }
}
```

### Risk properties

The root `risk` object describes the total climate-risk metric. It does not use a `key`.

| Property | Required | Description |
| --- | --- | --- |
| `name` | Yes | Display name in every dashboard language. |
| `description` | Recommended | Description in every dashboard language. |

Example:

```json
{
  "name": {
    "no": "Total risiko",
    "en": "Total risk"
  },
  "description": {
    "no": "Samlet indeks for klimarisiko.",
    "en": "Composite index of climate risk."
  }
}
```

### Determinant properties

| Property | Required | Description |
| --- | --- | --- |
| `key` | Yes | Unique string identifying the determinant. |
| `name` | Yes | Display name in every dashboard language. |
| `description` | Recommended | Description in every dashboard language. |
| `inverted` | No | Boolean. Set to `true` when the determinant direction must be inverted. Omission is equivalent to `false`. |
| `indicators` | Yes | Array containing at least one indicator object. |

The order of determinant objects controls their order in the dashboard.

Example:

```json
{
  "key": "r",
  "name": {
    "no": "Respons",
    "en": "Response"
  },
  "description": {
    "no": "Samlet respons.",
    "en": "Combined response."
  },
  "inverted": true,
  "indicators": []
}
```

### Indicator properties

| Property | Required | Description |
| --- | --- | --- |
| `key` | Yes | Unique string identifying the indicator. It must be unique across all determinants. |
| `name` | Yes | Display name in every dashboard language. |
| `description` | Recommended | Description in every dashboard language. |
| `url` | No, but recommended | Link to the indicator's detailed explanation. |
| `inverted` | No | Boolean. Set to `true` when the indicator direction must be inverted. Omission is equivalent to `false`. |

The dashboard functions without `url`, but indicators should include the official explanation link when one is available.

The order of indicator objects controls their order within the determinant.

Example:

```json
{
  "key": "fFlom",
  "name": {
    "no": "Flomfare",
    "en": "Flood hazard"
  },
  "description": {
    "no": "Kort norsk beskrivelse.",
    "en": "Short English description."
  },
  "url": "https://example.org/indicator"
}
```

### Complete example model

This example contains one year, one determinant, and one indicator:

```json
{
  "years": [
    {
      "key": "2025",
      "name": {
        "no": "2025",
        "en": "2025"
      },
      "description": {
        "no": "Referanseperiode",
        "en": "Reference period"
      }
    }
  ],
  "risk": {
    "name": {
      "no": "Total risiko",
      "en": "Total risk"
    },
    "description": {
      "no": "Samlet indeks for klimarisiko.",
      "en": "Composite index of climate risk."
    }
  },
  "determinants": [
    {
      "key": "f",
      "name": {
        "no": "Fare",
        "en": "Hazard"
      },
      "description": {
        "no": "Samlet fare.",
        "en": "Combined hazard."
      },
      "indicators": [
        {
          "key": "fFlom",
          "name": {
            "no": "Flomfare",
            "en": "Flood hazard"
          },
          "description": {
            "no": "Kort norsk beskrivelse.",
            "en": "Short English description."
          },
          "url": "https://example.org/indicator"
        }
      ]
    }
  ]
}
```

### Key rules

Keys connect the JSON model, Excel workbook, generated files, and dashboard. Treat them as stable identifiers.

- Use only ASCII letters, digits, underscores (`_`), and hyphens (`-`).
- Avoid spaces, `æ`, `ø`, `å`, accented characters, and other symbols.
- Keys are case-sensitive.
- Every year key must be unique.
- Every determinant key must be unique.
- Every indicator key must be unique across all determinants.
- Changing a year or indicator key also requires changing the matching Excel sheet or column names.

Names and descriptions may use normal Norwegian and English characters, including `æ`, `ø`, and `å`.

### Languages

Every `name` object must contain all languages supported by the dashboard. Descriptions should use the same language set.

The currently supported language keys are:

```json
{
  "no": "Norwegian Bokmål text",
  "en": "English text"
}
```

Adding a new language to the JSON file alone is not sufficient. The dashboard application must also be updated to support it.

### Inversion

Set an inversion flag using a JSON boolean:

```json
"inverted": true
```

Do not write `"true"` as a string. Omitting the property has the same effect as:

```json
"inverted": false
```

### JSON formatting

JSON has strict formatting requirements:

- property names and text values use double quotes;
- objects use `{}` and arrays use `[]`;
- properties are separated by commas;
- trailing commas are not allowed;
- booleans use `true` or `false` without quotes; and
- brackets, braces, and quotation marks must be correctly paired.

A code editor normally highlights syntax errors. Otherwise, the file can be checked with [JSONLint](https://jsonlint.com/) before running the preprocessing script.

Valid JSON syntax does not guarantee that the model is correct. Also check required properties, language fields, unique keys, and matching Excel names.

## 3. Update the Excel source file

Replace or edit:

```text
data-update/input-files/source_data.xlsx
```

The workbook must contain one sheet for every year in `source_data_model.json`.

### Sheet names

Each sheet must use this exact format:

```text
KomRang_<yearKey>
```

Examples:

```text
KomRang_2025
KomRang_2050
KomRang_2100
```

`<yearKey>` must exactly match the corresponding `key` in the model's `years` array.

### Required columns

Every year sheet must contain:

| Column | Content |
| --- | --- |
| `iKomNr` | Municipality number. Use the official four-digit municipality code. Storing it as text is safest for codes beginning with `0`. |
| `KomNavn` | Municipality name. |
| `<indicatorKey>_<yearKey>_0_100` | Value for every indicator defined in the data model. |

For indicator `fFlom` in year `2050`, the required column is:

```text
fFlom_2050_0_100
```

Every sheet must contain a column for every indicator in the model, regardless of which determinant contains it. Names and capitalization must match exactly.

Indicator values are expected to use the dashboard's normalized 0–100 scale.

### Excel checklist

Before running the script, confirm that:

- every year has a matching `KomRang_<yearKey>` sheet;
- every sheet contains `iKomNr` and `KomNavn`;
- every sheet contains all indicator columns;
- sheet and column names contain no extra spaces;
- municipality numbers are valid and consistent between sheets; and
- municipality numbers still match `kommune.geojson`.

## 4. Run the preprocessing script

From the `data-update` folder, activate the virtual environment if it is not already active.

Windows:

```bash
.venv\Scripts\activate
```

macOS or Linux:

```bash
source .venv/bin/activate
```

Run:

```bash
python prepare_data.py
```

The script automatically reads:

```text
data-update/input-files/source_data.xlsx
data-update/input-files/source_data_model.json
```

No path editing or command-line file arguments are required.

### Where the output files appear

The script writes the generated files to the **repository root**, one folder above `data-update`:

```text
klimarisk-data/kommune_data.json
klimarisk-data/kommune_data_model.json
```

They do **not** appear inside `data-update`.

This can be confusing if your file browser or editor is showing only the `data-update` folder. Open the parent `klimarisk-data` folder to find the generated output files.

Running the script replaces the existing root versions of these files. Do not manually edit the generated files. Correct the source Excel or JSON file and run the script again instead.

## 5. Check the generated files

After the script finishes, confirm that the root files have been updated:

```text
kommune_data.json
kommune_data_model.json
```

Check that:

- the expected years are present;
- the expected determinants and indicators are present;
- names and descriptions are available in Norwegian and English;
- all expected municipalities are included;
- municipality numbers retain four digits; and
- no missing-sheet, missing-column, or invalid-value errors were reported.

`kommune_data_model.json` is the processed dashboard model generated from `source_data_model.json`. The source file should continue to be edited in `data-update/input-files/`.

## 6. Update `kommune.geojson` only when required

The existing root `kommune.geojson` can normally be reused. Replace it when:

- municipality boundaries change;
- municipalities merge or split;
- municipality identifiers change; or
- an `iKomNr` in the Excel file no longer has a matching geometry.

### Required GeoJSON structure

The file must:

- be named `kommune.geojson`;
- be a GeoJSON `FeatureCollection`;
- contain municipality features with `Polygon` or `MultiPolygon` geometries;
- contain a `kommunenummer` property on every feature;
- store `kommunenummer` as a four-character string, not an integer; and
- use WGS 84 longitude and latitude coordinates (`EPSG:4326`).

Example feature:

```json
{
  "type": "Feature",
  "properties": {
    "kommunenummer": "0301"
  },
  "geometry": {
    "type": "MultiPolygon",
    "coordinates": []
  }
}
```

The identifiers must match:

```text
GeoJSON kommunenummer == Excel iKomNr
```

### File size and simplification

Keep `kommune.geojson` below 25 MB so it can be uploaded to GitHub and remains practical for the dashboard to load.

One suitable ArcGIS Pro workflow is:

1. use **Simplify Polygon**;
2. use the Douglas–Peucker algorithm with a tolerance of approximately 25 metres;
3. remove polygon parts smaller than approximately 25,000 m², such as small islands that are not visible at dashboard scale;
4. export the result as WGS 84 GeoJSON; and
5. confirm that `kommunenummer` remains a four-character string.

Use a projected coordinate system measured in metres while applying metre-based tolerances, then export the final file in WGS 84.

Do not simplify so aggressively that important boundaries or municipality shapes become misleading.

## 7. Commit and publish the files

The repository root on the `main` branch must contain:

```text
kommune_data.json
kommune_data_model.json
kommune.geojson
```

Commit the updated generated files and any changed source files:

```text
data-update/input-files/source_data.xlsx
data-update/input-files/source_data_model.json
```

A suitable commit message could be:

```text
Update data: Kommunerangeringen 2026
```

Changes to the root dashboard files on `main` are automatically published through GitHub Pages. The dashboard then fetches the updated data without requiring a new frontend deployment.

Allow a few minutes for deployment and browser caching.

## 8. Verify the live dashboard

Open the [live dashboard](https://tiltobias.github.io/klimarisk/) and check that:

- the dashboard loads without errors;
- all expected years appear in the correct order;
- the final year is selected by default;
- determinants and indicators appear in the intended order;
- Norwegian and English text is present;
- municipality names and values are available;
- the map contains every municipality;
- changing the year or selected indicator updates all views; and
- inverted determinants or indicators behave in the intended direction.

Use a hard refresh if the previous dataset still appears.

## Troubleshooting

| Problem | Likely cause |
| --- | --- |
| `source_data.xlsx` cannot be found | The file is missing, renamed, or not located in `data-update/input-files/`. |
| `source_data_model.json` cannot be found | The file is missing, renamed, or not located in `data-update/input-files/`. |
| JSON parsing error | Invalid JSON syntax, often a trailing comma, missing quote, or unmatched bracket. |
| A year sheet cannot be found | The sheet is not named exactly `KomRang_<yearKey>`. |
| An indicator column cannot be found | The indicator key, year key, or capitalization does not match the model. |
| An indicator is missing or overwritten | Indicator keys are duplicated across determinants. |
| Oslo or another municipality is missing | A leading zero was lost, or `iKomNr` does not match the GeoJSON `kommunenummer`. |
| A municipality has no map geometry | `kommune.geojson` is outdated or its `kommunenummer` property is missing or incorrect. |
| The generated files are not visible | They are written to the repository root, not inside `data-update`. Open the parent folder. |
| The dashboard still shows old data | GitHub Pages has not finished publishing, or the browser is using cached files. |
| Text is missing in one language | The matching `no` or `en` property is missing. |
| Values have the wrong risk direction | An `inverted` flag is missing, misplaced, or set on the wrong object. |


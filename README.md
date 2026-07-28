# Klimarisk data

Static JSON and GeoJSON data files used by the [Klimarisk dashboard](https://tiltobias.github.io/klimarisk/).

The dashboard application and frontend code are maintained separately in the [klimarisk repository](https://github.com/tiltobias/klimarisk). This repository is intended to make data updates possible without changing the dashboard code.

## Published dashboard files

The dashboard requires these files in the repository root:

- `kommune_data.json` — processed municipality and indicator values.
- `kommune_data_model.json` — processed metadata for the dataset.
- `kommune.geojson` — municipality geometries.

These filenames and their location in the repository root must remain unchanged.

## Updating the data

The editable source files and preprocessing script are located in `data-update/`.

- `input-files/source_data.xlsx` contains the municipality data.
- `input-files/source_data_model.json` defines the years, determinants, indicators, names, descriptions, and optional settings.
- `prepare_data.py` processes the source files.
- `requirements.txt` lists the required Python packages.

The script generates new versions of:

```text
kommune_data.json
kommune_data_model.json
```

These generated files must be placed in the repository root. `kommune.geojson` is maintained separately and normally only needs to be replaced when municipality boundaries or identifiers change.

Do not edit the generated root JSON files directly. Update the source files in `data-update/input-files/` and run the preprocessing script instead.

For complete instructions, see the [Norwegian](docs/MAINTAINER_GUIDE_NO.md) or [English maintainer guide](docs/MAINTAINER_GUIDE_EN.md).

## Deployment

Changes committed to the root data files on the `main` branch are automatically published through GitHub Pages. The live dashboard then fetches the updated files automatically without requiring a new frontend deployment.

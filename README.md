# Klimarisk data

Static JSON and GeoJSON datasets used by the [Klimarisk dashboard](https://tiltobias.github.io/klimarisk/).

This repository is kept separate from the [dashboard application repository](https://github.com/tiltobias/klimarisk) so maintainers can update and publish the climate-risk data without changing the frontend code. The source Excel workbook and source data model are processed with [`prepare_data.py`](https://github.com/tiltobias/klimarisk/blob/main/scripts/prepare_data.py). The generated files are then committed to this repository and published through GitHub Pages.

## Maintainer guides

- [Norsk vedlikeholdsveiledning](docs/MAINTAINER_GUIDE_NO.md)
- [English maintainer guide](docs/MAINTAINER_GUIDE_EN.md)

## Published data files

The dashboard requires these files in the repository root on the `main` branch:

- `kommune_data.json` — generated municipality and indicator data.
- `kommune_data_model.json` — generated dashboard data model.
- `kommune.geojson` — municipality geometries.

The published files are available from:

```text
https://tiltobias.github.io/klimarisk-data/
```

Do not edit the generated JSON files directly. Update the source workbook and source data model, run the preprocessing script, and publish the new outputs.

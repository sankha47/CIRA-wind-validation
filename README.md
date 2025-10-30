# 🌪️ WRF Surface Wind validattion with CIRA data — Cyclone Center Following Wind Fields

This repository contains a Python workflow to compute and visualize **surface wind fields** around the **tropical cyclone (TC) center** from **WRF model UPP outputs**
to validate it with CIRA surface wind data 
The core function `calculate_center_following_wind_wrf()` extracts wind components, computes wind speed in knots, and produces center-following wind plots over time.

---

## 🚀 Features

- Reads **WRF-Postprocessed (UPP)** NetCDF outputs (`ugrd10m`, `vgrd10m`).
- Follows the **TC track** dynamically and extracts a **4°×4° box** centered on the cyclone.
- Computes **wind speed in knots** from 10 m wind components.
- Generates **cartopy-based maps** with:
  - Contours and wind barbs
  - Coastlines and formatted lat–lon axes
  - Time-labeled subplots for multiple model hours

---

## 🧩 Dependencies

Make sure you have the following Python packages installed:
numpy 
pandas
xarray
matplotlib 
cartopy

```bash
pip install numpy pandas xarray matplotlib cartopy

## Requirements

- Python 3.x
- `xarray` for handling WRF datasets.
- `numpy` for numerical operations.
- WRF model output data (e.g., `ugrd10m`, `vgrd10m`, latitude, longitude, and time data).
- WRF track date (lat, lon position)

## Installation

To use this code, you can either clone the repository or download the script directly.

### Clone the repository:

```bash
git clone https://github.com/sankha47/CIRA-wind-validation.git

## Cite this work

If you use this code or functionality in your research, please reference it as follows:

> Sankhasubhra Chakraborty. (2025). *Center-following Wind Speed Extraction and Visualization from WRF UPP Output to validate with CIRA data*. GitHub Repository. Available at: [https://github.com/sankha47/CIRA-wind-validation](https://github.com/sankha47/CIRA-wind-validation).


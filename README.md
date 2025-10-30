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

## 📚 Cite this work

If you use this code or functionality in your research, please cite it as follows:

> Sankhasubhra Chakraborty. (2025). *Center-following Wind Speed Extraction and Visualization from WRF UPP Output to validate with CIRA data*. GitHub Repository. Available at: [https://github.com/sankha47/CIRA-wind-validation](https://github.com/sankha47/CIRA-wind-validation).

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

```
---

## CIRA: 
[CIRA](https://rammb-data.cira.colostate.edu/tc_realtime) Multi-Platform Tropical Cyclone Surface Wind Analysis:
This product integrates data from five different sources to generate a mid-level wind analysis near the 700 hPa level, using a variational method outlined by [Knaff and DeMaria (2006)](https://rammb-data.cira.colostate.edu/tc_realtime/images/mpsw.pdf). The resulting wind fields at this level are then adjusted to the surface using a straightforward single-column approach. Over the ocean, an adjustment factor is applied that varies with the radius from the cyclone center, ranging from 0.9 to 0.7, and the winds are rotated 20 degrees toward low pressure. On land, the ocean-derived winds are further reduced by 20% and rotated an additional 20 degrees toward low pressure.


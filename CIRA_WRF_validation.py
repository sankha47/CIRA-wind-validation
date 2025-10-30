#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 19:24:05 2025
@author: 
    Sankhasubhra Chakraborty
    Phd Scholar
    SEOCS
    IIT Bhubaneswar

"""

"""
This script extracts and visualizes 10-meter wind fields from WRF UPP outputs 
following the tropical cyclone (TC) center track to validate with CIRA wind speed. It subsets a 4°×4° box around 
the TC center, computes wind speed in knots, and generates center-following 
barb and contour plots for selected time steps.
"""

# CIRA: https://rammb-data.cira.colostate.edu/tc_realtime/


#%%

import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

def cal_close(arr, val): return int(abs(arr-val).argmin())


from  cartopy.mpl.ticker  import (LongitudeFormatter, LatitudeFormatter)

def calculate_center_following_wind_wrf(wrf_ds, wrf_lats, wrf_lons, wrf_res, track_lat,
                                        track_lon, idx, wrf_time):
    """
    Calculate the wind speed at a given time step for a 4x4 degree box centered 
    on the TC center (latitude, longitude).
    
    Parameters:
    - wrf_ds (xarray Dataset): The WRF UPP dataset.
    - wrf_lats (numpy array): Latitude array for WRF domain.
    - wrf_lons (numpy array): Longitude array for WRF domain.
    - wrf_res (float): The resolution of the WRF grid.
    - track_lat (numpy array): Array of latitudes from the track.
    - track_lon (numpy array): Array of longitudes from the track.
    - idx (int): The current index of the time step.
    - wrf_time (numpy array): The time steps of the WRF simulation.
    - cal_close (function): Function to calculate the closest index for a latitude or longitude.
    
    Returns:
    - u, v, wind_speed (numpy array): The wind speed components and magnitude in
    knots at the specified time step.
    """
    # Extract the timestep from wrf_time
    timeStep = wrf_time[idx]
    
    # Subset surface wind components from the main WRF dataset for the specified time step
    temp_ds = wrf_ds[['ugrd10m', 'vgrd10m']].sel(time=timeStep)
    
    # TC center lat, lon at the current time step
    cntr_lat = track_lat[idx]
    cntr_lon = track_lon[idx]
    
    # Calculate center lat, lon index based on the closest latitude and longitude
    cntr_lat_i = int(cal_close(wrf_lats, cntr_lat))
    cntr_lon_i = int(cal_close(wrf_lons, cntr_lon))
    
    # Subset a 4 x 4 degree box around the center
    sub_idx = int(2 / wrf_res)
    ds_sub = temp_ds.sel(lat=wrf_lats[(cntr_lat_i - sub_idx):(cntr_lat_i + sub_idx)],
                         lon=wrf_lons[(cntr_lon_i - sub_idx):(cntr_lon_i + sub_idx)])
    
    # Extract u, v wind components and convert to knots (multiply by 1.94)
    u = np.squeeze(ds_sub.ugrd10m) * 1.94
    v = np.squeeze(ds_sub.vgrd10m) * 1.94
    
    # Calculate wind speed in knots
    wind_speed = np.sqrt(u**2 + v**2)
    
    # extract lat, lon values of the box
    box_lat = ds_sub.lat.values
    box_lon = ds_sub.lon.values
    
    return u, v, wind_speed, box_lat, box_lon

#%%
# read WRF UPP (Unified Post Processor) output
wrf_path = './wrf_upp_output.nc'
wrf_ds = xr.open_dataset(wrf_path)
wrf_time = wrf_ds.time
wrf_lats = wrf_ds.lat
wrf_lons = wrf_ds.lon

# calculate the wrf resolution
wrf_res = (wrf_lats[1]-wrf_lats[0]).values


tracks_df = pd.read_csv('./wrf_track.csv')
track_lat, track_lon = tracks_df['lat'].values, tracks_df['lon'].values

#%% make the colorbar matching which CIRA

alp_seq = [chr(ord('a') + i) for i in range(26)]
import matplotlib 
cmap = matplotlib.colors.ListedColormap(['black','#76FF7B', '#FBDD7E', 'orange','#FF6347', 'grey'])
cb_levels = np.array([0, 20, 35, 50, 65, 80, 95])
norm = matplotlib.colors.BoundaryNorm(cb_levels, cmap.N)


#%% main plot

nrows = 2  ; ncols = 2
fig, axs = plt.subplots(nrows=nrows, ncols=ncols, subplot_kw={'projection': ccrs.PlateCarree()},
                        figsize=(ncols * 4, nrows * 4 - 1),)
axs = axs.flatten()
idx = [0, 12, 24, 48]
for i in range(0, nrows*ncols):
    
    ax =  axs[i]
    
    u, v, wind_speed, box_lat, box_lon = calculate_center_following_wind_wrf(wrf_ds, wrf_lats, wrf_lons,
                                                           wrf_res, track_lat, 
                                                           track_lon, idx[i], wrf_time)
    # =====================================================================
    # plot contourf    
    cs = ax.contour(box_lon, box_lat, wind_speed,
                    transform =ccrs.PlateCarree(),
                    levels = cb_levels, 
                    colors='k', 
                    extend = 'both')
    
    # plot wind barbs
    q = ax.barbs(box_lon, box_lat, u, v, wind_speed, transform =ccrs.PlateCarree(),
                     cmap=cmap, norm=norm, 
                     linewidth=0.5, length=6, 
                     regrid_shape = 30)
    
    l=ax.clabel(cs, inline=1, fontsize=16)
    
    
    
    # plot lat, lon axis ticks
    ax.set_xticks(np.linspace(box_lon.min(), box_lon.max(), 5).round(1), 
                  crs=ccrs.PlateCarree())
    ax.set_yticks(np.linspace(box_lat.min(), box_lat.max(), 5).round(1), 
                  crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(transform_precision=1)
    lat_formatter = LatitudeFormatter(transform_precision=1)
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    
    ax.tick_params(axis='both', labelsize=10, pad = 0.1)
    
    # add coastline
    ax.coastlines(color='k', linewidth=2)
    # axis title
    ax.set_title(f'Model hour: {idx[i]}h', fontsize = 15, fontweight = 'bold')
    ax.annotate(f"({alp_seq[i]})", xy=(0.02, 1.03), xycoords="axes fraction",
                fontweight='bold', fontsize = 16)
    
# =============================================================================
# plt.suptitle('CIRA-WRF surface wind validation',  fontweight="bold", fontsize = 20, x = 0.5, y= 1)

fig.tight_layout(pad = 2)
cbar = fig.colorbar(q, ax = axs[:], shrink = 0.5, orientation='vertical', pad=0.04)
cbar.ax.tick_params(axis='y', labelsize=15)
cbar.ax.set_title('Knots', size=16, x = 0.8, y= 1.03,)

# plt.savefig('./wrf_cira_wind_validation.png', dpi = 400, bbox_inches = 'tight')


# -*- coding: utf-8 -*-

from osgeo import gdal
import rasterio
import numpy as np 
import os, sys

nir_filename = "B5.tif"
red_filename = "B4.tif"

with rasterio.open(red_filename) as src:
    band_red = src.read(1)

with rasterio.open(nir_filename) as src:
    band_nir = src.read(1)


np.seterr(divide="ignore", invalid="ignore")

ndvi = (band_nir.astype(float) - band_red.astype(float)) / (band_nir + band_red)

kwargs = src.meta
kwargs.update(
    dtype=rasterio.float32,
    count = 1)

with rasterio.open('ndvi.tif', 'w', **kwargs) as dst:
        dst.write_band(1, ndvi.astype(rasterio.float32))
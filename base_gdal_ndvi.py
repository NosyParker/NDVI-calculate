# -*- coding: utf-8 -*-
import os
import sys
import argparse
import numpy as np

from osgeo import gdal

def calculate_ndvi(red_filename, nir_filename):
    red_dataset = gdal.Open (red_filename)
    red = np.array(red_dataset.GetRasterBand(1).ReadAsArray())
    
    nir_dataset = gdal.Open (nir_filename)
    nir = np.array(nir_dataset.GetRasterBand(1).ReadAsArray())
    
    if ( red_dataset.RasterXSize != nir_dataset.RasterXSize ) or \
            ( red_dataset.RasterYSize != nir_dataset.RasterYSize ):
        print ("Каналы не совпадают!!!")
        print ("Размеры красного канала: {}".format(red.shape))
        print ("Размеры NIR канала: {}".format(nir.shape))
        
        sys.exit ( -1 )
    # del nir_dataset
    # del red_dataset
    red = np.array(red, dtype = np.float32)
    nir = np.array(nir, dtype = np.float32)
    np.seterr(divide='ignore', invalid='ignore')
    ndvi = (nir-red)/(nir+red)
    # print (ndvi)
    return ndvi
    
def save_raster ( output_name, raster_data, dataset, driver="GTiff" ):

    g_input = gdal.Open ( dataset )
    geo_transform = g_input.GetGeoTransform ()
    x_size = g_input.RasterXSize
    y_size = g_input.RasterYSize
    srs = g_input.GetProjectionRef()
    if driver == "GTiff":
        driver = gdal.GetDriverByName ( driver )
        dataset_out = driver.Create ( output_name, x_size, y_size, 1, \
                gdal.GDT_Float32, ['TFW=YES', \
                'COMPRESS=LZW', 'TILED=YES'] )
    else:
        driver = gdal.GetDriverByName ( driver )
        dataset_out = driver.Create ( output_name, x_size, y_size, 1, \
                gdal.GDT_Float32 )
        
    dataset_out.SetGeoTransform ( geo_transform )
    dataset_out.SetProjection ( srs )
    dataset_out.GetRasterBand ( 1 ).WriteArray ( \
            raster_data.astype(np.float32) )
    dataset_out.GetRasterBand ( 1 ).SetNoDataValue ( float(-999) )
    dataset_out = None

if __name__ == "__main__":
    
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument( '-r', dest="red_filename", \
            help="The RED dataset" )
    arg_parser.add_argument( '-n', dest="nir_filename", \
            help="The NIR dataset" )
    arg_parser.add_argument( '-o', dest="out_filename", \
            help="The OUTPUT dataset" )
    arg_parser.add_argument( '-f',  dest="out_format", \
            default="GTiff", help="Output format" ) 
    options = arg_parser.parse_args()
                
    if not os.path.exists ( options.red_filename ):
        print ("ERROR: The red filename {} does not exist".format(options.red_filename))
        sys.exit ( -1 )
    if not os.path.exists ( options.nir_filename ):
        print ("ERROR: The nir filename {} does not exist".format(options.nir_filename))
        sys.exit ( -1 )
    if os.path.exists ( options.out_filename):
        print ("ERROR: The output filename {} does already exist".format(options.out_filename))
        print ("Select a different one, or delete the file.")
        sys.exit ( -1 )
        
        
    calc_ndvi = calculate_ndvi(options.red_filename, options.nir_filename)
    save_raster(options.out_filename, calc_ndvi, options.red_filename, driver=options.out_format)
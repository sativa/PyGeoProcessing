# Raster_read_write.py
# Program to read and write raster 
# Python Data Analysis-Script 5
# Author: Baburao Kamble


#import GDAL libraries 

from osgeo import gdal
from osgeo import _gdal
from osgeo import gdalnumeric
from osgeo.gdal_array import *
from osgeo.gdalconst import *


def image_read_function(filename):
#tmp = gdal.Open('L5029032_03220020730_B30.tif', GA_ReadOnly)
#filename='L5029032_03220020730_B30.tif'

    driver = gdal.GetDriverByName( 'GTiff' ) #Get Raster file format driver 
    tmp = gdal.Open(filename)                # open file 
    geoT = tmp.GetGeoTransform()            #Fetches the coefficients for transforming between pixel/line (P,L) raster space, and projection coordinates (Xp,Yp) space.
    proJ = tmp.GetProjection()              # Read Projection
                    
    cols = tmp.RasterXSize                  # Read number of column 
    rows = tmp.RasterYSize                 # Read number of Rows 
    bands = tmp.RasterCount                 # Read number of bands  

    print cols, rows, bands
    print geoT
    print proJ

    minx = geoT[0]
    miny = geoT[3] + cols*geoT[4] + rows*geoT[5] 
    maxx = geoT[0] + cols*geoT[1] + rows*geoT[2]
    maxy = geoT[3]
    print (minx,maxx,miny,maxy)
    DN = tmp.ReadAsArray(0, 0, cols, rows) #read entire image
# Write image 
    output_filename='MyOutputFile.tif'
    OutputDS = driver.Create(output_filename, cols, rows, 1, GDT_Float32)
    OutputDS.SetGeoTransform(tmp.GetGeoTransform())
    OutputDS.SetProjection(tmp.GetProjection())
    outBand_Output = OutputDS.GetRasterBand(1)
    outBand_Output.WriteArray(DN)   


filename='L5029032_03220020730_B30.tif'
image_read_function(filename)

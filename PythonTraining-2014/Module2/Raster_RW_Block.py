#Program to read data in block size 
#Program to write data in block size 

#import GDAL libraries 

from osgeo import gdal
from osgeo import _gdal
from osgeo import gdalnumeric
from osgeo.gdal_array import *
from osgeo.gdalconst import *

# utility to read blocks 
import imp
utils2 = imp.load_source('utils2', 'E:/Teaching/Python/Scripts/image/Utils/utils.py')


def image_read_function(filename):
#tmp = gdal.Open('L5029032_03220020730_B30.tif', GA_ReadOnly)
#filename='L5029032_03220020730_B30.tif'

    driver = gdal.GetDriverByName( 'GTiff' ) #Get Raster file format driver 
    tmp = gdal.Open(filename,GA_ReadOnly)                # open file 
    geoT = tmp.GetGeoTransform()            #Fetches the coefficients for transforming between pixel/line (P,L) raster space, and projection coordinates (Xp,Yp) space.
    proJ = tmp.GetProjection()              # Read Projection
                    
    cols = tmp.RasterXSize                  # Read number of column 
    rows = tmp.RasterYSize                 # Read number of Rows 
    bands = tmp.RasterCount                 # Read number of bands
    btmp1 = tmp.GetRasterBand(1)
#Output 
    Output_filename='MaheshMyfile2_Block_Write.tif'   
    OutputDS = driver.Create(Output_filename, cols, rows, 1, GDT_Float32)
    OutputDS.SetGeoTransform(tmp.GetGeoTransform())
    OutputDS.SetProjection(tmp.GetProjection())
    outBand_data = OutputDS.GetRasterBand(1)


    yBlockSize=2000
    xBlockSize=2000

    for i in range(0, rows, yBlockSize):
        if i + yBlockSize < rows:
            numRows = yBlockSize
        else:
            numRows = rows - i
        for j in range(0, cols, xBlockSize):
            if j + xBlockSize < cols:
                numCols = xBlockSize
            else:
                numCols = cols - j
                
                DN = BandReadAsArray(btmp1,j,i,numCols, numRows).astype(numpy.int)
                print (DN)
                outBand_data.WriteArray(DN, j, i)
                

#filename = input("Input filename ")
filename='L5029032_03220020730_B30.tif'
image_read_function(filename)

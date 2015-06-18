#Program to calculate NDVI 



#import GDAL libraries 

from osgeo import gdal
from osgeo import _gdal
from osgeo import gdalnumeric
from osgeo.gdal_array import *
from osgeo.gdalconst import *
import time, numpy

# utility to read blocks 
import imp
utils2 = imp.load_source('utils2', 'E:/Teaching/Python/Scripts/image/Utils/utils.py')


def image_read_function(RED, NIR):
#tmp = gdal.Open('L5029032_03220020730_B30.tif', GA_ReadOnly)
#filename='L5029032_03220020730_B30.tif'
    startTime = time.time()

    driver = gdal.GetDriverByName( 'GTiff' ) #Get Raster file format driver 
    tmp = gdal.Open(RED,GA_ReadOnly)                # open file 
    geoT = tmp.GetGeoTransform()            #Fetches the coefficients for transforming between pixel/line (P,L) raster space, and projection coordinates (Xp,Yp) space.
    proJ = tmp.GetProjection()              # Read Projection
                    
    cols = tmp.RasterXSize                  # Read number of column 
    rows = tmp.RasterYSize                 # Read number of Rows 
    bands = tmp.RasterCount                 # Read number of bands
    REDtmp = tmp.GetRasterBand(1)

    NIRf = gdal.Open(NIR,GA_ReadOnly)
    NIRtmp = NIRf.GetRasterBand(1)
     
    Output_filename='NDVI.tif'   
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
                
            REDdata = BandReadAsArray(REDtmp,j,i,numCols, numRows).astype(numpy.float)          #band 3  
            NIRdata = BandReadAsArray(NIRtmp,j,i,numCols, numRows).astype(numpy.float)          #band 4
            maskn = numpy.not_equal((REDdata), 0)
            ndvi = (NIRdata - REDdata) / (NIRdata + REDdata)           
            outBand_data.WriteArray(ndvi, j, i)
            del ndvi, REDdata, NIRdata 
    endTime = time.time()
    print 'The NDVI Processing took ' + str(endTime - startTime) + ' seconds'
                

#RED = input("Input filename ")
#NIR = input("Input filename ")
RED='L5029032_03220020730_B30.tif'
NIR='L5029032_03220020730_B40.tif'
image_read_function(RED, NIR)

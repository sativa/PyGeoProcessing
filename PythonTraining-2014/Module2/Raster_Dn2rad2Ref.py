#Purpose: Digital Number to Radiance to Reflectance 
#Author: Baburao Kamble and Ayse Kilic 

 


# For Image Processing
from math import *
import numpy, os,time, datetime
from osgeo import gdalnumeric
from osgeo import gdal
from osgeo.gdal_array import *
from osgeo.gdalconst import *


dirpath='I:/2002/Path29-Row31/L5029031_03120020730/'
os.chdir(dirpath)


# Input from the MTL file 
#DN to radiance conversion factors
Lmax=[193.000,365.000,264.000,221.000,30.200,15.303 ,16.500]
Lmin = [-1.520,-2.840,-1.170,-1.510,-0.370,1.238,-0.150]
#Exo-Atmospheric band-wise irradiance
KEXO = [1983,1796,1536,1031,220,1,83.44]
sun_elevation = 51.3428710
doy = 268
latitude=31.40
longitute=-98.075
acq_time=time.strptime("17:00:54", "%H:%M:%S")

# Do not change equations unless you are sure about new invention ;)
# Constants calculations  
AcqTime=datetime.timedelta(hours=acq_time.tm_hour, minutes=acq_time.tm_min, seconds=acq_time.tm_sec).seconds+longitute/15*60*60
#seasonal correction for solar time 
SolarCor=(0.1645*sin(4*pi*(doy-81)/364)-0.1255*cos(2*pi*(doy-81)/364)-0.025*sin(2*pi*(doy-81)/364))*60
AcqTimeMin=AcqTime/60+SolarCor
#inverse relative distance factor (squared) for the earth-sun [unitless],
dr=1+0.033*cos(2*pi*doy/365)
#solar declination [radians], 
delta=0.409*sin(2*pi/365*doy-1.39)
#latitude at the center of the image [radians], 
phi=latitude/180*pi 
#solar time angle (hour angle) 
omega=pi/12*(AcqTimeMin/60-12)
# Solar zenith angle
cos_theta=sin(delta)*sin(phi)+cos(delta)*cos(phi)*cos(omega)





print(' import_images')
landsat = list()
for filename in os.listdir(dirpath):
    name, extension = os.path.splitext(filename)
    if extension.lower() == ".tif":
        landsat.append((filename))  

# Set our output file format driver
driver = gdal.GetDriverByName( 'GTiff' )
# Set our output files Projection parameters
# from input file number 1
tmp = gdal.Open(landsat[0])
geoT = tmp.GetGeoTransform()
proJ = tmp.GetProjection()
#empty memory 
del tmp

#Top Of Atmosphere Reflectance
for i in range (0,7):
    print ("Processing Band"+str(i+1))
    DN = LoadFile(landsat[i])
    
    #Rad=(Lmax[i]-Lmin[i])/(255.0-1)*(DN-1)+Lmin[i] 
    Refl=pi*(Lmax[i]-Lmin[i])/(255.0-1)*(DN-1)+Lmin[i] *dr**2/(KEXO[i]*cos_theta)
    output_filename='b0'+str(i+1)+'_ref.tif'
    #Create output file with projection
    out = OpenArray(Refl)
    #out.dtype = numpy.int
    out.SetGeoTransform( geoT )
    out.SetProjection( proJ )
    driver.CreateCopy(output_filename, out)
    #SaveArray(result, output_filename, 'GTiff')
    #Empty memory objects 
    del Refl, DN, out



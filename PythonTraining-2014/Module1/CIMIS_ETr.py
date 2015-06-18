# Program to calculate Evapotranspiration from the CIMIS data 
# Python Data Analysis-Script
# Author: Baburao Kamble 

# Please refer ASCE manual for Evapotranspiration equations 
# http://www.kimberly.uidaho.edu/water/asceewri/ascestzdetmain2005.pdf (Allen et al, 2005) 
import numpy, os, csv



# data reading , cleaning and adding header 

datapath='E:/Teaching/Python/GIS-WR/Module1/Module1'
os.chdir(datapath)

for filename in os.listdir(os.getcwd()):
            name, extension = os.path.splitext(filename)
            if extension.lower() == ".csv":
                print 'processing---' + str(filename) 
                with open(filename,"rb") as source:
                    rdr= csv.reader( source )
                    newfile='new_'+str(filename)
                    
                    if not os.path.exists("Output"):
                        os.makedirs("Output")
                    os.chdir("Output")    
                    with open(newfile,"wb") as result:
                        wtr= csv.writer(result)
    
                        wtr.writerow( ('Station_Id','Date' , 'Julian_Date' , 'Solar_Radiation_Average' , 'Average_Soil_Temperature' , 'Maximum_Air_Temperature' , 'Minimum_Air_Temperature' ,  'Average_Air_Temperature' ,  'Average_Vapor_Pressure' , 'Average_Wind_Speed' ,  'Precipitation' ,  'Maximum_Relative_Humidity' , 'Minimum_Relative_Humidity' ,  'Reference_ETo' ,  'Average_Relative_Humidity' ,  'Dew_Point' ,  'Wind_Run'))                    
                        for r in rdr:
                            #print (r[0], r[1], r[2], r[4], r[6], r[8], r[10], r[12], r[14], r[16], r[18], r[20], r[22], r[24], r[26], r[28], r[30])
                            wtr.writerow( (r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[11], r[12], r[13], r[14], r[15], r[16]) )

# Create latitude longtitude,elevation  variables 
latitude=33.655       
longitude=-114.558 
elev=270
# create and open output file with write permission
myoutputfile=open("ETr.csv", "wb" )
wtr= csv.writer(myoutputfile)
    
for filename in os.listdir(os.getcwd()):
    if 'new_' in filename:
            my_data = numpy.genfromtxt(filename, delimiter=',',names=True)
            DOY=my_data["Julian_Date"]
            Tmax=my_data['Maximum_Air_Temperature']
            Tmin=my_data['Minimum_Air_Temperature']
            RHmax=my_data["Maximum_Relative_Humidity"]
            RHmin=my_data["Minimum_Relative_Humidity"]            
            Rs = my_data["Solar_Radiation_Average"]
            Windspeed=my_data["Average_Wind_Speed"]
            
            #Tmean=(Tmax+Tmin)/2
            Tmean= (Tmax+Tmin)/2
            #Atmospehric Pressure 
            AtmP=101.3*numpy.power((293-0.065*elev)/293, 5.26)
            #Psychrometric Constant
            Psy=0.000665*my_data["Average_Vapor_Pressure"]   
            #Slope Vapor Pressure Curve at air temperature T [kPa/C]
            SVP=4098*(0.6108*numpy.exp(17.27*Tmean/(Tmean+237.3)))/(numpy.power(Tmean+237.3, 2))
            # saturation vapor pressure [kPa]
            eO_Tmax=(0.6108*numpy.exp(17.27*Tmax/(Tmax+237.3)))
            eO_Tmin=(0.6108*numpy.exp(17.27*Tmin/(Tmin+237.3)))
                     
            es=(eO_Tmax+eO_Tmin)/2
            # actual vapor pressure [kPa]
            ea =((eO_Tmin *RHmax/100) + (eO_Tmax*RHmin/100))/2
            #Gsc = solar constant  [4.92 MJ m-2 h-1], 
            Gsc = 4.92                   
            #The inverse relative distance Earth-Sun
            dr = 1+0.033*numpy.cos(2*numpy.pi*DOY/365)
            #solar declination  [rad],
            delta = 0.409*numpy.sin(2*numpy.pi*DOY/365-1.39)
            #convert latitude into  [rad], 
            phi = (numpy.pi/180)*latitude
            # sunset hour angle
            ws = numpy.arccos(-1*numpy.tan(phi)*numpy.tan(delta))            
            Ra = (24/numpy.pi)*Gsc*dr*(ws*numpy.sin(phi)*numpy.sin(delta)+numpy.cos(phi)*numpy.cos(delta)*numpy.sin(ws))            
            # Solar Radiantion
            
            Rs = 0.0864*Rs         # covert the W m-2 into MJ m-2 day-1
            #Clear-sky solar radiation
            Rso = (0.75+2*numpy.power(10,-5)*elev)*Ra        # MJ m-2 day-1                      
            # Stefan-Boltzmann constant [4.901 x 10-9 MJ K-4 m-2 d-1]           
            stefn_boltzman=4.901e-09
            # cloudiness function [dimensionless]
            fcd=1.35*(Rs/Rso)-0.35
            #net long-wave radiation [MJ m-2 d-1],
            Rnl = stefn_boltzman*fcd*(0.34-0.14*numpy.power(ea,0.5))*(numpy.power(Tmax+273.16,4)+numpy.power(Tmin+273.16,4))/2 
            #Net Radiation (Rn )
            #Rn=Rs-Rnl    
            # net solar or short-wave radiation [MJ m-2 h-1],             
            Rn=(1-0.23)*Rs-Rnl    
            # daily soil heat flux density [MJ m-2 d-1].     
            G=0
            # height of wind measurement above ground surface [m].
            zw=2
            #Tall Reference constant  
            CnT=1600
            CdT=0.38        
            u2 = 4.87*Windspeed/(numpy.log(67.8*zw-5.42))   
            #Standardized reference crop evapotranspiration for Tall crop      
            ETr=((0.408*SVP*(Rn-G)+Psy*(CnT/(Tmean+273))*u2*(es-ea))/(SVP+Psy*(1+CdT*u2)))
            #Short Reference constant  
            CnS=900
            CdS=0.34 
            #Standardized reference crop evapotranspiration for Short crop          
            ETo=((0.408*SVP*(Rn-G)+Psy*(CnS/(Tmean+273))*u2*(es-ea))/(SVP+Psy*(1+CdS*u2)))
            rows = zip(DOY,Tmin,Tmax,RHmin,RHmax,Rs,Windspeed,es,ea,delta,fcd,Ra,Rs,Rso,Rnl, Rn, ETr, ETo)
            wtr.writerow(["DOY","Tmin","Tmax","RHmin","RHmax","Rs","Windspeed","es","ea","delta","fcd","Ra","Rs","Rso","Rnl", "Rn", "ETr","ETo"])
            for row in rows:
                wtr.writerow(row)
            print ("Done")
            myoutputfile.close()
          
            
            
import numpy as np 
from netCDF4 import Dataset
import glob
import geopandas as gpd
import pyproj
import sys
import pdb 
import datetime
import pickle 
import argparse
import os 
import importlib
import matplotlib.pyplot as plt
#homebrewed
import stationdata


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='to create station data pickle from 000.nc files')
    parser.add_argument('-i','--input', help='Input run name',required=True)
    args = parser.parse_args()

    runName = args.input
    inputConfig = importlib.machinery.SourceFileLoader('config_'+runName,os.getcwd()+'/config/config_'+runName+'.py').load_module()

    plotname        = inputConfig.params['plotname']
    dirStationLoc   = inputConfig.params['dirStationLoc']
    dirStationPicke = inputConfig.params['dirStationPicke']

    shapefile_path = glob.glob(dirStationLoc+'stationLocationMNH*'+'.shp')[0]
    
    # Read the shapefile
    gdf = gpd.read_file(shapefile_path)

    stations = []
    for station_name in gdf.name.unique():
        # Deserialize the object from the file
        with open("{:s}/{:s}-{:s}.pkl".format(dirStationPicke,plotname,station_name), "rb") as file:
            stations.append( pickle.load(file))

    fig = plt.figure(figsize=(10,5))
    #plot 2m wind
    ii = 0
    for station in stations:
        if '02' in station.name: 
            ax = plt.subplot(211)
            plt.plot(station.datetime.values, station.MER_WIND.values,label=station.name)
            if ii == 0:
              ax.set_ylabel('MERIDIONAL_WIND (m/s)')  
            ax = plt.subplot(212)
            plt.plot(station.datetime.values, station.ZON_WIND.values,label=station.name)
            if ii == 0:
              ax.set_ylabel('ZONAL_WIND (m/s)')  
            if ii==3:
                ax.legend()
            ii +=1  
    #plt.show()
    fig.savefig('station02m_mer_zonWind.png')
    plt.close(fig)

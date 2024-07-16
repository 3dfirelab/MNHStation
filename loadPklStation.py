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

    station = []
    for station_name in gdf.name.unique():
        # Deserialize the object from the file
        with open("{:s}/{:s}-{:s}.pkl".format(dirStationPicke,plotname,station_name), "rb") as file:
            station.append( pickle.load(file))

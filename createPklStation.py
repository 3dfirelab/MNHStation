import numpy as np 
from netCDF4 import Dataset
import glob
import geopandas as gpd
import sys
import pdb 
import pickle 
import importlib
import argparse
import os 

#homebrewed
import stationdata
import config

if __name__ == '__main__':

    importlib.reload(stationdata)

    parser = argparse.ArgumentParser(description='to create station data pickle from 000.nc files')
    parser.add_argument('-i','--input', help='Input run name',required=True)
    args = parser.parse_args()

    runName = args.input
    inputConfig = importlib.machinery.SourceFileLoader('config_'+runName,os.getcwd()+'/config/config_'+runName+'.py').load_module()

    plotname        = inputConfig.params['plotname']
    dirMNHFiles     = inputConfig.params['dirMNHFiles']
    dirStationLoc   = inputConfig.params['dirStationLoc']
    dirStationPicke = inputConfig.params['dirStationPicke']
        
    # Read the shapefile
    shapefile_path = glob.glob(dirStationLoc+'stationLocationMNH*'+'.shp')[0]
    gdf = gpd.read_file(shapefile_path)

    inputfiles = sorted(glob.glob(dirMNHFiles+ 'F{:s}.4.SP0*.000*.nc'.format(plotname.upper())))
    
    for station_name in gdf.name.unique():
        print(station_name)
        station_sp = []
        
        for inputfile in inputfiles:
            nc = Dataset(inputfile,'r')
            
            ncvarnames_all = nc.variables.keys()

            ncvarnames_station = []
            for name_ in ncvarnames_all:
                if station_name in name_:
                    ncvarnames_station.append(name_)

            station_ = stationdata.StationData(station_name)
            for name_ in ncvarnames_station:
                if ('PROC' not in name_) & ('DATIM' not in name_): continue

                station_.loadVar(nc[name_])

            station_sp.append(station_)

        station_allTime = stationdata.StationData.concatenate(station_sp)

        # Serialize the object to a file
        with open("{:s}/{:s}-{:s}.pkl".format(dirStationPicke,plotname,station_name), "wb") as file:
            pickle.dump(station_allTime, file)


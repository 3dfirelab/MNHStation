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
import f90nml
import datetime 

#homebrewed
import stationdata
import config

#####################################################
def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)


#####################################################
if __name__ == '__main__':
#####################################################

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
    ensure_dir(dirStationPicke)
    dirFFConfig     = inputConfig.params['dirFFConfig']    

    #read ff config to get ignition time in MNH time line
    ffnam =f90nml.read(dirFFConfig+'ff-param.nam')
    
    # Read the shapefile
    shapefile_path = glob.glob(dirStationLoc+'stationLocationMNH*'+'.shp')[0]
    gdf = gpd.read_file(shapefile_path)

    inputfiles = sorted(glob.glob(dirMNHFiles+ 'F{:s}.4.SP*.000*.nc'.format(plotname.upper())))
    
    print('globed inputFiles:')
    for inputfile in inputfiles:
        print('   - {:s}'.format(os.path.basename(inputfile)))
    print('')
    print('following stations are read:')
    for ist, station_name in enumerate(gdf.name.unique()):
        print(station_name)
        station_sp = []
        
        for iff, inputfile in enumerate(inputfiles):
            nc = Dataset(inputfile,'r')
            if (ist == 0) & (iff == 0):
                MNHrefTime = getattr(nc.variables['time'],'units').split('since')[1].strip().split('+')[0].strip()
                MNHIgniTime = datetime.datetime.strptime(MNHrefTime, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(seconds=int(ffnam['ff_ronan']['ignitiontime'])) 
            ncvarnames_all = nc.variables.keys()

            ncvarnames_station = []
            for name_ in ncvarnames_all:
                if station_name in name_:
                    ncvarnames_station.append(name_)

            station_ = stationdata.StationData(station_name,MNHIgniTime)
            for name_ in ncvarnames_station:
                if ('PROC' not in name_) & ('DATIM' not in name_): continue

                station_.loadVar(nc[name_])

            station_sp.append(station_)

        station_allTime = stationdata.StationData.concatenate(station_sp,MNHIgniTime)

        # Serialize the object to a file
        with open("{:s}/{:s}-{:s}.pkl".format(dirStationPicke,plotname,station_name), "wb") as file:
            pickle.dump(station_allTime, file)


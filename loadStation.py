import numpy as np 
from netCDF4 import Dataset
import glob
import geopandas as gpd
import pyproj
import sys
import pdb 
import datetime
import pickle 

#homebrewed
import stationdata


if __name__ == '__main__':

    plotname = 'sha1'
    dirStationLoc = './StationLocSha1/'
    dirStationPicke = './StationPickeSha1/'

    shapefile_path = glob.glob(dirStationLoc+'stationLocationMNH*'+'.shp')[0]
    
    # Read the shapefile
    gdf = gpd.read_file(shapefile_path)

    station = []
    for station_name in gdf.name.unique():
        # Deserialize the object from the file
        with open("{:s}/{:s}-{:s}.pkl".format(dirStationPicke,plotname,station_name), "rb") as file:
            station.append( pickle.load(file))

# MNHStation
This code load the data from station written with MNH.544
directory are set in `config/config_sha1.py` for example.
run 
```
run createPklStation.py -i sha1
```
to extract data from raw 000 MNH files. data is then saved in Pickle
to load the data from the pickle run 
```
run loadPklStation.py -i sha1
```


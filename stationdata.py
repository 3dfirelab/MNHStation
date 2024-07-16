import numpy as np
import datetime
import pdb 

class data:
    def __init__(self,values,comment):
        self.values = values
        self.comment = comment


class StationData:

    def __init__(self,name):
        self.name = name
    
    def loadVar(self,ncvar):
        if 'DATIM' in ncvar.getncattr('long_name'): 
            varname = 'datetime'
            val =  []
            for row in ncvar[:-1]:
                val.append(datetime.datetime.strptime('{:4.0f}-{:02.0f}-{:2.0f}'.format(*row[-4:-1]),'%Y-%M-%d') + datetime.timedelta(seconds=row[-1]))
            var = data(val,'-')
        else:
            varname = ncvar.getncattr('comment').split('-')[0].strip()
            var = data(np.squeeze(ncvar[:].data)[:-1],ncvar.getncattr('comment').split('-')[1].strip())
        
        setattr(self,varname, var)


    def concatenate(station_sp):
        variables = station_sp[0].__dict__
        new=StationData(station_sp[0].name)
        
        for varname in variables.keys():
            if varname =='name': continue
            data_ = getattr(station_sp[0], varname)
            comment_ = data_.comment
            values = []
            for ist, station_ in enumerate(station_sp):
                
                data_ = getattr(station_, varname)
                len_ = len(data_.values)
                
                ivalb = 0 if ist == 0 else 1
                ivale = len_ if ist == len(station_sp)-1 else len_-1
                for val in data_.values[ivalb:ivale]:
                    values.append(val)

            var = data(np.array(values), comment_)
            
            setattr(new,varname, var)

        return new

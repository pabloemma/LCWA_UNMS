'''
Created on Aug 19, 2020

@author: klein
'''
import json
import pandas as PD
from collections.abc import MutableMapping


class JsonRead(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.AllData = []  # has all the data in it

        #remove limits on columns and rows
        PD.set_option('display.max_rows', 10)
        PD.set_option('display.max_columns', 500)
        
    def ReadFile(self,filename):
        """
        Reads json file
        """
        with open(filename, "r") as read_file:
            self.data = json.load(read_file)
            if isinstance(self.data,list):
                for k in range(0,len(self.data)):
                    self.IterDict(self.data[k])
                    print('\n ******************************* \n')
            else:
                self.IterDict(self.data)
                
    def ReadData(self,data):
            
        self.data = json.loads(data)
        if isinstance(self.data,list):
            for k in range(0,len(self.data)):
                self.IterDict(self.data[k])
                
                print('\n ***************************\n')
            else:
                self.IterDict(self.data)
  
    def IterDict(self,dictionary):
        """ Iterates through nested dictionaries
        """
        flat_dict = {}   # the flattened dictionary
        if isinstance(dictionary,dict):
        
            for k,v in dictionary.items():
                if isinstance(v,dict):
                # we have a nested dictionary
                    self.IterDict(v)
                    print(" inner dict",v)
                else:
                    if(v != None):
                        print(k, ":",v)
                    else:
                        print(k ,": None")
        else:
            print(" we have a list")
            
            self.IterDict(dictionary[0])

    
    def CreatePandas(self):

        """ converts dictionaries into panda data structure
            where the data have been read into self.data
        """
        # loop over all the data and create a list of dictionaries
        for k in range(0,len(self.data)):
            flat_dict = self.FlatMyDict(self.data[k])
            self.AllData.append(flat_dict)
        # Now we have all in a list, we can create a large Pandas frame
        self.AllDataFrame = PD.DataFrame(self.AllData)
        print(self.AllDataFrame)

    def FilterSSID(self,filter):
        """this removes rows acoording to filter, where filter is a tuple"""
        self.AllDataFrameFiltered = self.AllDataFrame[self.AllDataFrame[filter[0]].str.startswith(filter[1], na=False)]
        
        pass

    def FilterPandas(self.filter):
        """ removes rows according to filter"""
        self.AllDataFrameFiltered.drop(self.AllDataFrameFiltered[self.AllDataFrameFiltered[filter[0]] != filter[1]].index, inplace = True)
        return

        

    def Pandas2CSV(self,filename):
        """converts pandas into csv file"""
        self.AllDataFrameFiltered.to_csv(filename)
        return

    def FlatMyDict(self,data: MutableMapping, sep: str= '.') -> MutableMapping:
        """ flattens the dictionary into one"""  
        [flat_dict] = PD.json_normalize(data, sep=sep).to_dict(orient='records')
        return flat_dict
      

if __name__ == '__main__':
    filename='/home/klein/scratch/AP.json'
    JR = JsonRead()
    JR.ReadFile(filename)
    JR.CreatePandas()
    filter = ['ssid','LCWN']
    JR.FilterSSID(filter)
    JR.Pandas2CSV('/home/klein/scratch/AP.csv')
    #JR.FlatMyDict()
    
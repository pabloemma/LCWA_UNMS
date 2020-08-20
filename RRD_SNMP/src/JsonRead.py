'''
Created on Aug 19, 2020

@author: klein
'''
import json


class JsonRead(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def ReadFile(self,filename):
        """
        Reads json file
        """
        with open(filename, "r") as read_file:
            self.data = json.load(read_file)
            if isinstance(self.data,list):
                for k in range(0,len(self.data)):
                    self.IterDict(self.data[k])
                    print('\n\n')
            else:
                self.IterDict(self.data)
                
    def ReadData(self,data):
            
        self.data = json.loads(data)
        if isinstance(self.data,list):
            for k in range(0,len(self.data)):
                self.IterDict(self.data[k])
                print('\n\n')
            else:
                self.IterDict(self.data)
  
    def IterDict(self,dictionary):
        """ Iterates through nested dictionaries
        """
        if isinstance(dictionary,dict):
        
            for k,v in dictionary.items():
                if isinstance(v,dict):
                # we have a nested dictionary
                    self.IterDict(v)
                else:
                    if(v != None):
                        print(k, ":",v)
        else:
            " we have a list"
            
            self.IterDict(dictionary[0])
            
                
            

if __name__ == '__main__':
    filename='/Users/klein/scratch/respo.json'
    JR = JsonRead()
    JR.ReadFile(filename)
    
'''
Created on Jul 25, 2020

@author: klein
'''

import datetime
import sys
import os



class MyError(object):
    '''
    simple class to deal with errors or messages in a program
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        self.program_name = os.path.basename(__file__)
        
        

    def Logging(self,program_name=None,message=None):
        """
        prints out erroro message with time
        """
        if(program_name == None):
            program_name =  self.program_name
        print(datetime.datetime.now(),program_name+' error > ',message)
        return
    
    
if __name__ == '__main__':
    MyE =MyError()
    MyE.Logging(message='this is a test')
    
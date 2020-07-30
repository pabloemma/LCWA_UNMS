'''
Created on Jul 26, 2020

@author: klein
'''


import json
import requests
import sys
from MyError  import MyError 
import platform
import argparse as argp
import textwrap
import os
from Request import RestRequest

class UNMSControl(object):
    '''
    establish  connection with UNMS
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.session = requests.Session()
        self.ME=MyError()
        self.program_name = os.path.basename(__file__)
 
        
        
        
    def Initialize(self):
        """
        Initialize the system
        """
        
        self.url ="https://{0}/nms/api/v2.1".format(self.Host)
        
        self.session.verify = ssl_verify = False
        
        
        #Instantiate the request system
    
        REQ = RestRequest(self.url)
        
            
    def Login(self):
        """
        Login to system
        """
        json_dict={'username':self.user,'password':self.password,'mobilePlatform':'ios','sessionTimeout':'0'}
        action = '/user/login'
        
        data = self.SessionPost(action,json_dict)
        self.auth_token =data['x-auth-token'] 
  
        return data

 
    
    
    
    def SessionPost(self,action,json_dict,content_type = None,auth_token = None):    
        """
        interface to the request system, specifially the post
        """
        
        #convert dict into json format
        json_dump = json.dumps(json_dict)
        api = self.url+action

        if not content_type:
            content_type = {'Content-Type': 'application/json'}
        else:
            content_type = {'Content-Type': content_type}

        self.headers = content_type

        if auth_token:
            self.headers['x-auth-token'] = auth_token


        
        
        
        
        try:
            #response = self.session.post(api,data = json_dump)
            response = self.session.request('POST',api,headers=self.headers,data = json_dump)
        except:
            message = " Problem with connecting to {0}".format(self.Host)
                       
            self.ME.Logging(self.program_name,message)
            sys.exit(0)
        
        

        #error handling
        
        if response.status_code in [200, 201]:
            try:
                json_data = json.loads(response.text)
                json_data['x-auth-token'] = response.raw.getheader('x-auth-token')
            except:
                try:
                    json_data = json.loads(response.text)
                except:
                    json_data = response.text
            return json_data
        else:
            message = 'Error Code: ' + str(response.status_code) + ' Data: ' \
                      + str(response.content)

            if response.status_code in [400, 404, 405, 415]:
                raise ValueError(message)
            elif response.status_code in [401]:
                raise PermissionError(message)
            elif response.status_code in [500, 503, 504]:
                raise ConnectionError(message)
            else:
                raise RuntimeError(message)

    
    def TestConnection(self):
        
        
        # make json data load; json needs a string dictionart
        json_load={'username':self.user,'password':self.password,'mobilePlatform':'ios','sessionTimeout':'0'}
        json_dump = json.dumps(json_load)
        
        #create login
        api = self.url +'/user/login'
        print(api)
        
        message = self.session.post(api,data = json_dump)
        
        print(message)
       # self.test = json.loads(message.headers)
        #print(message.content)
        #for lines in message.iter_lines(chunk_size=512, decode_unicode=None, delimiter=None):
        #    print(lines)
        #print (message.headers)
        print(type(message.content))
        json_data =  json.loads(message.content)
        print(json_data)
        for x, y in json_data.items():
            print(x, y)
  
        print(message.headers)
        for x, y in message.headers.items():
            print(x, y)
        
        print(message.headers['x-auth-token'])
       
    

       


    def GetArguments(self):
        """
        this method deals with arguments parsed on command line
        """
        #instantiate the parser
        parser = argp.ArgumentParser(
            prog='UNMSControl',
            formatter_class=argp.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent('''
            program to control UNMS 
             
             
             '''))

        
        # now we build up the different args we can have
        parser.add_argument("-p","--password",help = "Password" )
        parser.add_argument("-u","--user",default='admin',help = "User name" )
        parser.add_argument("-H","--Host",help = "IP address" )

        #parser.add_argument("-ip","--ip=ARG",help = "Attempt to bind to the specified IP address when connecting to servers" )
        
        
        
        #list of argument lists
        
        
        # here some of the defaults
        #Of courss Mac has the stuff in different places than Linux
        if platform.system() == 'Darwin':
            temp1=["/usr/local/bin/timeout","-k","300","200","/usr/local/bin/speedtest","--progress=no","-f","csv"] # we want csv output by default
        elif platform.system() == 'Linux':
            temp1=["/usr/bin/timeout", "-k", "300"," 200","/usr/bin/speedtest","--progress=no","-f","csv"] # we want csv output by default         
        # do our arguments
        else:
            print(' Sorry we don\'t do Windows yet')
            sys.exit(0)
        args = parser.parse_args()
        
        
        # deal with the arguments
        if(args.password != None):
            self.password=args.password
        else:
            self.ME.Logging(self.program_name,message = 'You need to provide a password')
            sys.exit(0)
            
        if(args.Host != None):
            self.Host=args.Host
        else:
            self.ME.Logging(self.program_name,message = 'You need to provide a Host')
            sys.exit(0)
 
        self.user=args.user




        #for k in dir(message):

         #   print (k)
        #for x, y in message.content.items():
        #    print(x, y)
        #print(message.raw)
        #print(message.request)
        
            
if __name__ == '__main__':
    MyC =UNMSControl()
    MyC.GetArguments()
    MyC.Initialize()
    MyC.Login()
    #MyC.FirstTest()
    #MyC.TestConnection()
    #MyC.FetchUser()

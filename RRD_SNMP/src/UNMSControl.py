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
    
        #REQ = RestRequest(self.url)
        
            
    def Login(self):
        """
        Login to system
        """
        json_dict={'username':self.user,'password':self.password,'mobilePlatform':'ios','sessionTimeout':'0'}
        action = '/user/login'
        
        data = self.SessionPost('POST',action,json_dict)
        self.auth_token =data['x-auth-token'] 
  
        return data

    def Logout(self,):
        """
        at the end of the session log out
        """
        
        json_dict={'username':self.user,'password':self.password,'mobilePlatform':'ios','sessionTimeout':'0'}
        action = '/user/logout'
        
        data = self.SessionPost('POST',action,json_dict, auth_token = self.auth_token)

        self.ME.Logging(self.program_name,data['message'])
        
        return data
  
    def GetUser(self):
        """
        Info about current user
        """
        
        #json_dict={'username':self.user,'password':self.password,'mobilePlatform':'ios','sessionTimeout':'0'}
        action = '/user'
        
        data = self.SessionPost('GET',action, auth_token = self.auth_token)

        #for x, y in data.items():
        #    print(x, y)
        print('username : ',data['username'])
        print('email : ',data['email'])

       
        return data

    def GetSiteID(self):
        """ retunrs the site id given the site name
        The sitename comes from command line arguments
        """
        
        if(self.sitename == None):
            self.ME.Logging(self.program_name,'You need to provide a sitename inorder to get the SiteID')
            sys.exit(0)
            
        action = '/sites/search'
        
        # make the query string
        q_string = '?query='+self.sitename+'&count=100&page=1'
                
        
        data = self.SessionPost('GET',action+q_string,auth_token = self.auth_token)
        
        
        #for k in range(len(data)):
        #    print(data[0]['identification'])
        
        #print(data)
        self.siteID = data[0]['identification']['id']
        self.siteParentID = data[0]['identification']['parent']
        print("the SiteID for ",self.sitename,'  is ',data[0]['identification']['id'])
        print(" \n\n\n***********The information for the parent is :*********")
        
        
        
        for x,y in data[0]['identification']['parent'].items():
            print(x,y)
        
        return data


    def GetSiteDetails(self):
        """
        Prints out details of a site.
        You need the siteid, which reuires to run GetSiteID first
        """
        
        if(self.siteID == None):
            self.ME.Logging(self.program_name,'No siteid found, probably need to run GetSiteID first')
            sys.exit(0)
        
        action = '/sites/'
        
        # make the query string
        q_string = self.siteID
                
        
        data = self.SessionPost('GET',action+q_string,auth_token = self.auth_token)
        
        print(data)
        print(type(data))
        #self.PrintDict(data['identification'])
        #self.PrintDict(data['identification']['parent'])
        #self.PrintDict(data['description'])
        #self.PrintDict(data['identification'])
        return data
            
    def GetSiteStatistic(self):
        """
        Returns traffic statistic bewteen siteID and parent
        The result is in two lists of dictionaries each {x=time,y=rate)
        self.upload and sel.download
        
        """
        if(self.timeinterval == None):
            self.ME.Logging(self.program_name,'No No Timeinterval found for statistics')
            sys.exit(0)
        action = '/sites/'
 
        q_string = self.siteID+'/statistics?interval='+self.timeinterval+'&siri=false'

        data = self.SessionPost('GET',action+q_string,auth_token = self.auth_token)
        
        self.download = data['download']
        self.upload = data['upload']
          #for k in range(len(data['download'])):
            #print(data['download'][k]['x'])
            #print(data['download'][k]['y'])
        
        

        #self.PrintDict(data['download'])
        

    def GetAircubeDetail(self):
        """ if there is an aircube we can get details of it
        """
        #first we determine if there is an aircube
        
        action = '/devices'
        
        #First we determine if there is an aircube
        
        q_string = '?siteId='+self.siteID+'&withInterfaces=false&authorized=true&type=airCube'
        data = self.SessionPost('GET',action+q_string,auth_token = self.auth_token)
        try:
            self.aircubeID = data[0]['identification']['id']
           
        except:
            self.ME.Logging(self.program_name,'No aircube found')
            return 
        
        #Now that we found an aircube lets get the detaisl of this puppy
        
        q_string='/aircubes/self.airCubeID'
            
        self.PrintDict(data[0])   
        
        return data
    
    
    
    def PrintDict(self, dict):
        """ prints dictionary """
        
        test = json.dumps(dict)
        
        for p_id, p_info in dict.items():
            print( '\n\n ******************  ',p_id,' *************************** \n')
            
            
            try:
                for key in p_info:
                    print(key + ':', p_info[key])
            except:
                print(p_info)


    

    
    
    def SessionPost(self,verb,action,json_dict=None,content_type = None,auth_token = None):    
        """
        interface to the request system, this is the heart of everything.
        """
        
        #convert dict into json format
        json_dump = json.dumps(json_dict)
        api = self.url+action

        if not content_type:
            content_type = {'Content-Type': 'application/json'}
        else:
            content_type = {'Content-Type': content_type}

        self.headers = content_type

        if (auth_token != None):
            self.headers['x-auth-token'] = auth_token
        


        
        
        
        
        try:
            #response = self.session.post(api,data = json_dump)
            response = self.session.request(verb,api,headers=self.headers,data = json_dump)
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
        parser.add_argument("-S","--SiteName",help = "name of the site to look for" )

        parser.add_argument("-T","--TimeInterval",help = "time interval for statistics, hour,day,month" )

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
        

        
        if(args.SiteName != None):
            self.sitename=args.SiteName
 
        if(args.TimeInterval != None):
            self.timeinterval=args.TimeInterval
        else:
            self.timeinterval = None


        
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
    MyC.GetUser()
    MyC.GetSiteID()
    MyC.GetSiteDetails()
    MyC.GetSiteStatistic()
    MyC.GetAircubeDetail()
    MyC.Logout()
    #MyC.FirstTest()
    #MyC.TestConnection()
    #MyC.FetchUser()

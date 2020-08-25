'''
Created on Jul 26, 2020

@author: klein
'''


import json
import requests
import sys
import platform
import argparse as argp
import textwrap
import os
import yaml

import urllib3
import numpy as np

#ak import
from MyError  import MyError 
from PlotUNMS  import PlotUNMS
from JsonRead import  JsonRead



class UNMSControl(object):
    '''
    establish  connection with UNMS
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.session = requests.Session()
        self.ME = MyError()
        self.JR = JsonRead()
        self.program_name = os.path.basename(__file__)
        
        self.PA = PlotUNMS()
                
        self.logtag = 'login'
        self.output_dirname = None # output directory for outputfiles

        
        
        
        # to suppress the insecure request warnings
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
      
        
        
        
    def Initialize(self, host = None , debug = None ):
        """
        Initialize the system
        """
        
        if (host != None):
            self.Host = host
        self.url ="https://{0}/nms/api/v2.1".format(self.Host)
        
        self.session.verify = ssl_verify = False
        
       #Here we initalize some of the values which in the standalone version would be given by CLI arguments
            
    def SetDebugLevel(self,debuglevel):
        """
        sets the debuglevel, mostlu used from GUI
        """
        self.debug = debuglevel
        return
            
    def Login(self):
        """
        Login to system
        """
        json_dict={'username':self.user,'password':self.password,'mobilePlatform':'ios','sessionTimeout':'0'}
        action = '/user/login'
        
        data = self.SessionPost('POST',action,json_dict)
        self.auth_token =data['x-auth-token'] 
  
        return data

    def Logout(self):
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

    def GetSiteID(self,sitename = None):
        """ retunrs the site id given the site name
        The sitename comes from command line arguments
        """
        if sitename != None:
            self.sitename = sitename
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
        try: 
            self.siteID = data[0]['identification']['id']
            self.siteParentID = data[0]['identification']['parent']['parentId']
            print("the SiteID for ",self.sitename,'  is ',data[0]['identification']['id'])
            print(" \n\n\n ***********The information for the parent is :*********")
            print("the SiteID for the parent is  ",self.siteParentID)

        except:
            self.ME.Logging(self.program_name,self.sitename+' not found')
        
        
        if self.debug == 1:
            #self.PrintDict1(data[0])
            self.JR.ReadData(json.dumps(data))
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
        
        if self.debug == 1:
            #self.PrintDict1(data)
        #self.JsonInterface(data)
            self.JR.ReadData(json.dumps(data))
        return data
            
    def GetSiteStatistic(self , timeinterval = None):
        """
        Returns traffic statistic bewteen siteID and parent
        The result is in two lists of dictionaries each {x=time,y=rate)
        self.upload and sel.download
        
        """
        if(timeinterval != None):
            self.timeinterval = timeinterval
        if(self.timeinterval == None):
            self.ME.Logging(self.program_name,'No No Timeinterval found for statistics')
            sys.exit(0)
        action = '/sites/'
 
        q_string = self.siteID+'/statistics?interval='+self.timeinterval+'&siri=false'

        data = self.SessionPost('GET',action+q_string,auth_token = self.auth_token)
        
        self.download = data['download']
        self.upload = data['upload']
        
        # determine length of array
        

        self.dl_array = np.array([]) # download data
        self.ul_array =  np.array([])#upload data
        self.time_array = np.array([]) #Unix time stamp
        
        for k in range(len(data['download'])):
            if data['download'][k]['y'] != None:
                self.dl_array = np.append(self.dl_array,data['download'][k]['y'])
                self.ul_array = np.append(self.ul_array,data['upload'][k]['y'])
                self.time_array = np.append(self.time_array,data['download'][k]['x']/1000) #time is in milliseconds
        
        print('debug',self.debug)      
        if(self.debug == 2):
            for k in range(len(data['download'])):
                print(data['download'][k]['x'],data['download'][k]['y'])
                print(data['upload'][k]['x'],data['upload'][k]['y'])
        
        

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
            
        #if self.debug == 1:
            #self.PrintDict1(data[0])
        self.JR.ReadData(json.dumps(data))
        
        return data
    
    def GetAircubeNetwork(self):
        """
        control aircube
        """
        action = '/devices/'
        
        #First we determine if there is an aircube
        
        q_string = 'aircubes/'+self.aircubeID+'/network'

        data = self.SessionPost('GET',action+q_string,auth_token = self.auth_token)
        
        self.JR.ReadData(json.dumps(data))

        return data
        
     
    def GetAircubeWireless(self):
        """
        control aircube
        """
        action = '/devices/'
        
        #First we determine if there is an aircube
        
        
        q_string = 'aircubes/'+self.aircubeID+'/wireless'

        data = self.SessionPost('GET',action+q_string,auth_token = self.auth_token)
        
        self.JR.ReadData(json.dumps(data))

        return data
         
    def GetAircubeSystem(self):
        """
        control aircube
        """
        action = '/devices/'
        
        #First we determine if there is an aircube
        
        
        q_string = 'aircubes/'+self.aircubeID+'/system'

        data = self.SessionPost('GET',action+q_string,auth_token = self.auth_token)
        
        self.JR.ReadData(json.dumps(data))


        outfil = 'LCWA_Aircube.txt'

        if(self.output_dirname != None):
            AirCubeoutput_file = self.output_dirname +outfil
        else:
            AirCubeoutput_file = os.getcwd() + '/'+outfil
        self.ME.Logging(self.program_name,'Your AirCube list is in file '+AirCubeoutput_file)
        #self.JsonInterface(json.dumps(data),AirCubeoutput_file)
        self.JsonInterface(data,AirCubeoutput_file)



        return data
    
    def PutAircubeSystem(self):  
        """
        programs some of the aircube info
        """
        mydict = {"deviceName": "", 
                  "timezone": "",
                  "zonename": "",
                  "username": "",
                  "newPassword": "",
                  "ledNightMode": {
                  "enable": True,
                  "start": 0,
                  "end": 0
                  },
                  "poePassthrough": True,
                  "resetButtonEnabled": True
                  } 
        
        action = '/devices/'
        
        
        
        q_string = 'aircubes/'+self.aircubeID+'/system'
        
        
        print(" these are your choices for aircube system")
        
        self.PrintDict1(mydict)

        #data = self.SessionPost('Put',action+q_string,json_dict = mydict,auth_token = self.auth_token)

        return
    
    def GetAirmaxDetail(self):
        """ if there is an airmax we can get details of it
        """
        #first we determine if there is an aircube
        
        action = '/devices'
        
        #First we determine if there is an aircube
        
        q_string = '?siteId='+self.siteID+'&withInterfaces=false&authorized=true&type=airMax'
        data = self.SessionPost('GET',action+q_string,auth_token = self.auth_token)
        try:
            self.airmaxID = data[0]['identification']['id']
           
        except:
            self.ME.Logging(self.program_name,'No airmax found')
            return 
        
        #Now that we found an aircube lets get the detaisl of this puppy
        
        q_string='/airmaxes/self.airMaxID'
            
        #if self.debug == 1:
            #self.PrintDict1(data[0])
        self.JR.ReadData(json.dumps(data))
        
        return data
 
    def GetEdgeRouterDetail(self):
        """ if there is an edgerouter we can get details of it
        """
        #first we determine if there is an aircube
        
        return
        
        action = '/devices'
        
        #First we determine if there is an aircube
        
        q_string = '?siteId='+self.siteID+'&withInterfaces=false&authorized=true&type=airMax'
        data = self.SessionPost('GET',action+q_string,auth_token = self.auth_token)
        try:
            self.airmaxID = data[0]['identification']['id']
           
        except:
            self.ME.Logging(self.program_name,'No airmax found')
            return 
        
        #Now that we found an aircube lets get the detaisl of this puppy
        
        q_string='/airmaxes/self.airMaxID'
            
        #if self.debug == 1:
            #self.PrintDict1(data[0])
        self.JR.ReadData(json.dumps(data))
   
        
        #return data
 
 
    
    def GetSiteClients(self, idsite = None):
        """
        Provides a list of all the clients of a site
        Either it is the parent id of the given site; for instance in madre de dios
        the parent id would be the one of ridgeroad. Or is is given as an argument
        """
        if(idsite != None):
            id_test = idsite
        else:
            #id_test = self.siteParentID
            id_test = self.siteID
    
        action = '/sites'
        
        #First we determine if there is an aircube
        
        q_string = '/'+id_test+'/clients'
        data = self.SessionPost('GET',action+q_string,auth_token = self.auth_token)

        if self.debug == 1:
            try:
                self.PrintDict1(data[0])
            except:
                self.ME.Logging(self.program_name,message = ' No site clients  for ' +self.sitename)
         
        
        return data

    def GetAllAP(self):
        """
        returns a list of all access points
        """
        action = '/devices'
        q_string = '/aps/profiles'
        data = self.SessionPost('GET',action+q_string,auth_token = self.auth_token)

        outfil = 'LCWA_ALL_AP.txt'
        if(self.output_dirname != None):
            APoutput_file = self.output_dirname +outfil
        else:
            APoutput_file = os.getcwd() + '/'+outfil
        self.ME.Logging(self.program_name,'Your AP list is in file '+APoutput_file)
        self.data(json.dumps(data),APoutput_file)

        return data
    def GetAllSSID(self):
        """provides list of wireless ssid
        """
        action = '/devices'
        q_string = '/ssids'
        data = self.SessionPost('GET',action+q_string,auth_token = self.auth_token)


        outfil = 'LCWA_ALL_SSID.txt'
        if(self.output_dirname != None):
            SSIDoutput_file = self.output_dirname +outfil
        else:
            SSIDoutput_file = os.getcwd() + '/'+outfil
        self.ME.Logging(self.program_name,'Your SSID list is in file '+SSIDoutput_file)
        self.data,SSIDoutput_file)

        return data


    def GetDevicesDiscovered(self):
        """provides list of devices
        """
        action = '/devices'
        q_string = '/discovered'
        data = self.SessionPost('GET',action+q_string,auth_token = self.auth_token)

        self.JR.ReadData(json.dumps(data))
        return data

    def GetDeviceCredential(self):
        action = ''
        
        #First we determine if there is an aircube
        
        q_string = '/settings'
        data = self.SessionPost('GET',action+q_string,auth_token = self.auth_token)
        return data
    
    def GetUNMSSettings(self):
        
        action = '/vault'
        
        #First we determine if there is an aircube
        
        q_string = '/'+self.siteID+'/credentials'
        data = self.SessionPost('GET',action+q_string,auth_token = self.auth_token)
        return data

    def GetLogWarnings(self):  
        print('\n \n ************************  warning log **************************')
        action = '/logs'
        
        #First we determine if there is an aircube
        if(self.logtag != None):
        
            q_string = '?count=1000&page=1&level=warning&tag='+self.logtag
        else:
            q_string = '?count=1000&page=1&level=warning'
        data = self.SessionPost('GET',action+q_string,auth_token = self.auth_token)
        
        try:
            self.PrintLogs(data)
        except:
            self.ME.Logging(self.program_name,message = 'No print in log warning')
        print('\n ************************  end warning log **************************')

 
        
        return data
   
    def GetLogErrors(self):  
        action = '/logs'
        print('\n \n ************************  error log **************************')
        #First we determine if there is an aircube
        if(self.logtag != None):

            q_string = '?count=1000&page=1&level=error&tag='+self.logtag
        else:
            q_string = '?count=1000&page=1&level=error'
        data = self.SessionPost('GET',action+q_string,auth_token = self.auth_token)


        try:
            self.PrintLogs(data)
        except:
            self.ME.Logging(self.program_name,message = 'No print in log errors')

        print('\n ************************  end error log **************************')
        
        return data
          
        
    def CreateBackup(self):
        """ Backup of UNMS at server
        """
        action = '/backups/create'
        q_string = ''
        data = self.SessionPost('GET',action+q_string,auth_token = self.auth_token)
        if self.debug == 1:
            #self.PrintDict1(data[0])
            self.JR.ReadData(json.dumps(data))
            
        return data

   
    def PlotData(self):
        """
        Plot all the data
        """
        if(self.output_dirname == None):
            self.output_dirname = os.path.expanduser("~")+'/UNMS/output/'
        self.PA.PlotData(self.sitename,self.time_array,self.dl_array,self.ul_array,self.output_dirname)

    def PrintDict(self, dict):
        """ prints dictionary """
        
        test = json.dumps(dict)
        for p_id, p_info in dict.items():
            print( '\n\n ******************  ',p_id,' *************************** \n')
            
            if not p_info is None and isinstance(p_info,dict): 
            
                for key in p_info:

                    print(key + ':', p_info[key])
            else:
                print(p_info)
            
        #print(dict)
    def PrintDict1(self,dict):
        #pprint.pprint(dict, width = 1 ,depth =2,sort_dicts=True)
        
        print('\n *************** new AP listing ****************** \n')
            #self.PrintDict(self.allAP[k])
        print( yaml.dump(dict, default_flow_style=False))
        test = yaml.dump(dict, default_flow_style=False)
        try:
            print (dict['name'])
        except:
            pass
        print('\n ************************************************* \n \n \n')

        self.gen_dict_extract('id',dict)



    def gen_dict_extract(self,key, var):
        if hasattr(var,'iteritems'):
            for k, v in var.iteritems():
                if k == key:
                    yield v
                if isinstance(v, dict):
                    for result in self.gen_dict_extract(key, v):
                        yield result
                elif isinstance(v, list):
                    for d in v:
                        for result in self.gen_dict_extract(key, d):
                            yield result



    def PrintLogs(self, dict):
        """ prints dictionary """
        
        #test = json.dumps(dict)
        test = dict['items']
        for k in range(0,len(test)):
            #print (test[k]['device']['name'],'  ',test[k]['timestamp'],'  ',test[k]['message'])
            print('{:<30s}{:>40s}   {:<60s}'.format(test[k]['device']['name'],test[k]['timestamp'],test[k]['message']))
        return 
    
    
    def JsonInterface(self,data,filename):
        """
        Currently takes a jason result and writes it to file test.json
        """
        with open(filename, "w") as write_file:
            json.dump(data, write_file,sort_keys= True,indent = 4)
    
    
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
#            formatter_class=argp.RawDescriptionHelpFormatter,
            formatter_class=argp.RawTextHelpFormatter,
            epilog=textwrap.dedent('''
            program to control UNMS 
             
             
             '''))

        
        # now we build up the different args we can have
        parser.add_argument("-p","--password",help = "Password" )
        parser.add_argument("-u","--user",default='admin',help = "User name" )
        parser.add_argument("-H","--Host",help = "IP address" )
        parser.add_argument("-S","--SiteName",help = "name of the site to look for" )

        parser.add_argument("-T","--TimeInterval",help = "time interval for statistics, hour,day,month" )
        parser.add_argument("-d","--debug",help = "debug switch, 0: no debug, 1: print out results of different queries 2: lots of info" )
        parser.add_argument("-l","--logtag",help = textwrap.dedent('''\

                            logtag for logging
                                                    allowed values:
                                            
                                                    blank (gives everything)
                                                    device
                                                    login
                                                    site
                                                    device-state
                                                    device-backup
                                                    device-upgrade
                                                    device-interface
                                                    nms-backup
                                                    nms-error
                                                    nms-error''' ))

        #store_true prohibits input
        parser.add_argument("-V","--Version",action="store_true", help = "Prints out version number " )

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

        # debug level
        if(args.debug != None):
            self.debug=int(args.debug)
        else:
            self.debug = 0      # is also logical False

        if(args.Version != None):
            self.PrintVersion(silent = False)

        if(args.logtag != None):
            self.logtag = args.logtag
        
        self.user=args.user


    def SetOutputFile(self,dirname,filename):
        """ 
        calling this function will redirect all stdout to a file
        """
        
        self.output_dirname = dirname
        self.output_filename = dirname + filename
        self.ME.Logging(self.program_name,'You have chosen '+self.output_filename+' as output, \n all subsequent output will be found there')
        
        
        sys.stdout = open(self.output_filename, "w")
        
        
        
    def PrintVersion(self, silent = False):
        """ deals with version"""
        
        
        self.version = '2.1.5'
        self.versiontext = []
        
        self.versiontext.append('################ version : '+self.version+'  #######################')
        self.versiontext.append('version 1.0.0 : base version with limited functionality')
        self.versiontext.append('version 2.0.0 : base version with limited functionality and plots')
        self.versiontext.append('version 2.0.01 : added UNMS backup')
        self.versiontext.append('version 2.1.0 : stable version')
        self.versiontext.append('version 2.1.1 : added logwarnig and logerror')
        self.versiontext.append('version 2.1.2 : rewrote json output routine')
        self.versiontext.append('version 2.1.3 : added file output')
        self.versiontext.append('version 2.1.4 : save plot to file')
        self.versiontext.append('version 2.1.5 : uploading system to aircube')
        
        if silent == False :
        
            for k in range(0,len(self.versiontext)):
                print(self.versiontext[k])
        return self.version
    
        
if __name__ == '__main__':
    MyC =UNMSControl()
    MyC.GetArguments()
    MyC.Initialize()
    MyC.Login()
    MyC.SetOutputFile('/Users/klein/UNMS/output/','UNMS.txt')
    #MyC.GetLogWarnings()
    #MyC.GetLogErrors()
    #
    
    
    #MyC.GetUser()
    MyC.GetSiteID()
    #MyC.GetSiteDetails()
    #MyC.GetSiteStatistic()
    #MyC.PlotData()
    #MyC.GetAircubeDetail()
    #MyC.GetAirmaxDetail()
    #MyC.GetSiteDetails()
    MyC.GetAllAP()
    #MyC.GetAllSSID()
    #MyC.GetDevicesDiscovered()

    #MyC.CreateBackup()
    MyC.Logout()
    #MyC.FirstTest()
    #MyC.TestConnection()
    #MyC.FetchUser()

'''
Created on Jul 26, 2020

@author: klein
'''

from pyunifi.controller import Controller
import json
import requests

class ConnectUNMS(object):
    '''
    establish  connection with UNMS
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.user = user ='admin'
        self.password = password ='!LcwA!99'
        self.url ='https://172.16.2.200/nms/api/v2.1'
        # make requests saty persistent
        self.session = requests.Session()
        self.session.verify = ssl_verify = False
    
    def TestConnection(self):
        
        
        # make json data load; json needs a string dictionart
        json_load={'username':'admin','password':'!LcwA!99','mobilePlatform':'ios','sessionTimeout':'0'}
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
       
            
    def FetchUser(self):
        api=self.url+'/nms/devices'
        message = self.session.get(api)
        print(message)
        #print(message)
        #json_data =  json.loads(message.headers)
        print (dir(message))

        if message.status_code in [200, 201]:
            try:
                json_data = json.loads(message.text)
                json_data['x-auth-token'] = message.raw.getheader('x-auth-token')
                print (json_data)
            except:
                try:
                    json_data = json.loads(message.text)
                except:
                    json_data = message.text
        print (json_data)
        print(message.text)
        







        #for k in dir(message):

         #   print (k)
        #for x, y in message.content.items():
        #    print(x, y)
        #print(message.raw)
        #print(message.request)
        
            
if __name__ == '__main__':
    MyC =ConnectUNMS()
    #MyC.FirstTest()
    MyC.TestConnection()
    #MyC.FetchUser()

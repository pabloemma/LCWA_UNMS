'''
Created on Aug 17, 2020

@author: klein
'''

import wx
import sys
import os
import socket
import pprint
import subprocess as sp
import json
import yaml


from pubsub import pub
from UNMSControl import UNMSControl
from loginpanel import LoginFrame
from MyError  import MyError
from TagBox  import TagBox



class UNMSrun(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        MyC=UNMSControl()
        MyC.Login()
        MyC =UNMSControl()
        MyC.GetArguments()
        MyC.Initialize()
        MyC.Login()
        MyC.GetLogWarnings()
        MyC.GetLogErrors()
        #
        
        
        #MyC.GetUser()
        #MyC.GetSiteID()
        #MyC.GetSiteDetails()
        #MyC.GetSiteStatistic()
        #MyC.PlotData()
        #MyC.GetAircubeDetail()
        #MyC.GetAirmaxDetail()
        #MyC.GetSiteClients()
        #MyC.GetAllAP()
        #MyC.GetAllSSID()
        #MyC.GetDevicesDiscovered()
    
        #MyC.CreateBackup()
        MyC.Logout()
        #MyC.FirstTest()
        #MyC.TestConnection()
        #MyC.FetchUser()

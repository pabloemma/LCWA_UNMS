'''
Created on Aug 4, 2020

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
from datetime import datetime


from pubsub import pub
from UNMSControl import UNMSControl
from loginpanel import LoginFrame
from MyError  import MyError
from TagBox  import TagBox
from OutputFileDialog import OutputFileDialog
import HelpGUI


class MyWindow(wx.Panel):
    """
    Creates a panel
    with a box sizer
    label: str for different Texctrl boxes
    
    
    """
    
    
    def __init__(self,parent,ID=-1,label="",pos =(800,200),size = (100,50)):
        wx.Panel.___init(self,parent,ID,pos,size,wx.RAISED_BORDER, label )
        
        self.label = label
        self.BackgroundColour("white")
        self.SetMinSize(size)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
    
    
    def OnPaint(self,event):
        sz = self.GetClientSize()
        dc = wx.PaintDC()
        w,h = dc.CanGetTextExtent(self.label)
        dc.SetFont(self.GetFont())
        dc.DrawText(self.label,(sz.width-w)/2,(sz.height-h)/2)
        
        
        

class MyFrame(wx.Frame):
    """
    The main Frame class
    """
    
    def __init__(self,parent,id,title):
        
        
        #define the Frame style
        mystyle = wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP
        
        
        
        wx.Frame.__init__(self,parent,id,title,style = mystyle)
     
     
             #instantiate UNMSControl
        self.UNMS = UNMSControl()
        self.unmsversion = self.UNMS.PrintVersion(silent = True)

        
        self.version = 'UNMS GUI Control for LCWA'
        self.author = 'Andi Klein'
        self.date = 'Summer 2020 '
        self.UNMSversion = 'UNMS version  '+self.unmsversion
        now=datetime.now()
        self.dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
 
        panel = wx.Panel(self,-1)
        vs =wx.StaticText(panel,-1,self.version, (100,20),(160,-1),wx.ALIGN_LEFT)
        font1 = wx.Font(30,wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True)
        font2 = wx.Font(30,wx.FONTFAMILY_MODERN, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, True)
        vs.SetFont(font1)
        vk =wx.StaticText(panel,-1,self.author, (100,70),(160,-1),wx.ALIGN_LEFT)
        vl =wx.StaticText(panel,-1,self.date, (100,100),(160,-1),wx.ALIGN_LEFT)
        vm =wx.StaticText(panel,-1,self.UNMSversion, (100,130),(160,-1),wx.ALIGN_CENTER)
        vn =wx.StaticText(panel,-1,self.dt_string, (100,160),(160,-1),wx.ALIGN_RIGHT)
        font = wx.Font(20,wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True)
        vk.SetFont(font2)
        vl.SetFont(font)
        vm.SetFont(font)
        vn.SetFont(font)
   

        self.UNMS.SetDebugLevel(0) #default, can be changed
        
        self.CreateStatusBar()
        self.CreateToolBar()

        self.CreateMenu()
        pub.subscribe(self.my_listener, "panel_listener") #for passing event handler back and forth

        self.ME=MyError()
        
        
        self.program_name = os.path.basename(__file__)
        
        #log into the system
        #self.OnLogin(0)
 
        # Set size of Frame
        
    def CreateMenu(self):
        """
        creates the menu on the frame
        """
        menubar = wx.MenuBar()
        



        
        # section for quit, file etc
        file_menu = wx.Menu()
        menubar.Append(file_menu,"&File \tCTRL+F")

        self.CreateMenuItem(file_menu, "Quit",self.OnExit)

        #section for action
        action_menu = wx.Menu()
        menubar.Append(action_menu,"&Action \tCTRL+A")

        self.CreateMenuItem(action_menu, "Login",self.OnLogin)
        self.CreateMenuItem(action_menu, "Logout",self.OnLogout)
        
        
        self.CreateMenuItem(action_menu, "Debug Level",self.OnDebugLevel)
        self.CreateMenuItem(action_menu, "Output file",self.OnSetOutputFile)
        
        action_menu.InsertSeparator(2)
        
        #section for services
        service_menu = wx.Menu()
        menubar.Append(service_menu,"Services")

        item = wx.MenuItem(service_menu,wx.ID_NEW, "Get User"," username and email")
        service_menu.Append(item)
        self.Bind(wx.EVT_MENU,self.OnGetUser,item)
       
        item = wx.MenuItem(service_menu,wx.ID_NEW, "Get SiteID"," get site id for given sitename")
        service_menu.Append(item)
        self.Bind(wx.EVT_MENU,self.OnGetSiteID,item)
        
        self.CreateMenuItem(service_menu, "Get Site Details",self.OnGetSiteDetails)
        self.CreateMenuItem(service_menu, "Get Site Statistic",self.OnGetSiteStatistics)
        self.CreateMenuItem(service_menu, "Get Site Clients",self.OnGetSiteClients)
        self.CreateMenuItem(service_menu, "Get All APs",self.OnGetAllAP)
        self.CreateMenuItem(service_menu, "Get Devices discovered",self.OnGetDevicesDiscovered)
        self.CreateMenuItem(service_menu, "Get All SSID",self.OnGetAllSSID)
        self.CreateMenuItem(service_menu, "Get Device credentials",self.OnGetDeviceCredential)



        devices_menu = wx.Menu()
        menubar.Append(devices_menu,"Devices")
        self.CreateMenuItem(devices_menu, "Get AirCubeDetail",self.OnGetAirCubeDetail)
        self.CreateMenuItem(devices_menu, "Get AirCubeNetwork",self.OnGetAirCubeNetwork)
        self.CreateMenuItem(devices_menu, "Get AirCubeWireless",self.OnGetAirCubeWireless)
        self.CreateMenuItem(devices_menu, "Set AirCubeNetwork",self.OnSetAirCubeNetwork)
        self.CreateMenuItem(devices_menu, "Get AirMaxDetail",self.OnGetAirmaxDetail)
        devices_menu.InsertSeparator(2)

        self.CreateMenuItem(devices_menu, "Get UNMS settings",self.OnGetUNMSSettings)
        self.CreateMenuItem(devices_menu, "Get UNMS warnings",self.OnGetLogWarnings)
        self.CreateMenuItem(devices_menu, "Get UNMS errors",self.OnGetLogErrors)
     
        nonunms_menu = wx.Menu()
        menubar.Append(nonunms_menu,"Non UNMS ")
        self.CreateMenuItem(nonunms_menu, "Run iperf3",self.OnRunIperf3)
 
 
        #Help Menu
        help_menu = wx.Menu()
        menubar.Append(help_menu,"Help")
        #self.CreateMenuItem(help_menu, "General overview",self.OnHelpGeneral)

        self.CreateMenuItem(help_menu, "General overview",self.OnHelpGui)

 
        self.SetMenuBar(menubar)
        return 
    
 
    def CreateMenuItem(self, menu, label, func, icon=None, id=None):
        if id:
            item = wx.MenuItem(menu, id, label)
        else:
            item = wx.MenuItem(menu, -1, label)

        if icon:
            item.SetBitmap(wx.Bitmap(icon))

        if id:
            self.Bind(wx.EVT_MENU, func, id=id)
        else:
            self.Bind(wx.EVT_MENU, func, id=item.GetId())

        menu.Append(item)
        return item 
 
 
 
 
 
    
    def OnExit(self,event):
        print("Program is terminating")
        self.Close(True)
        return 1 # needed
    
    def OnLogin(self,event):
        """
        Asks for IP,username and password
        """
        print("OnLogin")
        TF=LoginFrame()


        TF.Show()
        return 
    
    def OnLogout(self,event):
        print("Logging out of UNMS server")
        self.UNMS.Logout()
        
    def OnGetUser(self,event):
        """
        Print out username and email of device
        """
        self.user = self.UNMS.GetUser()
        

    def OnGetSiteDetails(self,event):
        """
        gets details on the specified site
        """
       
        self.sitedetails = self.UNMS.GetSiteDetails()
        self.PrintDict(self.sitedetails)
 
    
    def OnGetSiteID(self,event):
        """
        get info site id according to site name
        """
        dialog = wx.TextEntryDialog(None," Give name of the location",value="madre-de-dios",style=wx.OK | wx.CANCEL,pos=(800,500))
        if dialog.ShowModal() == wx.ID_OK:
            site_id = dialog.GetValue()
            self.siteid = self.UNMS.GetSiteID(site_id)
        dialog.Destroy()
        
    def OnGetSiteStatistics(self,event):
        """ 
        Gets the TX/RX statistics between the device and the parent
        """
        choices = ["hour","day","month"]
        dialog = wx.SingleChoiceDialog(None , "timeinterval" ,"Set time windows for statistics",choices)
        if dialog.ShowModal() == wx.ID_OK:
            timeinterval = dialog.GetStringSelection()
            self.sitestatistics = self.UNMS.GetSiteStatistic(timeinterval)
            self.UNMS.PlotData()
            
        dialog.Destroy()
        
    def OnGetSiteClients(self,event):
        """ provides a lits of the clients of a sites parent radio
        in the case of madre de dios that would be ridgeroad
        """
        self.siteclients = self.UNMS.GetSiteClients()
    
    def OnGetAllAP(self,event):
        self.allAP =  self.UNMS.GetAllAP()
        
#        self.PrintDict(json.dumps(self.allAP))
        for k in range(0,len(self.allAP)):
            self.PrintDict(self.allAP[k])
            
    def OnGetDevicesDiscovered(self,event):
        self.devdiscovered =  self.UNMS.GetDevicesDiscovered()
        
#        self.PrintDict(json.dumps(self.devdiscovered))
        for k in range(0,len(self.devdiscovered)):
            self.PrintDict(self.devdiscovered[k])
     
    def OnGetAllSSID(self,event):
        self.allssid =  self.UNMS.GetAllSSID()
        
#        self.PrintDict(json.dumps(self.devdiscovered))
        for k in range(0,len(self.allssid)):
            self.PrintDict(self.allssid[k])
    
    def OnGetDeviceCredential(self,event):
        self.devcredential =  self.UNMS.GetDeviceCredential()
        
#        self.PrintDict(json.dumps(self.devdiscovered))
        for k in range(0,len(self.devcredential)):
            self.PrintDict(self.devcredential[k])

    def OnGetUNMSSettings(self,event):
        self.UNMSSettings =  self.UNMS.GetUNMSSettings()
        
#        self.PrintDict(json.dumps(self.devdiscovered))
        for k in range(0,len(self.UNMSSettings)):
            self.PrintDict(self.UNMSSettings[k])
     
        
    def OnGetAirCubeDetail(self,event):
        self.aircube_details = self.UNMS.GetAircubeDetail()
        if(self.aircube_details != None):
            for k in range(0,len(self.aircube_details)):
                self.PrintDict(self.aircube_details[k])

    def OnGetAirCubeNetwork(self,event):
        self.aircube_network = self.UNMS.GetAircubeNetwork()
        if(self.aircube_network != None):
            for k in range(0,len(self.aircube_network)):
                self.PrintDict(self.aircube_network[k])

    def OnGetAirCubeWireless(self,event):
        self.aircube_wireless = self.UNMS.GetAircubeWireless()
        if(self.aircube_wireless != None):
            #for k in range(0,len(self.aircube_wireless)):
            print('\n\n\n Aircube Wireless ')
            self.PrintDict(self.aircube_wireless)
                
    def OnSetAirCubeNetwork(self,event):
        """
        Currently pass
        """
        pass
     
 
    def OnGetAirmaxDetail(self,event):
        self.airmax_details = self.UNMS.GetAirmaxDetail()
        if(self.airmax_details != None):
            for k in range(0,len(self.airmax_details)):
                self.PrintDict(self.airmax_details[k])
        
    def OnGetLogWarnings(self,event):
        
        
        #first get tag for logging
        TA=TagBox()
        TA.SetCode('Warning')

        TA.Show()
         
        
    def OnGetLogErrors(self,event): 

        #first get tag for logging

        TA=TagBox()
        TA.SetCode('Error')
        TA.Show()

        
       
    def OnSetOutputFile(self,event):   
        """
        When called all output from UNMS will go to this outputfile
        """
        OF=OutputFileDialog()
        OF.Show()
      
    ############Help system
    
    def OnHelpGeneral(self,event): 
        """
        provides an overview
        """
        frame = wx.Frame(parent = None,title ='Help System',size = (400,300))
        panel = wx.Panel(frame,-1) 
        
        
        text = " This is an overview of the UNMS_GUI \n and how to use it. First you need to make sure that you are connecetd to the VPN "
        
        help = wx.StaticText(panel,-1,text)
        help.Wrap(400)
        frame.Show(show=True)
        
    def OnHelpGui(self,event):
        """ give help on how to use the Control"""
        #open a panel
        print ("help gui")
        MyGH = HelpGUI.MyGuiApp(redirect = False) 
        MyGH.MainLoop()       
    
        
    #Here come the routines which do not have anything to do with UNMS
    def OnRunIperf3(self,event):
        """ 
        runs iperf between a client and an iper server
        currently not implemented. Needs to be run without vpn
    
        """
        #first check if we are in the 172 IP space
        hostname=socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        test = ip_address.split('.')
        if(test[0] != '172'):
            self.ME.Logging(self.program_name,'Not in the 172 network, cannot do iperf')
            return
        else:
            dialog = wx.TextEntryDialog(None," Enter IP of iperf server",value="172.16.10.249",style=wx.OK | wx.CANCEL,pos=(800,500))
            if dialog.ShowModal() == wx.ID_OK:
                self.iperf_ip = iperf_ip = dialog.GetValue()
                
                command =[]
                command.append('iperf3 -b 0 -c 172.16.10.249')

                command.append('iperf3 -R -b 0 -c 172.16.10.249')

                command.append('iperf3 -u -b 0 -c 172.16.10.249')

                command.append('iperf3 -R -u -b 0 -c 172.16.10.249')
                
                for coma in command:
                    process = sp.Popen(coma,
                         #stdout=outfile,
                        stdout=sp.PIPE,
                        stderr=sp.PIPE,
                        close_fds=True,
                        universal_newlines=True)
        
                    out,err = process.communicate()
                    if process.returncode != 0:
                        self.ME.Logging(self.program_name,' iperf error ' +err)
                    else:
                        print(out)
 
                
                    
            dialog.Destroy()
        
        
        print("Not implemented yet")
        
    
    def OnDebugLevel(self,event):
        """
        Sets the debug level of UNMSControl
        """
        choices = ["0","1","2"]
        dialog = wx.SingleChoiceDialog(None , "select debug level" ,"Set Debug Level",choices)
        if dialog.ShowModal() == wx.ID_OK:
            debuglevel = int(dialog.GetStringSelection())
            self.UNMS.SetDebugLevel(debuglevel)
        dialog.Destroy()
        

    def my_listener(self, message, arg2=None):
        """
        Listener function; each message starts with the identifier
        ;"login" : this comes from the login panel and includes IP,username and password
        """
        if (message[0] == "Login"):
            self.UNMS.host = self.ip_adress = message[1]
            self.UNMS.user = self.user_name = message[2]
            self.UNMS.password = self.password = message[3]
            self.UNMS.Initialize(self.UNMS.host)
            self.UNMS.Login()
            
            # here we get the token back
            self.auth_token = self.UNMS.auth_token
        elif (message[0]=='Tag' and message[1]=='Warning' ):
            self.UNMS.logtag = message[2]
            self.UNMS.GetLogWarnings()
        elif (message[0]=='Tag' and message[1]=='Error' ):
            self.UNMS.logtag = message[2]
            self.UNMS.GetLogErrors()
 
        elif (message[0] == "OutFile"):
            self.UNMS.SetOutputFile(message[1], message[2])
        
        #print(f"Received the following message: {message}")
        if arg2:
            print(f"Received another arguments: {arg2}")

    
    def PrintDict(self,dict):
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


 

class UNMS_GUI(wx.App):

    def __init__(self,redirect = True,filename=None):
        wx.App.__init__(self,redirect,filename)

    def OnInit(self):
        """
        Needs to be called to initailize the wx App
        """
        self.version = "1.0.0"
        self.author = "Andi Klein"
        
        print ("oninit")
        self.UF = MyFrame(parent = None , id = -1, title ='UNMS control')
        self.UF.Show()

        self.SetTopWindow(self.UF)

        self.UF.SetSize((600,300))
        #self.UF.Centre()
        self.UF.SetPosition((90,900))
        
       

        
        
        
        

        
        return True
    
    
        
 
        

  





if __name__ == '__main__':
    
    MA = UNMS_GUI(redirect=False)
    MA.MainLoop()




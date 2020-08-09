'''
Created on Aug 4, 2020

@author: klein
'''






import wx
import sys
from pubsub import pub
from UNMSControl import UNMSControl
from loginpanel import LoginFrame

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
        
        self.version = 'UNMS Control version v1.0.0'
        self.author = 'Andi Klein'
        self.date = 'Summer MMXX '
        panel = wx.Panel(self,-1)
        vs =wx.StaticText(panel,-1,self.version, (100,50),(160,-1),wx.ALIGN_CENTER)
        font = wx.Font(25,wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True)
        vs.SetFont(font)
        vk =wx.StaticText(panel,-1,self.author, (100,100),(160,-1),wx.ALIGN_CENTER)
        vl =wx.StaticText(panel,-1,self.date, (100,150),(160,-1),wx.ALIGN_CENTER)
        font = wx.Font(20,wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True)
        vk.SetFont(font)
        vl.SetFont(font)
        
   
        #instantiate UNMSControl
        self.UNMS = UNMSControl()

        self.UNMS.SetDebugLevel(0) #default, can be changed
        
        self.CreateStatusBar()
        self.CreateToolBar()

        self.CreateMenu()
        pub.subscribe(self.my_listener, "panel_listener") #for passing event handler back and forth

  

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



        devices_menu = wx.Menu()
        menubar.Append(devices_menu,"Devices")
        self.CreateMenuItem(devices_menu, "Get AirCubeDetail",self.OnGetAirCubeDetail)
        self.CreateMenuItem(devices_menu, "Get AirMaxDetail",self.OnGetAirmaxDetail)
      
        nonunms_menu = wx.Menu()
        menubar.Append(nonunms_menu,"Non UNMS ")
        self.CreateMenuItem(nonunms_menu, "Run iperf3",self.OnRunIperf3)
 
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
        
    def OnGetAirCubeDetail(self,event):
        self.aircube_details = self.UNMS.GetAircubeDetail()
 
    def OnGetAirmaxDetail(self,event):
        self.airmax_details = self.UNMS.GetAirmaxDetail()
        
        
        
        
        
    #Here come the routines which do not have anything to do with UNMS
    def OnRunIperf3(self,event):
        """ 
        runs iperf between a client and an iper server
        currently not implemented. Needs to be run without vpn
    
        """
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
        
        
        #print(f"Received the following message: {message}")
        if arg2:
            print(f"Received another arguments: {arg2}")


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

        self.UF.SetSize((500,400))
        #self.UF.Centre()
        self.UF.SetPosition((1000,40))
        
       

        
        
        
        

        
        return True
    
    
        
 
        

  





if __name__ == '__main__':
    
    MA = UNMS_GUI(redirect=False)
    MA.MainLoop()




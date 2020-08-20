'''
Created on Aug 7, 2020

@author: klein
'''


import wx
from pubsub import pub

class LoginFrame(wx.Frame):
    """
    this will ask for the Ip, username and address""
    """
    
    def __init__(self):
        wx.Frame.__init__(self,None,-1,"Login",pos=(50,50))
        panel = wx.Panel(self)
        
        
        #Create control labels
        
        #title label
        toplbl = wx.StaticText(panel,-1,"Login",style = wx.ALIGN_CENTRE_HORIZONTAL)
        toplbl.SetFont(wx.Font(18,wx.SWISS,wx.NORMAL,wx.BOLD))

        #Now come three labels: IP, username, password
        self.iplbl=iplbl = wx.StaticText(panel,-1,"IP adress: ")
        self.ipnumber=ipnumber = wx.TextCtrl(panel,-1,value ='172.16.2.200')
        #self.ipnumber=ipnumber = wx.TextCtrl(panel,-1,value ='192.168.2.23:8443')
        
        self.userlbl = userlbl = wx.StaticText(panel,-1,"Username: ")
        self.username = username = wx.TextCtrl(panel,-1,value = "admin")
        #self.username = username = wx.TextCtrl(panel,-1,value = "klein")

        self.pwdlbl =pwdlbl  = wx.StaticText(panel,-1,"Password: ")
        self.password =password = wx.TextCtrl(panel,-1,"",style=wx.TE_PASSWORD)
        
        
        
        
        self.savebtn =savebtn = wx.Button(panel, -1, "Save")
        self.Bind(wx.EVT_BUTTON,self.OnSave,self.savebtn)
        
        
        # now we can start laying out the panel with boxsizer
        
        #top sizer first
        mainsizer = wx.BoxSizer(wx.VERTICAL) # we arrange vertically
        mainsizer.Add(toplbl,0,wx.ALL,5)
        #add separation line
        mainsizer.Add(wx.StaticLine(panel),0,wx.EXPAND | wx.TOP | wx.BOTTOM,10)
        
        # now we do the subsizers which are FlexGridSizer
        loginsizer = wx.FlexGridSizer(cols = 2 , hgap = 10 , vgap = 10)
        loginsizer.AddGrowableCol(1)
        loginsizer.Add(iplbl,0,wx.ALIGN_LEFT|wx.ALIGN_CENTRE_VERTICAL)
        loginsizer.Add(ipnumber,0,wx.EXPAND)
        
        loginsizer.Add(userlbl,0,wx.ALIGN_LEFT|wx.ALIGN_CENTRE_VERTICAL)
        loginsizer.Add(username,0,wx.EXPAND)
        
        loginsizer.Add(pwdlbl,0,wx.ALIGN_LEFT|wx.ALIGN_CENTRE_VERTICAL)
        loginsizer.Add(password,0,wx.EXPAND)
        
        #now do the sizer for the save button
        
        btnsizer = wx.BoxSizer(wx.HORIZONTAL)
        btnsizer.Add((20,20),1)
        btnsizer.Add(savebtn)
        
        #now put everything into main sizer
        
        mainsizer.Add(loginsizer,0,wx.EXPAND | wx.ALL,10)
        mainsizer.Add(btnsizer,0,wx.EXPAND | wx.BOTTOM,10)
        
        
        panel.SetSizer(mainsizer)
        self.Show(show=True)
        
    def OnSave(self,event):  
        
        self.loginlist = []
        self.loginlist.append("Login")  # to determine which event has generated the message
        self.loginlist.append(self.ipnumber.GetValue())
        self.loginlist.append(self.username.GetValue())
        self.loginlist.append(self.password.GetValue())
        pub.sendMessage("panel_listener", message=self.loginlist)

        self.Close()
      
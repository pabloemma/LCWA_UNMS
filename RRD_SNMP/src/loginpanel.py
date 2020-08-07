'''
Created on Aug 7, 2020

@author: klein
'''


import wx

class LoginFrame(wx.Frame):
    """
    this will ask for the Ip, username and address""
    """
    
    def __init__(self):
        wx.Frame.__init__(self,None,-1,"Login")
        panel = wx.Panel(self)
        
        #Create control labels
        
        #title label
        toplbl = wx.StaticText(panel,-1,"Login",style = wx.ALIGN_CENTRE_HORIZONTAL)
        toplbl.SetFont(wx.Font(18,wx.SWISS,wx.NORMAL,wx.BOLD))

        #Now come three labels: IP, username, password
        iplbl = wx.StaticText(panel,-1,"IP adress: ")
        ipnumber = wx.TextCtrl(panel,-1,"")
        
        userlbl = wx.StaticText(panel,-1,"Username: ")
        username = wx.TextCtrl(panel,-1,"")

        pwdlbl = wx.StaticText(panel,-1,"Password: ")
        password = wx.TextCtrl(panel,-1,"",style=wx.TE_PASSWORD)
        
        
        
        
        savebtn = wx.Button(panel, -1, "Save")
        
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
        
      
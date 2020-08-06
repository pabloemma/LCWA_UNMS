'''
Created on Aug 4, 2020

@author: klein
'''






import wx
import sys

from UNMSControl import UNMSControl



class MyFrame(wx.Frame):
    """
    The main Frame class
    """
    
    def __init__(self,parent,id,title):
        
        
        #define the Frame style
        mystyle = wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP
        
        
        
        wx.Frame.__init__(self,parent,id,title,style = mystyle)
        
        
        self.CreateStatusBar()
        self.CreateToolBar()

        self.CreateMenu()


        # Set size of Frame
        
    def CreateMenu(self):
        """
        creates the menu on the frame
        """
        menubar = wx.MenuBar()
        



        
        # section for quit, file etc
        file_menu = wx.Menu()
        menubar.Append(file_menu,"&File \tCTRL+F")

        item = wx.MenuItem(file_menu,wx.ID_NEW, "&Quit \tCTRL+Q"," leaves the program")
        file_menu.Append(item)
        self.Bind(wx.EVT_MENU,self.OnExit,item)

        #section for action
        action_menu = wx.Menu()
        menubar.Append(action_menu,"&Action \tCTRL+A")

        #action_menu.Append(wx.ID_NEW, "Login"," Log into the device with password,username and IP")
        #action_menu.Append(wx.ID_NEW, "Logout"," Logout but dont exit program")
        self.CreateMenuItem(action_menu, "Login",self.OnLogin)
        self.CreateMenuItem(action_menu, "Logout",self.OnLogout)
        
        action_menu.InsertSeparator(2)
 
        
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
        print("OnLogin")
        return 
    
    def OnLogout(self,event):
        print("OnLogout")
 



class UNMS_GUI(wx.App):

    def __init__(self,redirect = False,filename=None):
        wx.App.__init__(self,redirect,filename)

    def OnInit(self):
        """
        Needs to be called to initailize the wx App
        """
        
        print ("oninit")
        self.UF = MyFrame(parent = None , id = -1, title ='UNMS control')
        self.UF.Show()

        self.SetTopWindow(self.UF)

        self.UF.SetSize((500,400))
        self.UF.Centre()
        

        
        
        
        
         #instantiate UNMSControl
        UNMS = UNMSControl()

        
        return True
    
    
        
 
        

  


    ################ Here start the routines ###############
    def OnLogin(self,event):
        """ Login to station
        """
        
        print("in Onlogin")
        
        pass
    
    def OnLogout(self,event):
        """
        Logout of system
        """
        print('Logging out')
        
        pass





if __name__ == '__main__':
    
    MA = UNMS_GUI(redirect=False)
    MA.MainLoop()




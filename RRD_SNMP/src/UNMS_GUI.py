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
        TF=LoginFrame()


        TF.Show()
        return 
    
    def OnLogout(self,event):
        print("OnLogout")
 

    def my_listener(self, message, arg2=None):
        """
        Listener function
        """
        print(f"Received the following message: {message}")
        if arg2:
            print(f"Received another arguments: {arg2}")


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
        #self.UF.Centre()
        self.UF.SetPosition((50,400))
        

        
        
        
        
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




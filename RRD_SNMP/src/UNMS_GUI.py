'''
Created on Aug 4, 2020

@author: klein
'''






import wx
import sys

from UNMSControl import UNMSControl



class UNMS_GUI(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(UNMS_GUI, self).__init__(*args, **kwargs)

        self.InitUI()
        
        #instantiate UNMSControl
        UNMS = UNMSControl()

        

    def InitUI(self):

        menubar = wx.MenuBar()
        #regular Menu Item
        filemenu = wx.Menu()
        
        # Action Menu for some of the more important stuff
        actionmenu = wx.Menu()
        
        
        #Create File menu
        
        #fileitem = filemenu.Append(wx.ID_EDIT,'Quit',' Quit Application') 
        self.Bind(wx.EVT_MENU,self.OnQuit,filemenu.Append(wx.ID_EDIT,'Quit',' Quit Application'))
         
         
         #Create Action menu
        self.Bind(wx.EVT_MENU,self.OnLogin,actionmenu.Append(wx.ID_EDIT,'Login',' Login into system'))
        self.Bind(wx.EVT_MENU,self.OnLogout,actionmenu.Append(wx.ID_EDIT,'Logout',' Log  off system'))

        
        
        menubar.Append(filemenu, 'File')
        menubar.Append(actionmenu, 'Action')
        
        
        self.SetMenuBar(menubar)
        
        
        
        #Now we need to bind the action

 
        self.SetSize((600, 400))
        self.SetTitle('UNMS Control')
        self.Centre()

    def OnQuit(self, e):
        self.Close()
        sys.exit(0)


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



def main():

    app = wx.App()
    ex = UNMS_GUI(None)
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()





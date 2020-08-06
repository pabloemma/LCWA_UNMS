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
        wx.Frame.__init__(self,parent,id,title)

        # Set size of Frame
        
        # Locate window
        # self.Centre() # works as well as doing self.UF in UNMS_GUI


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
    
    
        
 
        

  
    def OnQuit(self, e):
        print("OnQuit")
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





if __name__ == '__main__':
    
    MA = UNMS_GUI(redirect=False)
    MA.MainLoop()




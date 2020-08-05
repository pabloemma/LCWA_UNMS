'''
Created on Aug 4, 2020

@author: klein
'''






import wx


class Example(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)

        self.InitUI()

    def InitUI(self):

        menubar = wx.MenuBar()
        #regular Menu Item
        filemenu = wx.Menu()
        
        # Action Menu for some of the more important stuff
        actionmenu = wx.Menu()
        
        
        file_items = {self.OnQuit:'Quit'}
        
        
        action_items = {self.OnLogin:'Login',self.OnLogout:'Logout'}
        
        
        #Create Menu items according to the dictionary

        file_item_wx = {}
        for x,y in file_items.items():
            file_item_wx[x] = wx.MenuItem(filemenu,wx.ID_EDIT,y)
 
        action_item_wx = {}
        for x,y in action_items.items():
            action_item_wx[x] = wx.MenuItem(actionmenu,wx.ID_EDIT,y)
        
        
        
        # the file menu pull downs
        
         
        #fileItem = wx.MenuItem(filemenu,wx.ID_EDIT, "Quit")
        #fileItem1 = wx.MenuItem(editmenu,wx.ID_EDIT, "Quit1")
        #edit_item = wx.MenuItem(editmenu, wx.ID_EDIT, "Edit")

        
        
        # Create the Menus
        
        for x,y in file_item_wx.items():
            test = filemenu.Append(file_item_wx[x])
            self.Bind(wx.EVT_MENU, x,y )

        for x,y in action_item_wx.items():
            test = actionmenu.Append(action_item_wx[x])
            self.Bind(wx.EVT_MENU, x,y )
       #filemenu.Append(fileItem)
        #editmenu.Append(fileItem1)
        #editmenu.Append(edit_item)

        menubar.Append(filemenu, 'File')
        menubar.Append(actionmenu, 'Action')
        
        
        self.SetMenuBar(menubar)
        
        
        
        #Now we need to bind the action

 
        self.SetSize((600, 400))
        self.SetTitle('UNMS Control')
        self.Centre()

    def OnQuit(self, e):
        self.Close()


    ################ Here start the routines ###############
    def OnLogin(self,event):
        """ Login to station
        """
        pass
    
    def OnLogout(self,event):
        """
        Logout of system
        """
        pass



def main():

    app = wx.App()
    ex = Example(None)
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()





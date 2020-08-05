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
        editmenu = wx.Menu()
        
        
        # the file menu pull downs
        
         
        fileItem = wx.MenuItem(filemenu,wx.ID_EDIT, "Quit")
        fileItem1 = wx.MenuItem(editmenu,wx.ID_EDIT, "Quit1")
        edit_item = wx.MenuItem(editmenu, wx.ID_EDIT, "Edit")

        
        
        # The action menues
        
        filemenu.Append(fileItem)
        editmenu.Append(fileItem1)
        editmenu.Append(edit_item)
        menubar.Append(filemenu, 'File')
        menubar.Append(editmenu, 'Edit')
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnQuit, fileItem)
        self.Bind(wx.EVT_MENU, self.OnQuit, edit_item)

        self.SetSize((600, 400))
        self.SetTitle('UNMS Control')
        self.Centre()

    def OnQuit(self, e):
        self.Close()


def main():

    app = wx.App()
    ex = Example(None)
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()





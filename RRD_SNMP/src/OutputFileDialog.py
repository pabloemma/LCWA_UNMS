'''
Created on Aug 20, 2020

@author: klein
'''
import wx
from pubsub import pub
import os
class OutputFileDialog(wx.Frame):
    '''
    classdocs
    '''

    def __init__(self,default_dir = None, default_file=None):
        wx.Frame.__init__(self,None,-1,"Login",pos=(50,50))
        panel = wx.Panel(self)
        
        if(default_dir!=None):
            default_dir = default_dir
        else:
             default_dir ='/LCWA/data/new/' 
            
        if(default_file!=None):
            default_dir = default_file
        else:
             default_file ='reduced_devicedetail.csv' 
        
        #Create control labels
        
        #title label
        toplbl = wx.StaticText(panel,-1,"Output Filename",style = wx.ALIGN_CENTRE_HORIZONTAL)
        toplbl.SetFont(wx.Font(18,wx.SWISS,wx.NORMAL,wx.BOLD))

        #Now come three labels: IP, username, password
        self.outputlbl=outputlbl = wx.StaticText(panel,-1,"Output directory ")
        
        self.directory=directory = wx.TextCtrl(panel,-1,value =os.path.expanduser("~")+'/LCWA/data/new/')
        
        self.filelbl = filelbl = wx.StaticText(panel,-1,"Filename ")
        self.filename = filename = wx.TextCtrl(panel,-1,value = "reduce_devicedetail.csv")

        
        
        
        
        self.savebtn =savebtn = wx.Button(panel, -1, "Save")
        self.Bind(wx.EVT_BUTTON,self.OnSave,self.savebtn)
        
        
        # now we can start laying out the panel with boxsizer
        
        #top sizer first
        mainsizer = wx.BoxSizer(wx.VERTICAL) # we arrange vertically
        mainsizer.Add(toplbl,0,wx.ALL,5)
        #add separation line
        mainsizer.Add(wx.StaticLine(panel),0,wx.EXPAND | wx.TOP | wx.BOTTOM,10)
        
        # now we do the subsizers which are FlexGridSizer
        outfilesizer = wx.FlexGridSizer(cols = 2 , hgap = 10 , vgap = 10)
        outfilesizer.AddGrowableCol(1)
        outfilesizer.Add(outputlbl,0,wx.ALIGN_LEFT|wx.ALIGN_CENTRE_VERTICAL)
        outfilesizer.Add(directory,0,wx.EXPAND)
        
        outfilesizer.Add(filelbl,0,wx.ALIGN_LEFT|wx.ALIGN_CENTRE_VERTICAL)
        outfilesizer.Add(filename,0,wx.EXPAND)
        
        
        #now do the sizer for the save button
        
        btnsizer = wx.BoxSizer(wx.HORIZONTAL)
        btnsizer.Add((20,20),1)
        btnsizer.Add(savebtn)
        
        #now put everything into main sizer
        
        mainsizer.Add(outfilesizer,0,wx.EXPAND | wx.ALL,10)
        mainsizer.Add(btnsizer,0,wx.EXPAND | wx.BOTTOM,10)
        
        
        panel.SetSizer(mainsizer)
        self.Show(show=True)
        
    def OnSave(self,event):  
        
        self.filelist = []
        self.filelist.append("OutFile")  # to determine which event has generated the message
        self.filelist.append(self.directory.GetValue())
        self.filelist.append(self.filename.GetValue())
        pub.sendMessage("panel_listener", message=self.filelist)

        self.Close()
              
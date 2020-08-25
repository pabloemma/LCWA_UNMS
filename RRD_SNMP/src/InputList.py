'''
Created on Aug 24, 2020

@author: klein
'''


import wx
from pubsub import pub

from JsonRead import JsonRead  


class MyInputList(wx.Frame):
    '''
    this creates an input list for loading values
    '''


    def __init__(self, title = None):
        '''
        Constructor
        '''
        wx.Frame.__init__(self,None,-1,title)
        
        self.mypanel=wx.Panel(self)
        self.JR = JsonRead()
        
        #initialize some values
 
    def ReadWrapper(self,filename):
        
        self.inputdict=inputdict = self.JR.ReadFile(filename)
        self.InitVars(inputdict)

    
    def InitVars(self,inputdict = None):
        
        if(inputdict != None):
            self.inputdict = inputdict
            
    def CreateLayout(self):
        """
        takes the input dictionary, determines the length and creates a panel
        """
        label = []  # create an empty list for the labels
        value = []
        self.namelbl = []
        self.valuelbl = []
        #Loop over dictionary and get keys


        for p_id, p_info in self.inputdict.items():
#            label.append(p_id)
            if  p_info != None and isinstance(p_info,dict): 
                label.append(p_id)
                value.append('do not change')
                
                for key in p_info:

                    print(key + ':', p_info[key])
                    label.append(key)
                    value.append(p_info[key])
            else:
                print(p_id,p_info)
                label.append(p_id)
                value.append(p_info)
         
        for k in range(0,len(label)):
            self.namelbl.append(wx.StaticText(self.mypanel,-1,label[k]))        
            self.valuelbl.append(wx.TextCtrl(self.mypanel,-1,str(value[k]),size=(200,-1)))  
         
        self.value = value
        self.label = label 
            
        saveBtn = wx.Button(self.mypanel,-1,'Save')      
        cancelBtn = wx.Button(self.mypanel,-1,'Cancel')
        
        self.Bind(wx.EVT_BUTTON,self.OnSave,saveBtn)
        self.Bind(wx.EVT_BUTTON,self.OnCancel,cancelBtn)

        
        # Now comes the sizer part
        mainsizer = wx.BoxSizer(wx.VERTICAL)  
        # two coulmns
        subsizer = wx.FlexGridSizer(cols = 2, hgap =5,vgap =5)  
        subsizer.AddGrowableCol(1)
        
        for k in range(0,len(label)):
            subsizer.Add(self.namelbl[k],0, wx.ALIGN_RIGHT | wx.ALIGN_CENTRE_VERTICAL)
            subsizer.Add(self.valuelbl[k],0,wx.EXPAND)
        
        mainsizer.Add(subsizer,0,wx.EXPAND | wx.ALL,10)    
        #place the buttons
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add((20,20,),1)
        btnSizer.Add(saveBtn)
        btnSizer.Add((20,20,),1)
        btnSizer.Add(cancelBtn)
        btnSizer.Add((20,20,),1)
          
          
        mainsizer.Add(btnSizer,0,wx.EXPAND | wx.BOTTOM,10)  
        
        #finally
        self.mypanel.SetSizer(mainsizer)
        mainsizer.Fit(self)
        #mainsizer.SetSizeHints(self)
        return
    
    def OnCancel(self,event):
        """
        nothing changed
        """
        print("Cancel")
        self.Destroy()
        return

    def OnSave(self,event):
        """
        nothing changed
        """
        print("Saving")
        # get all the values
        self.aircubelist = []
        dictionary = {}
        self.aircubelist.append("Aircube")  # to determine which event has generated the message
        for k in range(0,len(self.label)):
            dictionary[self.label[k]]=self.valuelbl[k].GetValue()
        print(dictionary)
            
        #pub.sendMessage("panel_listener", message=self.aircubelist)

        
        self.Destroy()
        return
   
   
if __name__ == '__main__':
    app = wx.App(False)
    MyIL =MyInputList('aircube control')
    MyIL.ReadWrapper('/Users/klein/git/LCWA_UNMS/RRD_SNMP/src/LCWA_Aircube.txt')
    MyIL.CreateLayout()
    MyIL.Show()
    app.MainLoop()   
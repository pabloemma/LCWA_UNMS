'''
Created on Aug 16, 2020

@author: klein
'''
import wx
from pubsub import pub
class TagBox(wx.Frame):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        wx.Frame.__init__(self,None,-1,'Choose a tag',size =(250,300))
        panel=wx.Panel(self,-1)
        tag_list = ['login','device','email-dispatch','nms-backup','nms-update','nms-error','device-state','device-backup','device-upgrade','device-interface','site']
        listbox = wx.ListBox(panel,-1,(20,20),(150,250),tag_list,wx.LB_SINGLE)
        
        self.Bind(wx.EVT_LISTBOX, self.onListBox, listbox)
        self.Show()

    def onListBox(self, event): 
         
        li = event.GetEventObject().GetStringSelection()  
        print(li)
        message = ['Tag']
        message.append(self.co)
        message.append(li)
        pub.sendMessage("panel_listener", message=message)
        
        self.Close()
    def SetCode(self, co):
        """ this provides for eithe log or error message
        """
        self.co = co

if __name__ == '__main__':
    app = wx.App(False)
    TA = TagBox()
    TA.Show()
    app.MainLoop()               
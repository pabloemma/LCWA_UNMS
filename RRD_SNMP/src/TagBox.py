'''
Created on Aug 16, 2020

@author: klein
'''
import wx
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
        li = listbox.GetSelection() 
        print (tag_list[li])  

if __name__ == '__main__':
    app = wx.App(False)
    TA = TagBox()
    TA.Show()
    app.MainLoop()               
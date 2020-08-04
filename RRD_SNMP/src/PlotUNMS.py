'''
Created on Aug 3, 2020

@author: klein
'''

import matplotlib.pyplot as plt
import matplotlib.dates as md
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy as np 
import datetime as dt      
       
class PlotUNMS(object):
    '''
    classdocs
    '''


    def __init__(self):
    
        """
        test
        """
    
    
    
    def PlotData(self,x1,y1,y2):
        np.set_printoptions(precision=2)
        fig=plt.figure() 
        ax=fig.add_subplot(1,1,1)
        
        #convert to matplotlib time
        
        
        dates=[dt.datetime.fromtimestamp(ts) for ts in x1]
        temp1 = []
        for temp in dates:
            #datenums=md.date2num(list(dates))
            temp2=(md.datestr2num(str(temp)))
            if(temp2>729162.71):
                temp1.append(temp2)
        #print(datenums)
        datenums =np.array(temp1)

        #print(x1)
        #print(y1)
        #ax.text(.1,.36,'Average $\mu$ and Standard deviation $\sigma$',weight='bold',transform=ax.transAxes,fontsize=13)
        #ax.text(.1,.23,r'$\mu_{up}     = $'+str(np.around(np.mean(y2),2))+' '+'[Mb/s]'+r'   $\sigma_{up} =     $'+str(np.around(np.std(y2),2)),transform=ax.transAxes,fontsize=12)
        #ax.text(.1,.3,r'$\mu_{down} = $'+str(np.around(np.mean(y1),2))+' '+'[Mb/s]'+r'   $\sigma_{down} = $'+str(np.around(np.std(y1),2)),transform=ax.transAxes,fontsize=12)
        plt.plot([],[])
        plt.plot_date(temp1,y2,'g^',label='\n green UP ')
        plt.plot_date(temp1,y1,'bs',label=' blue DOWN')
        
        
        # Choose your xtick format string
        date_fmt = '%d-%m-%y %H:%M:%S'
        date_fmt = ' %H:%M:%S'


        #plt.text(1.,1.,r' $\sigma = .1$')
        plt.grid(True)

        #ax.xaxis.set_major_locator(md.MinuteLocator(interval=60))
        ax.xaxis.set_major_formatter(md.DateFormatter(date_fmt))
        plt.xlabel('Time')
        plt.ylabel('Speed in Mbs')
        plt.legend(facecolor='ivory',loc="lower right",shadow=True, fancybox=True)


        plt.xticks(rotation='vertical')
        #plt.tight_layout()

        #fig.savefig(file2, bbox_inches='tight')
        plt.show()
        return
    

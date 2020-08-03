'''
Created on Aug 3, 2020

@author: klein
'''

import matplotlib.pyplot as plt
import matplotlib.dates as md
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy as np       
       
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
        
        

        secs = md.epoch2num(x1)
        #ax.text(.1,.36,'Average $\mu$ and Standard deviation $\sigma$',weight='bold',transform=ax.transAxes,fontsize=13)
        #ax.text(.1,.23,r'$\mu_{up}     = $'+str(np.around(np.mean(y2),2))+' '+'[Mb/s]'+r'   $\sigma_{up} =     $'+str(np.around(np.std(y2),2)),transform=ax.transAxes,fontsize=12)
        #ax.text(.1,.3,r'$\mu_{down} = $'+str(np.around(np.mean(y1),2))+' '+'[Mb/s]'+r'   $\sigma_{down} = $'+str(np.around(np.std(y1),2)),transform=ax.transAxes,fontsize=12)

        plt.plot_date(secs,y2,'g^',label='\n green UP ')
        plt.plot_date(secs,y1,'bs',label=' blue DOWN')
        
        
        # Choose your xtick format string
        date_fmt = '%d-%m-%y %H:%M:%S'

        # Use a DateFormatter to set the data to the correct format.
        date_formatter = md.DateFormatter(date_fmt)
        ax.xaxis.set_major_formatter(date_formatter)

        # Sets the tick labels diagonal so they fit easier.
        #fig.autofmt_xdate()

        #plt.text(1.,1.,r' $\sigma = .1$')
        plt.grid(True)

        #ax.xaxis.set_major_locator(md.MinuteLocator(interval=60))
        ax.xaxis.set_major_formatter(md.DateFormatter(date_fmt))
        plt.xlabel('Time')
        plt.ylabel('Speed in Mbs')
        plt.legend(facecolor='ivory',loc="lower right",shadow=True, fancybox=True)

        if(np.around(np.mean(y1),2) > 21.e06):
            plt.ylim(0.,24.e06) # set yaxis limit
        elif(np.around(np.mean(y1),2) <= 21.e06 and np.around(np.mean(y1),2) > 12.e06):
            plt.ylim(0.,24.e06) # set yaxis limit
        elif(np.around(np.mean(y1),2) <= 12.e06 and np.around(np.mean(y1),2) > 7.e06):
            plt.ylim(0.,12.e06) # set yaxis limit
             # set yaxis limit
        elif(np.around(np.mean(y1),2) <= 7.e06 ):
            plt.ylim(0.,7.e06) # set yaxis limit

        #plt.xticks(rotation='vertical')
        #plt.tight_layout()

        #fig.savefig(file2, bbox_inches='tight')
        plt.show()
        return
    

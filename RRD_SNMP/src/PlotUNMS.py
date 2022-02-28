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
import math    
       
class PlotUNMS(object):
    '''
    classdocs
    '''


    def __init__(self):
    
        """
        test
        """
        #Create empty tlists for plot arrays. The arrays are numpy arrays
        self.time = []
        self.y1   = []
        self.y2   = []
        self.ylab = []
        self.sitename = []
    
    
    def PlotData(self,sitename,x1,y1,y2,dirname):
        self.dirname = dirname
        self.sitename.append(sitename)
        np.set_printoptions(precision=2)
        fig=plt.figure() 
        ax=fig.add_subplot(1,1,1)
        bbox=(0.03,.03,1.,0.25)
        
        #to make room for the xaxis label
        #plt.tight_layout()
        plt.gcf().subplots_adjust(bottom=0.25)
        
        #convert to matplotlib time
        
        
        dates=[dt.datetime.fromtimestamp(ts) for ts in x1]
        temp1 = []
        counter = 0 
        for temp in dates:
            #datenums=md.date2num(list(dates))
            temp2=(md.datestr2num(str(temp)))
            #print(temp2)
            if(y1[counter] != 0):
                temp1.append(temp2)
            counter +=1
        #print(datenums)
        datenums =np.array(temp1)

        #print(x1)
        #print(y1)
        #ax.text(.1,.36,'Average $\mu$ and Standard deviation $\sigma$',weight='bold',transform=ax.transAxes,fontsize=13)
        #ax.text(.1,.23,r'$\mu_{up}     = $'+str(np.around(np.mean(y2),2))+' '+'[Mb/s]'+r'   $\sigma_{up} =     $'+str(np.around(np.std(y2),2)),transform=ax.transAxes,fontsize=12)
        #ax.text(.1,.3,r'$\mu_{down} = $'+str(np.around(np.mean(y1),2))+' '+'[Mb/s]'+r'   $\sigma_{down} = $'+str(np.around(np.std(y1),2)),transform=ax.transAxes,fontsize=12)
        #plt.plot([],[])
        plt.plot_date(temp1,y2,'g^',label='\n green UP ')
        plt.plot_date(temp1,y1,'bs',label=' blue DOWN')

        # Choose your xtick format string
        date_fmt = '%d-%m-%y %H:%M'
        #date_fmt = ' %H:%M:%S'


        #plt.text(1.,1.,r' $\sigma = .1$')
        plt.grid(True)

        #ax.xaxis.set_major_locator(md.MinuteLocator(interval=60))
        ax.xaxis.set_major_formatter(md.DateFormatter(date_fmt))
        plt.xlabel('Time')
        ylab = "Transfer between {0} and parent in Mb/s".format(sitename)
        plt.ylabel(ylab)
        plt.legend(facecolor='ivory',loc="upper left",shadow=True, fancybox=True)

        degrees = 90
        plt.xticks(rotation=degrees)

        #save data in list:
        self.time.append(temp1)
        self.y1.append(y1)
        self.y2.append(y2)
        self.ylab.append(ylab)



        #plt.tight_layout()
        file2 = dirname+sitename+'.pdf'
        fig.savefig(file2, bbox_inches='tight')
        plt.show()
        return
    
    def PlotAll(self):
        print('now creating multiple plots')
        print('length lo list',len(self.time))

        if len(self.y1) == 1:   #only one plot
            return
        else:
            # create multiple plots on one page
            fig = plt.figure()  # create a figure
            ax = []  # will hold array of subplots
            plt.rc('axes', labelsize=5)

            # now create subplots, fist detrmine how many we have.
            # we will fill them in a grid of 2 wide and n deep
            n = math.ceil(len(self.y1)/2.)
            for k in range(len(self.y1)):
                ax.append(fig.add_subplot(n,2,k+1))
                #plt.rc('axes', labelsize=5)

                plt.plot_date(self.time[k],self.y2[k],'g^',markersize = 3 ,label='\n green UP ')
                plt.plot_date(self.time[k],self.y1[k],'bs',markersize = 3 ,label=' blue DOWN')

                date_fmt = '%d-%m-%y %H:%M'
                plt.grid(True)

                ax[k].xaxis.set_major_formatter(md.DateFormatter(date_fmt))
                plt.xlabel('Time')
                #reduce label size

                plt.ylabel(self.ylab[k])
                
                #plt.legend(facecolor='ivory',loc="lower left",shadow=True, fancybox=True)

                degrees = 90
                plt.xticks(rotation=degrees)

            #plt.tight_layout(pad=0.2, w_pad=0.2, h_pad=.1)

            plt.tight_layout(w_pad=.2)
            fig.set_size_inches(8., 11.)
            myfile = self.dirname+self.sitename[0]+'_trace.pdf'
            fig.savefig(myfile, bbox_inches='tight')

            plt.show()
 



        return
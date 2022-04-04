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
import time
import numpy as np


class PlotUNMS(object):
    '''
    classdocs
    '''

    def __init__(self):
        """
        test
        """
        # Create empty tlists for plot arrays. The arrays are numpy arrays

        self.time = []
        self.y1 = []
        self.y2 = []
        self.ylab = []
        self.sitename = []
        self.names = []

    def ResetArrays(self): 
        """Clera previuops arrays"""
        self.time = []
        self.y1 = []
        self.y2 = []
        self.ylab = []
        self.sitename = []
        self.names = []
 

    def PlotDataShort(self, sitename, x1, y1, y2, dirname, pltflag=True):
        self.dirname = dirname
        self.sitename.append(sitename)
        dates = [dt.datetime.fromtimestamp(ts) for ts in x1]
        temp1 = []
        counter = 0
        for temp in dates:
            # datenums=md.date2num(list(dates))
            temp2 = (md.datestr2num(str(temp)))
            # print(temp2)
            if(y1[counter] != 0):
                temp1.append(temp2)
            counter += 1
        # print(datenums)
        ylab = "Transfer between {0} and parent in Mb/s".format(sitename)
 
        datenums = np.array(temp1)
        self.time.append(temp1)
        self.y1.append(y1)
        self.y2.append(y2)
        self.ylab.append(ylab)
        self.names.append(sitename)
        return
        

    def PlotData(self, sitename, x1, y1, y2, dirname, pltflag=True):
        self.dirname = dirname
        self.sitename.append(sitename)
        np.set_printoptions(precision=2)
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        bbox = (0.03, .03, 1., 0.25)

        # to make room for the xaxis label
        # plt.tight_layout()
        plt.gcf().subplots_adjust(bottom=0.25)

        # convert to matplotlib time

        dates = [dt.datetime.fromtimestamp(ts) for ts in x1]
        temp1 = []
        counter = 0
        for temp in dates:
            # datenums=md.date2num(list(dates))
            temp2 = (md.datestr2num(str(temp)))
            # print(temp2)
            if(y1[counter] != 0):
                temp1.append(temp2)
            counter += 1
        # print(datenums)
        datenums = np.array(temp1)

        # print(x1)
        # print(y1)
        #ax.text(.1,.36,'Average $\mu$ and Standard deviation $\sigma$',weight='bold',transform=ax.transAxes,fontsize=13)
        #ax.text(.1,.23,r'$\mu_{up}     = $'+str(np.around(np.mean(y2),2))+' '+'[Mb/s]'+r'   $\sigma_{up} =     $'+str(np.around(np.std(y2),2)),transform=ax.transAxes,fontsize=12)
        #ax.text(.1,.3,r'$\mu_{down} = $'+str(np.around(np.mean(y1),2))+' '+'[Mb/s]'+r'   $\sigma_{down} = $'+str(np.around(np.std(y1),2)),transform=ax.transAxes,fontsize=12)
        # plt.plot([],[])
        plt.plot_date(temp1, y2, 'g^', label='\n green UP ')
        plt.plot_date(temp1, y1, 'bs', label=' blue DOWN')

        # Choose your xtick format string
        date_fmt = '%d-%m-%y %H:%M'
        #date_fmt = ' %H:%M:%S'

        #plt.text(1.,1.,r' $\sigma = .1$')
        plt.grid(True)

        # ax.xaxis.set_major_locator(md.MinuteLocator(interval=60))
        ax.xaxis.set_major_formatter(md.DateFormatter(date_fmt))
        plt.xlabel('Time')
        ylab = "Transfer between {0} and parent in Mb/s".format(sitename)
        plt.ylabel(ylab)
        plt.legend(facecolor='ivory', loc="upper left",
                   shadow=True, fancybox=True)

        degrees = 90
        plt.xticks(rotation=degrees)

        # save data in list:
        self.time.append(temp1)
        self.y1.append(y1)
        self.y2.append(y2)
        self.ylab.append(ylab)
        self.names.append(sitename)

        # plt.tight_layout()
        file2 = dirname+sitename+'.pdf'
        fig.savefig(file2, bbox_inches='tight')
        if(pltflag):
            plt.show()
        return

    def PlotAll(self):
        print('now creating multiple plots')
        print('length lo list', len(self.time))
        if plt.get_fignums():
            plt.close('all')
            # window(s) open


        if len(self.y1) == 1:  # only one plot
            return
        else:
            # create multiple plots on one page
            fig = plt.figure()  # create a figure
            ax = []  # will hold array of subplots
            plt.rc('axes', labelsize=5)

            # now create subplots, fist detrmine how many we have.
            # we will fill them in a grid of 2 wide and n deep
            n = math.ceil(len(self.y1)/2.)
            print('\n\n We have', len(self.y1), '  plots \n\n')
            for k in range(len(self.y1)):
                ax.append(fig.add_subplot(n, 2, k+1))
                #plt.rc('axes', labelsize=5)

                plt.plot_date(self.time[k], self.y2[k],
                              'g^', markersize=3, label='\n green UP ')
                plt.plot_date(self.time[k], self.y1[k],
                              'bs', markersize=3, label=' blue DOWN')

                date_fmt = '%d-%m-%y %H:%M'
                plt.grid(True)

                ax[k].xaxis.set_major_formatter(md.DateFormatter(date_fmt))
                plt.xlabel('Time')
                # reduce label size

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

    def PlotAllNew(self):
        """not working yet"""
        
        #check if any figures are open
        if plt.get_fignums():
            plt.close('all')
            # window(s) open


        if len(self.y1) == 1:  # only one plot
            return
        else:
            # create multiple plots on one page

            print('\n\n We have', len(self.y1), '  plots \n\n')
            # we will plot 12 plots per page, so we need  many pages
            num_pages = math.ceil(len(self.y1)/12.)
            #num_pages  = 1
            # here starts outer loop
            myfile = self.dirname+self.sitename[0]+'_trace.pdf'
            pdf = PdfPages(myfile)

            # create the lists for figures and axes
            fig_array = [0 for k in range(num_pages)]
            axes_array = [0 for k in range(num_pages)]
            
            #outarray1 = np.add(self.y1[0],self.y1[1] ) # create first array
            #outarray2 = np.add(self.y2[0],self.y2[1] ) # create first array
            outarray1 = self.SumPlots(self.y1[0],self.y1[1])
            outarray2 = self.SumPlots(self.y2[0],self.y2[1])
            for num in range(num_pages):
                numx = 4
                numy = 3
                fig_array[num], axes_array[num] = plt.subplots(
                    numx, numy, sharex=True)

                for k, ax in enumerate(axes_array[num].flatten()):
                    l = k + num*numx*numy
                    if(l>1) and l<len(self.y1)-2:
                        #print('this \is l ',l)
                        
                        outarray1 = self.SumPlots(outarray1,self.y1[l])
                        outarray2 = self.SumPlots(outarray2,self.y2[l])
                    if(l > len(self.y1)-1):
                        break
                    #ax.plot_date(self.time[l],self.y2[l],'g^',markersize = 3 ,label='\n green UP ')
                    #ax.plot_date(self.time[l],self.y1[l],'bs',markersize = 3 ,label=' blue DOWN')
                    
                    ax.plot(self.time[l], self.y2[l], 'g^',
                            markersize=3, label='\n green UP ')
                    ax.plot(self.time[l], self.y1[l], 'bs',
                            markersize=3, label=' blue DOWN')
                       

                    date_fmt = '%d-%m-%y %H:%M'
                    # plt.grid(True)

                    ax.xaxis.set_major_formatter(md.DateFormatter(date_fmt))
                    ax.set_xlabel('Time')
                    # ax.set_yscale('log')
                    ax.set_title(self.names[l])
                    ax.set_yscale('linear')
                    ax.set_ybound(lower=0., upper=3.e7)
                    if(l == len(self.y1)-1):
                        ax.plot(self.time[l], outarray1, 'rs',
                        markersize=3, label=' blue DOWN')
                        ax.set_ybound(lower=0., upper=2.e8)
                    ax.xaxis_date()
                    for tick in ax.get_xticklabels():
                        tick.set_rotation(90)

                fig_array[num].set_size_inches(8., 11.)

                # plt.savefig(pdf,format='pdf')
                pdf.savefig(fig_array[num])
            #fig.savefig(myfile, bbox_inches='tight')
        # plt.clf()
        plt.show()
        pdf.close()
        self.ResetArrays() # clear plots
        
        
        
        return

    def SumPlots(self,arr1,arr2):
        """sums all the different arrays"""
        if arr1.size !=0 and arr2.size !=0 and arr1.shape == arr2.shape:
            return np.add(arr1,arr2)
        else:
            print('problems with adding the two arrys fromk numpy')
            return arr1

    def KunPlot(self):
        """not working yet"""

        if len(self.y1) == 1:  # only one plot
            return
        else:
            # create multiple plots on one page
            data = np.random.randn(36, 1024)

            print('\n\n We have', len(self.y1), '  plots \n\n')
            # we will plot 12 plots per page, so we need  many pages
            num_pages = math.ceil(len(self.y1)/12.)
            #num_pages  = 1
            # here starts outer loop
            #myfile = self.dirname+self.sitename[0]+'_trace.pdf'
            myfile = 'test.pdf'
            pdf = PdfPages(myfile)
            nplots_per_page = 12
            for idx, sample in enumerate(self.y1):
                # for idx, sample in enumerate(data):
                time.sleep(1)
                print("Makeing plot %d" % idx)
                lid = idx % nplots_per_page
                if lid == 0:
                    fig = plt.figure()
                plt.subplot2grid((12, 1), (lid, 0))
                #plt.hist(sample, 50)
                plt.plot(self.time[idx], self.y2[idx], 'g^',
                         markersize=3, label='\n green UP ')
                plt.plot(self.time[idx], self.y1[idx], 'bs',
                         markersize=3, label=' blue DOWN')

                date_fmt = '%d-%m-%y %H:%M'
                # plt.grid(True)

                # plt.xaxis.set_major_formatter(md.DateFormatter(date_fmt))
                # ax.set_xlabel('Time')
                # ax.set_yscale('log')
                # ax.set_title(self.names[l])
                # ax.set_yscale('linear')
                #ax.set_ybound(lower = 0. , upper = 3.e7)
                # ax.xaxis_date()
                # for tick in ax.get_xticklabels():
                #    tick.set_rotation(90)

                if lid+1 == nplots_per_page:

                    pdf.savefig(fig)
                    plt.show(block=False)
                    # IMPORTANT: matplotlib only update GUI once the system is in IDLE
                    plt.pause(2)
            a = input('Press any key to continue')
        # write to disk
            pdf.close()

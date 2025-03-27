#Copyright National Research Foundation (SARAO), 2005-2025. All Rights Reserved.
#Author: Mattieu de Villiers (email: mattieu@sarao.ac.za)
"""
Copyright National Research Foundation (SARAO), 2005-2025. All Rights Reserved.
Author: Mattieu de Villiers (email: mattieu@sarao.ac.za)
"""
import pickle
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from matplotlib.widgets import Button
from matplotlib.widgets import CheckButtons

class FlagPlot:
    ind = 0
    start=[0,0,0,0,0]
    rubberband=0
    origaxis=0
    def __init__(self,h5,scanantindex,sigma,selectedantennas,radialscan_allantenna,refMHz,dMHz,flags,freqflags,dirname,targetname=None,flagspeed=None,flagextratime=None,autocorrelations=False):
        self.selfobj=None
        self.autocorrelations=autocorrelations
        self.targetname=targetname
        self.dirname=dirname
        self.dMHz=dMHz
        self.refMHz=refMHz
        self.radialscan_allantenna=radialscan_allantenna
        self.selectedantennas=selectedantennas
        self.corrprod_to_index = dict([(tuple(cp), ind) for cp, ind in zip(np.r_[h5.corr_products,h5.corr_products[::,::-1]], np.r_[range(len(h5.corr_products)),range(len(h5.corr_products))])])
        self.flags=flags
        self.flagspeed=flagspeed
        self.flagextratime=flagextratime
        self.sigma=sigma
        self.freqflags=freqflags
        self.scanantindex=scanantindex
        self.plotlist=[('h','h',1),('v','v',1),('h','v',1),('v','h',1),('h','h',0),('v','v',0),('h','v',0),('v','h',0)];
        self.h5=h5
        self.plotphase=0
        self.implementflag=0
        self.preparedata()
        i = self.ind % len(self.displist)
        self.fig=plt.figure()
        self.fig.canvas.mpl_connect('key_press_event', self.onpress)
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.fig.canvas.mpl_connect('button_release_event', self.onrelease)
        self.fig.canvas.mpl_connect('motion_notify_event',self.onmousemove)
        self.fig.text(0.5,0.975,dirname,horizontalalignment='center',verticalalignment='top')
        self.origax=self.fig.add_subplot(111)
        plt.subplots_adjust(bottom=0.2)
        self.plotmeanbaselines(i)

    def start(self,flagobj,datasetcallback):
        self.selfobj=flagobj
        self.axsave = plt.axes([0.1, 0.05, 0.15, 0.075])
        self.axplotphase = plt.axes([0.4, 0.05, 0.09, 0.035])
        self.aximpl = plt.axes([0.4, 0.085, 0.09, 0.035])
        self.axundo = plt.axes([0.6, 0.05, 0.09, 0.075])
        self.axprev = plt.axes([0.7, 0.05, 0.09, 0.075])
        self.axnext = plt.axes([0.8, 0.05, 0.09, 0.075])
        self.bsave = Button(self.axsave, 'Save&quit')
        self.bsave.on_clicked(flagobj.save)
        self.bimpl = CheckButtons(self.aximpl, ['Apply'],[self.implementflag])
        self.bimpl.on_clicked(flagobj.impl)
        self.bplotphase = CheckButtons(self.axplotphase, ['Phase'],[self.plotphase])
        self.bplotphase.on_clicked(flagobj.plotphase)
        self.bundo = Button(self.axundo, 'Undo')
        self.bundo.on_clicked(flagobj.undo)
        self.bnext = Button(self.axnext, 'Next')
        self.bnext.on_clicked(flagobj.next)
        self.bprev = Button(self.axprev, 'Prev')
        self.bprev.on_clicked(flagobj.prev)
        self.datasetcallback=datasetcallback
    
    #pol can be 'h' or 'v' and ax is 0 (for freq) or 1 (for time)
    def plotmeanbaselines(self,listind):
        dat=self.displist[listind]
        if (dat[8]==0):#freq plot
            for data in dat[self.plotphase]:
                plt.plot(dat[2],data,'.')
            for fl in self.freqflags:
                plt.axvspan(fl[0], fl[1], color='red', alpha=0.5)
            for cd in self.chandivisions:
                plt.axvline(cd,linestyle=':',color='k')
            ext=plt.axis()
            if (len(self.freqgrid)>1 and np.abs(self.freqgrid[1]-self.freqgrid[0])<1.0):
                for idiv in range(1,len(self.chandivisions)):
                    x=0.5*(self.chandivisions[idiv]+self.chandivisions[idiv-1]);                
                    plt.text(x,ext[3],str(float(self.freqgrid[idiv])),horizontalalignment='center',verticalalignment='top',rotation=90,fontsize='smaller')
            else:
                for idiv in range(1,len(self.chandivisions)):
                    x=0.5*(self.chandivisions[idiv]+self.chandivisions[idiv-1]);                
                    plt.text(x,ext[3],str(int(self.freqgrid[idiv])),horizontalalignment='center',verticalalignment='top',rotation=90,fontsize='smaller')
            plt.xlim([dat[2][0],dat[2][-1]])
        else:#time plot
            if (dat[7]==''):
                for data in dat[self.plotphase]:
                    plt.plot(dat[2],data)
            else:
                for data in dat[self.plotphase]:
                    plt.plot(dat[2],data,'.')
            for fl in self.flags:
                plt.axvspan(fl[0], fl[1], color='red', alpha=0.5)
            plt.xlim([dat[2][0],dat[2][-1]])
        plt.xlabel(dat[3])
        plt.ylabel(dat[4])
        plt.title(dat[5])
    
    def preparedata(self):
        self.h5.select(reset='TFB')
        freqMHz=self.h5.channel_freqs/1E6
        startMHz=self.refMHz+np.round(((freqMHz[0])-self.refMHz)/self.dMHz)*self.dMHz#includes all valid channels
        self.freqgrid=np.arange(startMHz,(freqMHz[-1]-self.dMHz/2.0),-self.dMHz)#center frequencies to be evaluated
        self.divisions=0.5*(self.freqgrid[:-1]+self.freqgrid[1:])
        self.chandivisions=np.interp(self.divisions,freqMHz[[-1,0]],self.h5.channels[[-1,0]])        
        
        self.channel_range=range(len(self.h5.channels))
        self.ch0=self.channel_range[0]
        self.ch1=self.channel_range[-1]
        #channel_range=range(200,800);
        #freqflags=[(225,226),(347,351),(482,488),(512,513),(641,645),(649,657)];#for virgo a
        #freqflags=[(448,449),(487,488),(512,513)];#for 1331
        if (self.implementflag):
            nchannels=len(self.channel_range)
            for c in range(nchannels):
                for flagrange in self.freqflags:
                    if (c>=flagrange[0] and c <=flagrange[1]):
                        try:
                            self.channel_range.remove(c);
                        except:
                            pass
    #
        #flags=[(0.16,0.35),(1.32,1.5),(1.8,2.23),(2.3,2.7),(3.04,3.22),(4.9,5.25),(5.6,6.0),(6.2,6.55),(7.2,7.55),(8.005,8.195)];#for virgo a
        #flags=[(0.45,0.7),(2.3,2.6),(3.25,3.35),(3.6,4.65),(4.8,5.7),(6.2,6.8)];#poor0,poor1
        #flags =[(1.76,1.87),(7.25,7.35),(3.8,4.5),(4.9,5.65)];#start and stop times for flags in hours from beginning of observation


        print('Calculating timestamps')
        flagmask=np.zeros(np.shape(self.h5.timestamps),dtype='int');
        self.time=np.array((self.h5.timestamps[:]))/60.0/60.0;
        self.time0=self.time[0]
        self.time1=self.time[-1]
        self.time-=self.time0

        if (self.flagspeed!=None):
            #speed=np.sqrt(np.abs(np.diff(self.h5.target_x[:,self.scanantindex]))**2+np.abs(np.diff(self.h5.target_y[:,self.scanantindex]))**2)
            speed=np.sqrt(np.abs(np.diff(self.h5.az[:,self.scanantindex]))**2+np.abs(np.diff(self.h5.el[:,self.scanantindex]))**2)
            speedd=0.5*(np.r_[0,speed]+np.r_[speed,0])*180.0/np.pi
            idx=np.nonzero(speedd>self.flagspeed)[0]
            plt.figure()
            plt.plot(speedd)
            print('speed min ',np.min(speedd),'speed max ',np.max(speedd),'nflagged ',len(idx))
            if (self.flagextratime is None):
                self.flags=[(self.time[ti]-0.1/60.0/60.0,self.time[ti]+0.1/60.0/60.0) for ti in idx]
            else:
                self.flags=[(self.time[ti]-self.flagextratime/60.0/60.0,self.time[ti]+self.flagextratime/60.0/60.0) for ti in idx]
        if (self.flags=='flagslew'):
            slewing=(self.h5.sensor['Observation/scan_state']=='slew')
            idx=np.nonzero(slewing)[0]
            self.flags=[(self.time[ti]-0.1/60.0/60.0,self.time[ti]+0.1/60.0/60.0) for ti in idx]
            print('ntime',len(self.time),'slew flagged',len(idx),'nflags',len(self.flags))
        if (self.targetname!=None):
            namelist=[tar.name for tar in self.h5.catalogue.targets]
            if (self.targetname in namelist):
                ind=namelist.index(self.targetname)
                targetmask=(self.h5.sensor['Observation/target_index']!=ind)
                idx=np.nonzero(np.diff(targetmask)!=0)[0]
                if (targetmask[0]):
                    idx=np.r_[0,idx]
                if (targetmask[-1]):
                    idx=np.r_[idx,len(targetmask)-1]
                self.flags.extend([ (self.time[idx[ii*2]]-0.1/60.0/60.0,self.time[idx[ii*2+1]]+0.1/60.0/60.0) for ii in range(len(idx)//2)])
                print('target '+self.targetname+' flags',self.flags)
        self.displist=[];
        self.displist.append(self.getdata([],'el','',1))
        self.displist.append(self.getdata([],'az','',1))

        if (self.implementflag):
            for flagrange in self.flags:
                flagmask|=np.array(np.array(self.time>=flagrange[0]) & np.array(self.time<=flagrange[1]),dtype='int');

        self.h5.select(channels=self.channel_range);
        if (np.isnan(self.sigma)):
            self.h5.select(dumps=np.array((1-flagmask),dtype='bool'));
        else:
            self.h5.select(dumps=np.array((np.array((self.h5.target_x[:,self.scanantindex])**2+(self.h5.target_y[:,self.scanantindex])**2<self.sigma**2,dtype='int') & (1-flagmask)),dtype='bool'));
    #    h5.select(dumps=np.array((np.array((targetx)**2+(targety)**2<options.sigma**2,dtype='int') & (1-flagmask)),dtype='bool'));
        self.time=np.array((self.h5.timestamps))/60.0/60.0-self.time0;
        print('Number of on-axis time samples is %d using sigma %g'%(len(self.h5.timestamps),self.sigma))
        ax=1
        #thevis=np.mean(self.h5.vis[:,:,:],axis=ax);
        thevis=np.max(np.abs(self.h5.vis[:,:,:]),axis=ax);
        for c in self.plotlist:
            if (ax!=c[2]):
                ax=c[2]
                if (ax==1):
                    nchan=self.h5.vis[:,:,:].shape[1]
                    thevis=np.max(abs(self.h5.vis[:,(nchan/5):(nchan-nchan/5),:]),axis=1);
                else:
                    thevis=np.max(abs(self.h5.vis[:,:,:]),axis=0);
    #            thevis=np.mean(h5.vis[:,:,:],axis=ax);            
            self.displist.append(self.getdata(thevis,c[0],c[1],c[2]))
        
        self.h5.select(reset='TFB')
        
    
    def getdata(self,thevis,pol1,pol2,ax):
        tf=[' freq',' time']
        print('Processing '+pol1+' '+ pol2+' on '+tf[ax])
        if (pol1=='el'):
            return ([self.h5.el],[self.h5.el],self.time,'Time [hrs]','Elevation [deg]','Elevation',pol1,pol2,ax)
        if (pol1=='az'):
            return ([self.h5.az],[self.h5.az],self.time,'Time [hrs]','Azimuth [deg]','Azimuth',pol1,pol2,ax)
        if (pol1=='I'):
            avg12=np.zeros(np.shape(self.h5.vis)[0],dtype='complex');
            nchan=self.h5.vis[:,:,:].shape[1]
            thevis=np.max(abs(self.h5.vis[:,(nchan/5):(nchan-nchan/5),:]),axis=1);
            for a1 in trackantennas:
                for a2 in scanantennas:
                    if a1>a2:
                        sa1=a2;sa2=a1;
                    else:
                        sa1=a1;sa2=a2;
                    if ((self.radialscan_allantenna[sa1]+'h', self.radialscan_allantenna[sa2]+'h') in self.corrprod_to_index):
                        avg12=np.max([avg12,thevis[:,self.corrprod_to_index[(self.radialscan_allantenna[sa1]+'h', self.radialscan_allantenna[sa2]+'h')]].reshape(-1)],axis=0)
                    else:
                        avg12=0
                    if ((self.radialscan_allantenna[sa1]+'v', self.radialscan_allantenna[sa2]+'v') in self.corrprod_to_index):
                        avg12=np.max([avg12,thevis[:,self.corrprod_to_index[(self.radialscan_allantenna[sa1]+'v', self.radialscan_allantenna[sa2]+'v')]].reshape(-1)],axis=0)                
            return (20.0*np.log10(abs(avg12)),180.0/np.pi*np.angle(avg12),self.time,'Time [hrs]','','Max cross baseline for on-axis pointing, pols I',pol1,pol2,1)
        # avg12=np.zeros(np.shape(h5.vis)[1-ax],dtype='complex');
        abs12=[]
        ang12=[]
        if (self.autocorrelations==False):
            for a1 in range(len(self.selectedantennas)):
                for a2 in range(a1+1,len(self.selectedantennas)):
                    prod=(self.radialscan_allantenna[self.selectedantennas[a1]]+pol1, self.radialscan_allantenna[self.selectedantennas[a2]]+pol2)
                    if (prod in self.corrprod_to_index):
                        abs12.append(20.0*np.log10(abs(thevis[:,self.corrprod_to_index[prod]].reshape(-1))))
                        ang12.append(180.0/np.pi*np.angle(thevis[:,self.corrprod_to_index[prod]].reshape(-1)))
            if (ax):
                return (abs12,ang12,self.time,'Time [hrs]','','Max cross baseline for on-axis pointing, pols '+pol1+' '+pol2,pol1,pol2,ax)
            else:
                return (abs12,ang12,self.channel_range,'Frequency [channel]','','Max cross baseline for on-axis pointing, pols '+pol1+' '+pol2,pol1,pol2,ax)
        #else auto correlations
        for a1 in range(len(self.selectedantennas)):
            prod=(self.radialscan_allantenna[self.selectedantennas[a1]]+pol1, self.radialscan_allantenna[self.selectedantennas[a1]]+pol2)
            if (prod in self.corrprod_to_index):
                print('a1',a1,'prod',prod)
                abs12.append(20.0*np.log10(abs(thevis[:,self.corrprod_to_index[prod]].reshape(-1))))
                ang12.append(180.0/np.pi*np.angle(thevis[:,self.corrprod_to_index[prod]].reshape(-1)))
            
        if (ax):
            return (abs12,ang12,self.time,'Time [hrs]','','Max autocorrelations for on-axis pointing, pols '+pol1+' '+pol2,pol1,pol2,ax)
        else:
            return (abs12,ang12,self.channel_range,'Frequency [channel]','','Max autocorrelations for on-axis pointing, pols '+pol1+' '+pol2,pol1,pol2,ax)
    
    def save(self, event):
        output=open(self.dirname+'flags', 'wb')
        pickle.dump(self.flags,output)
        pickle.dump(self.freqflags,output)
        output.close();
        print('saving %d flags and %d freqflags to'%(len(self.flags),len(self.freqflags)),self.dirname+'flags')
        self.datasetcallback()
        plt.close(self.fig)
        #del self.selfobj

    def impl(self,event):
        i = self.ind % len(self.displist)
        self.implementflag=1-self.implementflag
        self.preparedata()
        ax = plt.subplot(111)
        plt.cla()
        ax = plt.subplot(111)
        self.plotmeanbaselines(i)
        plt.draw()
        
    def plotphase(self,event):
        i = self.ind % len(self.displist)
        self.plotphase=1-self.plotphase
        ax = plt.subplot(111)
        plt.cla()
        ax = plt.subplot(111)
        self.plotmeanbaselines(i)
        plt.draw()
        
    def next(self, event):
        self.ind += 1
        i = self.ind % len(self.displist)
        ax = plt.subplot(111)
        plt.cla()
        ax = plt.subplot(111)
        self.plotmeanbaselines(i)
        plt.draw()

    def prev(self, event):
        self.ind -= 1
        i = self.ind % len(self.displist)
        ax = plt.subplot(111)
        plt.cla()
        ax = plt.subplot(111)
        self.plotmeanbaselines(i)
        plt.draw()

    def undo(self, event):
        i = self.ind % len(self.displist)
        if (self.displist[i][8]==1):
            self.flags=self.flags[:-1]
            print(self.flags)
        else:
            self.freqflags=self.freqflags[:-1]
            print(self.freqflags)
            
        ax = plt.subplot(111)
        plt.cla()
        ax = plt.subplot(111)
        self.plotmeanbaselines(i)
        plt.draw()

    def onrelease(self, event):
        i = self.ind % len(self.displist)
        if (self.rubberband):
            self.rubberband.remove()
            self.rubberband=0
            plt.draw()
        thismanager = plt.get_current_fig_manager()
        end=[event.xdata,event.ydata,1]
        if (event.inaxes!=self.origax):
            if (event.x<self.start[3]):
                end[0]=-10000;
            else:
                end[0]=10000;
        if (self.start[:2]==end[:2] or self.start[2]!=1 or thismanager.toolbar.mode!=''):
            self.start=[0,0,0,0,0];
            return;
        if (self.displist[i][8]==1):
            if (end[0]<0.0):
                end[0]=0.0
            elif(end[0]>self.time1-self.time0):
                end[0]=self.time1-self.time0
            if (end[0]<self.start[0]):
                self.flags.append((end[0],self.start[0]))
            else:
                self.flags.append((self.start[0],end[0]))
            print(self.flags)
            ax = plt.subplot(111)
            xmax=ax.viewLim.xmax
            xmin=ax.viewLim.xmin
            ymax=ax.viewLim.ymax
            ymin=ax.viewLim.ymin
            plt.cla()
            ax = plt.subplot(111)
            self.plotmeanbaselines(i)
            plt.xlim((xmin,xmax))
            plt.ylim((ymin,ymax))
            plt.draw()
        else:
            if (end[0]<self.ch0):
                end[0]=self.ch0
            elif(end[0]>self.ch1):
                end[0]=self.ch1
            if (end[0]<self.start[0]):
                self.freqflags.append((end[0],self.start[0]))
            else:
                self.freqflags.append((self.start[0],end[0]))
            print(self.freqflags)
            ax = plt.subplot(111)
            xmax=ax.viewLim.xmax
            xmin=ax.viewLim.xmin
            ymax=ax.viewLim.ymax
            ymin=ax.viewLim.ymin
            plt.cla()
            ax = plt.subplot(111)
            self.plotmeanbaselines(i)
            plt.xlim((xmin,xmax))
            plt.ylim((ymin,ymax))
            plt.draw()
        self.start=[0,0,0,0,0];
        
    def onmousemove(self, event):
        thismanager = plt.get_current_fig_manager()
        if (self.start==[0,0,0,0,0] or thismanager.toolbar.mode!=''):
            return;
        if (self.rubberband):
            self.rubberband.remove()
            ax = plt.subplot(111)
            self.rubberband=plt.axvspan(self.start[0], event.xdata, facecolor="yellow", alpha=0.4)
            plt.draw()
    def onclick(self, event):
        thismanager = plt.get_current_fig_manager()
        if (event.inaxes!=self.origax or thismanager.toolbar.mode!=''):
            self.start=[0,0,0,0,0];
            return;
        self.start=[event.xdata,event.ydata,1,event.x,event.y]
#        self.rect=[event.x,ax.viewLim.ymin,event.x,ax.viewLim.ymax];
        ax = plt.subplot(111)
        self.rubberband=plt.axvspan(event.xdata, event.xdata, facecolor="yellow", alpha=0.4)
        plt.draw()
    def onpress(self, event):
        print('key pressed')

class FlagPlotASC:
    ind = 0
    start=[0,0,0,0,0]
    rubberband=0
    starttime=0
    doplotpow=1
    doplotphase=0
    def __init__(self,dataset,flags=[],scanlengthtime=180,datasetcallback=None):
        self.datasetcallback=datasetcallback
        self.flags=flags
        self.dataset=dataset
        self.scanlengthtime=scanlengthtime
        self.fig=plt.figure()
        self.fig.canvas.mpl_connect('key_press_event', self.onpress)
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.fig.canvas.mpl_connect('button_release_event', self.onrelease)
        self.fig.canvas.mpl_connect('motion_notify_event',self.onmousemove)
        self.fig.text(0.5,0.975,self.dataset.filename,horizontalalignment='center',verticalalignment='top')
        self.origax=self.fig.add_subplot(111)
        plt.subplots_adjust(bottom=0.2)
        self.plot()

        self.axsave = plt.axes([0.1, 0.05, 0.15, 0.075])
        self.axplotpow = plt.axes([0.4, 0.05, 0.09, 0.035])
        self.axplotphase = plt.axes([0.4, 0.085, 0.09, 0.035])
        self.axundo = plt.axes([0.6, 0.05, 0.09, 0.075])
        self.axprev = plt.axes([0.7, 0.05, 0.09, 0.075])
        self.axnext = plt.axes([0.8, 0.05, 0.09, 0.075])
        self.bsave = Button(self.axsave, 'Save&quit')
        self.bsave.on_clicked(self.save)
        self.bplotpow = CheckButtons(self.axplotpow, ['Pow'],[self.doplotpow])
        self.bplotpow.on_clicked(self.plotpow)
        self.bplotphase = CheckButtons(self.axplotphase, ['Phase'],[self.doplotphase])
        self.bplotphase.on_clicked(self.plotphase)
        self.bundo = Button(self.axundo, 'Undo')
        self.bundo.on_clicked(self.undo)
        self.bnext = Button(self.axnext, 'Next')
        self.bnext.on_clicked(self.next)
        self.bprev = Button(self.axprev, 'Prev')
        self.bprev.on_clicked(self.prev)
    
    def plot(self):
        D2R=np.pi/180.0
        plt.sca(self.origax)
        plt.cla()
        valid=np.nonzero(np.logical_and(self.dataset.rawtime-self.dataset.rawtime[0]>=self.starttime,self.dataset.rawtime-self.dataset.rawtime[0]<self.starttime+self.scanlengthtime))[0]
        leg=[]
        if (self.doplotpow):
            vis=np.log10(np.abs(self.dataset.visibilities[0])+1)
            plt.plot(self.dataset.rawtime[valid]-self.dataset.rawtime[0],100*(vis[valid]-(np.nanmin(vis)))/(np.nanmax(vis)-np.nanmin(vis)),'g.')
            leg.append('power')
        if (self.doplotphase):
            vis=np.angle(self.dataset.visibilities[0])
            plt.plot(self.dataset.rawtime[valid]-self.dataset.rawtime[0],100*(vis[valid]-(np.min(vis)))/(np.max(vis)-np.min(vis)),'m.')
            leg.append('phase')
        plt.plot(self.dataset.rawtime[valid]-self.dataset.rawtime[0],100*(self.dataset.scanel[valid]-np.min(self.dataset.scanel))/(np.max(self.dataset.scanel)-np.min(self.dataset.scanel)),'k.')
        plt.plot(self.dataset.rawtime[valid]-self.dataset.rawtime[0],100*(self.dataset.scanaz[valid]-np.min(self.dataset.scanaz))/(np.max(self.dataset.scanaz)-np.min(self.dataset.scanaz)),'b.')
        leg.append('el')
        leg.append('az')
        plt.xlim([self.starttime,self.starttime+self.scanlengthtime])
        plt.ylim([-20,120])
        plt.xlabel('Time [s]')
        plt.ylabel('[%]')
        plt.legend(leg)
        for flags in self.flags:
            plt.axvspan(flags[0], flags[1], facecolor="red", alpha=0.4)
    
    def save(self, event):
        freqflags=[]
        output=open(self.dataset.dirname+'flags', 'wb')
        pickle.dump(self.flags,output)
        pickle.dump(freqflags,output)
        output.close();
        print('saving %d flags and %d freqflags to'%(len(self.flags),len(freqflags)),self.dataset.dirname+'flags')
        if (self.datasetcallback is not None):
            self.datasetcallback()
        plt.close(self.fig)

    def plotpow(self, event):
        self.doplotpow=1-self.doplotpow
        self.plot()
        plt.draw()

    def plotphase(self, event):
        self.doplotphase=1-self.doplotphase
        self.plot()
        plt.draw()
        
    def next(self, event):
        print([self.starttime,self.starttime+self.scanlengthtime])
        self.starttime+=+self.scanlengthtime//2
        self.plot()
        plt.draw()

    def prev(self, event):
        print([self.starttime,self.starttime+self.scanlengthtime])
        self.starttime-=+self.scanlengthtime//2
        self.plot()
        plt.draw()

    def undo(self, event):
        self.flags=self.flags[:-1]
        print(self.flags)
        self.plot()
        plt.draw()

    def onrelease(self, event):
        if (self.rubberband):
            self.rubberband.remove()
            self.rubberband=0
            plt.draw()
        thismanager = plt.get_current_fig_manager()
        end=[event.xdata,event.ydata,1]
        if (event.inaxes!=self.origax):
            if (event.x<self.start[3]):
                end[0]=-100000;
            else:
                end[0]=100000;
        if (self.start[:2]==end[:2] or self.start[2]!=1 or thismanager.toolbar.mode!=''):
            self.start=[0,0,0,0,0];
            return;
        if (end[0]<0.0):
            end[0]=0.0
        elif(end[0]>self.dataset.rawtime[-1]-self.dataset.rawtime[0]):
            end[0]=self.dataset.rawtime[-1]-self.dataset.rawtime[0]
        if (end[0]<self.start[0]):
            self.flags.append((end[0],self.start[0]))
        else:
            self.flags.append((self.start[0],end[0]))
        print(self.flags)
        self.plot()
        plt.draw()
        self.start=[0,0,0,0,0];
        
    def onmousemove(self, event):
        thismanager = plt.get_current_fig_manager()
        if (self.start==[0,0,0,0,0] or thismanager.toolbar.mode!=''):
            return;
        if (self.rubberband):
            self.rubberband.remove()
            plt.sca(self.origax)
            self.rubberband=plt.axvspan(self.start[0], event.xdata, facecolor="yellow", alpha=0.4)
            plt.draw()

    def onclick(self, event):
        thismanager = plt.get_current_fig_manager()
        if (event.inaxes!=self.origax or thismanager.toolbar.mode!=''):
            self.start=[0,0,0,0,0];
            return;
        self.start=[event.xdata,event.ydata,1,event.x,event.y]
        plt.sca(self.origax)
        self.rubberband=plt.axvspan(event.xdata, event.xdata, facecolor="yellow", alpha=0.4)
        plt.draw()

    def onpress(self, event):
        print('key pressed')


#Copyright National Research Foundation (SARAO), 2005-2025. All Rights Reserved.
#Author: Mattieu de Villiers (email: mattieu@sarao.ac.za)
"""
    Copyright National Research Foundation (SARAO), 2005-2025. All Rights Reserved.
    Author: Mattieu de Villiers (email: mattieu@sarao.ac.za)
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scikits.fitting import NonLinearLeastSquaresFit, PiecewisePolynomial1DFit, Spline2DScatterFit, GaussianFit
from scipy.optimize import minimize
import scikits.fitting as fitting
import array
import scipy
import os,sys,time
from multiprocessing import Process, Queue, cpu_count
import katdal
import pickle
import optparse
from .utilities import *
from .flag import FlagPlot,FlagPlotASC
import re
import katpoint
import datetime

def pydftdelay(signal):
    validsignal=np.nonzero(signal!=0.0)[0]
    ws=np.roll(np.linspace(-np.pi,np.pi,len(signal),endpoint=False),len(signal)//2)
    Fsignal=np.abs(np.fft.fft(signal))
    iFsignal=np.argmax(Fsignal)
    x=np.arange(len(signal),dtype='float')
    w0=ws[iFsignal]-(ws[1]-ws[0])/2
    w1=ws[iFsignal]+0
    w2=ws[iFsignal]+(ws[1]-ws[0])/2
    F0=np.abs(np.sum(signal*np.exp(-1j*x*w0)))#direct fourier transform at this w
    F1=Fsignal[iFsignal]
    F2=np.abs(np.sum(signal*np.exp(-1j*x*w2)))#direct fourier transform at this w
    for iterate in range(50):
        if F0>=F1 or F0>F2:
            F2=F1;w2=w1;
        else:
            F0=F1;w0=w1;
        w1=0.5*(w0+w2)
        F1=np.abs(np.sum(signal*np.exp(-1j*x*w1)))#direct fourier transform at this w
    delay_rad_per_sample=w1#radians per sample
    return delay_rad_per_sample

#should actually be caled pydftdelayt
#per second (x), not per sample
#vis*np.exp(-1j*delay*np.arange(len(vis)))
#vis*np.exp(-1j*delay*x)
#note that the FFT of signal may be multimodal, thats why doing FFT first
def pydftdelayx(x,signal,ws0=-np.pi/2,ws1=np.pi/2,nsamples=1024):
    # nsamples=1024
    Fs=np.zeros(nsamples,dtype='float')
    ws=np.linspace(ws0,ws1,nsamples)
    for i,w in enumerate(ws):
        Fs[i]=np.abs(np.sum(signal*np.exp(-1j*x*w)))
    imax=np.argmax(Fs[1:-1])+1#avoid possibility of selecting limits
    w0=ws[imax-1]
    w1=ws[imax]
    w2=ws[imax+1]
    F0=Fs[imax-1]
    F1=Fs[imax]
    F2=Fs[imax+1]
    for iterate in range(50):
        if F0>=F1 or F0>F2:
            F2=F1;w2=w1;
        else:
            F0=F1;w0=w1;
        w1=0.5*(w0+w2)
        F1=np.abs(np.sum(signal*np.exp(-1j*x*w1)))#direct fourier transform at this w
    delay_rad_per_sample=w1#radians per sample
    return delay_rad_per_sample#actually per (x) time, not sample


#note that offdata should include all the data used on target too - I hope - which would be best
def nextinterpbestwrap(offdata,ondata,offtime,ontime):
    result=np.zeros(offdata.shape,dtype='complex')
    s_per_wrap=[]
    scan_periods=[]
    for it in range(len(ontime)-1):
        t0=ontime[it]
        t1=ontime[it+1]
        dt=t1-t0
        validfittimeind=np.nonzero((abs(offtime-t0)<20)+(abs(offtime-t1)<20))[0]# 10 sec around time division markers included
        # validfittimeind=np.nonzero((offtime>t0-10)*(offtime<t1+10))[0]# include all data inbetween too
        
        valid=np.nonzero(np.logical_and(offtime>=t0,offtime<t1))[0]
        a0=np.abs(ondata[it])
        a1=np.abs(ondata[it+1])
        ph0=np.angle(ondata[it])
        ph1=np.angle(ondata[it+1])
        
        delay_rad_s=pydftdelayx(offtime[validfittimeind]-t0,offdata[validfittimeind])
        # scan_periods.append('%.1f'%(t1-t0))
        scan_periods.append([t0,t1])
        s_per_wrap.append('%.1f'%(np.pi/(delay_rad_s)))
        interpdata=scipy.interp(x=offtime[valid],xp=[t0,t1],fp=[a0,a1])*np.exp(1j*scipy.interp(x=offtime[valid],xp=[t0,t1],fp=[ph0,ph0+delay_rad_s*(t1-t0)]))
        result[valid]=interpdata

    print('\nScan periods [s]:',scan_periods)
    print('\nPhase wrap periods [s]:',s_per_wrap)
    return result

#there an integer number of wraps, not needed to fit anything
def interpbestwrapgood8degscans(offdata,ondata,offtime,ontime):
    result=np.zeros(offdata.shape,dtype='complex')
    bestfitnesses=[]
    s_per_wrap=[]
    scan_periods=[]
    for it in range(len(ontime)-1):
        t0=ontime[it]
        t1=ontime[it+1]
        dt=t1-t0
        validtimeind=np.nonzero((abs(offtime-t0)<10)+(abs(offtime-t1)<10))[0]# 20 sec around time division markers included
        # validtimeind=np.nonzero((offtime>t0-10)*(offtime<t1+10))[0]# include all data inbetween too
        # validtimeind=np.nonzero(np.logical_and(offtime>=t0,offtime<t1))[0]
        
        valid=np.nonzero(np.logical_and(offtime>=t0,offtime<t1))[0]
        if it==0:
            minind=valid[0]
        a0=np.abs(ondata[it])
        a1=np.abs(ondata[it+1])
        ph0=np.angle(ondata[it])
        ph1=np.angle(ondata[it+1])
        bestnwraps=0
        bestfitness=-1e300
        for nwraps in range(-4,5,1):
            contend=(ph1-ph0)/(t1-t0)-(2*np.pi*nwraps)/(t1-t0)
            w1=contend
            x=offtime[validtimeind]-t0#note these may be beyond t0 to t1 range
            phaseadj=x*w1+ph0#add ph0
            gainadj=(a1-a0)/(t1-t0)*x+a0
            signal=offdata[validtimeind]
            adjsignal=signal/gainadj*np.exp(-1j*phaseadj) 
            # fitness=np.abs(np.sum(signal*np.exp(-1j*x*w1)))#this effectively applies the phase slope correction to the data, and simply sums and then take abs value; it is also the fourier transform
            # fouriertrans=np.sum(signal*np.exp(-1j*x*w1))
            # fitness=np.abs(fouriertrans.real)**2-np.abs(fouriertrans.imag)**2#maximizes main lobe real component, ideally zero imaginary component
            fitness=np.sum(adjsignal.real)#maximizes main lobe real positive component, ideally zero imaginary component
            #fitness=np.sum(adjsignal.real*np.abs(adjsignal.real))#maximizes main lobe real positive component, ideally zero imaginary component
            if fitness>bestfitness:
                bestfitness=fitness
                bestnwraps=nwraps
        bestfitnesses.append(bestfitness)
        delay_rad_s=(ph1-ph0)/(t1-t0)-(2*np.pi*bestnwraps)/(t1-t0)
        # scan_periods.append('%.1f'%(t1-t0))
        scan_periods.append([t0,t1])
        s_per_wrap.append('%.1f'%(np.pi/(delay_rad_s)))
        # delay_rad_s=(ph1-ph0)/(t1-t0)-(2*np.pi*0)/(t1-t0)
        interpdata=scipy.interp(x=offtime[valid],xp=[t0,t1],fp=[a0,a1])*np.exp(1j*scipy.interp(x=offtime[valid],xp=[t0,t1],fp=[ph0,ph0+delay_rad_s*(t1-t0)]))
        result[valid]=interpdata
    maxind=valid[-1]
    result[:minind]=result[minind]#end bits zero order interpolation
    result[maxind:]=result[maxind]
    print('\nbestfitnesses:',bestfitnesses)
    print('\nScan periods [s]:',scan_periods)
    print('\nPhase wrap periods [s]:',s_per_wrap)
    return result
    
def interpbestwrap(offdata,ondata,offtime,ontime):    
    offdelay_rad_s=pydftdelayx(offtime,offdata,ws0=-np.pi/2/10,ws1=np.pi/2/10,nsamples=1024*8)
    onphase=offdelay_rad_s*(ontime-ontime[0])
    offphase=offdelay_rad_s*(offtime-offtime[0])
    result=scipy.interp(x=offtime,xp=ontime,fp=np.abs(ondata))*np.exp(1j*(scipy.interp(x=offtime,xp=ontime,fp=np.unwrap(np.angle(ondata)-onphase))+offphase))

    print('\nScan periods [s]:',np.mean(np.diff(ontime)))
    print('\nAvg phase wrap period [s]:',2*np.pi/offdelay_rad_s)
    return result
    
class Dataset(object):
    """Dataset object interacts with file to read visibilities. 
    
    For ASC files, reads entire file and store az,el and data. 
    For H5 files, reads from file as necessary.
    """
    def __init__(self,filename,telescopename,targetaz_deg=None,targetel_deg=None,freq_MHz=None,clipextent=None,method='direct',gainintervaltime=30*60,onaxisnormalise=True,ignoreantennas=[],testmx=[1.0,0.0,0.0,1.0],targetname=None,onaxissampling=None,katdal_centre_freq=None,extralmoffset=[0.0,0.0],timingoffset=0,phaseslope=0,flaglimit=None,dodelay=False,dobandpass=False,scanantname=None,ascscantime=None,ascapplylabels=True,ascflags=[],findwrap=False,select_loadscan_cycle=None,select_loadscan_group=None):
        """Create a holography dataset object from one of a variety of file types (.rdb .h5, .asc, .pat)

        Parameters
        ----------
        filename : string or katdal object
            Filename, with recognised type (.rdb .h5, .asc, .pat)
        telescopename: string
            Recognised telescope name
            ('kat7', 'hirax', 'xdm', 'kat7emss', 'meerkat', 'mopra' or 'vla')
        targetaz_deg: float
            For files of type .asc, specify the azimuth angle to the satelite, in degrees.
            Ignore for .h5 files
        targetel_deg: float
            For files of type .asc, specify the elevation angle to the satelite, in degrees.
            Ignore for .h5 files
        freq_MHz: float
            For files of type .asc, or .pat, specify the frequency of the observation, in MHz.
            Ignore for .h5 files
        clipextent: float
            Diameter extent to which the beam data should be clipped, in degrees. 
        method: string
            Calibration method to use, 'direct', or 'model'.
        gainintervaltime: int
            Period of an interval for gain solutions, in seconds
        ignoreantennas: list of strings
            Antenna names of antennas to exclude.
        onaxissampling: None or float
            If None, determined automatically, else the radius in degrees for region used to 
            use for on-axis calibration.
                    
        Note if pointing offset seems inaccurate (e.g. when doing beam.plotcuts() with correct pointingoffset applied) then may be necessary to reduce gainintervaltime to say gainintervaltime=10*60
        """
        self.findwrap=findwrap
        self.katdal_centre_freq=katdal_centre_freq
        self.phaseslope=phaseslope
        self.speedoflight=299792458.0
        self.testmx=testmx
        self.database={}
        self.polc=None
        self.rawtime=None
        self.flaglimit=flaglimit
        self.dodelay=dodelay
        self.dobandpass=dobandpass
        self.extralmoffset=extralmoffset
        #a subdirectory can be specified under a directory of same name of h5 file as a directory for output also containing flag information
        self.telescopename=telescopename
        self.method=method
        self.gainintervaltime=gainintervaltime
        self.onaxisnormalise=onaxisnormalise
        self.flagfirstslew_index=0
        self.scanantname=scanantname
        if (isinstance(filename,dict)):
            self.fileext='.DICT'
            rho=np.sqrt(filename['x']**2+filename['y']**2)
            if (clipextent!=None):
                valid=np.nonzero(rho*(180.0/np.pi)<clipextent/2.0)[0]
            else:
                valid=range(len(rho))
            self.ll=filename['x'][valid]
            self.mm=filename['y'][valid]
            ind_onaxis=np.nonzero((self.ll==0.0)*(self.mm==0.0))[0]
            self.visibilities=[filename['HH'][valid],filename['VV'][valid],filename['HV'][valid],filename['VH'][valid]]
            self.targetaz,self.targetel=0,0#targetaz_deg*D2R,targetel_deg*D2R
            self.scanaz,self.scanel=0,0#(targetaz_deg+scanrelaz_deg)*D2R,(targetel_deg+scanrelel_deg)*D2R
            self.h5=None
            self.channel_range=[0]            
            self.radialscan_centerfreq=np.array([np.float64(freq_MHz)*1e6])
            self.radialscan_channels=np.array([0])
            self.radialscan_allantenna=['ant1','ant2']
            self.radialscan_scanantenna=['ant1']
            self.trackantennas=np.array([1],dtype='int')
            self.time_range=np.arange(len(self.mm))
            self.flagmask=np.zeros(self.mm.shape,dtype='bool')
            self.radialscan_sampling,self.radialscan_extent=self.findsampling(self.ll,self.mm,self.flagmask)
            self.flags=[]
            self.freqflags=[]
            self.pols_to_use = ['HH','HV','VH','VV']
            return
        elif (isinstance(filename,katdal.DataSet)):
            self.h5=filename
            filename=self.h5.name.split('|')[0].replace(' ','').split(',')[0]+'.rdb'
        else:
            self.h5=None
        upperfilename=filename.upper()
        print('filename is',filename)            
        if (upperfilename.endswith(".DICT") or upperfilename.endswith(".RDB") or upperfilename.endswith(".H5") or upperfilename.endswith(".ASC") or upperfilename.endswith(".RIASC") or upperfilename.endswith(".PAT") or upperfilename.endswith(".MAT")):
            self.dirname=os.path.splitext(filename)[0]+'/';
            self.fulldirectory=os.path.abspath(self.dirname)+'/'
            self.subdirectory=""
            self.filename=filename
        else:#look for h5 file by going up tree towards root
            self.fulldirectory=os.path.abspath(filename)+'/'
            lookdirectory=self.fulldirectory;
            self.subdirectory=""
            while(len(lookdirectory) and not os.path.exists(lookdirectory[:-1]+'.h5') ):
                ind=(lookdirectory[:-1].rfind('/'))+1
                self.subdirectory=lookdirectory[ind:]+self.subdirectory
                lookdirectory=lookdirectory[:ind]
            self.dirname=lookdirectory
            if (self.dirname==''):
                print('Please provide .rdb .h5, .ASC or .PAT filename as argument, or a subdirectory')
                return
            self.filename=self.dirname[:-1]+'.h5'
            upperfilename=self.filename.upper()
        #creates subdirectory if does not exist
        # if (not os.path.exists(self.fulldirectory)):
        #     try:
        #         os.makedirs(self.fulldirectory)
        #     except:
        #         print('WARNING: could not create %s'%(self.fulldirectory))
        #         pass
        if (upperfilename.endswith('.PAT')):
            self.fileext='.PAT'
            if (freq_MHz==None):
                print('Error: importing PAT file requires specification for freq_MHz')
            self.ll,self.mm,E_xy, E_xx = self.loadPattern(filename, clipextent,None)
            self.targetaz,self.targetel=0,0#targetaz_deg*D2R,targetel_deg*D2R
            self.scanaz,self.scanel=0,0#(targetaz_deg+scanrelaz_deg)*D2R,(targetel_deg+scanrelel_deg)*D2R
            self.visibilities=[E_xx, E_xy]
            self.h5=None
            self.channel_range=[0]            
            self.radialscan_centerfreq=np.array([np.float64(freq_MHz)*1e6])
            self.radialscan_channels=np.array([0])
            self.radialscan_allantenna=['ant1','ant2']
            self.radialscan_scanantenna=['ant1']
            self.trackantennas=np.array([1],dtype='int')
            self.time_range=np.arange(len(self.mm))
            self.flagmask=np.zeros(self.mm.shape,dtype='bool')
            self.radialscan_sampling,self.radialscan_extent=self.findsampling(self.ll,self.mm,self.flagmask)
            self.flags=[]
            self.freqflags=[]
            self.pols_to_use=['HH','HV']
        elif (upperfilename.endswith('.MAT')):
            import scipy.io
            self.fileext='.MAT'
            D = scipy.io.loadmat(filename)
            th=D["th"].squeeze()#degrees
            ph = D["ph"][:-1].squeeze()#degrees
            phi,rho = np.meshgrid(ph*np.pi/180,np.sin(th*np.pi/180))
            phi=phi.reshape(-1)#direction cosine
            rho=rho.reshape(-1)#direction cosine
            if (clipextent!=None):
                valid=np.nonzero(rho*(180.0/np.pi)<clipextent/2.0)[0]
            else:
                valid=range(len(rho))
            self.ll=rho[valid]*np.sin(phi[valid])#direction cosine
            self.mm=rho[valid]*np.cos(phi[valid])#direction cosine
            ind_onaxis=np.nonzero((self.ll==0.0)*(self.mm==0.0))[0]
            if ("JHH" in D.keys()):
                JHH = D["JHH"][:,:-1].squeeze().reshape(-1)[valid]
                JHV = D["JHV"][:,:-1].squeeze().reshape(-1)[valid]
                JVH = D["JVH"][:,:-1].squeeze().reshape(-1)[valid]
                JVV = D["JVV"][:,:-1].squeeze().reshape(-1)[valid]
            else:#new kind of mat file
                if 'freqMHz' in D:
                    ichan=D['freqMHz'][0].tolist().index(np.float64(freq_MHz))
                    JHH = D["Jqh"][ichan,:,:-1].squeeze().reshape(-1)[valid]
                    JHV = D["Jqv"][ichan,:,:-1].squeeze().reshape(-1)[valid]
                    JVH = D["Jph"][ichan,:,:-1].squeeze().reshape(-1)[valid]
                    JVV = D["Jpv"][ichan,:,:-1].squeeze().reshape(-1)[valid]
                else:
                    JHH = D["Jqh"][:,:-1].squeeze().reshape(-1)[valid]
                    JHV = D["Jqv"][:,:-1].squeeze().reshape(-1)[valid]
                    JVH = D["Jph"][:,:-1].squeeze().reshape(-1)[valid]
                    JVV = D["Jpv"][:,:-1].squeeze().reshape(-1)[valid]
            self.rawvisibilities=[JHH,JVV,JHV,JVH]
            self.visibilities=[JHH/np.mean(JHH[ind_onaxis]),JVV/np.mean(JVV[ind_onaxis]),JHV/np.mean(JHH[ind_onaxis]),JVH/np.mean(JVV[ind_onaxis])]
             
            #self.visibilities=[JHH,JVV,JHV,JVH]
            self.targetaz,self.targetel=0,0#targetaz_deg*D2R,targetel_deg*D2R
            self.scanaz,self.scanel=0,0#(targetaz_deg+scanrelaz_deg)*D2R,(targetel_deg+scanrelel_deg)*D2R
            self.h5=None
            self.channel_range=[0]            
            self.radialscan_centerfreq=np.array([np.float64(freq_MHz)*1e6])
            self.radialscan_channels=np.array([0])
            self.radialscan_allantenna=['ant1','ant2']
            self.radialscan_scanantenna=['ant1']
            self.trackantennas=np.array([1],dtype='int')
            self.time_range=np.arange(len(self.mm))
            self.flagmask=np.zeros(self.mm.shape,dtype='bool')
            self.radialscan_sampling,self.radialscan_extent=self.findsampling(self.ll,self.mm,self.flagmask)
            self.flags=[]
            self.freqflags=[]
            self.pols_to_use = ['HH','HV','VH','VV']
            
        elif (upperfilename.endswith('.ASC') or upperfilename.endswith('.RIASC')):
            if (upperfilename.endswith(".ASC")):
                self.fileext='.ASC'
            else:
                self.fileext='.RIASC'
            if (targetaz_deg!=None and targetel_deg!=None and freq_MHz!=None):
                vals = np.genfromtxt(self.filename,comments="#")
                if (np.shape(vals)[1]>5):
                    labels = np.genfromtxt(self.filename,comments="#",dtype='string')[:,5]
                    labels = np.array([label[:4].lower() for label in labels])
                    if ascscantime is not None:
                        print('Applying ascscantime %s'%ascscantime)
                        stop=np.nonzero(labels=='stop')[0]
                        times=vals[:,4]
                        ontarget=[]
                        offtarget=[]
                        meanx=[]
                        meany=[]
                        meant=[]
                        for istop in stop:
                        	isscan=np.nonzero(((times<times[istop]) & (times>times[istop]-ascscantime)))[0]
                        	labels[isscan]='scan'
                        	it=istop
                        	if labels[istop+1]!='stop':
                        		while labels[it]!='scan':
                        			it+=1
                        		ontarget.append(it)
                        		while it<len(labels) and labels[it]=='scan':
                        			it+=1
                        		offtarget.append(it)
                        		meanx.append(np.mean(vals[ontarget[-1]:offtarget[-1],0]))
                        		meany.append(np.mean(vals[ontarget[-1]:offtarget[-1],1]))
                        		meant.append(np.mean(vals[ontarget[-1]:offtarget[-1],4]))
                        xoffset=np.interp(vals[:,4],meant,meanx)
                        yoffset=np.interp(vals[:,4],meant,meany)
                        vals[:,0]-=xoffset
                        vals[:,1]-=yoffset
                    if True:
                        #convert labels into flags
                        rawtime=vals[:,4]
                        rawtime=rawtime-rawtime[0]
                        c=0
                        self.ascflags=[]
                        while (c<len(labels)):
                            while (labels[c]=='scan' or labels[c]=='trac'):
                                c+=1
                                if (c>=len(labels)):
                                    break
                            if (c>=len(labels)):
                                break
                            if (c>0):
                                flagstart=0.5*(rawtime[c]+rawtime[c-1])
                            else:
                                flagstart=rawtime[c]-0.1
                            while (not (labels[c]=='scan' or labels[c]=='trac')):
                                c+=1
                                if (c>=len(labels)):
                                    break
                            if (c>=len(labels)):
                                flagstop=rawtime[-1]+0.1
                            else:
                                flagstop=0.5*(rawtime[c-1]+rawtime[c])
                            self.ascflags.append((flagstart,flagstop))
                    if (ascapplylabels):
                        vals = np.array([vals[c,:5] for c in range(vals.shape[0]) if (labels[c]=='scan' or labels[c]=='trac')])
                    if (len(ascflags)):
                        rawtime=vals[:,4]
                        rawtime=rawtime-rawtime[0]
                        valid=np.ones(len(rawtime))
                        for flags in ascflags:
                            ind=np.nonzero(np.logical_and(rawtime>=flags[0],rawtime<=flags[1]))[0]
                            valid[ind]=0
                        validind=np.nonzero(valid)[0]
                        vals=vals[validind,:]  
                        self.ascflags=ascflags                      
                        
                #vals = np.genfromtxt(self.filename,comments="#",delimiter=",")
                #print('WARNING - using PERLEYFACTOR 0.765')
                perleyfactor=1.0;#0.765
                scanrelaz_deg,scanrelel_deg,amp,phase_deg=vals[:,0]*perleyfactor,vals[:,1]*perleyfactor,vals[:,2],vals[:,3]
                if (np.shape(vals)[1]>4):
                    self.rawtime=vals[:,4]
                    
                self.targetaz,self.targetel=targetaz_deg*D2R,targetel_deg*D2R
                if (self.targetaz==0.0 and self.targetel==0.0):
                    self.scanaz,self.scanel=scanrelaz_deg*D2R,scanrelel_deg*D2R
                    self.ll,self.mm=scanrelaz_deg*D2R,scanrelel_deg*D2R
                else:
                    self.scanaz,self.scanel=(targetaz_deg+scanrelaz_deg)*D2R,(targetel_deg+scanrelel_deg)*D2R
                    self.ll,self.mm=sphere_to_plane_holography(self.targetaz,self.targetel,self.scanaz,self.scanel);
                if (self.fileext=='.ASC'):
                    self.visibilities=[amp*np.exp(1j*(-phase_deg*D2R))]
                else:
                    self.visibilities=[amp+1j*phase_deg]
                if (self.rawtime is not None and self.flaglimit is not None):#flag data with spikes
                    keep=np.nonzero(np.abs(self.visibilities[0])<self.flaglimit)[0]
                    self.visibilities[0]=self.visibilities[0][keep]
                    self.rawtime=self.rawtime[keep]
                    self.ll=self.ll[keep]
                    self.mm=self.mm[keep]
                    self.scanel=self.scanel[keep]
                    self.scanaz=self.scanaz[keep]
                if (clipextent!=None):
                    if (clipextent>0):
                        valid=np.nonzero(np.logical_and(np.abs(self.ll)<clipextent/2.0*D2R,np.abs(self.mm)<clipextent/2.0*D2R))[0]
                    else:
                        valid=np.nonzero(np.sqrt(self.ll**2+self.mm**2)<-clipextent/2.0*D2R)[0]
                    self.ll=self.ll[valid]
                    self.mm=self.mm[valid]
                    self.scanel=self.scanel[valid]
                    self.scanaz=self.scanaz[valid]
                    self.visibilities[0]=self.visibilities[0][valid]
                    if (self.rawtime is not None):
                        self.rawtime=self.rawtime[valid]
                self.h5=None
                self.channel_range=[0]
                self.radialscan_centerfreq=np.array([np.float64(freq_MHz)*1e6])
                self.radialscan_channels=np.array([0])
                self.radialscan_allantenna=['ant1','ant2']
                self.radialscan_scanantenna=['ant1']
                self.trackantennas=np.array([1],dtype='int')
                self.time_range=np.arange(len(self.mm))
                self.flagmask=np.zeros(self.mm.shape,dtype='bool')
                self.radialscan_sampling,self.radialscan_extent=self.findsampling(self.ll,self.mm,self.flagmask)
                self.flags=[]
                self.freqflags=[]
                self.pols_to_use=['HH']
                if (onaxissampling is not None):
                    self.radialscan_sampling=onaxissampling*np.pi/180.0
            else:
                print('Error: importing ASC file requires a specification for targetaz_deg, targetel_deg, freq_MHz')
        elif (upperfilename.endswith('.H5') or upperfilename.endswith('.RDB')):
            self.fileext='.h5'
            if (self.h5):
                self.h5.select()
            else:
                # self.h5=katdal.open(self.filename,quicklook=True,centre_freq=self.katdal_centre_freq)
                self.h5=katdal.open(self.filename,centre_freq=self.katdal_centre_freq,time_offset=timingoffset)
            self.radialscan_allantenna=[ant.name for ant in self.h5.ants]
            self.radialscan_scanantenna=[]
            if (hasattr(self.h5,'file') and len(self.h5.file)>0 and 'MetaData' in self.h5.file['/']):
                #self.pols_to_use = ['VV','VH','HV','HH']#Corresponds to XX,XY,YX,YY for correlation matrix [[XX,XY],[YX,YY]]
                self.pols_to_use = ['HH','HV','VH','VV']
                param=self.h5.obs_params['script_arguments']#self.h5.file['MetaData/Configuration/Observation'].attrs['script_arguments'];
                if len(param.split('-l '))>1:
                    self.radialscan_extent=np.double(param.split('-l ')[1].split(' ')[0])
                elif len(param.split('--scan-extent='))>1:
                    self.radialscan_extent=np.double(param.split('--scan-extent=')[1].split(' ')[0])
                elif len(param.split('--scan-extent '))>1:
                    self.radialscan_extent=np.double(param.split('--scan-extent ')[1].split(' ')[0])
                else:
                    print('Error: '+self.filename+' is not a holography dataset')
                    self.radialscan_extent=None
                if (hasattr(self.h5,'obs_params') and 'scan_ants' in self.h5.obs_params):
                    self.radialscan_scanantenna=self.h5.obs_params['scan_ants'].split(',')
                elif (1):#automatically detect scanning antennas from azel data
                    #Determine which indices are valid
                    #degrees per minute of antenna movement
                    self.deg_per_min=60.0*np.sqrt(np.abs(np.diff(self.h5.az,axis=0))**2+np.abs(np.diff(self.h5.el,axis=0))**2)/(self.h5.timestamps[1]-self.h5.timestamps[0])
                    #self.mean_deg_per_min=np.mean(self.deg_per_min,axis=0)#mean_deg_per_min=np.percentile(deg_per_min,[80],axis=0)[0]
                    #mean does not work well for taua1850apr2.h5 etc where scanning starts from stow position (if auto attenuate done long before and carried over)
                    self.mean_deg_per_min=np.median(self.deg_per_min,axis=0)#mean_deg_per_min=np.percentile(deg_per_min,[80],axis=0)[0]
                    if (np.max(self.mean_deg_per_min)<1.0):#fastest antenna moves slower than 1 degree a minute on average, assume all are tracking
                        print('WARNING: Fastest antenna moves slower than 1deg per minute, assuming all are tracking')
                        scanning=[]
                    elif (np.min(self.mean_deg_per_min)>1.0):#slowest antenna moves faster than 1 degree a minute on average, assume all are scanning
                        print('WARNING: Slowest antenna moves faster than 1deg per minute, assuming all are scanning')
                        scanning=range(self.h5.az.shape[1])
                    else:#typical solution
                        thresh=(np.min(self.mean_deg_per_min)+np.max(self.mean_deg_per_min))/2.0
                        scanning=np.nonzero(self.mean_deg_per_min>thresh)[0]
                    self.radialscan_scanantenna=[self.h5.ants[iscan].name for iscan in scanning]
                    # debugging info
                    # print 'mean_deg_per_min',mean_deg_per_min
                    # print 'threshold:',thresh,' scanning: ',[h5.ants[iscan].name for iscan in scanning]                    
                else:
                    for ant in self.radialscan_allantenna:
                        if (np.sum(self.h5.sensor['Antennas/%s/activity'%(ant)] == 'track')<self.h5.timestamps.shape[0]/2):
                            self.radialscan_scanantenna.append(ant)
            elif(len(self.h5.ants)==2 and self.h5.ants[1].diameter==1.0):#assume it is an old style holography file
                self.pols_to_use=['HH']
                self.radialscan_scanantenna=[self.h5.ants[0].name]
                self.radialscan_extent=None
            else:
                print('Error: '+self.filename+' is not a holography dataset')
                print('Trying anyways')
                self.pols_to_use = ['HH','HV','VH','VV']
                #Determine which indices are valid
                #degrees per minute of antenna movement
                self.deg_per_min=60.0*np.sqrt(np.abs(np.diff(self.h5.az,axis=0))**2+np.abs(np.diff(self.h5.el,axis=0))**2)/(self.h5.timestamps[1]-self.h5.timestamps[0])
                #self.mean_deg_per_min=np.mean(self.deg_per_min,axis=0)#mean_deg_per_min=np.percentile(deg_per_min,[80],axis=0)[0]
                #mean does not work well for taua1850apr2.h5 etc where scanning starts from stow position (if auto attenuate done long before and carried over)
                self.mean_deg_per_min=np.median(self.deg_per_min,axis=0)#mean_deg_per_min=np.percentile(deg_per_min,[80],axis=0)[0]
                if (hasattr(self.h5,'obs_params') and 'scan_ants' in self.h5.obs_params):
                    self.radialscan_scanantenna=self.h5.obs_params['scan_ants'].split(',')
                elif (1):
                    if (np.max(self.mean_deg_per_min)<1.0):#fastest antenna moves slower than 1 degree a minute on average, assume all are tracking
                        print('WARNING: Fastest antenna moves slower than 1deg per minute, assuming all are tracking')
                        scanning=[]
                    elif (np.min(self.mean_deg_per_min)>1.0):#slowest antenna moves faster than 1 degree a minute on average, assume all are scanning
                        print('WARNING: Slowest antenna moves faster than 1deg per minute, assuming all are scanning')
                        scanning=range(self.h5.az.shape[1])
                    else:#typical solution
                        thresh=(np.min(self.mean_deg_per_min)+np.max(self.mean_deg_per_min))/2.0
                        scanning=np.nonzero(self.mean_deg_per_min>thresh)[0]
                    self.radialscan_scanantenna=[self.h5.ants[iscan].name for iscan in scanning]
                self.radialscan_extent=None
            
            self.options=optparse.Values()
            self.options.maxbaseline=None
            self.options.minbaseline=0
            self.options.normgainperbaseline=False
            self.scanantname=scanantname if (scanantname is not None) else np.r_[self.radialscan_scanantenna,self.radialscan_allantenna][0]
            # self.h5=katdal.open(self.filename,ref_ant=self.scanantname,centre_freq=self.katdal_centre_freq)#reopens with ref_ant
            self.h5.select()
            print('Extracting timestamps')
            self.rawtime=self.h5.timestamps[:]
            self.h5.select(compscans="~") # Datasets sometimes start with unlabeled compscans, causing target[0] to be 'Nothing'
            self.h5.select(reset="", scans="track", compscans="~slew") # Eliminate scans like azimuthunwrap
            if (targetname!=None and targetname in [tar.name for tar in self.h5.catalogue.targets]):
                self.target=self.h5.catalogue.targets[[tar.name for tar in self.h5.catalogue.targets].index(targetname)]
            elif (len(self.h5.target_indices)==1):
                self.target=self.h5.catalogue.targets[self.h5.target_indices[0]]#use target rather than tracking antenna, incase there are no tracking antennas
            else:
                radec_target_indices=[ind for ind in self.h5.target_indices if self.h5.catalogue.targets[ind].body_type=='radec']
                self.target=self.h5.catalogue.targets[radec_target_indices[0]]#should be only one target selected
                # self.target=self.h5.catalogue.targets[self.h5.target_indices[0]]#use target rather than tracking antenna, incase there are no tracking antennas
            self.h5.select(reset="T") # Undo previous select
            antnames=[ant.name for ant in self.h5.ants]
            if (scanantname in antnames):
                self.target.antenna=self.h5.ants[antnames.index(scanantname)] #target azel must be wrt scanning antenna position (not array center nor tracking antenna), in direction of target
            else:
                print('Error scanning antenna: '+scanantname+' not in '+','.join(antnames))
            targetname=None
            self.targetaz,self.targetel=self.target.azel(self.rawtime)#note this is in radians already#behind the scenes it is using h5.refant as observer position
            self.scanaz,self.scanel=self.h5.az[:,self.radialscan_allantenna.index(self.scanantname)]*D2R,self.h5.el[:,self.radialscan_allantenna.index(self.scanantname)]*D2R
            self.ll,self.mm=sphere_to_plane_holography(self.targetaz,self.targetel,self.scanaz,self.scanel)
            self.ll-=self.extralmoffset[0]*np.pi/180.0
            self.mm-=self.extralmoffset[1]*np.pi/180.0
            if (onaxissampling is None):
                self.radialscan_sampling=None
            else:
                self.radialscan_sampling=onaxissampling*np.pi/180.0
            self.flagdata(ignoreantennas=ignoreantennas,clipextent=clipextent,targetname=targetname,cycle=select_loadscan_cycle,group=select_loadscan_group)
        else:
            print('Error: Unknown file format')

    def printenv(self):
        print('Environmental summary for '+self.filename)
        print('Time start %s duration %s'%(self.env_time[1],str(datetime.timedelta(seconds=np.round(self.rawtime[self.time_range][-1]-self.rawtime[self.time_range][0])))))
        print('Elevation [deg] min %.1f max %.1f mean %.1f'%(self.env_el[1],self.env_el[2],self.env_el[0]))
        print('Windspeed [mps] min %.1f max %.1f mean %.1f'%(self.env_wind[1],self.env_wind[2],self.env_wind[0]))
        print('Wind direction [deg] min %.1f max %.1f mean %.1f'%(self.env_wind_dir[1],self.env_wind_dir[2],self.env_wind_dir[0]))
        print('Ambient temp [deg C] min %.1f max %.1f mean %.1f'%(self.env_temp[1],self.env_temp[2],self.env_temp[0]))
        print('Pressure [mbar] min %.1f max %.1f mean %.1f'%(self.env_pressure[1],self.env_pressure[2],self.env_pressure[0]))
        print('Humidity [%%] min %.1f max %.1f mean %.1f'%(self.env_humidity[1],self.env_humidity[2],self.env_humidity[0]))
        print('Sun angle [deg] min %.1f max %.1f mean %.1f'%(self.env_sun[1],self.env_sun[2],self.env_sun[0]))
        print('Antenna mean speed [deg per min] scan %.1f track %.1f'%(np.mean(self.mean_deg_per_min[self.scanantennas]),np.mean(self.mean_deg_per_min[self.trackantennas])))
    
    def flagplot(self,ignoreantennas=[],flagslew=False,refMHz=1800.0,dMHz=16,sigma=None,targetname=None,flagspeed=None,flagextratime=None,autocorrelations=False):
        self.ignoreantennas=ignoreantennas
        if sigma==None:
            sigma=self.radialscan_sampling/D2R
        if (flagslew):
            flagger=FlagPlot(self.h5,np.r_[self.scanantennas,self.trackantennas][0],sigma,np.sort(np.append(self.trackantennas,self.scanantennas)),self.radialscan_allantenna,refMHz,dMHz,'flagslew',self.freqflags,self.dirname+self.subdirectory,targetname=targetname,flagspeed=flagspeed,flagextratime=flagextratime,autocorrelations=autocorrelations)
        else:
            flagger=FlagPlot(self.h5,np.r_[self.scanantennas,self.trackantennas][0],sigma,np.sort(np.append(self.trackantennas,self.scanantennas)),self.radialscan_allantenna,refMHz,dMHz,self.flags,self.freqflags,self.dirname+self.subdirectory,targetname=targetname,flagspeed=flagspeed,flagextratime=flagextratime,autocorrelations=autocorrelations)
        flagger.start(flagger,self.finaliseflagplot)
        return flagger

    def finaliseflagplot(self):
        self.flagdata(ignoreantennas=self.ignoreantennas)#note: reads flags from file
        
    #assuming there are multiple cycles, find and use best scans only in dataset, maintaining one complete cycle in total.
    # best ones change least in phase from start to end calibration points when averaged over frequency range
    #antnamepair=('m001','m002')
    def findworstscanflags(self,freqMHz,dMHz,scanantennaname,trackantennaname,doplot=None):
        # channel_start=channel_ind[0]
        # channel_width=len(channel_ind)
        corrprod_to_index = dict([(tuple(cp), ind) for cp, ind in zip(np.r_[self.h5.corr_products,self.h5.corr_products[::,::-1]], np.r_[range(len(self.h5.corr_products)),range(len(self.h5.corr_products))])])
        
        antnames=np.sort([scanantennaname,trackantennaname])
        polprods = [("%s%s" % (antnames[0],p[0].lower()), "%s%s" % (antnames[1],p[1].lower())) for p in self.pols_to_use]
        cpindices=[corrprod_to_index.get(p) for p in polprods]

        scancalstart,scanstart,scanstop,scancalstop,nscanspercycle=self.findcyclescans(doplot=None,hrs=False)
        bestscan=np.zeros(nscanspercycle,dtype=np.int)
        bestscanvar=1e100*np.ones(nscanspercycle)
        if (isinstance(freqMHz,(np.int, np.float))):
            freqMHz=[freqMHz]
        for iscan in range(len(scanstop)):
            accvar=0.0
            for frequencyMHz in freqMHz:
                channel_ind=self.getchannelindices(frequencyMHz,dMHz,printout=False)
                for cp in cpindices:
                    accvar+=np.var(self.h5.vis[scancalstart[iscan]:scancalstop[iscan],channel_ind[0]:channel_ind[-1],cp].reshape(-1))
                    # accvar+=np.var(np.r_[self.h5.vis[scancalstart[iscan]:scanstart[iscan],channel_ind[0]:channel_ind[-1],cp].reshape(-1),self.h5.vis[scanstop[iscan]:scancalstop[iscan],channel_ind[0]:channel_ind[-1],cp].reshape(-1)])
            if (bestscanvar[iscan%nscanspercycle]>accvar):
                bestscanvar[iscan%nscanspercycle]=accvar
                bestscan[iscan%nscanspercycle]=iscan
        scancalstart_hrs=[(self.rawtime[it]-self.rawtime[0])/60./60. for it in scancalstart]
        scanstart_hrs=[(self.rawtime[it]-self.rawtime[0])/60./60. for it in scanstart]
        scanstop_hrs=[(self.rawtime[it]-self.rawtime[0])/60./60. for it in scanstop]
        scancalstop_hrs=[(self.rawtime[it]-self.rawtime[0])/60./60. for it in scancalstop]
        flagtime=[]
        halfsampletime=(self.rawtime[1]-self.rawtime[0])/60./60./2.0
        currenttime=-halfsampletime
        endtime=(self.rawtime[-1]-self.rawtime[0])/60./60.
        for iscan in range(len(scancalstop_hrs)):
            if (bestscan[iscan%nscanspercycle]==iscan):
                if (scancalstart_hrs[iscan]-halfsampletime>currenttime):
                    flagtime.append([currenttime,scancalstart_hrs[iscan]-halfsampletime])
                currenttime=scancalstop_hrs[iscan]+halfsampletime
        if (currenttime<endtime+halfsampletime):
            flagtime.append([currenttime,endtime+halfsampletime])
        if (doplot):
            plt.figure()
            if (doplot=='az' or doplot=='ll'):
                plt.plot((self.rawtime-self.rawtime[0])/60./60.,self.ll*180.0/np.pi)
            else:
                plt.plot((self.rawtime-self.rawtime[0])/60./60.,self.mm*180.0/np.pi)
            for iscan in range(nscanspercycle):
                if (iscan%2):
                    plt.fill([scancalstart_hrs[bestscan[iscan]],scanstart_hrs[bestscan[iscan]],scanstop_hrs[bestscan[iscan]],scancalstop_hrs[bestscan[iscan]],scancalstart_hrs[bestscan[iscan]]],[0,self.radialscan_extent/2.0*180.0/np.pi,self.radialscan_extent/2.0*180.0/np.pi,0,0],color=[0.5,0.5,0.5,0.5])
                else:
                    plt.fill([scancalstart_hrs[bestscan[iscan]],scanstart_hrs[bestscan[iscan]],scanstop_hrs[bestscan[iscan]],scancalstop_hrs[bestscan[iscan]],scancalstart_hrs[bestscan[iscan]]],[0,-self.radialscan_extent/2.0*180.0/np.pi,-self.radialscan_extent/2.0*180.0/np.pi,0,0],color=[0.5,0.5,0.5,0.5])
            for flagrange in flagtime:
                plt.fill([flagrange[0],flagrange[1],flagrange[1],flagrange[0]],[-self.radialscan_extent/2.0*180.0/np.pi,-self.radialscan_extent/2.0*180.0/np.pi,self.radialscan_extent/2.0*180.0/np.pi,self.radialscan_extent/2.0*180.0/np.pi],color=[0.5,0.,0.,0.5])
            plt.ylabel('Target plane coordinates [degrees]')
            plt.xlabel('Hours since '+time.ctime(self.rawtime[0]))
            plt.title(self.filename+' found %d scans, %d scans per cycle'%(len(scanstop_hrs),nscanspercycle))
        return flagtime
        
    def findcyclescans(self,doplot=None,hrs=False):
        #finds the individual cycle scans start and stop positions
        #doplot could be 'az' or 'el'
        r=np.sqrt(self.ll**2+self.mm**2)
        onradial=np.array((r>(0.5*self.radialscan_extent/2.0))*(r<(0.75*self.radialscan_extent/2.0)),dtype=np.int32)
        donradial=np.diff(onradial)
        radialedges=np.nonzero(donradial[self.flagfirstslew_index:]==1)[0]
        radialstarts=radialedges[::2]+self.flagfirstslew_index
        radialends=radialedges[1::2]+self.flagfirstslew_index
        radialangles=np.array([np.angle(np.mean(self.ll[radialstarts[i]:radialends[i]])+np.mean(self.mm[radialstarts[i]:radialends[i]])*1j) for i in range(len(radialends))])
        unwrapradialangles=np.unwrap(radialangles)
        dangle=np.median(np.diff(np.unwrap(radialangles)))
        nscanspercycle=2*int(np.round(np.pi/dangle))
        ontarget=(r<self.radialscan_sampling)
        scanindex=[]
        scanangle=[]
        scancalstart=[]
        scanstart=[]
        scanstop=[]
        scancalstop=[]
        for iangle in range(len(radialends)):
            idx=np.nonzero(ontarget*(np.arange(len(r))<radialstarts[iangle]))
            if (len(idx[0])==0):
                break
            iontarget=np.max(idx[0])
            scanstart.append(iontarget)            
            while ((ontarget[iontarget] or np.sum(ontarget[iontarget:scanstart[-1]])<3) and iontarget>0):
                iontarget-=1
            scancalstart.append(iontarget)
            idx=np.nonzero(ontarget*(np.arange(len(r))>radialends[iangle]))
            if (len(idx[0])==0):
                scancalstart.pop()
                break
            iontarget=np.min(idx[0])
            scanstop.append(iontarget)
            while ((ontarget[iontarget] or np.sum(ontarget[scanstop[-1]:iontarget])<3) and iontarget<len(r)-1):
                iontarget+=1
            scancalstop.append(iontarget)
            scanangle.append(radialangles[iangle])
        scancalstart_hrs=[(self.rawtime[it]-self.rawtime[0])/60./60. for it in scancalstart]
        scanstart_hrs=[(self.rawtime[it]-self.rawtime[0])/60./60. for it in scanstart]
        scanstop_hrs=[(self.rawtime[it]-self.rawtime[0])/60./60. for it in scanstop]
        scancalstop_hrs=[(self.rawtime[it]-self.rawtime[0])/60./60. for it in scancalstop]
        if (doplot):
            plt.figure()
            if (doplot=='az' or doplot=='ll'):
                plt.plot((self.rawtime-self.rawtime[0])/60./60.,self.ll*180.0/np.pi)
            else:
                plt.plot((self.rawtime-self.rawtime[0])/60./60.,self.mm*180.0/np.pi)
            for iscan in range(len(scanstop_hrs)):
                if (iscan%2):
                    plt.fill([scancalstart_hrs[iscan],scanstart_hrs[iscan],scanstop_hrs[iscan],scancalstop_hrs[iscan],scancalstart_hrs[iscan]],[0,self.radialscan_extent/2.0*180.0/np.pi,self.radialscan_extent/2.0*180.0/np.pi,0,0],color=[0.5,0.5,0.5,0.5])
                else:
                    plt.fill([scancalstart_hrs[iscan],scanstart_hrs[iscan],scanstop_hrs[iscan],scancalstop_hrs[iscan],scancalstart_hrs[iscan]],[0,-self.radialscan_extent/2.0*180.0/np.pi,-self.radialscan_extent/2.0*180.0/np.pi,0,0],color=[0.5,0.5,0.5,0.5])                
            plt.ylabel('Target plane coordinates [degrees]')
            plt.xlabel('Hours since '+time.ctime(self.rawtime[0]))
            plt.title(self.filename+' found %d scans, %d scans per cycle'%(len(scanstop_hrs),nscanspercycle))
        if (hrs):
            return scancalstart_hrs,scanstart_hrs,scanstop_hrs,scancalstop_hrs,nscanspercycle
        else:
            return scancalstart,scanstart,scanstop,scancalstop,nscanspercycle
            
        
    def findcycles(self,cycleoffset=0,onradial=[0.5,0.75],doplot=None):
        #doplot could be 'az' or 'el'
        #note if this crashes, use a higher cycleoffset
        r=np.sqrt(self.ll**2+self.mm**2)
        #onradial=(r>(0.5*self.radialscan_extent/2.0))*(r<(0.75*self.radialscan_extent/2.0))
        onradial=(r>(onradial[0]*self.radialscan_extent/2.0))*(r<(onradial[1]*self.radialscan_extent/2.0))
        donradial=np.diff(onradial)
        radialedges=np.nonzero(donradial[self.flagfirstslew_index:]==1)[0]
        radialstarts=radialedges[::2]+self.flagfirstslew_index
        radialends=radialedges[1::2]+self.flagfirstslew_index
        radialangles=np.array([np.angle(np.mean(self.ll[radialstarts[i]:radialends[i]])+np.mean(self.mm[radialstarts[i]:radialends[i]])*1j) for i in range(len(radialends))])
        unwrapradialangles=np.unwrap(radialangles)
        dangle=np.median(np.diff(np.unwrap(radialangles)))

        ianglestart=[cycleoffset]
        iangleend=[]
        while True:
            nextianglecycle=np.nonzero(np.abs((unwrapradialangles-unwrapradialangles[ianglestart[-1]]-2.0*np.pi))<dangle/2.0)[0]
            lastiangle=np.nonzero(np.abs((unwrapradialangles-unwrapradialangles[ianglestart[-1]]-2.0*np.pi+dangle))<dangle/2.0)[0]
            if len(lastiangle)==1:
                iangleend.append(lastiangle[0])
            else:
                print('Cycle %d is an incomplete cycle. Unexpected len(lastiangle)=%d'%(len(iangleend),len(lastiangle)))
            if len(nextianglecycle)==1:
                ianglestart.append(nextianglecycle[0])
            else:
                break
        #note len(iangleend) may be less than len(ianglestart) if incomplete cycles
        ianglestart=ianglestart[:len(iangleend)]
        #now get ontarget indices before start and after end for each cycle
        ontarget=(r<self.radialscan_sampling)
        cyclestart=[]
        cyclestop=[]
        for icycle in range(len(iangleend)):
            idx=np.nonzero(ontarget*(np.arange(len(r))<radialstarts[ianglestart[icycle]]))
            iontarget=np.max(idx[0])
            while (ontarget[iontarget] and iontarget>0):
                iontarget-=1
            cyclestart.append(iontarget)
            idx=np.nonzero(ontarget*(np.arange(len(r))>radialends[iangleend[icycle]]))
            iontarget=np.min(idx[0])
            while (ontarget[iontarget] and iontarget<len(r)-1):
                iontarget+=1
            cyclestop.append(iontarget)
        
        if (len(iangleend)>0):
            nscanspercycle=int(np.median(np.array(iangleend)-np.array(ianglestart))+1)//2
        else:
            nscanspercycle=0
            print('Error: no complete cycles found. Try flagging data using Dataset.flagplot()')
        cyclestart_hrs=[(self.rawtime[it]-self.rawtime[0])/60./60. for it in cyclestart]
        cyclestop_hrs=[(self.rawtime[it]-self.rawtime[0])/60./60. for it in cyclestop]
        if (doplot):
            plt.figure()
            if (doplot=='az' or doplot=='ll'):
                plt.plot((self.rawtime-self.rawtime[0])/60./60.,self.ll*180.0/np.pi)
            else:
                plt.plot((self.rawtime-self.rawtime[0])/60./60.,self.mm*180.0/np.pi)
            for icycle in range(len(cyclestop_hrs)):
                if (icycle%2):
                    plt.fill([cyclestart_hrs[icycle],cyclestop_hrs[icycle],cyclestop_hrs[icycle],cyclestart_hrs[icycle]],[0,0,self.radialscan_extent*180.0/np.pi,self.radialscan_extent*180.0/np.pi],color=[0.5,0.5,0.5,0.5])
                else:
                    plt.fill([cyclestart_hrs[icycle],cyclestop_hrs[icycle],cyclestop_hrs[icycle],cyclestart_hrs[icycle]],[-self.radialscan_extent*180.0/np.pi,-self.radialscan_extent*180.0/np.pi,0,0,],color=[0.5,0.5,0.5,0.5])
            plt.ylabel('Target plane coordinates [degrees]')
            plt.xlabel('Hours since '+time.ctime(self.rawtime[0]))
            plt.title(self.filename+' found %d cycles, %d scans per cycle'%(len(cyclestart_hrs),nscanspercycle))
            
        return cyclestart_hrs,cyclestop_hrs,nscanspercycle
        
    def flagdata(self,lookdirectory=None,minfreqMHz=0,maxfreqMHz=1e300,ignoreantennas=[],clipextent=None,timestart_hrs=0,timeduration_hrs=1e300,minelevation_deg=0,maxelevation_deg=1e10,targetname=None,flagfirstslew=True,flags_hrs=[],flagslew=False,cycle=None,group=None):
        self.h5.select(reset='TBF')
        if (cycle is not None and group is not None):
            if not isinstance(cycle,(list,np.ndarray)):#i.e. should be int
                cycle=[cycle]
            if not isinstance(group,(list,np.ndarray)):#i.e. should be int
                group=[group]
            self.h5.select()#clears selection
            compscans=[]
            for icycle in cycle:
                for igroup in group:
                    compscans+=['%d.%d.%d'%(icycle,igroup,iscan) for iscan in range(self.h5.obs_params['num_scans'])]
            self.h5.select(compscans=compscans)
            radec_target_indices=[ind for ind in self.h5.target_indices if self.h5.catalogue.targets[ind].name!='azimuthunwrap']
            if len(radec_target_indices)!=1:#ideally there should be only one target, but some files have azel target due to mislabeling bug at end of a cycle when busy slewing due to prepopulate time
                raise Exception('Expect one radec target within cycle only')
            target=self.h5.catalogue.targets[radec_target_indices[0]]#should be only one target selected
            self.h5.select(compscans=compscans,targets=[target.name])#this re-selection overcomes mislabeling in some datasets such as 1562708834_sdp_l0.full.rdb icycle=2,igroup=0 
            groupmask=np.ones(len(self.rawtime),dtype=bool)
            groupmask[self.h5.dumps]=0
            self.h5.select(reset='TBF')
        else:
            groupmask=np.zeros(len(self.rawtime),dtype=bool)

        self.database={}
        self.channel_range=range(self.h5.shape[1]);
        self.freqflags=[]
        self.flags=[]
        self.scanantennas=[]
        self.trackantennas=[];
        if (lookdirectory==None):
            lookdirectory=self.dirname+self.subdirectory
        for iant in range(len(self.radialscan_allantenna)):
            if (self.radialscan_allantenna[iant] in ignoreantennas):
                continue
            if (self.radialscan_allantenna[iant] in self.radialscan_scanantenna):
                self.scanantennas.append(iant)
            else:
                self.trackantennas.append(iant)
        self.scanantennas=np.array(self.scanantennas,dtype='int')
        self.trackantennas=np.array(self.trackantennas,dtype='int')
        #read flag information if present
        while(len(lookdirectory) and not os.path.exists(lookdirectory+'flags')):
            lookdirectory=lookdirectory[:(lookdirectory[:-1].rfind('/'))+1]
        if (os.path.exists(lookdirectory+'flags')):
            print('Loading flags from '+lookdirectory)
            output=open(lookdirectory+'flags', 'rb')
            self.flags=pickle.load(output)
            self.freqflags=pickle.load(output)
            output.close();
        targetmask=np.zeros(len(self.rawtime),dtype=bool)
        if (targetname!=None):
            namelist=[tar.name for tar in self.h5.catalogue.targets]
            if (targetname in namelist):
                ind=namelist.index(targetname)
                targetmask=(self.h5.sensor['Observation/target_index']==ind)

        for flags in flags_hrs:
            self.flags.append(flags)
        #determines frequency flagging indices
        for c in range(self.h5.shape[1]):
            for flagrange in self.freqflags:
                if ((c>=flagrange[0] and c <=flagrange[1]) or self.h5.channel_freqs[c]/1E6<minfreqMHz or self.h5.channel_freqs[c]/1E6>maxfreqMHz):
                    try:
                        self.channel_range.remove(c)
                    except:
                        pass
        #determine time flagging indices
        _time=(np.array(self.rawtime))/60.0/60.0;
        _time=_time-_time[0]
        
        if (clipextent==None):
            clipextent=180.0
        self.flagmask=np.array(groupmask|targetmask|(self.h5.el[:,np.r_[self.scanantennas,self.trackantennas][0]]<minelevation_deg)|(self.h5.el[:,np.r_[self.scanantennas,self.trackantennas][0]]>maxelevation_deg)|((self.ll**2+self.mm**2)>(clipextent/2.0*np.pi/180.0)**2),dtype='int');
        if (flagslew):
            slewing=(self.h5.sensor['Observation/scan_state']=='slew')
            self.flagmask|=slewing
            print('Flagged %d timestamps due to slew'%(np.sum(slewing)))

        #attempt to eliminate initial slew duration
        if (flagfirstslew):
            r_deg=np.sqrt(np.sum(self.h5.target_x**2,axis=1)+np.sum(self.h5.target_y**2,axis=1))*180.0/np.pi
            r_ind=np.nonzero(r_deg<0.1)[0]
            if (len(r_ind)>1):
                r_it=r_ind[0]
                while(r_deg[r_it+1]<r_deg[r_it]):
                    r_it+=1
                self.flags.append([_time[0],_time[r_it]])
                self.flagfirstslew_index=r_it
                # self.flagmask|=np.array(_time<=_time[r_it],dtype='int')

        for flagrange in self.flags:
            self.flagmask|=np.array(np.array(_time>=flagrange[0]) & np.array(_time<=flagrange[1]),dtype='int')
        self.flagmask|=np.array(np.array(_time<timestart_hrs) | np.array(_time>timestart_hrs+timeduration_hrs),dtype='int')
        self.time_range=np.nonzero(self.flagmask==0)[0]
        self.radialscan_centerfreq=self.h5.channel_freqs[self.channel_range]
        self.radialscan_channels=self.h5.channels[self.channel_range]
        tmpsampling,self.radialscan_extent=self.findsampling(self.ll,self.mm,self.flagmask)
        if (self.radialscan_sampling==None):
            self.radialscan_sampling=tmpsampling
        ##determine environmental summary
        times=[0.5*(self.h5.timestamps[self.time_range][0]+self.h5.timestamps[self.time_range][-1]),self.h5.timestamps[self.time_range][0],self.h5.timestamps[self.time_range][-1]]
        self.env_times=times
        self.env_time=[time.asctime(time.localtime(times[0])),time.asctime(time.localtime(times[1])),time.asctime(time.localtime(times[2]))]
        self.env_el=np.array([np.mean(self.scanel[self.time_range]),np.min(self.scanel[self.time_range]),np.max(self.scanel[self.time_range])])/D2R
        self.env_az=np.array([self.targetaz[self.time_range[len(self.time_range)//2]],np.min(self.targetaz[self.time_range]),np.max(self.targetaz[self.time_range])])/D2R
        sun=[self.target.separation(katpoint.Target("Sun, special"),katpoint.Timestamp(tm)) for tm in [times[0],times[1],times[2]]]
        try:
            self.env_wind=np.array([np.mean(self.h5.wind_speed[self.time_range]),np.min(self.h5.wind_speed[self.time_range]),np.max(self.h5.wind_speed[self.time_range])])
        except:
            self.env_wind=np.tile(np.nan,len(self.time_range))
            print('Error: no wind speed measurements')
            pass
        try:
            self.env_wind_dir=np.array([180.0/np.pi*np.arctan2(np.mean(np.sin(self.h5.wind_direction[self.time_range]*np.pi/180.0)),np.mean(np.cos(self.h5.wind_direction[self.time_range]*np.pi/180.0))),np.min(self.h5.wind_direction[self.time_range]),np.max(self.h5.wind_direction[self.time_range])])
        except:
            self.env_wind_dir=np.tile(np.nan,len(self.time_range))
            print('Error: no wind direction measurements')
            pass
        try:
            self.env_humidity=np.array([np.mean(self.h5.humidity[self.time_range]),np.min(self.h5.humidity[self.time_range]),np.max(self.h5.humidity[self.time_range])])
        except:
            self.env_humidity=np.tile(np.nan,len(self.time_range))
            print('Error: no wind speed measurements')
            pass
        try:
            self.env_pressure=np.array([np.mean(self.h5.pressure[self.time_range]),np.min(self.h5.pressure[self.time_range]),np.max(self.h5.pressure[self.time_range])])
        except:
            self.env_pressure=np.tile(np.nan,len(self.time_range))
            print('Error: no wind speed measurements')
            pass
        try:
            self.env_temp=np.array([np.mean(self.h5.temperature[self.time_range]),np.min(self.h5.temperature[self.time_range]),np.max(self.h5.temperature[self.time_range])])
        except:
            self.env_temp=np.tile(np.nan,len(self.time_range))
            print('Error: no temperature measurements')
            pass
        self.env_sun=np.array([sun[0],np.min(sun),np.max(sun)])/D2R
                    
    def getchannelindices(self,frequencyMHz,dMHz,minchannels=1,printout=True):
        freqMHz=self.radialscan_centerfreq/1E6
        chan_indices=np.nonzero((freqMHz>frequencyMHz-dMHz/2.0) * (freqMHz<=frequencyMHz+dMHz/2.0))[0]
        nch=len(chan_indices)
        if (nch<minchannels):
            print('warning: no channels near %dMHz, using overlapping neighbouring data'%(frequencyMHz))
            for factor in np.arange(1,20,0.1):
                chan_indices=np.nonzero((freqMHz>frequencyMHz-dMHz/2.0*factor) * (freqMHz<=frequencyMHz+dMHz/2.0*factor))[0]
                nch=len(chan_indices)
                if (nch>=minchannels):
                    print('resolved using %d channels, %.1fMHz bandwidth instead of %.1fMHz, (%.1f-%.1f)'%(nch,dMHz*factor,dMHz,freqMHz[chan_indices[-1]],freqMHz[chan_indices[0]]))
                    break;
        else:
            factor=1
        if (nch<minchannels):
            print('unable to recover')
            exit()
        elif printout:
            print('Number of channels %d at %fMHz within %fMHz bandwidth (%fMHz)'%(nch,frequencyMHz,dMHz*factor,dMHz))
        return chan_indices
    
    # a possible robust improvement could be to look at max radius in a number of directions/sections, and choose the median, to avoid stows or when starting off target.
    def findsampling(self,targetx,targety,flagmask):
        rad2=targetx**2+targety**2
        notflagged=np.nonzero((1-flagmask))[0]
        extent=2.0*min([np.max(targetx[notflagged]),np.max(-targetx[notflagged]),np.max(targety[notflagged]),np.max(-targety[notflagged])])#somewhat more robust, to avoid e.g. stows
        maxrad2low=((extent/2.0)*0.3)**2
        maxrad2high=((extent/2.0)*0.7)**2
        inrange=np.nonzero((rad2[:-1]<maxrad2high)&(rad2[:-1]>maxrad2low)&(1-flagmask[:-1]))[0]
        interdist=np.sqrt((targetx[:-1]-targetx[1:])**2+(targety[:-1]-targety[1:])**2)[inrange]#note this extraction must be done after diff calculation
        sampling=np.mean(interdist)/2#NOTE because it is calculated as a diameter quantity but used as a radius quantity
        print('Find sampling %f[deg], extent %f[deg]'%(sampling*180.0/np.pi,extent*180.0/np.pi))
        return sampling,extent
        
    #interval from (including) to (excluding)
    def average(self,signal,intervalfrom,intervalto):
        shp=list(np.shape(signal))
        shp[0]=len(intervalfrom)
        newsignal=np.zeros(shp,dtype=signal.dtype)
        for ii,i0 in enumerate(intervalfrom):
            newsignal[ii]=np.mean(signal[i0:intervalto[ii]],axis=0)
        return newsignal
    
    #Note the following is in error in that the gains should be computed independently per antenna pair instead of combination
    #so its ok if evaluated when there is only one tracking antenna in dataset... must relook at this for that reason.
    
    #Note that pointing offset is related to where the bulk dish is pointing, and might not correspond to peak gain direction
    # which is an electromagnetic feature, possibly due to feed mounting. The bulk dish has 12m diameter which corresponds 
    # to 1sq degree mainlobe area. So it is 1sq degree (at 50% power) this which is fitted for to determine pointing offset.
    
    #gain normalisation (in intervals, with linear interpolation) for the purpose of simply finding the pointing offsets 
    # and Gx,Gy power gains can be done by fitting a gaussian of unity amplitude, with unknown offsets and widths to eg Gx 
    # while simultaneusly solving for a few the gain intervals. The phase components can be determined by minimizing the power
    # contribution of the resulting Dx component and setting the phase of the Gx component at pointing center to zero.
    
    #direct holography calculation, full jones matrix
    #measures pointing offsets by fitting gaussian to |Gx|,|Gy| beams, while also determining/compensating for gain drifts
    def processoffaxisindependentwithgaindrift(self,h5,targetx,targety,channel_range,flagmask,trackantennas,scanantenna, channel_start, channel_width, frequencyMHz, gainintervaltime=30*60, cycletime=None):
        if (len(trackantennas)==0):
            target=h5.catalogue.targets[h5.target_indices[0]]#use target rather than tracking antenna, incase there are no tracking antennas

        sigma2fwhm=2.0 * np.sqrt(2.0 * np.log(2.0))#multiply sigma of gaussian by this to get fwhm
        #beam_R1=1.3 * 1.25*(wavelength/h5.ants[scanantenna].diameter*180/np.pi) # Approximately first null of parabolic taper's pattern
        beam_R1=2.0 #note frequency/wavelength not yet known at this point#LAMBDA/DIAMETER*R2D=(0.21/12)*(180/pi)=1.0026761414789405
        beamregion=np.array((np.sqrt(targetx**2+targety**2)*180.0/np.pi)<beam_R1,dtype='bool')#only use data within first null
        h5.select(reset='F',channels=channel_range)
        h5.select(reset='T')
        h5.select(dumps=np.logical_and(beamregion,np.array((1-flagmask),dtype='bool')));

        wavelength=self.speedoflight/(frequencyMHz*1e6)
        beamradius=0.8*(wavelength/h5.ants[scanantenna].diameter*180/np.pi)#approximate beam radius in degrees out to half power point 1.22/2=0.61, but we use bit bigger area 0.8
        sigma0=1.22*(wavelength/h5.ants[scanantenna].diameter*180/np.pi)/sigma2fwhm*np.pi/180.0

         # prepare to write main dict
        corrprod_to_index = dict([(tuple(cp), ind) for cp, ind in zip(np.r_[h5.corr_products,h5.corr_products[::,::-1]], np.r_[range(len(h5.corr_products)),range(len(h5.corr_products))])])
        theindices=h5._time_keep.nonzero()[0]

        offaxistime=h5.timestamps[:]
        storetargetx=targetx[theindices]
        storetargety=targety[theindices]            
        
        ngainintervals=int(np.ceil((offaxistime[-1]-offaxistime[0])/(gainintervaltime)))#linearly interpolates gain, in time.
        if (ngainintervals<2):
            ngainintervals=2
        #direct calculation from visibilities
        #in order REAL yyt0,yxt0,xyt0,xxt0,yyt1,yxt1,xyt1,xxt1,... , IMAG yyt0,yxt0,xyt0,xxt0,yyt1,yxt1,xyt1,xxt1,.....
        ntime=len(theindices)
        beamoffsets=[]
        print('Independent DIRECT calculation')
        print('using %d time samples and %d channels'%(ntime,channel_width))
        for itrack in trackantennas:#only extract baselines between tracking antennas and scanning antenna
            t1=time.time()
            if (itrack>scanantenna):
                iant=scanantenna;
                jant=itrack;
                doconj=0
            else:
                iant=itrack;
                jant=scanantenna;
                doconj=1
            polprods = [("%s%s" % (self.radialscan_allantenna[iant],p[0].lower()), "%s%s" % (self.radialscan_allantenna[jant],p[1].lower())) for p in self.pols_to_use]
            sys.stdout.write(self.radialscan_allantenna[scanantenna]+': '+self.radialscan_allantenna[iant]+'-'+self.radialscan_allantenna[jant]);sys.stdout.flush();
            cpindices=[corrprod_to_index.get(p) for p in polprods]
            
            if (cycletime is not None):
                ncycles=int(np.floor((offaxistime[-1]-offaxistime[0])/cycletime))
                cycleperiod=cycletime
            else:
                ncycles=1
                cycleperiod=offaxistime[-1]-offaxistime[0]+1
            timestart=offaxistime[0]
            timebeamoffsets=[]
            for icycle in range(ncycles):
                if (self.options.maxbaseline!=None):
                    blrad=(h5.u[:, cpindices[0]]**2+h5.v[:, cpindices[0]]**2)**0.5#uses the last cp_index
                    bltimerange=np.nonzero((offaxistime>=timestart)*(offaxistime<timestart+cycleperiod)*(blrad<self.options.maxbaseline)*(blrad>self.options.minbaseline))[0]#flags long baselines for resolved sources and short baselines for antenna shadowing
                else:
                    bltimerange=np.nonzero((offaxistime>=timestart)*(offaxistime<timestart+cycleperiod))[0]
                timestart+=cycleperiod
                blntime=len(bltimerange)
                if (blntime==0):
                    print(' ntime: 0')
                    continue

                changrange=np.arange(channel_start,channel_start+channel_width)
                if (0):
                    xx=np.reshape(h5.vis[bltimerange,changrange,cpindices[0]],[blntime,channel_width])
                    xy=np.reshape(h5.vis[bltimerange,changrange,cpindices[1]],[blntime,channel_width])
                    yx=np.reshape(h5.vis[bltimerange,changrange,cpindices[2]],[blntime,channel_width])
                    yy=np.reshape(h5.vis[bltimerange,changrange,cpindices[3]],[blntime,channel_width])
                    
                    visdataxx=np.mean(np.abs(xx+self.dxy*xy+self.dyx*yx+self.dxy*self.dy*yy),axis=1).reshape(-1)
                    visdatayy=np.mean(np.abs(xx),axis=1).reshape(-1)
                else:
                    if (h5.vis.shape[0]==blntime):#fancy indexing not supported in dask
                        # debug
                        visdataxx=np.mean(np.abs(np.reshape(h5.vis[:,changrange,cpindices[0]],[blntime,channel_width])),axis=1).reshape(-1)
                        visdatayy=np.mean(np.abs(np.reshape(h5.vis[:,changrange,cpindices[3]],[blntime,channel_width])),axis=1).reshape(-1)
                    else:
                        visdataxx=np.mean(np.abs(np.reshape(h5.vis[bltimerange,changrange,cpindices[0]],[blntime,channel_width])),axis=1).reshape(-1)
                        visdatayy=np.mean(np.abs(np.reshape(h5.vis[bltimerange,changrange,cpindices[3]],[blntime,channel_width])),axis=1).reshape(-1)

                # visdataxx=np.sqrt(visdataxx**2+np.mean(np.abs(np.reshape(h5.vis[bltimerange,changrange,cpindices[2]],[blntime,channel_width])),axis=1).reshape(-1)**2)
                # visdatayy=np.sqrt(visdatayy**2+np.mean(np.abs(np.reshape(h5.vis[bltimerange,changrange,cpindices[1]],[blntime,channel_width])),axis=1).reshape(-1)**2)
                
                t2=time.time()
                sys.stdout.write(' ntime: %d load: %.1f'%(blntime,t2-t1));sys.stdout.flush();

                validpts=bltimerange
                absGx=visdataxx**2
                absGy=visdatayy**2
                absI=(absGx+absGy)
                maxabsGx=np.max(absGx)
                maxabsGy=np.max(absGy)
                maxabsI=np.max(absI)
                if (1):#this works good
                    fitptsI=np.nonzero(np.array((np.sqrt(storetargetx[validpts]**2+storetargety[validpts]**2)*180.0/np.pi)<beamradius,dtype='bool'))[0]
                    fitptsGx=fitptsI
                    fitptsGy=fitptsI
                else:#this is misleading if significant changes in gain through course of observation
                    fitptsGx=np.nonzero(absGx>0.5*maxabsGx)[0]
                    fitptsGy=np.nonzero(absGy>0.5*maxabsGy)[0]
                    fitptsI=np.nonzero(absI>0.5*maxabsI)[0]

                initialparams=np.r_[[0,0,sigma0,sigma0],maxabsI*np.ones(ngainintervals)]
                fitterGx=NonLinearLeastSquaresFit(gaussdrift,initialparams)
                fitterGx.fit([storetargetx[validpts][fitptsGx],storetargety[validpts][fitptsGx],offaxistime[validpts][fitptsGx]],absGx[fitptsGx])
                #print('x params',fitterGx.params)

                initialparams=np.r_[[0,0,sigma0,sigma0],maxabsI*np.ones(ngainintervals)]
                fitterGy=NonLinearLeastSquaresFit(gaussdrift,initialparams)
                fitterGy.fit([storetargetx[validpts][fitptsGy],storetargety[validpts][fitptsGy],offaxistime[validpts][fitptsGy]],absGy[fitptsGy])
                #print('y params',fitterGy.params)

                initialparams=np.r_[[0,0,sigma0,sigma0],maxabsI*np.ones(ngainintervals)]
                fitterI=NonLinearLeastSquaresFit(gaussdrift,initialparams)
                fitterI.fit([storetargetx[validpts][fitptsI],storetargety[validpts][fitptsI],offaxistime[validpts][fitptsI]],absI[fitptsI])
                #print('i params',fitterI.params)
        
                #meanx,meany,widthx,widthy,gains...
                timebeamoffsets.append([fitterI.params[:2],fitterGx.params[:2],fitterGy.params[:2],fitterI.params[2:4]*sigma2fwhm,fitterGx.params[2:4]*sigma2fwhm,fitterGy.params[2:4]*sigma2fwhm])
            
            beamoffsets.extend(timebeamoffsets)
            t3=time.time()
            print(' process: %.1f'%(t3-t2))
        
        print('Fitting done')
        return beamoffsets
        #return vis, storeparang[validpts], storeparangscan[validpts], storetargetx[validpts], storetargety[validpts]

    def processoffaxisauto(self,h5,targetx,targety,channel_range,flagmask,trackantennas,scanantenna, channel_start, channel_width, ich, frequencyMHz, dMHz, method='raw',gainintervaltime=30*60):
        if (len(trackantennas)==0):
            target=h5.catalogue.targets[h5.target_indices[0]]#use target rather than tracking antenna, incase there are no tracking antennas

        h5.select(reset='F',channels=channel_range)
        h5.select(reset='T')
        h5.select(dumps=np.array((1-flagmask),dtype='bool'));            

         # prepare to write main dict
        corrprod_to_index = dict([(tuple(cp), ind) for cp, ind in zip(np.r_[h5.corr_products,h5.corr_products[::,::-1]], np.r_[range(len(h5.corr_products)),range(len(h5.corr_products))])])
        theindices=h5._time_keep.nonzero()[0]

        if (len(trackantennas)==0):
            storeparang=target.parallactic_angle(h5.timestamps[:])
        else:
            storeparang=h5.parangle[:,trackantennas[0]]*np.pi/180.0
    #    storeparangscan=h5.parangle[:,scanantennas[0]]*np.pi/180.0#original
        storeparangscan=storeparang#-parcorangle[theindices]#normal

        offaxistime=h5.timestamps[:]
        storetargetx=targetx[theindices]
        storetargety=targety[theindices]

        ngainintervals=np.ceil((offaxistime[-1]-offaxistime[0])/(gainintervaltime))#linearly interpolates gain, in time.
        if (ngainintervals<2):
            ngainintervals=2
        #direct calculation from visibilities
        #in order REAL yyt0,yxt0,xyt0,xxt0,yyt1,yxt1,xyt1,xxt1,... , IMAG yyt0,yxt0,xyt0,xxt0,yyt1,yxt1,xyt1,xxt1,.....
        ntime=len(theindices)
        aGx=np.zeros(ntime,dtype='complex');aGy=np.zeros(ntime,dtype='complex');aDx=np.zeros(ntime,dtype='complex');aDy=np.zeros(ntime,dtype='complex');acount=np.zeros(ntime,dtype='float');
        print('RAW calculation')
        print('using %d time samples and %d channels'%(ntime,channel_width))
        t1=time.time()
        iant=scanantenna;
        jant=scanantenna;
        doconj=0
        polprods = [("%s%s" % (self.radialscan_allantenna[iant],p[0].lower()), "%s%s" % (self.radialscan_allantenna[jant],p[1].lower())) for p in self.pols_to_use]
        sys.stdout.write(self.radialscan_allantenna[scanantenna]+': '+self.radialscan_allantenna[iant]+'-'+self.radialscan_allantenna[jant]);sys.stdout.flush();
        cpindices=[corrprod_to_index.get(p) for p in polprods]
        if (self.options.maxbaseline!=None):
            blrad=(h5.u[:, cpindices[0]]**2+h5.v[:, cpindices[0]]**2)**0.5#uses the last cp_index
            bltimerange=np.nonzero((blrad<self.options.maxbaseline)*(blrad>self.options.minbaseline))[0]#flags long baselines for resolved sources and short baselines for antenna shadowing
        else:
            bltimerange=np.arange(ntime)
        blntime=len(bltimerange)

        changrange=np.arange(channel_start,channel_start+channel_width)
        swaptrackxy=False
        visdataxx=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[0]],[blntime,channel_width])),axis=1).reshape(-1)
        visdataxy=-np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[1]],[blntime,channel_width])),axis=1).reshape(-1)
        visdatayx=-np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[2]],[blntime,channel_width])),axis=1).reshape(-1)
        visdatayy=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[3]],[blntime,channel_width])),axis=1).reshape(-1)
        # visdataxx=np.mean(np.conj(np.abs(np.reshape(h5.vis[bltimerange,changrange,cpindices[0]],[blntime,channel_width]))),axis=1).reshape(-1)
        # visdataxy=-np.mean(np.conj(np.abs(np.reshape(h5.vis[bltimerange,changrange,cpindices[1]],[blntime,channel_width]))),axis=1).reshape(-1)
        # visdatayx=-np.mean(np.conj(np.abs(np.reshape(h5.vis[bltimerange,changrange,cpindices[2]],[blntime,channel_width]))),axis=1).reshape(-1)
        # visdatayy=np.mean(np.conj(np.abs(np.reshape(h5.vis[bltimerange,changrange,cpindices[3]],[blntime,channel_width]))),axis=1).reshape(-1)
        t2=time.time()
        sys.stdout.write(' ntime: %d load: %.1f'%(blntime,t2-t1));sys.stdout.flush();
        if (doconj):#apply conjugate transpose
            visdataxx=np.conj(visdataxx)
            tmp=np.conj(visdatayx)
            visdatayx=np.conj(visdataxy)
            visdataxy=tmp
            visdatayy=np.conj(visdatayy)
                        
                        
        aGx[bltimerange]+=visdataxx
        aDx[bltimerange]+=visdataxy
        aDy[bltimerange]+=visdatayx
        aGy[bltimerange]+=visdatayy
        acount[bltimerange]+=1

        validpts=np.nonzero(acount)[0]   
        aGx=aGx[validpts]/acount[validpts]
        aDx=aDx[validpts]/acount[validpts]
        aDy=aDy[validpts]/acount[validpts]
        aGy=aGy[validpts]/acount[validpts]
                
        vis=[aGx,aGy,aDx,aDy]
        return vis, storeparang[validpts], storeparangscan[validpts], storetargetx[validpts], storetargety[validpts]

#just averages raw
    def processoffaxisraw(self,h5,targetx,targety,channel_range,flagmask,trackantennas,scanantenna, channel_start, channel_width, ich, frequencyMHz, dMHz, method='raw',gainintervaltime=30*60):
        if (len(trackantennas)==0):
            target=h5.catalogue.targets[h5.target_indices[0]]#use target rather than tracking antenna, incase there are no tracking antennas

        h5.select(reset='F',channels=channel_range)
        h5.select(reset='T')
        h5.select(dumps=np.array((1-flagmask),dtype='bool'));            

         # prepare to write main dict
        corrprod_to_index = dict([(tuple(cp), ind) for cp, ind in zip(np.r_[h5.corr_products,h5.corr_products[::,::-1]], np.r_[range(len(h5.corr_products)),range(len(h5.corr_products))])])
        theindices=h5._time_keep.nonzero()[0]

        if (len(trackantennas)==0):
            storeparang=target.parallactic_angle(h5.timestamps[:])
        else:
            storeparang=h5.parangle[:,trackantennas[0]]*np.pi/180.0
    #    storeparangscan=h5.parangle[:,scanantennas[0]]*np.pi/180.0#original
        storeparangscan=storeparang#-parcorangle[theindices]#normal

        offaxistime=h5.timestamps[:]
        storetargetx=targetx[theindices]
        storetargety=targety[theindices]

        ngainintervals=np.ceil((offaxistime[-1]-offaxistime[0])/(gainintervaltime))#linearly interpolates gain, in time.
        if (ngainintervals<2):
            ngainintervals=2
        #direct calculation from visibilities
        #in order REAL yyt0,yxt0,xyt0,xxt0,yyt1,yxt1,xyt1,xxt1,... , IMAG yyt0,yxt0,xyt0,xxt0,yyt1,yxt1,xyt1,xxt1,.....
        ntime=len(theindices)
        aGx=np.zeros(ntime,dtype='complex');aGy=np.zeros(ntime,dtype='complex');aDx=np.zeros(ntime,dtype='complex');aDy=np.zeros(ntime,dtype='complex');acount=np.zeros(ntime,dtype='float');
        print('RAW calculation')
        print('using %d time samples and %d channels'%(ntime,channel_width))
        for itrack in trackantennas:#only extract baselines between tracking antennas and scanning antenna
            t1=time.time()
            if (itrack>scanantenna):
                iant=scanantenna;
                jant=itrack;
                doconj=0
            else:
                iant=itrack;
                jant=scanantenna;
                doconj=1
            polprods = [("%s%s" % (self.radialscan_allantenna[iant],p[0].lower()), "%s%s" % (self.radialscan_allantenna[jant],p[1].lower())) for p in self.pols_to_use]
            sys.stdout.write(self.radialscan_allantenna[scanantenna]+': '+self.radialscan_allantenna[iant]+'-'+self.radialscan_allantenna[jant]);sys.stdout.flush();
            cpindices=[corrprod_to_index.get(p) for p in polprods]
            if (self.options.maxbaseline!=None):
                blrad=(h5.u[:, cpindices[0]]**2+h5.v[:, cpindices[0]]**2)**0.5#uses the last cp_index
                bltimerange=np.nonzero((blrad<self.options.maxbaseline)*(blrad>self.options.minbaseline))[0]#flags long baselines for resolved sources and short baselines for antenna shadowing
            else:
                bltimerange=np.arange(ntime)
            blntime=len(bltimerange)
            if (blntime==0):
                print(' ntime: 0')
                continue

            changrange=np.arange(channel_start,channel_start+channel_width)
            swaptrackxy=False
            if (self.dodelay==-1):
                cable_delay=0.
                turns = np.outer((h5.w[bltimerange, cpindices[0]] / katpoint.lightspeed) - cable_delay, self.h5.channel_freqs[changrange])
                visdataxx=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[0]]*np.exp(-2j * np.pi * turns[:,:,np.newaxis]),[blntime,channel_width])),axis=1).reshape(-1)*np.exp(1j*self.phaseslope*(offaxistime-offaxistime[0]))
                turns = np.outer((h5.w[bltimerange, cpindices[1]] / katpoint.lightspeed) - cable_delay, self.h5.channel_freqs[changrange])
                visdataxy=-np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[1]]*np.exp(-2j * np.pi * turns[:,:,np.newaxis]),[blntime,channel_width])),axis=1).reshape(-1)*np.exp(1j*self.phaseslope*(offaxistime-offaxistime[0]))
                turns = np.outer((h5.w[bltimerange, cpindices[2]] / katpoint.lightspeed) - cable_delay, self.h5.channel_freqs[changrange])
                visdatayx=-np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[2]]*np.exp(-2j * np.pi * turns[:,:,np.newaxis]),[blntime,channel_width])),axis=1).reshape(-1)*np.exp(1j*self.phaseslope*(offaxistime-offaxistime[0]))
                turns = np.outer((h5.w[bltimerange, cpindices[3]] / katpoint.lightspeed) - cable_delay, self.h5.channel_freqs[changrange])
                visdatayy=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[3]]*np.exp(-2j * np.pi * turns[:,:,np.newaxis]),[blntime,channel_width])),axis=1).reshape(-1)*np.exp(1j*self.phaseslope*(offaxistime-offaxistime[0]))
            elif (self.dodelay):#with geometric delays;but it seems perhaps knowledge of the antenna positions are inaccurate for RTS at the moment
                cable_delay=0.
                turns = -np.outer((h5.w[bltimerange, cpindices[0]] / katpoint.lightspeed) - cable_delay, self.h5.channel_freqs[changrange])
                visdataxx=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[0]]*np.exp(-2j * np.pi * turns[:,:,np.newaxis]),[blntime,channel_width])),axis=1).reshape(-1)*np.exp(1j*self.phaseslope*(offaxistime-offaxistime[0]))
                turns = -np.outer((h5.w[bltimerange, cpindices[1]] / katpoint.lightspeed) - cable_delay, self.h5.channel_freqs[changrange])
                visdataxy=-np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[1]]*np.exp(-2j * np.pi * turns[:,:,np.newaxis]),[blntime,channel_width])),axis=1).reshape(-1)*np.exp(1j*self.phaseslope*(offaxistime-offaxistime[0]))
                turns = -np.outer((h5.w[bltimerange, cpindices[2]] / katpoint.lightspeed) - cable_delay, self.h5.channel_freqs[changrange])
                visdatayx=-np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[2]]*np.exp(-2j * np.pi * turns[:,:,np.newaxis]),[blntime,channel_width])),axis=1).reshape(-1)*np.exp(1j*self.phaseslope*(offaxistime-offaxistime[0]))
                turns = -np.outer((h5.w[bltimerange, cpindices[3]] / katpoint.lightspeed) - cable_delay, self.h5.channel_freqs[changrange])
                visdatayy=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[3]]*np.exp(-2j * np.pi * turns[:,:,np.newaxis]),[blntime,channel_width])),axis=1).reshape(-1)*np.exp(1j*self.phaseslope*(offaxistime-offaxistime[0]))
            else:
                visdataxx=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[0]],[blntime,channel_width])),axis=1).reshape(-1)*np.exp(1j*self.phaseslope*(offaxistime-offaxistime[0]))
                visdataxy=-np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[1]],[blntime,channel_width])),axis=1).reshape(-1)*np.exp(1j*self.phaseslope*(offaxistime-offaxistime[0]))
                visdatayx=-np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[2]],[blntime,channel_width])),axis=1).reshape(-1)*np.exp(1j*self.phaseslope*(offaxistime-offaxistime[0]))
                visdatayy=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[3]],[blntime,channel_width])),axis=1).reshape(-1)*np.exp(1j*self.phaseslope*(offaxistime-offaxistime[0]))
            # visdataxx=np.mean(np.conj(np.abs(np.reshape(h5.vis[bltimerange,changrange,cpindices[0]],[blntime,channel_width]))),axis=1).reshape(-1)
            # visdataxy=-np.mean(np.conj(np.abs(np.reshape(h5.vis[bltimerange,changrange,cpindices[1]],[blntime,channel_width]))),axis=1).reshape(-1)
            # visdatayx=-np.mean(np.conj(np.abs(np.reshape(h5.vis[bltimerange,changrange,cpindices[2]],[blntime,channel_width]))),axis=1).reshape(-1)
            # visdatayy=np.mean(np.conj(np.abs(np.reshape(h5.vis[bltimerange,changrange,cpindices[3]],[blntime,channel_width]))),axis=1).reshape(-1)
            t2=time.time()
            sys.stdout.write(' ntime: %d load: %.1f'%(blntime,t2-t1));sys.stdout.flush();
            if (doconj):#apply conjugate transpose
                visdataxx=np.conj(visdataxx)
                tmp=np.conj(visdatayx)
                visdatayx=np.conj(visdataxy)
                visdataxy=tmp
                visdatayy=np.conj(visdatayy)
                        
                        
            aGx[bltimerange]+=visdataxx
            aDx[bltimerange]+=visdataxy
            aDy[bltimerange]+=visdatayx
            aGy[bltimerange]+=visdatayy
            acount[bltimerange]+=1

        validpts=np.nonzero(acount)[0]   
        aGx=aGx[validpts]/acount[validpts]
        aDx=aDx[validpts]/acount[validpts]
        aDy=aDy[validpts]/acount[validpts]
        aGy=aGy[validpts]/acount[validpts]
                
        vis=[aGx,aGy,aDx,aDy]
        return vis, storeparang[validpts], storeparangscan[validpts], storetargetx[validpts], storetargety[validpts]
    
    def extractdata(self,poi_l,poi_k,poi_sigma,targetx,targety,channel_range,flagmask,trackantennas,scanantenna,chan_indices,doradec=False,douvr=False):
        largestroi=0
        nexpansions=0

        if (len(trackantennas)==0):
            target=self.h5.catalogue.targets[h5.target_indices[0]]#use target rather than tracking antenna, incase there are no tracking antennas

        if (doradec):#note for this case the poi_l is the number of radialscan_sampling steps oway from target
            targetra, targetdec = target.radec()#note this is in radians already
            targetra*=180.0/np.pi
            targetdec*=180.0/np.pi
            raroi=max(np.abs(self.h5.ra[:,scanantenna]*180.0/12.0-targetra))*radialscan_sampling*2.0/radialscan_extent
            decroi=max(np.abs(self.h5.dec[:,scanantenna]-targetdec))*radialscan_sampling*2.0/radialscan_extent
            ra_center=targetra+raroi*poi_l*np.cos(poi_k*np.pi/180.0);
            dec_center=targetdec+decroi*poi_l*np.sin(poi_k*np.pi/180.0);
            print('Extracting data at RA %0.2g DEC %0.2g (region radius %0.2g,%0.2g)'%(ra_center,dec_center,raroi,decroi))
        else:    #in target plane coordinates
            poi_center_x=poi_l-self.extralmoffset[0]*np.pi/180.0;
            poi_center_y=poi_k-self.extralmoffset[1]*np.pi/180.0;
            print('Extracting data at %0.2g %0.2g in target field (region radius %0.2g)'%(poi_center_x,poi_center_y,poi_sigma))

        self.h5.select(reset='F',channels=channel_range)
        numtrackantenna=len(self.radialscan_allantenna)-len(self.radialscan_scanantenna)
        if (numtrackantenna==0):
            numtrackantenna=len(self.radialscan_scanantenna)#not really, but this cannot be zero
        thedumps=[]
        for roif in [1.0,1.1,1.25,1.5,1.75,2.0,3.0,4.0,5.0,8.0,10.0,12.0,15.0,20.0,25.0,30.0,40.0,50.0,100.0]:
            self.h5.select(reset='T')
            if (doradec):
                self.h5.select(scans='~slew',dumps=np.array((np.array(((self.h5.ra[:,scanantenna]*180.0/12.0-ra_center)/(raroi*roif))**2+((self.h5.dec[:,scanantenna]-dec_center)/(decroi*roif))**2<1.0,dtype='int') & (1-flagmask)),dtype='bool'));
                print('roif',roif,np.shape(self.h5.timestamps)[0])
            else:
    #            h5.select(scans='~slew',dumps=np.array((np.array((targetx-poi_center_x)**2+(targety-poi_center_y)**2<(roif*poi_sigma)**2,dtype='int') & (1-flagmask)),dtype='bool'));
                self.h5.select(dumps=np.array((np.array((targetx-poi_center_x)**2+(targety-poi_center_y)**2<(roif*poi_sigma)**2,dtype='int') & (1-flagmask)),dtype='bool'));

            if (np.shape(self.h5.timestamps)[0]*numtrackantenna>=8):
                if (roif>1.0):
                    if (largestroi<roif):
                        largestroi=roif
                    print('Warning, region increased by factor '+str(roif))
                break;
        if (roif>1.0):
            nexpansions+=1#counts total number of times performed
            if (roif>=100.0):
                print('Insufficient data for pointing ')
                exit()

         # prepare to write main dict
        corrprod_to_index = dict([(tuple(cp), ind) for cp, ind in zip(np.r_[self.h5.corr_products,self.h5.corr_products[::,::-1]], np.r_[range(len(self.h5.corr_products)),range(len(self.h5.corr_products))])])
        theindices=self.h5._time_keep.nonzero()[0]
        scan_len = self.h5.shape[0]
        #find scan intervals automatically by testing jumps>5sec in time indices
        interv=np.nonzero(np.diff(self.h5.timestamps)>5)[0]+1
        intervalfrom=np.r_[0,interv]
        intervalto=np.r_[interv,len(self.h5.timestamps)]#up to but not including
        print('Detected %d on-axis time intervals'%(len(intervalfrom)))
        
        #make a baseline matrix to store data
        self.storebandpass=[[np.zeros([0,len(self.h5.channels),4],dtype='complex64') for ia in range(len(self.h5.ants))] for ia in range(len(self.h5.ants))]
        storedata=[[np.zeros([0,len(self.h5.channels),4],dtype='complex64') for ia in range(len(self.h5.ants))] for ia in range(len(self.h5.ants))]
        storemodelphase=[[0 for ia in range(len(self.h5.ants))] for ia in range(len(self.h5.ants))]
        storegain=[[[np.ones([scan_len],dtype='float') for ia in range(len(self.h5.ants))] for ia in range(len(self.h5.ants))] for ic in range(len(chan_indices))]
        storebl=[[np.zeros([0]) for ia in range(len(self.h5.ants))] for ia in range(len(self.h5.ants))]
        storeu=[[np.zeros(0) for ia in range(len(self.h5.ants))] for ia in range(len(self.h5.ants))]    
        storev=[[np.zeros(0) for ia in range(len(self.h5.ants))] for ia in range(len(self.h5.ants))]    
        storeuvr2=[[np.zeros(0) for ia in range(len(self.h5.ants))] for ia in range(len(self.h5.ants))]    

            # load all data for this scan up front, as this improves disk throughput
        t0=time.time()
        scan_data = self.h5.vis[:]
        t1=time.time()
        print('DEBUG NOTE Time to load upfront: ',t1-t0)
            # MS expects timestamps in MJD seconds

    #        utc_seconds=h5.timestamps[:]
    #        storeutc=np.concatenate([storeutc,utc_seconds],axis=0)
    #        parang=katp[target.name].parallactic_angle(utc_seconds)
        if (len(trackantennas)==0):
            storeparang=target.parallactic_angle(self.h5.timestamps[:])
            storeaz,storeel=target.azel(self.h5.timestamps[:])
        else:
            storeparang=self.h5.parangle[:,trackantennas[0]]*np.pi/180.0
            storeel=self.h5.el[:,trackantennas[0]]*np.pi/180.0
            storeaz=self.h5.az[:,trackantennas[0]]*np.pi/180.0
    #    storeparangscan=h5.parangle[:,scanantenna]*np.pi/180.0#original
        storeparangscan=storeparang#-parcorangle[theindices]#normal
    #    storeparangscan=storeparang+parcorangle[theindices]#neg - seem to have minor effect
        storetargetx=targetx[theindices]
        storetargety=targety[theindices]
        storetime=self.h5.timestamps[:]

        storeparang=self.average(storeparang,intervalfrom,intervalto)
        storeparangscan=self.average(storeparangscan,intervalfrom,intervalto)
        storeel=self.average(storeel,intervalfrom,intervalto)
        storeaz=self.average(storeaz,intervalfrom,intervalto)
        storetargetx=self.average(storetargetx,intervalfrom,intervalto)
        storetargety=self.average(storetargety,intervalfrom,intervalto)
        storetime=self.average(storetime,intervalfrom,intervalto)

        for ant1_index, ant1 in enumerate(self.h5.ants):
            for ant2_index, ant2 in enumerate(self.h5.ants):
                if ant2_index <= ant1_index:#dont need autocorrelations either
                    continue
                if (poi_l !=0.0 and not doradec):#only keep data for baselines between tracking and scanning antennas; except for on-axis pointing
                    if ((ant1.name in radialscan_scanantenna) and (ant2.name in radialscan_scanantenna)):
                        continue
                    if ((ant1.name not in radialscan_scanantenna) and (ant2.name not in radialscan_scanantenna)):
                        continue                
                polprods = [("%s%s" % (ant1.name,p[0].lower()), "%s%s" % (ant2.name,p[1].lower())) for p in self.pols_to_use]
                cpindices=[corrprod_to_index.get(p) for p in polprods]
                vis_data=scan_data[:,:,cpindices]
                if (self.dodelay==-1):
                    print('doing neg delay for onaxis data')
                    cable_delay=0.
                    for ipol,cpindex in enumerate(cpindices):
                        turns = np.outer((self.h5.w[:, cpindices[ipol]] / katpoint.lightspeed) - cable_delay, self.h5.channel_freqs[:])
                        vis_data[:,:,ipol]*=np.exp(-2j * np.pi * turns)
                    print('done')
                elif (self.dodelay):
                    print('doing delay for onaxis data')
                    cable_delay=0.
                    for ipol,cpindex in enumerate(cpindices):
                        turns = -np.outer((self.h5.w[:, cpindices[ipol]] / katpoint.lightspeed) - cable_delay, self.h5.channel_freqs[:])
                        vis_data[:,:,ipol]*=np.exp(-2j * np.pi * turns)
                    print('done')
                
                if (self.options.maxbaseline!=None):
                    if (ant1_index==0 and ant2_index==1):
                        print('Calculating uv coordinates for baseline length flagging: %g to %g'%(self.options.minbaseline,self.options.maxbaseline))
                    blrad=(self.h5.u[:, cpindices[0]]**2+self.h5.v[:, cpindices[0]]**2)**0.5#uses the last cp_index
                    storebl[ant1_index][ant2_index]=np.nonzero((blrad<self.options.maxbaseline)*(blrad>self.options.minbaseline))[0]#flags long baselines for resolved sources and short baselines for antenna shadowing
                else:
                    storebl[ant1_index][ant2_index]=np.arange(scan_len)
                if (self.options.normgainperbaseline and len(storebl[ant1_index][ant2_index])):#note normalization by mean only done for storebl time points out of the lot
                    storedata[ant1_index][ant2_index]=np.array(vis_data,dtype='complex64')
                    for ich,channel_ind in enumerate(chan_indices):
    #orig                    storegain[ich][ant1_index][ant2_index]=np.abs(np.mean(vis_data[:,channel_ind,0],axis=1)+np.mean(vis_data[:,channel_ind,3],axis=1)) #assume here I=Vxx+Vyy; average over all freq channels
    #                    storegain[ich][ant1_index][ant2_index]=(np.mean(np.abs(vis_data[:,channel_ind,0])+np.abs(vis_data[:,channel_ind,3]),axis=1)) #sumabs assume here I=Vxx+Vyy; average over all freq channels
                        storegain[ich][ant1_index][ant2_index]=(np.mean(np.abs(vis_data[:,channel_ind,0]+vis_data[:,channel_ind,3]),axis=1)) #abssum assume here I=Vxx+Vyy; average over all freq channels

                        storegain[ich][ant1_index][ant2_index]=np.mean((storegain[ich][ant1_index][ant2_index])[storebl[ant1_index][ant2_index]])/storegain[ich][ant1_index][ant2_index]
    #                    storegain[ich][ant1_index][ant2_index]=1.0/storegain[ich][ant1_index][ant2_index]
    #                    storegain[ich][ant1_index][ant2_index]=upperpercentilemean((storegain[ich][ant1_index][ant2_index])[storebl[ant1_index][ant2_index]],0.97)/storegain[ich][ant1_index][ant2_index]

                        storedata[ant1_index][ant2_index][:,channel_ind,:]*=(storegain[ich][ant1_index][ant2_index])[:,np.newaxis,np.newaxis]

                        storegain[ich][ant1_index][ant2_index]=self.average(storegain[ich][ant1_index][ant2_index],intervalfrom,intervalto)
                        storedata[ant1_index][ant2_index][:,channel_ind,:]=self.average(storedata[ant1_index][ant2_index][:,channel_ind,:],intervalfrom,intervalto)
                else:
                    storedata[ant1_index][ant2_index]=self.average(np.array(vis_data,dtype='complex64'),intervalfrom,intervalto)
                if (self.dobandpass):#only phase, not amplitude correction - else messes up amplitude of cross correlations
                    if (self.dobandpass=='model'):
                        #only operate on hh, vv pol, not hv and vh
                        storemodelphase[ant1_index][ant2_index]=getunwrappedmodelphase(self.h5.timestamps,vis_data[:,:,np.array([0,3])],intervalfrom,intervalto,self.h5.corr_products[np.array(cpindices)][np.array([0,3])])
                        self.storebandpass[ant1_index][ant2_index]=np.exp(1j*np.arange(vis_data.shape[1],dtype=np.float)*storemodelphase[ant1_index][ant2_index]).repeat(4).reshape(vis_data.shape[1],4)
                        print('calc model bandpass',storemodelphase[ant1_index][ant2_index])
                        # bandpass=np.mean(np.array(vis_data,dtype='complex64'),axis=0)#shape nchans,pols
                        # mbandpass=np.exp(1j*np.array([np.arange(vis_data.shape[1])*np.median(np.diff(np.angle(bandpass[:,ipol]))) for ipol in range(len(cpindices))]).transpose())
                        # #self.temp=np.array([np.diff(np.angle(bandpass[:,ipol])) for ipol in range(len(cpindices))]).transpose()
                        # self.storebandpass[ant1_index][ant2_index]=mbandpass
                    elif (self.dobandpass=='modelfft'):
                        #only operate on hh, vv pol, not hv and vh
                        storemodelphase[ant1_index][ant2_index]=-getunwrappedmodelphasefft(self.h5.timestamps,vis_data[:,:,np.array([0,3])],intervalfrom,intervalto,self.h5.corr_products[np.array(cpindices)][np.array([0,3])])
                        self.storebandpass[ant1_index][ant2_index]=np.exp(1j*np.arange(vis_data.shape[1],dtype=np.float)*storemodelphase[ant1_index][ant2_index]).repeat(4).reshape(vis_data.shape[1],4)
                        print('calc modelfft bandpass',storemodelphase[ant1_index][ant2_index])
                    elif (type(self.dobandpass)==tuple or type(self.dobandpass)==list):
                        self.storebandpass[ant1_index][ant2_index]=np.exp(1j*np.angle(np.mean(np.array(vis_data[self.dobandpass[0]:self.dobandpass[1],:,:],dtype='complex64'),axis=0)))
                        print('averaging bandpass over',self.dobandpass,' of ',vis_data.shape[0])
                        print('TODO DELETE THIS')
                        self.the_timestamps=self.h5.timestamps[:]
                        self.the_vis_data=vis_data
                    else:
                        self.storebandpass[ant1_index][ant2_index]=np.exp(1j*np.angle(np.mean(np.array(vis_data,dtype='complex64'),axis=0)))
                        
                if (douvr):
                    storeu[ant1_index][ant2_index]=self.average((self.h5.u[:,cpindices[0]])/1000,intervalfrom,intervalto)
                    storev[ant1_index][ant2_index]=self.average((self.h5.v[:,cpindices[0]])/1000,intervalfrom,intervalto)
                    storeuvr2[ant1_index][ant2_index]=self.average((self.h5.u[:,cpindices[0]]**2+self.h5.v[:,cpindices[0]]**2)/1000**2,intervalfrom,intervalto)
                    
        print('number of time samples ',str(len(storeparang)), ' ROI used: ',str(roif*poi_sigma))
        return storedata, storeparang, storeparangscan, storetargetx, storetargety, storetime, storegain, storebl, storeel, storeaz, storeu, storev, storeuvr2

    #must manufacture single point per scan that is closest to origin
    def extractdatanoh5(self,poi_l,poi_k,poi_sigma,targetx,targety,flagmask):
        largestroi=0
        nexpansions=0

        poi_center_x=poi_l-self.extralmoffset[0]*np.pi/180.0;
        poi_center_y=poi_k-self.extralmoffset[1]*np.pi/180.0;
        print('Extracting data at %0.2g %0.2g in target field (region radius %0.2g)'%(poi_center_x,poi_center_y,poi_sigma))

        for roif in [1.0,1.1,1.25,1.5,1.75,2.0,3.0,4.0,5.0,8.0,10.0,12.0,15.0,20.0,25.0,30.0,40.0,50.0,100.0]:
            dumps=np.array((np.array((targetx-poi_center_x)**2+(targety-poi_center_y)**2<(roif*poi_sigma)**2,dtype='int') & (1-flagmask)),dtype='bool');
            timekeep=np.nonzero(dumps)[0]
            if (np.shape(timekeep)[0]*2>=8):
                if (roif>1.0):
                    if (largestroi<roif):
                        largestroi=roif
                    print('Warning, region increased by factor '+str(roif))
                break;
        if (roif>1.0):
            nexpansions+=1#counts total number of times performed
            if (roif>=100.0):
                print('Insufficient data for pointing ')
                exit()

         # prepare to write main dict
        self.timekeep=timekeep
        scan_len = len(timekeep)
        #find scan intervals automatically by testing jumps>5sec in time indices
        interv=np.nonzero(np.diff(self.rawtime[timekeep])>5)[0]+1
        intervalfrom=np.r_[0,interv]
        intervalto=np.r_[interv,len(self.rawtime[timekeep])]#up to but not including
        c=0
        while c<len(intervalfrom):
            if (intervalto[c]-intervalfrom[c]<3):                
                timekeep=np.r_[timekeep[:intervalfrom[c]],timekeep[intervalto[c]+1:]]
                self.timekeep=timekeep
                scan_len = len(timekeep)
                #find scan intervals automatically by testing jumps>5sec in time indices
                interv=np.nonzero(np.diff(self.rawtime[timekeep])>5)[0]+1
                intervalfrom=np.r_[0,interv]
                intervalto=np.r_[interv,len(self.rawtime[timekeep])]#up to but not including
            else:
                c+=1
                
        # while(1):
        #     remove=np.nonzero(np.diff(interv)<2)[0]
        #     if (len(remove)==0):
        #         break
        #     timekeep=np.r_[timekeep[:interv[remove[0]]],timekeep[(interv[remove[0]]+1):]]
        #     interv=np.r_[interv[:remove[0]],interv[(remove[0]+1):]]
        
        #discards datasets if there is only one datapoint
        # interv=interv[np.nonzero(np.diff(interv)>2)[0]]#
        intervalfrom=np.r_[0,interv]
        intervalto=np.r_[interv,len(self.rawtime[timekeep])]#up to but not including
        print('Detected %d on-axis time intervals'%(len(intervalfrom)))
        
        #make a baseline matrix to store data
        nants=2
        nchans=1
        storedata=[[np.zeros([0,nchans,1],dtype='complex64') for ia in range(nants)] for ia in range(nants)]
        storegain=[[[np.ones([scan_len],dtype='float') for ia in range(nants)] for ia in range(nants)] for ic in range(nchans)]
        storebl=[[np.zeros([0]) for ia in range(nants)] for ia in range(nants)]

        # MS expects timestamps in MJD seconds

        storetargetx=self.ll[timekeep]
        storetargety=self.mm[timekeep]
        storetime=self.rawtime[timekeep]

        storetargetx=self.average(storetargetx,intervalfrom,intervalto)
        storetargety=self.average(storetargety,intervalfrom,intervalto)
        storetime=self.average(storetime,intervalfrom,intervalto)

        storebl[0][1]=np.arange(scan_len)
        storedata[0][1]=self.average(np.array(self.visibilities[0][timekeep],dtype='complex64'),intervalfrom,intervalto)
                    
        print('number of time samples ',str(scan_len), ' ROI used: ',str(roif*poi_sigma))
        return storedata, storetargetx, storetargety, storetime, storegain, storebl


    def processoffaxisdatagainrawabs(self,h5,targetx,targety,channel_range,flagmask,trackantennas,scanantenna,storedata, storeparang, storeparangscan, storetargetx, storetargety, storetime, storegain, storebl, storeel, storeaz, channel_start, channel_width):
        if (len(trackantennas)==0):
            target=h5.catalogue.targets[h5.target_indices[0]]#use target rather than tracking antenna, incase there are no tracking antennas

        h5.select(reset='F',channels=channel_range)
        h5.select(reset='T')
    #    h5.select(scans='~slew',dumps=np.array((1-flagmask),dtype='bool'));
        h5.select(dumps=np.array((1-flagmask),dtype='bool'));

         # prepare to write main dict
        corrprod_to_index = dict([(tuple(cp), ind) for cp, ind in zip(np.r_[h5.corr_products,h5.corr_products[::,::-1]], np.r_[range(len(h5.corr_products)),range(len(h5.corr_products))])])
        theindices=h5._time_keep.nonzero()[0]

    #        utc_seconds=h5.timestamps[:]
    #        storeutc=np.concatenate([storeutc,utc_seconds],axis=0)
    #        parang=katp[target.name].parallactic_angle(utc_seconds)
        if (len(trackantennas)==0):
            storeparang=target.parallactic_angle(h5.timestamps[:])
        else:
            storeparang=h5.parangle[:,trackantennas[0]]*np.pi/180.0
    #    storeparangscan=h5.parangle[:,scanantenna]*np.pi/180.0#original
        storeparangscan=storeparang#-parcorangle[theindices]#normal
    #    storeparangscan=storeparang+parcorangle[theindices]#neg - seem to have minor effect
        offaxistime=h5.timestamps[:]
        storetargetx=targetx[theindices]
        storetargety=targety[theindices]

        Gxgainlist=[]
        Gygainlist=[]
        Dxgainlist=[]
        Dygainlist=[]

        #direct calculation from visibilities
        #in order REAL yyt0,yxt0,xyt0,xxt0,yyt1,yxt1,xyt1,xxt1,... , IMAG yyt0,yxt0,xyt0,xxt0,yyt1,yxt1,xyt1,xxt1,.....
        ntime=len(theindices)
        aGx=np.zeros(ntime,dtype='complex');aGy=np.zeros(ntime,dtype='complex');aGxDx=np.zeros(ntime,dtype='complex');aGyDy=np.zeros(ntime,dtype='complex');acount=np.zeros(ntime,dtype='float');
        print('GAINRAWABS calculation')
        print('using %d time samples and %d channels'%(ntime,channel_width))
        for itrack in trackantennas:#only extract baselines between tracking antennas and scanning antenna
            t1=time.time()
            if (itrack>scanantenna):
                iant=scanantenna;
                jant=itrack;
                doconj=0
            else:
                iant=itrack;
                jant=scanantenna;
                doconj=1
            polprods = [("%s%s" % (self.radialscan_allantenna[iant],p[0].lower()), "%s%s" % (self.radialscan_allantenna[jant],p[1].lower())) for p in self.pols_to_use]
            sys.stdout.write(self.radialscan_allantenna[scanantenna]+': '+self.radialscan_allantenna[iant]+'-'+self.radialscan_allantenna[jant]);sys.stdout.flush();
            cpindices=[corrprod_to_index.get(p) for p in polprods]
            if (self.options.maxbaseline!=None):
                blrad=(h5.u[:, cpindices[0]]**2+h5.v[:, cpindices[0]]**2)**0.5#uses the last cp_index
                bltimerange=np.nonzero((blrad<self.options.maxbaseline)*(blrad>self.options.minbaseline))[0]#flags long baselines for resolved sources and short baselines for antenna shadowing
            else:
                bltimerange=np.arange(ntime)
            blntime=len(bltimerange)
            if (blntime==0):
                print(' ntime: 0')
                continue

            changrange=np.arange(channel_start,channel_start+channel_width)#note problem here!!
            if (1):#process frequency channels in bulk
                if (self.dodelay==-1):
                    print('doing delay')
                    cable_delay=0.
                    turns = np.outer((h5.w[bltimerange, cpindices[0]] / katpoint.lightspeed) - cable_delay, self.h5.channel_freqs[changrange])
                    ovisdataxx=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[0]]*np.exp(-2j * np.pi * turns[:,:,np.newaxis]),[blntime,channel_width])),axis=1).reshape(-1)
                    turns = np.outer((h5.w[bltimerange, cpindices[1]] / katpoint.lightspeed) - cable_delay, self.h5.channel_freqs[changrange])
                    ovisdataxy=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[1]]*np.exp(-2j * np.pi * turns[:,:,np.newaxis]),[blntime,channel_width])),axis=1).reshape(-1)
                    turns = np.outer((h5.w[bltimerange, cpindices[2]] / katpoint.lightspeed) - cable_delay, self.h5.channel_freqs[changrange])
                    ovisdatayx=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[2]]*np.exp(-2j * np.pi * turns[:,:,np.newaxis]),[blntime,channel_width])),axis=1).reshape(-1)
                    turns = np.outer((h5.w[bltimerange, cpindices[3]] / katpoint.lightspeed) - cable_delay, self.h5.channel_freqs[changrange])
                    ovisdatayy=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[3]]*np.exp(-2j * np.pi * turns[:,:,np.newaxis]),[blntime,channel_width])),axis=1).reshape(-1)
                elif (self.dodelay):
                    print('doing delay')
                    cable_delay=0.
                    turns = -np.outer((h5.w[bltimerange, cpindices[0]] / katpoint.lightspeed) - cable_delay, self.h5.channel_freqs[changrange])
                    ovisdataxx=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[0]]*np.exp(-2j * np.pi * turns[:,:,np.newaxis]),[blntime,channel_width])),axis=1).reshape(-1)
                    turns = -np.outer((h5.w[bltimerange, cpindices[1]] / katpoint.lightspeed) - cable_delay, self.h5.channel_freqs[changrange])
                    ovisdataxy=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[1]]*np.exp(-2j * np.pi * turns[:,:,np.newaxis]),[blntime,channel_width])),axis=1).reshape(-1)
                    turns = -np.outer((h5.w[bltimerange, cpindices[2]] / katpoint.lightspeed) - cable_delay, self.h5.channel_freqs[changrange])
                    ovisdatayx=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[2]]*np.exp(-2j * np.pi * turns[:,:,np.newaxis]),[blntime,channel_width])),axis=1).reshape(-1)
                    turns = -np.outer((h5.w[bltimerange, cpindices[3]] / katpoint.lightspeed) - cable_delay, self.h5.channel_freqs[changrange])
                    ovisdatayy=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[3]]*np.exp(-2j * np.pi * turns[:,:,np.newaxis]),[blntime,channel_width])),axis=1).reshape(-1)
                elif (self.dobandpass):
                    print('doing bandpass')
                    ovisdataxx=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[0]],[blntime,channel_width])/self.storebandpass[iant][jant][changrange,0]),axis=1).reshape(-1)
                    ovisdataxy=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[1]],[blntime,channel_width])/self.storebandpass[iant][jant][changrange,1]),axis=1).reshape(-1)
                    ovisdatayx=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[2]],[blntime,channel_width])/self.storebandpass[iant][jant][changrange,2]),axis=1).reshape(-1)
                    ovisdatayy=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[3]],[blntime,channel_width])/self.storebandpass[iant][jant][changrange,3]),axis=1).reshape(-1)
                else:
                    print('not doing delay')
                    if (h5.vis.shape[0]==blntime):#fancy indexing not supported in dask
                        ovisdataxx=np.mean(np.conj(np.reshape(h5.vis[:,changrange,cpindices[0]],[blntime,channel_width])),axis=1).reshape(-1)
                        ovisdataxy=np.mean(np.conj(np.reshape(h5.vis[:,changrange,cpindices[1]],[blntime,channel_width])),axis=1).reshape(-1)
                        ovisdatayx=np.mean(np.conj(np.reshape(h5.vis[:,changrange,cpindices[2]],[blntime,channel_width])),axis=1).reshape(-1)
                        ovisdatayy=np.mean(np.conj(np.reshape(h5.vis[:,changrange,cpindices[3]],[blntime,channel_width])),axis=1).reshape(-1)
                    else:
                        ovisdataxx=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[0]],[blntime,channel_width])),axis=1).reshape(-1)
                        ovisdataxy=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[1]],[blntime,channel_width])),axis=1).reshape(-1)
                        ovisdatayx=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[2]],[blntime,channel_width])),axis=1).reshape(-1)
                        ovisdatayy=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[3]],[blntime,channel_width])),axis=1).reshape(-1)
                t2=time.time()
                sys.stdout.write(' ntime: %d load: %.1f'%(blntime,t2-t1));sys.stdout.flush();
                onaxntime=len(storetime)
                if (self.dobandpass):
                    visdataxx=np.mean(np.conj(np.reshape(storedata[iant][jant][:,changrange,0],[onaxntime,channel_width])/self.storebandpass[iant][jant][changrange,0]),axis=1).reshape(-1)
                    visdataxy=np.mean(np.conj(np.reshape(storedata[iant][jant][:,changrange,1],[onaxntime,channel_width])/self.storebandpass[iant][jant][changrange,1]),axis=1).reshape(-1)
                    visdatayx=np.mean(np.conj(np.reshape(storedata[iant][jant][:,changrange,2],[onaxntime,channel_width])/self.storebandpass[iant][jant][changrange,2]),axis=1).reshape(-1)
                    visdatayy=np.mean(np.conj(np.reshape(storedata[iant][jant][:,changrange,3],[onaxntime,channel_width])/self.storebandpass[iant][jant][changrange,3]),axis=1).reshape(-1)        
                else:
                    visdataxx=np.mean(np.conj(np.reshape(storedata[iant][jant][:,changrange,0],[onaxntime,channel_width])),axis=1).reshape(-1)
                    visdataxy=np.mean(np.conj(np.reshape(storedata[iant][jant][:,changrange,1],[onaxntime,channel_width])),axis=1).reshape(-1)
                    visdatayx=np.mean(np.conj(np.reshape(storedata[iant][jant][:,changrange,2],[onaxntime,channel_width])),axis=1).reshape(-1)
                    visdatayy=np.mean(np.conj(np.reshape(storedata[iant][jant][:,changrange,3],[onaxntime,channel_width])),axis=1).reshape(-1)

                if (self.findwrap):
                    visdataxx=interpbestwrap(ovisdataxx,visdataxx,offaxistime[bltimerange],storetime)
                    visdataxy=interpbestwrap(ovisdataxy,visdataxy,offaxistime[bltimerange],storetime)
                    visdatayx=interpbestwrap(ovisdatayx,visdatayx,offaxistime[bltimerange],storetime)
                    visdatayy=interpbestwrap(ovisdatayy,visdatayy,offaxistime[bltimerange],storetime)
                else:
                    visdataxx=np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.abs(visdataxx))*np.exp(1j*np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.unwrap(np.angle(visdataxx))))
                    visdataxy=np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.abs(visdataxy))*np.exp(1j*np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.unwrap(np.angle(visdataxy))))
                    visdatayx=np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.abs(visdatayx))*np.exp(1j*np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.unwrap(np.angle(visdatayx))))
                    visdatayy=np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.abs(visdatayy))*np.exp(1j*np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.unwrap(np.angle(visdatayy))))
                XXYY=np.array([[ovisdataxx/visdataxx,ovisdataxy/visdataxy],[ovisdatayx/visdatayx,ovisdatayy/visdatayy]],dtype='complex').transpose(2,0,1)
                # XXYY=np.array([[ovisdataxx,ovisdataxy],[ovisdatayx,ovisdatayy]],dtype='complex').transpose(2,0,1)
                # XXYY=np.array([[ovisdataxx/visdataxx,ovisdataxy/visdataxx],[ovisdatayx/visdatayy,ovisdatayy/visdatayy]],dtype='complex').transpose(2,0,1)
                #XXYY=np.array([[ovisdataxx/visdataxx,ovisdataxy/visdataxx],[ovisdatayx/visdataxx,ovisdatayy/visdataxx]],dtype='complex').transpose(2,0,1)
                #test XXYY=np.array([[ovisdataxx/visdataxx,ovisdataxy/visdatayy],[ovisdatayx/visdataxx,ovisdatayy/visdatayy]],dtype='complex').transpose(2,0,1)
                
                if (doconj):#conjugate transpose
                    Gxgainlist.append(np.conj(visdataxx))
                    Dxgainlist.append(-np.conj(visdatayx))
                    Dygainlist.append(-np.conj(visdataxy))
                    Gygainlist.append(np.conj(visdatayy))
                else:
                    Gxgainlist.append(visdataxx)
                    Dxgainlist.append(-visdataxy)
                    Dygainlist.append(-visdatayx)
                    Gygainlist.append(visdatayy)
                invonaxisXXYY=np.array([[visdatayy,-visdataxy],[-visdatayx,visdataxx]],dtype='complex').transpose(2,0,1)/(visdataxx*visdatayy-visdatayx*visdataxy)[:,np.newaxis,np.newaxis];
                
                if (doconj):#test
                    dde=np.conj(XXYY[:,:,:]).transpose(0,2,1)
                else:
                    dde=XXYY[:,:,:]

                # weight=np.mean(np.abs(visdataxx)**2+np.abs(visdatayy)**2)
                # aGx[bltimerange]+=dde[:,0,0]*weight
                # aGxDx[bltimerange]+=dde[:,0,1]*weight
                # aGyDy[bltimerange]+=dde[:,1,0]*weight
                # aGy[bltimerange]+=dde[:,1,1]*weight
                # acount[bltimerange]+=weight
                aGx[bltimerange]+=dde[:,0,0]
                aGxDx[bltimerange]+=dde[:,0,1]
                aGyDy[bltimerange]+=dde[:,1,0]
                aGy[bltimerange]+=dde[:,1,1]
                acount[bltimerange]+=1
            t3=time.time()
            print(' process: %.1f'%(t3-t2))

        validpts=np.nonzero(acount)[0]   
        vis=[aGx[validpts]/acount[validpts], aGy[validpts]/acount[validpts], -(aGxDx[validpts]/acount[validpts]), -(aGyDy[validpts]/acount[validpts])]
        return vis, storeparang[validpts], storeparangscan[validpts], storetargetx[validpts], storetargety[validpts],Gxgainlist,Gygainlist,Dxgainlist,Dygainlist
    
    
#must make a version where we first normalise on-axis gains for all correlation products independently
#and then set phases at origin to zero for correlation products independently
#then we find real valued rotation for x and y feeds independently that represents the leakages or physical rotations 
#of feeds with respect to each other
#record these rotations as function of frequency
    
    #gainraw holography calculation, full jones matrix
    #raw but with onaxis gain correction (without matrix inversion)
    def processoffaxisdatagainraw(self,h5,targetx,targety,channel_range,flagmask,trackantennas,scanantenna,storedata, storeparang, storeparangscan, storetargetx, storetargety, storetime, storegain, storebl, storeel, storeaz, channel_start, channel_width):
        if (len(trackantennas)==0):
            target=h5.catalogue.targets[h5.target_indices[0]]#use target rather than tracking antenna, incase there are no tracking antennas

        h5.select(reset='F',channels=channel_range)
        h5.select(reset='T')
    #    h5.select(scans='~slew',dumps=np.array((1-flagmask),dtype='bool'));
        h5.select(dumps=np.array((1-flagmask),dtype='bool'));

         # prepare to write main dict
        corrprod_to_index = dict([(tuple(cp), ind) for cp, ind in zip(np.r_[h5.corr_products,h5.corr_products[::,::-1]], np.r_[range(len(h5.corr_products)),range(len(h5.corr_products))])])
        theindices=h5._time_keep.nonzero()[0]

    #        utc_seconds=h5.timestamps[:]
    #        storeutc=np.concatenate([storeutc,utc_seconds],axis=0)
    #        parang=katp[target.name].parallactic_angle(utc_seconds)
        if (len(trackantennas)==0):
            storeparang=target.parallactic_angle(h5.timestamps[:])
        else:
            storeparang=h5.parangle[:,trackantennas[0]]*np.pi/180.0
    #    storeparangscan=h5.parangle[:,scanantenna]*np.pi/180.0#original
        storeparangscan=storeparang#-parcorangle[theindices]#normal
    #    storeparangscan=storeparang+parcorangle[theindices]#neg - seem to have minor effect
        offaxistime=h5.timestamps[:]
        storetargetx=targetx[theindices]
        storetargety=targety[theindices]

        Gxgainlist=[]
        Gygainlist=[]
        Dxgainlist=[]
        Dygainlist=[]

        #direct calculation from visibilities
        #in order REAL yyt0,yxt0,xyt0,xxt0,yyt1,yxt1,xyt1,xxt1,... , IMAG yyt0,yxt0,xyt0,xxt0,yyt1,yxt1,xyt1,xxt1,.....
        ntime=len(theindices)
        aGx=np.zeros(ntime,dtype='complex');aGy=np.zeros(ntime,dtype='complex');aGxDx=np.zeros(ntime,dtype='complex');aGyDy=np.zeros(ntime,dtype='complex');acount=np.zeros(ntime,dtype='float');
        print('GAINRAW calculation')
        print('using %d time samples and %d channels'%(ntime,channel_width))
        for itrack in trackantennas:#only extract baselines between tracking antennas and scanning antenna
            t1=time.time()
            if (itrack>scanantenna):
                iant=scanantenna;
                jant=itrack;
                doconj=0
            else:
                iant=itrack;
                jant=scanantenna;
                doconj=1
            polprods = [("%s%s" % (self.radialscan_allantenna[iant],p[0].lower()), "%s%s" % (self.radialscan_allantenna[jant],p[1].lower())) for p in self.pols_to_use]
            sys.stdout.write(self.radialscan_allantenna[scanantenna]+': '+self.radialscan_allantenna[iant]+'-'+self.radialscan_allantenna[jant]);sys.stdout.flush();
            cpindices=[corrprod_to_index.get(p) for p in polprods]
            if (self.options.maxbaseline!=None):
                blrad=(h5.u[:, cpindices[0]]**2+h5.v[:, cpindices[0]]**2)**0.5#uses the last cp_index
                bltimerange=np.nonzero((blrad<self.options.maxbaseline)*(blrad>self.options.minbaseline))[0]#flags long baselines for resolved sources and short baselines for antenna shadowing
            else:
                bltimerange=np.arange(ntime)
            blntime=len(bltimerange)
            if (blntime==0):
                print(' ntime: 0')
                continue

            changrange=np.arange(channel_start,channel_start+channel_width)#note problem here!!
            if (1):#process frequency channels in bulk

                if (self.dodelay):
                    print('doing neg delay')
                    cable_delay=0.
                    turns = np.outer((h5.w[bltimerange, cpindices[0]] / katpoint.lightspeed) - cable_delay, self.h5.channel_freqs[changrange])
                    ovisdataxx=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[0]]*np.exp(-2j * np.pi * turns[:,:,np.newaxis]),[blntime,channel_width])),axis=1).reshape(-1)
                    turns = np.outer((h5.w[bltimerange, cpindices[1]] / katpoint.lightspeed) - cable_delay, self.h5.channel_freqs[changrange])
                    ovisdataxy=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[1]]*np.exp(-2j * np.pi * turns[:,:,np.newaxis]),[blntime,channel_width])),axis=1).reshape(-1)
                    turns = np.outer((h5.w[bltimerange, cpindices[2]] / katpoint.lightspeed) - cable_delay, self.h5.channel_freqs[changrange])
                    ovisdatayx=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[2]]*np.exp(-2j * np.pi * turns[:,:,np.newaxis]),[blntime,channel_width])),axis=1).reshape(-1)
                    turns = np.outer((h5.w[bltimerange, cpindices[3]] / katpoint.lightspeed) - cable_delay, self.h5.channel_freqs[changrange])
                    ovisdatayy=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[3]]*np.exp(-2j * np.pi * turns[:,:,np.newaxis]),[blntime,channel_width])),axis=1).reshape(-1)
                elif (self.dodelay):
                    print('doing delay')
                    cable_delay=0.
                    turns = -np.outer((h5.w[bltimerange, cpindices[0]] / katpoint.lightspeed) - cable_delay, self.h5.channel_freqs[changrange])
                    ovisdataxx=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[0]]*np.exp(-2j * np.pi * turns[:,:,np.newaxis]),[blntime,channel_width])),axis=1).reshape(-1)
                    turns = -np.outer((h5.w[bltimerange, cpindices[1]] / katpoint.lightspeed) - cable_delay, self.h5.channel_freqs[changrange])
                    ovisdataxy=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[1]]*np.exp(-2j * np.pi * turns[:,:,np.newaxis]),[blntime,channel_width])),axis=1).reshape(-1)
                    turns = -np.outer((h5.w[bltimerange, cpindices[2]] / katpoint.lightspeed) - cable_delay, self.h5.channel_freqs[changrange])
                    ovisdatayx=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[2]]*np.exp(-2j * np.pi * turns[:,:,np.newaxis]),[blntime,channel_width])),axis=1).reshape(-1)
                    turns = -np.outer((h5.w[bltimerange, cpindices[3]] / katpoint.lightspeed) - cable_delay, self.h5.channel_freqs[changrange])
                    ovisdatayy=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[3]]*np.exp(-2j * np.pi * turns[:,:,np.newaxis]),[blntime,channel_width])),axis=1).reshape(-1)
                else:
                    print('not doing delay')
                    ovisdataxx=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[0]],[blntime,channel_width])),axis=1).reshape(-1)
                    ovisdataxy=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[1]],[blntime,channel_width])),axis=1).reshape(-1)
                    ovisdatayx=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[2]],[blntime,channel_width])),axis=1).reshape(-1)
                    ovisdatayy=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[3]],[blntime,channel_width])),axis=1).reshape(-1)
                t2=time.time()
                sys.stdout.write(' ntime: %d load: %.1f'%(blntime,t2-t1));sys.stdout.flush();
                onaxntime=len(storetime)
                visdataxx=np.mean(np.conj(np.reshape(storedata[iant][jant][:,changrange,0],[onaxntime,channel_width])),axis=1).reshape(-1)
                visdataxy=np.mean(np.conj(np.reshape(storedata[iant][jant][:,changrange,1],[onaxntime,channel_width])),axis=1).reshape(-1)
                visdatayx=np.mean(np.conj(np.reshape(storedata[iant][jant][:,changrange,2],[onaxntime,channel_width])),axis=1).reshape(-1)
                visdatayy=np.mean(np.conj(np.reshape(storedata[iant][jant][:,changrange,3],[onaxntime,channel_width])),axis=1).reshape(-1)
                visdataxx=np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.real(visdataxx))+1j*np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.imag(visdataxx))
                visdataxy=np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.real(visdataxy))+1j*np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.imag(visdataxy))
                visdatayx=np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.real(visdatayx))+1j*np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.imag(visdatayx))
                visdatayy=np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.real(visdatayy))+1j*np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.imag(visdatayy))
                XXYY=np.array([[ovisdataxx/visdataxx,ovisdataxy/visdataxy],[ovisdatayx/visdatayx,ovisdatayy/visdatayy]],dtype='complex').transpose(2,0,1)
                # XXYY=np.array([[ovisdataxx,ovisdataxy],[ovisdatayx,ovisdatayy]],dtype='complex').transpose(2,0,1)
                # XXYY=np.array([[ovisdataxx/visdataxx,ovisdataxy/visdataxx],[ovisdatayx/visdatayy,ovisdatayy/visdatayy]],dtype='complex').transpose(2,0,1)
                #XXYY=np.array([[ovisdataxx/visdataxx,ovisdataxy/visdataxx],[ovisdatayx/visdataxx,ovisdatayy/visdataxx]],dtype='complex').transpose(2,0,1)
                #test XXYY=np.array([[ovisdataxx/visdataxx,ovisdataxy/visdatayy],[ovisdatayx/visdataxx,ovisdatayy/visdatayy]],dtype='complex').transpose(2,0,1)
                
                if (doconj):#conjugate transpose
                    Gxgainlist.append(np.conj(visdataxx))
                    Dxgainlist.append(-np.conj(visdatayx))
                    Dygainlist.append(-np.conj(visdataxy))
                    Gygainlist.append(np.conj(visdatayy))
                else:
                    Gxgainlist.append(visdataxx)
                    Dxgainlist.append(-visdataxy)
                    Dygainlist.append(-visdatayx)
                    Gygainlist.append(visdatayy)
                invonaxisXXYY=np.array([[visdatayy,-visdataxy],[-visdatayx,visdataxx]],dtype='complex').transpose(2,0,1)/(visdataxx*visdatayy-visdatayx*visdataxy)[:,np.newaxis,np.newaxis];
                
                if (doconj):#test
                    dde=np.conj(XXYY[:,:,:]).transpose(0,2,1)
                else:
                    dde=XXYY[:,:,:]

                # weight=np.mean(np.abs(visdataxx)**2+np.abs(visdatayy)**2)
                # aGx[bltimerange]+=dde[:,0,0]*weight
                # aGxDx[bltimerange]+=dde[:,0,1]*weight
                # aGyDy[bltimerange]+=dde[:,1,0]*weight
                # aGy[bltimerange]+=dde[:,1,1]*weight
                # acount[bltimerange]+=weight
                aGx[bltimerange]+=dde[:,0,0]
                aGxDx[bltimerange]+=dde[:,0,1]
                aGyDy[bltimerange]+=dde[:,1,0]
                aGy[bltimerange]+=dde[:,1,1]
                acount[bltimerange]+=1
            t3=time.time()
            print(' process: %.1f'%(t3-t2))

        validpts=np.nonzero(acount)[0]   
        vis=[aGx[validpts]/acount[validpts], aGy[validpts]/acount[validpts], -(aGxDx[validpts]/acount[validpts]), -(aGyDy[validpts]/acount[validpts])]
        return vis, storeparang[validpts], storeparangscan[validpts], storetargetx[validpts], storetargety[validpts],Gxgainlist,Gygainlist,Dxgainlist,Dygainlist
    
    def processoffaxisdatagainrawnoh5(self,targetx,targety,flagmask,storedata, storetargetx, storetargety, storetime, storegain, storebl):
        theindices=range(len(self.rawtime))
        offaxistime=self.rawtime[:]
        storetargetx=targetx[theindices]
        storetargety=targety[theindices]

        Gxgainlist=[]

        #direct calculation from visibilities
        #in order REAL yyt0,yxt0,xyt0,xxt0,yyt1,yxt1,xyt1,xxt1,... , IMAG yyt0,yxt0,xyt0,xxt0,yyt1,yxt1,xyt1,xxt1,.....
        ntime=len(theindices)
        aGx=np.zeros(ntime,dtype='complex');acount=np.zeros(ntime,dtype='float');
        print('GAINRAW no h5 calculation')
        print('using %d time samples'%(ntime))
        t1=time.time()
        bltimerange=range(ntime)
        ovisdataxx=self.visibilities[0][bltimerange]
        t2=time.time()
        sys.stdout.write(' ntime: %d load: %.1f'%(len(bltimerange),t2-t1));sys.stdout.flush();
        onaxntime=len(storetime)
        visdataxx=storedata[0][1]
        visdataxx=np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.real(visdataxx))+1j*np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.imag(visdataxx))
        XXYY=ovisdataxx/visdataxx
        Gxgainlist.append(visdataxx)
        dde=XXYY
        aGx[bltimerange]+=dde
        acount[bltimerange]+=1
        t3=time.time()
        print(' process: %.1f'%(t3-t2))
        self.gains=visdataxx

        validpts=np.nonzero(acount)[0]   
        vis=[aGx[validpts]/acount[validpts], np.zeros(np.shape(aGx)), np.zeros(np.shape(aGx)), np.zeros(np.shape(aGx))]
        return vis, storetargetx[validpts], storetargety[validpts],Gxgainlist

    def processoffaxisdatagainrawnoh5abs(self,targetx,targety,flagmask,storedata, storetargetx, storetargety, storetime, storegain, storebl):
        theindices=range(len(self.rawtime))
        offaxistime=self.rawtime[:]
        storetargetx=targetx[theindices]
        storetargety=targety[theindices]

        Gxgainlist=[]

        #direct calculation from visibilities
        #in order REAL yyt0,yxt0,xyt0,xxt0,yyt1,yxt1,xyt1,xxt1,... , IMAG yyt0,yxt0,xyt0,xxt0,yyt1,yxt1,xyt1,xxt1,.....
        ntime=len(theindices)
        aGx=np.zeros(ntime,dtype='complex');acount=np.zeros(ntime,dtype='float');
        print('GAINRAW abs no h5 calculation')
        print('using %d time samples'%(ntime))
        t1=time.time()
        bltimerange=range(ntime)
        ovisdataxx=self.visibilities[0][bltimerange]
        t2=time.time()
        sys.stdout.write(' ntime: %d load: %.1f'%(len(bltimerange),t2-t1));sys.stdout.flush();
        onaxntime=len(storetime)
        visdataxx=storedata[0][1]
        visdataxx=np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.abs(visdataxx))*np.exp(1j*np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.unwrap(np.angle(visdataxx))))
        XXYY=ovisdataxx/visdataxx
        Gxgainlist.append(visdataxx)
        dde=XXYY
        aGx[bltimerange]+=dde
        acount[bltimerange]+=1
        t3=time.time()
        print(' process: %.1f'%(t3-t2))
        self.gains=visdataxx

        validpts=np.nonzero(acount)[0]   
        vis=[aGx[validpts]/acount[validpts], np.zeros(np.shape(aGx)), np.zeros(np.shape(aGx)), np.zeros(np.shape(aGx))]
        return vis, storetargetx[validpts], storetargety[validpts],Gxgainlist
    
    #direct holography calculation, full jones matrix
    def processoffaxisdatadirect(self,h5,targetx,targety,channel_range,flagmask,trackantennas,scanantenna,storedata, storeparang, storeparangscan, storetargetx, storetargety, storetime, storegain, storebl, storeel, storeaz, channel_start, channel_width):
        if (len(trackantennas)==0):
            target=h5.catalogue.targets[h5.target_indices[0]]#use target rather than tracking antenna, incase there are no tracking antennas

        h5.select(reset='F',channels=channel_range)
        h5.select(reset='T')
    #    h5.select(scans='~slew',dumps=np.array((1-flagmask),dtype='bool'));
        h5.select(dumps=np.array((1-flagmask),dtype='bool'));

         # prepare to write main dict
        corrprod_to_index = dict([(tuple(cp), ind) for cp, ind in zip(np.r_[h5.corr_products,h5.corr_products[::,::-1]], np.r_[range(len(h5.corr_products)),range(len(h5.corr_products))])])
        theindices=h5._time_keep.nonzero()[0]

    #        utc_seconds=h5.timestamps[:]
    #        storeutc=np.concatenate([storeutc,utc_seconds],axis=0)
    #        parang=katp[target.name].parallactic_angle(utc_seconds)
        if (len(trackantennas)==0):
            storeparang=target.parallactic_angle(h5.timestamps[:])
        else:
            storeparang=h5.parangle[:,trackantennas[0]]*np.pi/180.0
    #    storeparangscan=h5.parangle[:,scanantenna]*np.pi/180.0#original
        storeparangscan=storeparang#-parcorangle[theindices]#normal
    #    storeparangscan=storeparang+parcorangle[theindices]#neg - seem to have minor effect
        offaxistime=h5.timestamps[:]
        storetargetx=targetx[theindices]
        storetargety=targety[theindices]

        Gxgainlist=[]
        Gygainlist=[]
        Dxgainlist=[]
        Dygainlist=[]

        #direct calculation from visibilities
        #in order REAL yyt0,yxt0,xyt0,xxt0,yyt1,yxt1,xyt1,xxt1,... , IMAG yyt0,yxt0,xyt0,xxt0,yyt1,yxt1,xyt1,xxt1,.....
        ntime=len(theindices)
        aGx=np.zeros(ntime,dtype='complex');aGy=np.zeros(ntime,dtype='complex');aGxDx=np.zeros(ntime,dtype='complex');aGyDy=np.zeros(ntime,dtype='complex');acount=np.zeros(ntime,dtype='float');
        print('DIRECT calculation')
        print('using %d time samples and %d channels'%(ntime,channel_width))
        for nameoffset in range(len(self.radialscan_allantenna[0])):
            if (self.radialscan_allantenna[0][nameoffset].isdigit()):
                break
        for itrack in trackantennas:#only extract baselines between tracking antennas and scanning antenna
            t1=time.time()
            if (itrack>scanantenna):
                iant=scanantenna;
                jant=itrack;
            else:
                iant=itrack;
                jant=scanantenna;
            doconj= 0 if (int(self.radialscan_allantenna[itrack][nameoffset:])>int(self.radialscan_allantenna[scanantenna][nameoffset:])) else 1
            
            polprods = [("%s%s" % (self.radialscan_allantenna[iant],p[0].lower()), "%s%s" % (self.radialscan_allantenna[jant],p[1].lower())) for p in self.pols_to_use]
            sys.stdout.write(self.radialscan_allantenna[scanantenna]+': '+self.radialscan_allantenna[iant]+'-'+self.radialscan_allantenna[jant]);sys.stdout.flush();
            cpindices=[corrprod_to_index.get(p) for p in polprods]
            if (self.options.maxbaseline!=None):
                blrad=(h5.u[:, cpindices[0]]**2+h5.v[:, cpindices[0]]**2)**0.5#uses the last cp_index
                bltimerange=np.nonzero((blrad<self.options.maxbaseline)*(blrad>self.options.minbaseline))[0]#flags long baselines for resolved sources and short baselines for antenna shadowing
            else:
                bltimerange=np.arange(ntime)
            blntime=len(bltimerange)
            if (blntime==0):
                print(' ntime: 0')
                continue

            changrange=np.arange(channel_start,channel_start+channel_width)#note problem here!!
            if (1):#process frequency channels in bulk
                if (0):#self.extraturn):
                    # delays = {}
                    # delays['h'] = {'ant1': 2.32205060e-05, 'ant2': 2.32842541e-05, 'ant3': 2.34093761e-05, 'ant4': 2.35162232e-05, 'ant5': 2.36786287e-05, 'ant6': 2.37855760e-05, 'ant7': 2.40479534e-05}
                    # delays['v'] = {'ant1': 2.32319854e-05, 'ant2': 2.32902574e-05, 'ant3': 2.34050180e-05, 'ant4': 2.35194585e-05, 'ant5': 2.36741915e-05, 'ant6': 2.37882216e-05, 'ant7': 2.40424086e-05}
                    # cable_delay = delays[p[1][-1]][ant2.name] - delays[p[0][-1]][ant1.name]
                    cable_delay=0
                    turns = -np.outer((h5.w[bltimerange, cpindices[0]] / katpoint.lightspeed) - cable_delay, h5.channel_freqs[changrange])
                    vis_data=h5.vis[bltimerange,changrange,cpindices[0]]*np.exp(-2j * np.pi * turns[:,:,np.newaxis])
                    ovisdataxx=np.mean(np.conj(np.reshape(vis_data,[blntime,channel_width])),axis=1).reshape(-1)
                    
                    turns = -np.outer((h5.w[bltimerange, cpindices[1]] / katpoint.lightspeed) - cable_delay, h5.channel_freqs[changrange])
                    vis_data=h5.vis[bltimerange,changrange,cpindices[1]]*np.exp(-2j * np.pi * turns[:,:,np.newaxis])
                    ovisdataxy=np.mean(np.conj(np.reshape(vis_data,[blntime,channel_width])),axis=1).reshape(-1)
                    turns = -np.outer((h5.w[bltimerange, cpindices[2]] / katpoint.lightspeed) - cable_delay, h5.channel_freqs[changrange])
                    vis_data=h5.vis[bltimerange,changrange,cpindices[2]]*np.exp(-2j * np.pi * turns[:,:,np.newaxis])
                    ovisdatayx=np.mean(np.conj(np.reshape(vis_data,[blntime,channel_width])),axis=1).reshape(-1)
                    turns = -np.outer((h5.w[bltimerange, cpindices[3]] / katpoint.lightspeed) - cable_delay, h5.channel_freqs[changrange])
                    vis_data=h5.vis[bltimerange,changrange,cpindices[3]]*np.exp(-2j * np.pi * turns[:,:,np.newaxis])
                    ovisdatayy=np.mean(np.conj(np.reshape(vis_data,[blntime,channel_width])),axis=1).reshape(-1)
                elif (self.dobandpass):
                    # print 'doing bandpass'
                    # plt.plot(np.angle(h5.vis[-1,:,cpindices[2]].reshape(-1)/self.storebandpass[iant][jant][:,2].reshape(-1)).reshape(-1),'b')
                    # plt.plot(np.angle(h5.vis[-1,:,cpindices[2]]).reshape(-1),'r')
                    # debug
                    ovisdataxx=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[0]],[blntime,channel_width])/self.storebandpass[iant][jant][changrange,0]),axis=1).reshape(-1)
                    ovisdataxy=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[1]],[blntime,channel_width])/self.storebandpass[iant][jant][changrange,1]),axis=1).reshape(-1)
                    ovisdatayx=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[2]],[blntime,channel_width])/self.storebandpass[iant][jant][changrange,2]),axis=1).reshape(-1)
                    ovisdatayy=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[3]],[blntime,channel_width])/self.storebandpass[iant][jant][changrange,3]),axis=1).reshape(-1)
                else:
                    ovisdataxx=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[0]],[blntime,channel_width])),axis=1).reshape(-1)
                    ovisdataxy=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[1]],[blntime,channel_width])),axis=1).reshape(-1)
                    ovisdatayx=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[2]],[blntime,channel_width])),axis=1).reshape(-1)
                    ovisdatayy=np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindices[3]],[blntime,channel_width])),axis=1).reshape(-1)
                
                if (self.phaseslope!=0):
                    ovisdataxx*=np.exp(1j*self.phaseslope*(offaxistime[bltimerange]-offaxistime[0]))
                    ovisdataxy*=np.exp(1j*self.phaseslope*(offaxistime[bltimerange]-offaxistime[0]))
                    ovisdatayx*=np.exp(1j*self.phaseslope*(offaxistime[bltimerange]-offaxistime[0]))
                    ovisdatayy*=np.exp(1j*self.phaseslope*(offaxistime[bltimerange]-offaxistime[0]))
                t2=time.time()
                sys.stdout.write(' ntime: %d load: %.1f'%(blntime,t2-t1));sys.stdout.flush();
                XXYY=np.array([[ovisdataxx,ovisdataxy],[ovisdatayx,ovisdatayy]],dtype='complex').transpose(2,0,1)
                onaxntime=len(storetime)
                if (self.dobandpass):
                    visdataxx=np.mean(np.conj(np.reshape(storedata[iant][jant][:,changrange,0],[onaxntime,channel_width])/self.storebandpass[iant][jant][changrange,0]),axis=1).reshape(-1)
                    visdataxy=np.mean(np.conj(np.reshape(storedata[iant][jant][:,changrange,1],[onaxntime,channel_width])/self.storebandpass[iant][jant][changrange,1]),axis=1).reshape(-1)
                    visdatayx=np.mean(np.conj(np.reshape(storedata[iant][jant][:,changrange,2],[onaxntime,channel_width])/self.storebandpass[iant][jant][changrange,2]),axis=1).reshape(-1)
                    visdatayy=np.mean(np.conj(np.reshape(storedata[iant][jant][:,changrange,3],[onaxntime,channel_width])/self.storebandpass[iant][jant][changrange,3]),axis=1).reshape(-1)
                else:
                    visdataxx=np.mean(np.conj(np.reshape(storedata[iant][jant][:,changrange,0],[onaxntime,channel_width])),axis=1).reshape(-1)
                    visdataxy=np.mean(np.conj(np.reshape(storedata[iant][jant][:,changrange,1],[onaxntime,channel_width])),axis=1).reshape(-1)
                    visdatayx=np.mean(np.conj(np.reshape(storedata[iant][jant][:,changrange,2],[onaxntime,channel_width])),axis=1).reshape(-1)
                    visdatayy=np.mean(np.conj(np.reshape(storedata[iant][jant][:,changrange,3],[onaxntime,channel_width])),axis=1).reshape(-1)
                    
                if (self.phaseslope!=0):
                    visdataxx*=np.exp(1j*self.phaseslope*(storetime-storetime[0]))
                    visdataxy*=np.exp(1j*self.phaseslope*(storetime-storetime[0]))
                    visdatayx*=np.exp(1j*self.phaseslope*(storetime-storetime[0]))
                    visdatayy*=np.exp(1j*self.phaseslope*(storetime-storetime[0]))
                # phvisdataxx=-np.mean((np.reshape(storemodelphase[iant][jant][:,changrange,0],[onaxntime,channel_width])),axis=1).reshape(-1)
                # phvisdataxy=-np.mean((np.reshape(storemodelphase[iant][jant][:,changrange,1],[onaxntime,channel_width])),axis=1).reshape(-1)
                # phvisdatayx=-np.mean((np.reshape(storemodelphase[iant][jant][:,changrange,2],[onaxntime,channel_width])),axis=1).reshape(-1)
                # phvisdatayy=-np.mean((np.reshape(storemodelphase[iant][jant][:,changrange,3],[onaxntime,channel_width])),axis=1).reshape(-1)

                if (0):#abs interpolation unwrapped modeled phase instead of real imag
                    print('doing abs model unwrap phase interp')
                    visdataxx=np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.abs(visdataxx))*np.exp(1j*np.interp(x=offaxistime[bltimerange],xp=storetime,fp=phvisdataxx))
                    visdataxy=np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.abs(visdataxy))*np.exp(1j*np.interp(x=offaxistime[bltimerange],xp=storetime,fp=phvisdataxy))
                    visdatayx=np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.abs(visdatayx))*np.exp(1j*np.interp(x=offaxistime[bltimerange],xp=storetime,fp=phvisdatayx))
                    visdatayy=np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.abs(visdatayy))*np.exp(1j*np.interp(x=offaxistime[bltimerange],xp=storetime,fp=phvisdatayy))
                elif (1):#abs interpolation instead of real imag for magnitude, and re im for phase
                    print('doing abs interp reimphase')
                    avisdataxx=np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.abs(visdataxx))
                    avisdataxy=np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.abs(visdataxy))
                    avisdatayx=np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.abs(visdatayx))
                    avisdatayy=np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.abs(visdatayy))
                    reimvisdataxx=np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.real(visdataxx)/np.abs(visdataxx))+1j*np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.imag(visdataxx)/np.abs(visdataxx))
                    reimvisdataxy=np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.real(visdataxy)/np.abs(visdataxy))+1j*np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.imag(visdataxy)/np.abs(visdataxy))
                    reimvisdatayx=np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.real(visdatayx)/np.abs(visdatayx))+1j*np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.imag(visdatayx)/np.abs(visdatayx))
                    reimvisdatayy=np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.real(visdatayy)/np.abs(visdatayy))+1j*np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.imag(visdatayy)/np.abs(visdatayy))
                    visdataxx=avisdataxx*reimvisdataxx
                    visdataxy=avisdataxy*reimvisdataxy
                    visdatayx=avisdatayx*reimvisdatayx
                    visdatayy=avisdatayy*reimvisdatayy
                elif (1):#abs interpolation instead of real imag
                    print('doing abs interp')
                    visdataxx=np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.abs(visdataxx))*np.exp(1j*np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.unwrap(np.angle(visdataxx))))
                    visdataxy=np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.abs(visdataxy))*np.exp(1j*np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.unwrap(np.angle(visdataxy))))
                    visdatayx=np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.abs(visdatayx))*np.exp(1j*np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.unwrap(np.angle(visdatayx))))
                    visdatayy=np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.abs(visdatayy))*np.exp(1j*np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.unwrap(np.angle(visdatayy))))
                else:
                    visdataxx=np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.real(visdataxx))+1j*np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.imag(visdataxx))
                    visdataxy=np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.real(visdataxy))+1j*np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.imag(visdataxy))
                    visdatayx=np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.real(visdatayx))+1j*np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.imag(visdatayx))
                    visdatayy=np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.real(visdatayy))+1j*np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.imag(visdatayy))
                if (doconj):#conjugate transpose
                    Gxgainlist.append(np.conj(visdataxx))
                    Dxgainlist.append(-np.conj(visdatayx))
                    Dygainlist.append(-np.conj(visdataxy))
                    Gygainlist.append(np.conj(visdatayy))
                else:
                    Gxgainlist.append(visdataxx)
                    Dxgainlist.append(-visdataxy)
                    Dygainlist.append(-visdatayx)
                    Gygainlist.append(visdatayy)
                invonaxisXXYY=np.array([[visdatayy,-visdataxy],[-visdatayx,visdataxx]],dtype='complex').transpose(2,0,1)/(visdataxx*visdatayy-visdatayx*visdataxy)[:,np.newaxis,np.newaxis];
                
                if (self.onaxisnormalise):
                    if (doconj):
                        dde=np.conj(dodot([invonaxisXXYY[:,:,:],XXYY[:,:,:]])).transpose(0,2,1)
                    else:
                        dde=dodot([XXYY[:,:,:],invonaxisXXYY[:,:,:]])
                else:
                    if (doconj):#test
                        dde=np.conj(XXYY[:,:,:]).transpose(0,2,1)
                    else:
                        dde=XXYY[:,:,:]

                weight=np.mean(np.abs(visdataxx)**2+np.abs(visdatayy)**2)
                aGx[bltimerange]+=dde[:,0,0]*weight
                aGxDx[bltimerange]+=dde[:,0,1]*weight
                aGyDy[bltimerange]+=dde[:,1,0]*weight
                aGy[bltimerange]+=dde[:,1,1]*weight
                acount[bltimerange]+=weight
            else:#do calculation per frequency channel and average afterwards...
                dde=np.zeros([blntime,2,2],dtype='complex')
                for ich in changrange:
                    visdataxx=np.conj(h5.vis[bltimerange,ich,cpindices[0]]).reshape(-1)
                    visdataxy=np.conj(h5.vis[bltimerange,ich,cpindices[1]]).reshape(-1)
                    visdatayx=np.conj(h5.vis[bltimerange,ich,cpindices[2]]).reshape(-1)
                    visdatayy=np.conj(h5.vis[bltimerange,ich,cpindices[3]]).reshape(-1)
                    XXYY=np.array([[visdataxx,visdataxy],[visdatayx,visdatayy]],dtype='complex').transpose(2,0,1)
                    onaxntime=len(storetime)
                    visdataxx=np.conj(storedata[iant][jant][:,ich,0]).reshape(-1)
                    visdataxy=np.conj(storedata[iant][jant][:,ich,1]).reshape(-1)
                    visdatayx=np.conj(storedata[iant][jant][:,ich,2]).reshape(-1)
                    visdatayy=np.conj(storedata[iant][jant][:,ich,3]).reshape(-1)
                    visdataxx=np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.real(visdataxx))+1j*np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.imag(visdataxx))
                    visdataxy=np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.real(visdataxy))+1j*np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.imag(visdataxy))
                    visdatayx=np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.real(visdatayx))+1j*np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.imag(visdatayx))
                    visdatayy=np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.real(visdatayy))+1j*np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.imag(visdatayy))
                    invonaxisXXYY=np.array([[visdatayy,-visdataxy],[-visdatayx,visdataxx]],dtype='complex').transpose(2,0,1)/(visdataxx*visdatayy-visdatayx*visdataxy)[:,np.newaxis,np.newaxis];
                    if (doconj):
                        dde+=np.conj(dodot([invonaxisXXYY[:,:,:],XXYY[:,:,:]])).transpose(0,2,1)
                    else:
                        dde+=dodot([XXYY[:,:,:],invonaxisXXYY[:,:,:]])
                dde/=float(len(changrange))
                aGx[bltimerange]+=dde[:,0,0]
                aGxDx[bltimerange]+=dde[:,0,1]
                aGyDy[bltimerange]+=dde[:,1,0]
                aGy[bltimerange]+=dde[:,1,1]
                acount[bltimerange]+=1
                t2=t1
            t3=time.time()
            print(' process: %.1f'%(t3-t2))

        validpts=np.nonzero(acount)[0]   
        vis=[aGx[validpts]/acount[validpts], aGy[validpts]/acount[validpts], -(aGxDx[validpts]/acount[validpts]), -(aGyDy[validpts]/acount[validpts])]
        return vis, storeparang[validpts], storeparangscan[validpts], storetargetx[validpts], storetargety[validpts],Gxgainlist,Gygainlist,Dxgainlist,Dygainlist
    
    #classic holography calculation
    def processoffaxisdataclassic(self,h5,targetx,targety,channel_range,flagmask,trackantennas,scanantenna,storedata, storeparang, storeparangscan, storetargetx, storetargety, storetime, storegain, storebl, storeel, storeaz, channel_start, channel_width):
        if (len(trackantennas)==0):
            target=h5.catalogue.targets[h5.target_indices[0]]#use target rather than tracking antenna, incase there are no tracking antennas

        h5.select(reset='F',channels=channel_range)
        h5.select(reset='T')
        
        #MUST CHECK OUT THIS - EXCLUDE MULTIPlE DUPLICATE POINTS AT/NEAR ORIGIN FOR SUCCESSFUL DFT
        #WHEN INTERPOLATING MUST COMBINE CLUSTER OF POINTS AT ORIGIN INTO SINGLE POINT RATHER ELSE LOOSE SHAPE OF PEAK NEAR ORIGIN
        h5.select(dumps=np.array((np.array((targetx)**2+(targety)**2>=(self.radialscan_sampling)**2,dtype='int') & (1-flagmask)),dtype='bool'));
        #h5.select(dumps=np.array((1-flagmask),dtype='bool'));

         # prepare to write main dict
        corrprod_to_index = dict([(tuple(cp), ind) for cp, ind in zip(np.r_[h5.corr_products,h5.corr_products[::,::-1]], np.r_[range(len(h5.corr_products)),range(len(h5.corr_products))])])
        theindices=h5._time_keep.nonzero()[0]

    #        utc_seconds=h5.timestamps[:]
    #        storeutc=np.concatenate([storeutc,utc_seconds],axis=0)
    #        parang=katp[target.name].parallactic_angle(utc_seconds)
        if (len(trackantennas)==0):
            storeparang=target.parallactic_angle(h5.timestamps[:])
        else:
            storeparang=h5.parangle[:,trackantennas[0]]*np.pi/180.0
    #    storeparangscan=h5.parangle[:,scanantenna]*np.pi/180.0#original
        storeparangscan=storeparang#-parcorangle[theindices]#normal
    #    storeparangscan=storeparang+parcorangle[theindices]#neg - seem to have minor effect
        offaxistime=h5.timestamps[:]
        storetargetx=targetx[theindices]
        storetargety=targety[theindices]

        #direct calculation from visibilities
        #in order REAL yyt0,yxt0,xyt0,xxt0,yyt1,yxt1,xyt1,xxt1,... , IMAG yyt0,yxt0,xyt0,xxt0,yyt1,yxt1,xyt1,xxt1,.....
        ntime=len(theindices)
        vis=[np.zeros(ntime,dtype='complex') for p in self.pols_to_use]
        acount=np.zeros(ntime,dtype='float');
        print('CLASSIC calculation')
        print('using %d time samples and %d channels'%(ntime,channel_width))
        for itrack in trackantennas:#only extract baselines between tracking antennas and scanning antenna
            t1=time.time()
            if (itrack>scanantenna):
                iant=scanantenna;
                jant=itrack;
                doconj=0
            else:
                iant=itrack;
                jant=scanantenna;
                doconj=1
            polprods = [("%s%s" % (self.radialscan_allantenna[iant],p[0].lower()), "%s%s" % (self.radialscan_allantenna[jant],p[1].lower())) for p in self.pols_to_use]
            trackautopolprods = [("%s%s" % (self.radialscan_allantenna[itrack],p[0].lower()), "%s%s" % (self.radialscan_allantenna[itrack],p[1].lower())) for p in self.pols_to_use]
            scanautopolprods = [("%s%s" % (self.radialscan_allantenna[scanantenna],p[0].lower()), "%s%s" % (self.radialscan_allantenna[scanantenna],p[1].lower())) for p in self.pols_to_use]
            sys.stdout.write(self.radialscan_allantenna[scanantenna]+': '+self.radialscan_allantenna[iant]+'-'+self.radialscan_allantenna[jant]);sys.stdout.flush();
            cpindices=[corrprod_to_index.get(p) for p in polprods]
            trackautocpindices=[corrprod_to_index.get(p) for p in trackautopolprods]
            scanautocpindices=[corrprod_to_index.get(p) for p in scanautopolprods]
            if (self.options.maxbaseline!=None):
                blrad=(h5.u[:, cpindices[0]]**2+h5.v[:, cpindices[0]]**2)**0.5#uses the last cp_index
                bltimerange=np.nonzero((blrad<self.options.maxbaseline)*(blrad>self.options.minbaseline))[0]#flags long baselines for resolved sources and short baselines for antenna shadowing
            else:
                bltimerange=np.arange(ntime)
            blntime=len(bltimerange)
            if (blntime==0):
                print(' ntime: 0')
                continue

            changrange=np.arange(channel_start,channel_start+channel_width)#note problem here!!
            crossvisdata=[np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,cpindex],[blntime,channel_width])),axis=1).reshape(-1) for cpindex in cpindices]
            trackautovisdata=[np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,trackautocpindex],[blntime,channel_width])),axis=1).reshape(-1) for trackautocpindex in trackautocpindices]
            scanautovisdata=[np.mean(np.conj(np.reshape(h5.vis[bltimerange,changrange,scanautocpindex],[blntime,channel_width])),axis=1).reshape(-1) for scanautocpindex in scanautocpindices]
            t2=time.time()
            sys.stdout.write(' ntime: %d load: %.1f'%(blntime,t2-t1));sys.stdout.flush();
            onaxntime=len(storetime)            
            visdata=[np.mean(np.conj(np.reshape(storedata[iant][jant][:,changrange,ind],[onaxntime,channel_width])),axis=1).reshape(-1) for ind in range(len(self.pols_to_use))]
            crossonvisdata=[np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.real(visdata[ind]))+1j*np.interp(x=offaxistime[bltimerange],xp=storetime,fp=np.imag(visdata[ind])) for ind in range(len(self.pols_to_use))]
            if (doconj):
                for ipol in range(len(self.pols_to_use)):
                    vis[ipol][bltimerange]+=np.conj(crossvisdata[ipol]/crossonvisdata[ipol])
            else:
                for ipol in range(len(self.pols_to_use)):
                    vis[ipol][bltimerange]+=(crossvisdata[ipol]/crossonvisdata[ipol])

            acount[bltimerange]+=1
            t3=time.time()
            print(' process: %.1f'%(t3-t2))

        validpts=np.nonzero(acount)[0]
        vis=[ivis[validpts]/acount[validpts] for ivis in vis]
        return vis, storeparang[validpts], storeparangscan[validpts], storetargetx[validpts], storetargety[validpts]

    #get raw visibilities in on axis direction
    #future improvement may be to do in arbitrary direction (for scanning antennas) by fitting polynomial and reading off smoothed values in that direction
    def getonaxisrawvis(self,frequencyMHz=None,dMHz=None,antennanames=None):
        channel_ind=self.getchannelindices(frequencyMHz,dMHz)
        channel_start=channel_ind[0]
        channel_width=len(channel_ind)
        
        targetx,targety=self.ll,self.mm
        beamregion=np.array((np.sqrt(targetx**2+targety**2)*180.0/np.pi)<2.0,dtype='bool')#only use data within 2 degrees - TODO should rather be calculated from freq and dish size
        h5.select(reset='F',channels=channel_range)
        h5.select(reset='T')
        h5.select(dumps=np.logical_and(beamregion,np.array((1-flagmask),dtype='bool')));

        wavelength=self.speedoflight/(frequencyMHz*1e6)
        beamradius=0.8*(wavelength/h5.ants[scanantenna].diameter*180/np.pi)#approximate beam radius in degrees out to half power point

         # prepare to write main dict
        corrprod_to_index = dict([(tuple(cp), ind) for cp, ind in zip(np.r_[h5.corr_products,h5.corr_products[::,::-1]], np.r_[range(len(h5.corr_products)),range(len(h5.corr_products))])])
        theindices=h5._time_keep.nonzero()[0]

        offaxistime=h5.timestamps[:]
        #keep all relevant correlation products
        
        ngainintervals=np.ceil((offaxistime[-1]-offaxistime[0])/(gainintervaltime))#linearly interpolates gain, in time.
        if (ngainintervals<2):
            ngainintervals=2
        #direct calculation from visibilities
        #in order REAL yyt0,yxt0,xyt0,xxt0,yyt1,yxt1,xyt1,xxt1,... , IMAG yyt0,yxt0,xyt0,xxt0,yyt1,yxt1,xyt1,xxt1,.....
        ntime=len(theindices)
        beamoffsets=[]
        print('Independent DIRECT calculation')
        print('using %d time samples and %d channels'%(ntime,channel_width))
        for itrack in trackantennas:#only extract baselines between tracking antennas and scanning antenna
            t1=time.time()
            if (itrack>scanantenna):
                iant=scanantenna;
                jant=itrack;
                doconj=0
            else:
                iant=itrack;
                jant=scanantenna;
                doconj=1
            polprods = [("%s%s" % (self.radialscan_allantenna[iant],p[0].lower()), "%s%s" % (self.radialscan_allantenna[jant],p[1].lower())) for p in self.pols_to_use]
            sys.stdout.write(self.radialscan_allantenna[scanantenna]+': '+self.radialscan_allantenna[iant]+'-'+self.radialscan_allantenna[jant]);sys.stdout.flush();
            cpindices=[corrprod_to_index.get(p) for p in polprods]
            if (self.options.maxbaseline!=None):
                blrad=(h5.u[:, cpindices[0]]**2+h5.v[:, cpindices[0]]**2)**0.5#uses the last cp_index
                bltimerange=np.nonzero((blrad<self.options.maxbaseline)*(blrad>self.options.minbaseline))[0]#flags long baselines for resolved sources and short baselines for antenna shadowing
            else:
                bltimerange=np.arange(ntime)
            blntime=len(bltimerange)
            if (blntime==0):
                print(' ntime: 0')
                continue

            changrange=np.arange(channel_start,channel_start+channel_width)
            visdataxx=np.mean(np.abs(np.reshape(h5.vis[bltimerange,changrange,cpindices[0]],[blntime,channel_width])),axis=1).reshape(-1)
            visdatayy=np.mean(np.abs(np.reshape(h5.vis[bltimerange,changrange,cpindices[3]],[blntime,channel_width])),axis=1).reshape(-1)
            t2=time.time()
            sys.stdout.write(' ntime: %d load: %.1f'%(blntime,t2-t1));sys.stdout.flush();

            validpts=bltimerange
            absGx=visdataxx
            absGy=visdatayy
            absI=absGx+absGy
            maxabsGx=np.max(absGx)
            maxabsGy=np.max(absGy)
            maxabsI=np.max(absI)
            if (1):#this works good
                fitptsI=np.nonzero(np.array((np.sqrt(storetargetx[validpts]**2+storetargety[validpts]**2)*180.0/np.pi)<beamradius,dtype='bool'))[0]
        
        self.onaxisdatabase[(frequencyMHz,dMHz,antennanames)]=[visibilities]
        return ll,mm,visibilities,beamoffsets,Gxgainlist,Gygainlist,Dxgainlist,Dygainlist
        
    def parseantennanames(self,scanantennaname=None,trackantennanames=None):
        if (scanantennaname!=None):
            if (scanantennaname not in self.radialscan_allantenna):
                print('Antenna '+scanantennaname+' not found in',self.radialscan_allantenna)
                scanantennaname=None #will cause exception
        else:
            scanantennaname=self.radialscan_scanantenna[0]
        if (trackantennanames==None or len(trackantennanames)==0):
            trackantennanames=tuple([self.radialscan_allantenna[ia] for ia in self.trackantennas])#use current track antennas
        elif (trackantennanames=='all'):
            trackantennanames=[]
            for antname in self.radialscan_allantenna:
                if (antname not in self.radialscan_scanantenna):
                    trackantennanames.append(antname)
            trackantennanames=tuple(np.sort(trackantennanames))#should already be sorted
        else:
            if (type(trackantennanames)==str):
                trackantennanames=[trackantennanames]
            invalid=np.nonzero([trackantenna in self.radialscan_scanantenna or trackantenna not in self.radialscan_allantenna for trackantenna in trackantennanames])[0]
            if (len(invalid)>0):
                print('Error: these antennas are not tracking antennas: ',[trackantennanames[inv] for inv in invalid])
                trackantennanames=[] #will cause exception
            else:
                trackantennanames=tuple(np.sort(trackantennanames))
#        thistrackantennas=np.array([self.radialscan_allantenna.index(trackname) for trackname in trackantennanames],dtype='int');
#        thisscanantenna=self.radialscan_allantenna.index(scanantennaname)
        return scanantennaname,trackantennanames
        
    def processinterferometricpointing(self,cycletime=60,freqMHz=None,dMHz=None,scanantennaname=None,trackantennanames=None):
        scanantennaname,trackantennanames=self.parseantennanames(scanantennaname,trackantennanames)
        thisscanantenna=self.radialscan_allantenna.index(scanantennaname)
        thistrackantennas=np.array([self.radialscan_allantenna.index(trackname) for trackname in trackantennanames],dtype='int');
        channel_ind=self.getchannelindices(freqMHz,dMHz)
        channel_start=channel_ind[0]
        channel_width=len(channel_ind)
        beamoffsets=self.processoffaxisindependentwithgaindrift(self.h5,self.ll,self.mm,self.channel_range,self.flagmask,thistrackantennas,thisscanantenna,channel_start,channel_width,freqMHz,1e10,cycletime)
        return beamoffsets
        
    
    def getvisslice(self,frequencyMHz=None,dMHz=None,scanantennaname=None,trackantennanames=None,ich=0):
        """Returns az el visibility data for slice. Note trackantennanames should be a list or could be a single antenna name, or 'all'. Current selection of trackantennanames used otherwise."""
        if (self.fileext=='.ASC' or self.fileext=='.RIASC'):
            if (self.rawtime is not None):
                if (self.method=='raw'):
                    visibilities=self.visibilities
                    Gxgainlist=[]
                elif (self.method=='abs'):
                    storedata,storetargetx,storetargety,storetime,storegain,storebl=self.extractdatanoh5(0,0,self.radialscan_sampling,self.ll,self.mm,self.flagmask);
                    visibilities,ll,mm,Gxgainlist=self.processoffaxisdatagainrawnoh5abs(self.ll,self.mm,self.flagmask,storedata,storetargetx,storetargety,storetime,storegain,storebl);
                else:
                    storedata,storetargetx,storetargety,storetime,storegain,storebl=self.extractdatanoh5(0,0,self.radialscan_sampling,self.ll,self.mm,self.flagmask);
                    visibilities,ll,mm,Gxgainlist=self.processoffaxisdatagainrawnoh5(self.ll,self.mm,self.flagmask,storedata,storetargetx,storetargety,storetime,storegain,storebl);
                print('CALVIS')
                self.calvis=visibilities
                return self.ll,self.mm,visibilities,[[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]],Gxgainlist,[],[],[]
            return self.ll,self.mm,self.visibilities,[[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]],[],[],[],[]
        elif (self.fileext=='.PAT' or self.fileext=='.MAT' or self.fileext=='.DICT'):
            return self.ll,self.mm,self.visibilities,[[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]],[],[],[],[]
        
        scanantennaname,trackantennanames=self.parseantennanames(scanantennaname,trackantennanames)
        thisscanantenna=self.radialscan_allantenna.index(scanantennaname)
        thistrackantennas=np.array([self.radialscan_allantenna.index(trackname) for trackname in trackantennanames],dtype='int');
        if (thisscanantenna==None or thistrackantennas==[]):
            return 0,0,[0],[[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]] for it in self.trackantennas],[],[],[],[]
                
        if ((frequencyMHz,dMHz,scanantennaname,trackantennanames) in self.database):
            return self.database[(frequencyMHz,dMHz,scanantennaname,trackantennanames)]
        channel_ind=self.getchannelindices(frequencyMHz,dMHz)
        channel_start=channel_ind[0]
        channel_width=len(channel_ind)

        self.douvr=False
        if (len(self.pols_to_use)>1 and (not (self.method[:3]=='raw' or self.method[:3]=='auto'))):
            beamoffsets=self.processoffaxisindependentwithgaindrift(self.h5,self.ll,self.mm,self.channel_range,self.flagmask,thistrackantennas,thisscanantenna,channel_start,channel_width,frequencyMHz,self.gainintervaltime)
        else:
            beamoffsets=[[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]]
            Gxgainlist,Gygainlist,Dxgainlist,Dygainlist=[],[],[],[]
        if (self.method=='auto'):
            Gxgainlist,Gygainlist,Dxgainlist,Dygainlist=[],[],[],[]
            visibilities,storeparang,storeparangscan,ll,mm=self.processoffaxisauto(self.h5,self.ll,self.mm,self.channel_range,self.flagmask,thistrackantennas,thisscanantenna,channel_start,channel_width,ich,frequencyMHz,dMHz,self.method,self.gainintervaltime)
        elif (self.method=='raw'):
            Gxgainlist,Gygainlist,Dxgainlist,Dygainlist=[],[],[],[]
            visibilities,storeparang,storeparangscan,ll,mm=self.processoffaxisraw(self.h5,self.ll,self.mm,self.channel_range,self.flagmask,thistrackantennas,thisscanantenna,channel_start,channel_width,ich,frequencyMHz,dMHz,self.method,self.gainintervaltime)
        elif (self.method=='gainraw'):
            storedata,storeparang,storeparangscan,storetargetx,storetargety,storetime,storegain,storebl,storeel,storeaz,storeu,storev,storeuvr2=self.extractdata(0,0,self.radialscan_sampling,self.ll,self.mm,self.channel_range,self.flagmask,thistrackantennas,thisscanantenna,[channel_ind]);
            visibilities,storeparang,storeparangscan,ll,mm,Gxgainlist,Gygainlist,Dxgainlist,Dygainlist=self.processoffaxisdatagainraw(self.h5,self.ll,self.mm,self.channel_range,self.flagmask,thistrackantennas,thisscanantenna,storedata,storeparang,storeparangscan,storetargetx,storetargety,storetime,storegain,storebl,storeel,storeaz,channel_start,channel_width);
        elif (self.method=='gainrawabs'):
            storedata,storeparang,storeparangscan,storetargetx,storetargety,storetime,storegain,storebl,storeel,storeaz,storeu,storev,storeuvr2=self.extractdata(0,0,self.radialscan_sampling,self.ll,self.mm,self.channel_range,self.flagmask,thistrackantennas,thisscanantenna,[channel_ind]);
            visibilities,storeparang,storeparangscan,ll,mm,Gxgainlist,Gygainlist,Dxgainlist,Dygainlist=self.processoffaxisdatagainrawabs(self.h5,self.ll,self.mm,self.channel_range,self.flagmask,thistrackantennas,thisscanantenna,storedata,storeparang,storeparangscan,storetargetx,storetargety,storetime,storegain,storebl,storeel,storeaz,channel_start,channel_width);
        elif (self.method=='offsetonly'):
            Gxgainlist,Gygainlist,Dxgainlist,Dygainlist=[],[],[],[]
            visibilities,storeparang,storeparangscan,ll,mm=np.array([]),np.array([]),np.array([]),np.array([]),np.array([])
        else:
            storedata,storeparang,storeparangscan,storetargetx,storetargety,storetime,storegain,storebl,storeel,storeaz,storeu,storev,storeuvr2=self.extractdata(0,0,self.radialscan_sampling,self.ll,self.mm,self.channel_range,self.flagmask,thistrackantennas,thisscanantenna,[channel_ind]);
            if (len(self.pols_to_use)==1):
                visibilities,storeparang,storeparangscan,ll,mm=self.processoffaxisdataclassic(self.h5,self.ll,self.mm,self.channel_range,self.flagmask,thistrackantennas,thisscanantenna,storedata,storeparang,storeparangscan,storetargetx,storetargety,storetime,storegain,storebl,storeel,storeaz,channel_start,channel_width);
            else:
                visibilities,storeparang,storeparangscan,ll,mm,Gxgainlist,Gygainlist,Dxgainlist,Dygainlist=self.processoffaxisdatadirect(self.h5,self.ll,self.mm,self.channel_range,self.flagmask,thistrackantennas,thisscanantenna,storedata,storeparang,storeparangscan,storetargetx,storetargety,storetime,storegain,storebl,storeel,storeaz,channel_start,channel_width);
            
        self.database[(frequencyMHz,dMHz,scanantennaname,trackantennanames)]=[ll,mm,np.nan_to_num(visibilities),beamoffsets,Gxgainlist,Gygainlist,Dxgainlist,Dygainlist]
        return ll,mm,np.nan_to_num(visibilities),beamoffsets,Gxgainlist,Gygainlist,Dxgainlist,Dygainlist

    def plotonaxis(self,quant='HH',comp='abs',frequencyMHz=None,dMHz=None,scanantennaname=None,trackantennanames=None,doclf=True,doapply=True):
        iquant=['HH','HV','VH','VV'].index(quant)
        scanantennaname,trackantennanames=self.parseantennanames(scanantennaname,trackantennanames)
        thisscanantenna=self.radialscan_allantenna.index(scanantennaname)
        thistrackantennas=np.array([self.radialscan_allantenna.index(trackname) for trackname in trackantennanames],dtype='int');
        channel_ind=self.getchannelindices(frequencyMHz,dMHz)
        channel_start=channel_ind[0]
        channel_width=len(channel_ind)
        storedata,storeparang,storeparangscan,storetargetx,storetargety,storetime,storegain,storebl,storeel,storeaz,storeu,storev,storeuvr2=self.extractdata(0,0,self.radialscan_sampling,self.ll,self.mm,self.channel_range,self.flagmask,thistrackantennas,thisscanantenna,[channel_ind],douvr=True);
        self.tmpstoredata=storedata
        if (doclf):
            plt.clf()
        timeax=(storetime-self.polc.storetime[0])/60./60.
        for iant in range(len(self.polc.selectedantennas)):
            for jant in range(iant+1,len(self.polc.selectedantennas)):
                if (self.polc!=None):
                    modeldata=self.polc.projectfullpolmodeldata()
                    
                plt.subplot(len(self.polc.selectedantennas)-1,len(self.polc.selectedantennas)-1,iant*(len(self.polc.selectedantennas)-1)+jant)
                if (doapply==False):
                    if (comp=='abs' or comp=='mag'):
                        plt.plot(timeax,np.abs(np.mean(storedata[self.polc.selectedantennas[iant]][self.polc.selectedantennas[jant]][:,channel_start:channel_start+channel_width,iquant],axis=1)))
                        plt.plot(timeax,np.abs(self.polc.storedatamx[iant][jant][:,iquant]),'-')
                        plt.plot(timeax,np.abs(modeldata[iant][jant][:,iquant]))
                    elif (comp=='arg' or comp=='phase'):
                        plt.plot(timeax,np.angle(np.mean(storedata[self.polc.selectedantennas[iant]][self.polc.selectedantennas[jant]][:,channel_start:channel_start+channel_width,iquant],axis=1))*180.0/np.pi)
                        plt.plot(timeax,np.angle(self.polc.storedatamx[iant][jant][:,iquant])*180.0/np.pi)
                        plt.plot(timeax,np.angle(modeldata[iant][jant][:,iquant])*180.0/np.pi)
                    elif (comp=='real'):
                        plt.plot(timeax,np.real(np.mean(storedata[self.polc.selectedantennas[iant]][self.polc.selectedantennas[jant]][:,channel_start:channel_start+channel_width,iquant],axis=1)))
                        plt.plot(timeax,np.real(self.polc.storedatamx[iant][jant][:,iquant]))           
                        plt.plot(timeax,np.real(modeldata[iant][jant][:,iquant]))
                    elif (comp=='imag'):
                        plt.plot(timeax,np.imag(np.mean(storedata[self.polc.selectedantennas[iant]][self.polc.selectedantennas[jant]][:,channel_start:channel_start+channel_width,iquant],axis=1)))
                        plt.plot(timeax,np.imag(self.polc.storedatamx[iant][jant][:,iquant]))
                        plt.plot(timeax,np.imag(modeldata[iant][jant][:,iquant]))
                else:
                    D=storedata[iant][jant]
                    D=np.zeros([len(storetime),2,2],dtype='complex')
                    D[:,0,0]=np.mean(storedata[self.polc.selectedantennas[iant]][self.polc.selectedantennas[jant]][:,channel_start:channel_start+channel_width,0],axis=1)
                    D[:,0,1]=np.mean(storedata[self.polc.selectedantennas[iant]][self.polc.selectedantennas[jant]][:,channel_start:channel_start+channel_width,1],axis=1)
                    D[:,1,0]=np.mean(storedata[self.polc.selectedantennas[iant]][self.polc.selectedantennas[jant]][:,channel_start:channel_start+channel_width,2],axis=1)
                    D[:,1,1]=np.mean(storedata[self.polc.selectedantennas[iant]][self.polc.selectedantennas[jant]][:,channel_start:channel_start+channel_width,3],axis=1)
                    # D=np.conj(D)
                    cD=self.polc.applyij(self.polc.Gx,self.polc.Gy,self.polc.Dx,self.polc.Dy,self.polc.faraday,self.polc.resu,self.polc.resv,self.polc.resp,self.polc.storetime[0],self.polc.storetime[-1],iant,jant,D,storetime,storeu[self.polc.selectedantennas[iant]][self.polc.selectedantennas[jant]],storev[self.polc.selectedantennas[iant]][self.polc.selectedantennas[jant]],storeparang)
                    fcD=np.zeros([len(storetime),4],dtype='complex')
                    fcD[:,0]=cD[:,0,0]
                    fcD[:,1]=cD[:,0,1]
                    fcD[:,2]=cD[:,1,0]
                    fcD[:,3]=cD[:,1,1]
                    mD=np.zeros([len(storetime),2,2],dtype='complex')
                    mD[:,0,0]=modeldata[iant][jant][:,0]
                    mD[:,0,1]=modeldata[iant][jant][:,1]
                    mD[:,1,0]=modeldata[iant][jant][:,2]
                    mD[:,1,1]=modeldata[iant][jant][:,3]
                    # mD=np.conj(mD)
                    cmD=self.polc.applyij(self.polc.Gx,self.polc.Gy,self.polc.Dx,self.polc.Dy,self.polc.faraday,self.polc.resu,self.polc.resv,self.polc.resp,self.polc.storetime[0],self.polc.storetime[-1],iant,jant,mD,storetime,storeu[self.polc.selectedantennas[iant]][self.polc.selectedantennas[jant]],storev[self.polc.selectedantennas[iant]][self.polc.selectedantennas[jant]],storeparang)
                    fcmD=np.zeros([len(storetime),4],dtype='complex')
                    fcmD[:,0]=cmD[:,0,0]
                    fcmD[:,1]=cmD[:,0,1]
                    fcmD[:,2]=cmD[:,1,0]
                    fcmD[:,3]=cmD[:,1,1]
                    
                    if (comp=='abs' or comp=='mag'):
                        plt.plot(timeax,np.abs(fcD[:,iquant]))
                        plt.plot(timeax,np.abs(fcmD[:,iquant]))
                    elif (comp=='arg' or comp=='phase'):
                        plt.plot(timeax,np.angle(fcD[:,iquant])*180.0/np.pi)
                        plt.plot(timeax,np.abs(fcmD[:,iquant])*180.0/np.pi)
                    elif (comp=='real'):
                        plt.plot(timeax,np.real(fcD[:,iquant]))
                        plt.plot(timeax,np.abs(fcmD[:,iquant]))
                    elif (comp=='imag'):
                        plt.plot(timeax,np.imag(fcD[:,iquant]))                
                        plt.plot(timeax,np.abs(fcmD[:,iquant]))
        
        

    def plot(self,plottype='lm',component='pow',doclf=True,linetype='-'):
        """Plots specified aspects of the dataset

        Parameters
        ----------
        plottype : string
            Quantity to plot, one of:
            'lm': lm feed plane coordinates of data samples
            'azel': azimuth versus elevation coordinates of data samples
            'el': elevation versus time
            'az': azimuth versus time
            'wind': windspeed versus time
            'wind_dir': wind direction
            'pressure': air pressure
            'humidity': humidity
            'temp': ambient temperature
            'sun': angle between Sun and target versus time
            'speed': speed of antenna movement versus time
        doclf : boolean
            Clears the figure before plotting, default: True

        Returns
        -------
        Nothing

        """
        if (doclf):
            plt.clf()
        if (plottype=='lm'):
            discarded=list(set(range(len(self.mm)))-set(self.time_range))            
            plt.plot(self.ll[discarded]/D2R,self.mm[discarded]/D2R,'ko',markersize=5,markerfacecolor='w',markeredgecolor='k')
            plt.plot(self.ll[self.time_range]/D2R,self.mm[self.time_range]/D2R,'.k',markersize=2)
            plt.title('Feed plane coordinates')
            plt.xlabel('l [degrees]')
            plt.ylabel('m [degrees]')
        elif (plottype=='azel'):
            discarded=list(set(range(len(self.mm)))-set(self.time_range))            
            plt.plot(self.scanaz[discarded]/D2R,self.scanel[discarded]/D2R,'ko',markersize=5,markerfacecolor='w',markeredgecolor='k')
            plt.plot(self.scanaz[self.time_range]/D2R,self.scanel[self.time_range]/D2R,'.k',markersize=2)
            plt.title('Scanning antenna pointing coordinates')
            plt.xlabel('Azimuth [degrees]')
            plt.xlabel('Elevation [degrees]')            
        elif (plottype=='el'):
            plt.plot(self.rawtime-self.rawtime[0],self.scanel/D2R,linetype)
            if (hasattr(self,'env_time')):
                plt.xlabel('Time [s] since '+self.env_time[1])
            else:
                plt.xlabel('Time [s]')
            plt.ylabel('Elevation [degrees]')
        elif (plottype=='az'):
            plt.plot(self.rawtime-self.rawtime[0],self.scanaz/D2R,linetype)
            if (hasattr(self,'env_time')):
                plt.xlabel('Time [s] since '+self.env_time[1])
            else:
                plt.xlabel('Time [s]')
            plt.ylabel('Azimuth [degrees]')
        elif (plottype=='speed'):
            plt.plot(self.rawtime[:-1]-self.rawtime[0],self.deg_per_min,linetype)
            plt.xlabel('Time [s] since '+self.env_time[1])
            plt.ylabel('Scan speed [deg per min]')            
        elif (plottype=='wind'):
            if (self.h5!=None):
                plt.plot(self.rawtime-self.rawtime[0],self.h5.wind_speed,linetype)
                plt.xlabel('Time [s] since '+self.env_time[1])
                plt.ylabel('Windspeed [meters per seconds]')
        elif (plottype=='wind_dir'):
            if (self.h5!=None):
                plt.plot(self.rawtime-self.rawtime[0],self.h5.wind_direction,linetype)
                plt.xlabel('Time [s] since '+self.env_time[1])
                plt.ylabel('Wind direction [deg]')
        elif (plottype=='humidity'):
            if (self.h5!=None):
                plt.plot(self.rawtime-self.rawtime[0],self.h5.humidity,linetype)
                plt.xlabel('Time [s] since '+self.env_time[1])
                plt.ylabel('Humidity [%%]')
        elif (plottype=='pressure'):
            if (self.h5!=None):
                plt.plot(self.rawtime-self.rawtime[0],self.h5.pressure,linetype)
                plt.xlabel('Time [s] since '+self.env_time[1])
                plt.ylabel('Air pressure [mbar]')
        elif (plottype=='temp'):
            if (self.h5!=None):
                plt.plot(self.rawtime-self.rawtime[0],self.h5.temperature,linetype)
                plt.xlabel('Time [s] since '+self.env_time[1])
                plt.ylabel('Ambient temperature [degrees Celsius]')
        elif (plottype=='sun'):
            plt.plot(self.rawtime-self.rawtime[0],[self.target.separation(katpoint.Target("Sun, special"),katpoint.Timestamp(tm)) for tm in self.rawtime],linetype)
            plt.xlabel('Time [s] since '+self.env_time[1])
            plt.ylabel('Angle to sun [degrees]')
            
    def plottime(self,freqMHz,dMHz,ant1='ant1h',ant2='ant2h',component='pow'):
        quant=np.mean(self.h5.vis[:,self.getchannelindices(freqMHz,dMHz,minchannels=1),self.h5.corr_products.tolist().index([ant1,ant2])],axis=1).reshape(-1)
        if (component=='pow'):
            quant=20*np.log10(np.abs(quant))
            ylabel='Power [db]'
        elif (component=='abs' or component=='mag'):
            quant=np.abs(quant)
            ylabel='Magnitude [counts]'
        elif (component=='real' or component=='re'):
            quant=quant.real
            ylabel='Real [counts]'
        elif (component=='imag' or component=='im'):
            quant=quant.imag
            ylabel='Imaginary [counts]'
        elif (component=='phase' or component=='arg'):
            quant=180.0/np.pi*np.angle(quant)
            ylabel='Phase [degrees]'
        plt.plot(self.rawtime-self.rawtime[0],quant)
        plt.xlabel('Time [s] since '+self.env_time[1])
        plt.ylabel(ylabel)
        
    #note that az, el are really ll,mm ie direction cosines
    def loadPattern(self,filename, az, el, scale=1.0, lookBehind=False):
        """Load EMSS pattern and regrid it onto pixel grid.

        The pixel grid is defined by the az and el vectors.

        Parameters
        ----------
        filename : string
            Name of pat file to load
        az : real array, shape (numPixels)
            Vector of azimuth coordinates, in degrees
        el : real array, shape (numPixels)
            Vector of elevation coordinates, in degrees
        scale : float
            Factor by which to scale radial coordinates of pattern [default=1.0]
        lookBehind : bool
            True if pattern should be turned inside out so that the origin is in
            the opposite direction of the beam center (to look behind the dish)

        Returns
        -------
        E_x : complex array, shape (numPixels, numPixels)
            Voltage response along x (+el) direction, as a function of (az, el)
        E_y : complex array, shape (numPixels, numPixels)
            Voltage response along y (-az) direction, as a function of (az, el)
        gainOffset : float
            Gain offset, in dB (typically gain at beam center)

        """
        # Read file
        lines = file(filename).readlines()
        # Setup regexp to parse one line of pat file
        floatNum = r'([0-9.\-E]+)'
        complexNum = r'\(\s*' + floatNum + r',\s*' + floatNum + r'\)'
        row = re.compile(r'^\s*' + r'\s+'.join([floatNum, floatNum, complexNum, complexNum]) + r'\s*$', \
                         flags=(re.IGNORECASE | re.MULTILINE))
        # Parse file data and convert to floating-point
        data = np.array(re.findall(row, ''.join(lines)), dtype='float64')
        # Find gain expression somewhere in first few lines, if it exists
        gainExp = re.findall(r'Gain = 20 x log_10\(\|E\|\) \+ ' + floatNum, ''.join(lines[:20]))
        if len(gainExp) > 0:
            gainOffset = float(gainExp[0])
        else:
            gainOffset = 0.0

        # Extract variables
        theta, phi = data[:, 0], data[:, 1]
        E_theta, E_phi = data[:, 2] + 1j * data[:, 3], data[:, 4] + 1j * data[:, 5]
        # Invert theta axis to look behind the dish
        if lookBehind:
            theta = 180.0 - theta
        # Scale beam pattern to approximate the pattern at a different frequency
        theta *= scale
        # Prevent angle wrap-around
        valid_theta = (theta <= 180.0)
        theta, phi = theta[valid_theta], phi[valid_theta]
        E_theta, E_phi = E_theta[valid_theta], E_phi[valid_theta]
        # Convert polar coordinates in degrees to normalised rectangular coordinates
        sin_theta, cos_theta = np.sin(theta * np.pi / 180.0), np.cos(theta * np.pi / 180.0)
        cos_theta = 1.0
        sin_phi, cos_phi = np.sin(phi * np.pi / 180.0), np.cos(phi * np.pi / 180.0)
        pol_az, pol_el = sin_theta * sin_phi, sin_theta * cos_phi
        # Convert field strengths from antenna (theta, phi) coords to Stokes (x, y) coords
        E_x_pol =  E_theta * cos_theta * cos_phi - E_phi * sin_phi
        E_y_pol = -E_theta * cos_theta * sin_phi - E_phi * cos_phi

        # The EMSS pattern contains multiple versions of the beam center, where theta=0
        # but phi differs. Replace them with a single averaged version.
        beamCenter = (theta == 0.0)
        E_x_pol[beamCenter] = E_x_pol[beamCenter].mean()
        E_y_pol[beamCenter] = E_y_pol[beamCenter].mean()

        if (el==None):
            # Restrict data to slightly bigger region than specified one, and remove duplicate points
            # Always work in upper half of sphere, as the projection don't allow theta > 90 degrees
            if (az!=None):
                beamRange = (az) / 2.0
                expandedRange = min(1.1 * np.sin(beamRange * np.pi / 180.0), 1.0)
                select = (np.abs(pol_az) <= expandedRange) & (np.abs(pol_el) <= expandedRange) & \
                         (theta > 0.0) & (theta <= 90.0) & (phi < 360.0)
            else:
                select = (theta > 0.0) & (theta <= 90.0) & (phi < 360.0)
                
            select[np.where(beamCenter)[0][0]] = True
            return pol_az[select],pol_el[select],E_x_pol[select],E_y_pol[select]
        
        # Restrict data to slightly bigger region than specified one, and remove duplicate points
        # Always work in upper half of sphere, as the projection don't allow theta > 90 degrees
        beamRange = (az[-1] - az[0]) / 2.0
        expandedRange = min(1.1 * np.sin(beamRange * np.pi / 180.0), 1.0)
        select = (np.abs(pol_az) <= expandedRange) & (np.abs(pol_el) <= expandedRange) & \
                 (theta > 0.0) & (theta <= 90.0) & (phi < 360.0)
        select[np.where(beamCenter)[0][0]] = True
            
        # Set up rectangular grid for image coordinates
        print('Interpolating data onto pixel grid')
        elGrid, azGrid = np.meshgrid(el, az)
        rect = np.sin(np.vstack((azGrid.ravel(), elGrid.ravel())) * np.pi / 180.0)
        # Interpolate spherical coordinates onto rectangular plot
        interp = fitting.Delaunay2DScatterFit(default_val=0.0, jitter=True)
        polar = np.vstack((pol_az[select], pol_el[select]))
        interp.fit(polar, E_x_pol.real[select])
        E_xr = interp(rect).reshape(len(az), len(el))
        interp.fit(polar, E_x_pol.imag[select])
        E_xi = interp(rect).reshape(len(az), len(el))
        interp.fit(polar, E_y_pol.real[select])
        E_yr = interp(rect).reshape(len(az), len(el))
        interp.fit(polar, E_y_pol.imag[select])
        E_yi = interp(rect).reshape(len(az), len(el))
        E_x = E_xr + 1.0j * E_xi
        E_y = E_yr + 1.0j * E_yi

        return E_x, E_y, gainOffset
    

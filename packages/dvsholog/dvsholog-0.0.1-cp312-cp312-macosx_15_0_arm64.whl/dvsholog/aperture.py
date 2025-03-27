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
import astropy.io.fits as pyfits
import array
import scipy
import scipy.spatial
import os,sys,time
from multiprocessing import Process, Queue, cpu_count
import katdal
from matplotlib import path
import pickle
import numbers
import optparse
from .utilities import *

class ApertureMap(object):
    """ ApertureMap object stores a single two dimensional aperture plane map, with settings and results pertaining
        to a single frequency for a single feed of a single dish.
    """
    #specify feedoffset=[offsetx,offsety,offsetz] in mm if known, else it is determined from the data.
    def __init__(self,dataset,scanantennaname=None,trackantennanames=None,dMHz=16,freqMHz=None,blockdiameter=None,blockstrut=None,blockazimuth=None,dishdiameter=None,focallength=None,mapsize=None,gridsize=None,xyzoffsets=None,xmag=None,feedoffset=None,feed='H',dovoronoi=True,voronoimaxweight=None,ndftproc=None,gainadjustment=None,parabolaoffset=[0.0,0.0],parabolaoffsetdev=None,applypointing=None,flatmode='pointingonly',flatregion=None,flipx=None,flipy=None,flipz=None,excluderegions=None,feedtheta=0,feedepsilon=0,feedphi=0,feedcombine=None,copolmap=None,crosspolmap=None,fitampmap=None,dodftgain=False,newweight=None,applyvisgrid=None,applyvisextent=None,domiriad=True):
        """
        Creates an ApertureMap object from the holography dataset.
        
        Parameters
        ----------
        dataset : dvsholog.Dataset object
            Dataset object from which to derive aperture map.
        scanantennaname : string
            Name of antenna for which to create aperture map. If None then the first scanning antenna is used.
        trackantennanames : list of strings
            Names of antennas to use as tracking antennas to create aperture map. If None, all tracking antennas will be used.
        dMHz : float
            Width of frequency range to use for averaging channels together, in MHz.
        freqMHz : float
            Center frequency of aperture map slice, in MHz
        blockdiameter : float
            If not None, override telescopename default blockage diameter, in meters.
        blockstrut : float
            If not None, override telescopename default blockage strut width, in meters. If positive then +, if negative then diagonally orientated
        blockazimuth : float
            Experimental feature.
        dishdiameter : float
            If not None, override telescopename default dish diameter, in meters.
        focallength : float
            If not None, override telescopename default focallength, in meters.
        mapsize : float
            If not None, override telescopename default mapsize, in meters.
            (typically 20-30%% larger than dishdiameter).
        gridsize : int
            If not None, override number of cells in map along one axis.
        xyzoffsets : list of 3 floats
            If not None, override non-intersecting axis offsets of antenna, in meters.
        xmag : float
            If not None, override subreflector magnification factor.
        feedoffset : float of 3 floats
            If not None, applies this feed offset as a phase correction.
        feed : 'H' or 'V'
            Specifies which feed's data to use.
        dovoronoi : bool
            Perform voronoi tesselation to weight datapoints.
        voronoimaxweight : float
            Clip maximum voronoi weights to this value.
        ndftproc : int
            Speficies number of processes to use for Direct Fourier Transform. 
        flatmode: string
            Specifies mode to use for flattening -'pointingonly' or 'flat' or 'feed pointing co cross'
        """
        self.domiriad=domiriad
        self.newweight=newweight
        self.feedtheta=feedtheta
        self.feedepsilon=feedepsilon
        self.feedphi=feedphi
        self.feedcombine=feedcombine
        self.copolmap=copolmap
        self.crosspolmap=crosspolmap
        self.fitampmap=fitampmap
        self.feed=feed
        self.parabolaoffset=parabolaoffset
        self.parabolaoffsetdev=parabolaoffsetdev
        self.flatmode=flatmode
        self.dodftgain=dodftgain
        self.weight=1.0
        if (isinstance(dataset,dict)):
            self.dataset=None
            self.telescopename=dataset['telescopename'] if 'telescopename' in dataset else ''
            self.scanantennaname=dataset['scanantennaname'] if 'scanantennaname' in dataset else ''
            self.trackantennanames=dataset['trackantennanames'] if 'trackantennanames' in dataset else []
            self.filename=dataset['filename'] if 'filename' in dataset else ''
            if 'freqMHz' in dataset:
                self.freqMHz=dataset['freqMHz']
        else:
            self.dataset=dataset
            self.filename=dataset.filename
            self.telescopename=self.dataset.telescopename
            self.scanantennaname,self.trackantennanames=dataset.parseantennanames(scanantennaname,trackantennanames)
            #determine single frequency if not provided
            if (freqMHz==None):
                freqMHz=0
            if (freqMHz<=0):
                if (len(self.dataset.radialscan_centerfreq)==1):
                    self.freqMHz=self.dataset.radialscan_centerfreq[0]/1e6
                else:
                    if (dMHz<0.0):
                        dMHz*=(self.dataset.h5.channel_freqs[1]-self.dataset.h5.channel_freqs[0])/1e6            
                    cenfreqMHz=self.dataset.radialscan_centerfreq/1E6
                    refMHz=1800.0;
                    startMHz=refMHz+np.round(((cenfreqMHz[0])-refMHz)/dMHz)*dMHz#includes all valid channels
                    self.freqMHz=np.arange(startMHz,(cenfreqMHz[-1]-dMHz/2.0),-dMHz)[int(-freqMHz)]#center frequencies to be evaluated
            else:
                self.freqMHz=freqMHz
        self.dMHz=dMHz
            
        self.colmap=matplotlib.colors.ListedColormap(sqrcolmap(),'sqr')
        self.dishoutline=None
        if (self.telescopename.lower()=='kat7'):
            self.blockdiameter=1.2
            self.blockstrut=0
            self.dishdiameter=12.0
            self.focallength=4.56
            self.mapsize=15.0
            self.gridsize=512
            self.xyzoffsets=[0.0,0.325,0.84]
            self.xmag=1.0
            self.parabolaoffsetdev=[0.0,0.0]
            self.flipx=False
            self.flipy=False
            self.flipz=False
        elif (self.telescopename.lower()=='hirax'):
            self.blockdiameter=0
            self.blockstrut=0
            self.dishdiameter=6.0
            self.focallength=1.5
            self.mapsize=8.0
            self.gridsize=512
            self.xyzoffsets=[0.0,0.0,0.0]
            self.xmag=1.0
            self.parabolaoffsetdev=[0.0,0.0]
            self.flipx=False
            self.flipy=False
            self.flipz=False
        elif (self.telescopename.lower()=='xdm'):
            self.blockdiameter=1.5
            self.self.blockstrut=0
            self.dishdiameter=15.0
            self.focallength=7.5
            self.mapsize=20.0
            self.gridsize=512
            self.xyzoffsets=[0.0,0.0,1.44]
            self.xmag=1.0
            self.parabolaoffsetdev=[0.0,0.0]
            self.flipx=False
            self.flipy=False
            self.flipz=False
        elif (self.telescopename.lower()=='mopra'):
            self.blockdiameter=2.8
            self.blockstrut=0
            self.dishdiameter=22.0
            self.focallength=7.7
            self.mapsize=30.0
            self.gridsize=512
            self.xyzoffsets=[0.0,0.0,0.0]
            self.xmag=9.0
            self.parabolaoffsetdev=[0.0,0.0]
            self.flipx=False
            self.flipy=False
            self.flipz=False
        elif (self.telescopename.lower()=='kat7emss'):
            self.blockdiameter=1.2
            self.blockstrut=0
            self.dishdiameter=12.0
            self.focallength=4.56
            self.mapsize=15.0
            self.gridsize=512
            self.xyzoffsets=[0.0,0.0,0.0]
            self.xmag=1.0
            self.parabolaoffsetdev=[0.0,0.0]
            self.flipx=False
            self.flipy=False
            self.flipz=False
        elif (self.telescopename.lower()=='ghana'):
            self.blockdiameter=2.8956
            self.blockstrut=-0.8
            self.dishdiameter=32.072
            self.focallength=10.2792#107.6828#might be 10.2792
            self.mapsize=34.0
            self.gridsize=512
            self.xyzoffsets=[0.0,0.0,-1.829]
            self.xmag=18.15276932440654#Magnification from subtended angles =  10.4758#Magnification from eccentricity=18.15276932440654
            self.parabolaoffsetdev=[0.0,0.0]
            self.flipx=False
            self.flipy=False
            self.flipz=True
            self.designpointingparams=np.array([0.0,0.0,0.0])
            self.designfeedparams=np.array([0.0,0.0,0.8388,0,0,0])
            self.designellipsoidparams=np.array([0.0,0.0,0.5*(10.2792+0.8388),2.100053035044593,2.100053035044593,4.2273,0,0,0])
            self.designmainparams=np.array([0.0,0.0,0.0,10.2792,0.0,0.0,0.0])
            self.designparabolavertex_to_phasecenter_offset=np.array([0.0,0.0])
            self.designsub='hyperboloid'
            # #ghana hyperboloid:
            # A=8.4546/2.
            # C=9.4404/2.
            # xs=sqrt(C**2-A**2)
            # zs=A
            # 1=Z^2/A^2-R^2/(C^2-A^2)
            # R=linspace(-10,10,1000)
            # Z=A*sqrt(1./(C**2-A**2)*R**2+1.)
            # plot(R,Z+0.5*(10.2792+0.8388))
            # plot(R,-Z+0.5*(10.2792+0.8388))
            #eccentricity=E=C/A=1.116599247746789
            #magnification=(E+1)/(E-1)=18.15276932440654
        elif (self.telescopename.lower()=='ska'):
            self.blockdiameter=0.0
            self.blockstrut=0
            self.dishdiameter=15
            self.focallength=5.71768#from Mariet V email 31/10/2018
            self.mapsize=17.0
            self.gridsize=512
            self.xyzoffsets=[0.0,0.0,0.0]
            self.xmag=1.1832#from Mariet V email 31/10/2018#note use xmag=1.0 to determine feed pos errors, but xmag!=0 to determine subreflector errors
            self.parabolaoffsetdev=[0.0,self.dishdiameter/2.0]
            self.flipx=True
            self.flipy=True
            self.flipz=False
        elif (self.telescopename.lower()=='meerkataph'):
            self.blockdiameter=0.0
            self.blockstrut=0
            self.dishdiameter=13.5
            self.focallength=7.425#note this needs to be parabola focallength 5.48617 for getdeviation to work, which differs from effective focallength 7.425 by xmag. Here it is unclear if xmag is 1/xmag; depends on definitions
            self.mapsize=17.0
            self.gridsize=512
            self.xyzoffsets=[0.0,-1.55,-2.4762]
            self.xmag=0.7389#=paraboloidfocallength/effectivefocallength=5.48617/7.425=0.7388781144781146
            self.parabolaoffsetdev=[0.0,self.dishdiameter/2.0]
            self.flipx=True
            self.flipy=True
            self.flipz=False
        elif (self.telescopename.lower()=='meerkat'):
            self.blockdiameter=0.0
            self.blockstrut=0
            self.dishdiameter=13.5
            self.focallength=5.48617#note needs to be 5.48617 for getdeviation to work#note this must be the true focallength of the main reflector, not the effective focal length
            self.mapsize=17.0
            self.gridsize=512
            self.xyzoffsets=[0.0,-1.55,-2.4762]
            self.xmag=1.0/0.7389#1.394#from Adriaan PH email 2/7/2015
            self.parabolaoffsetdev=[0.0,self.dishdiameter/2.0]
            self.flipx=True
            self.flipy=True
            self.flipz=False
            x=np.array([204.05,2295.2,2300.08,4536.37,4540.94,4715.08,5806.53,5748.55,5750.81,5932.42,6850.07,6789.53,6790.99,6973.21,7410.97,7303.12,7303.81,7473.95,6336.84,5981.91,5983.61,6104.98,3671.61,3503.79,3498.96,2.5 ])
            y=np.array([57.2632,617.585,618.892,1218.11,1219.33,1265.99,3190.71,3318.92,3323.12,3427.97,5115.44,5209.79,5214.06,5353.89,7178.17,7303.12,7307.35,7477.49,10127.1,10366.,10368.9,10579.1,13011.5,13066.7,13068.,13528.3])
            z=np.array([2.04676,257.437,258.531,1005.37,1007.39,1086.13,2000.32,2007.82,2010.28,2139.22,3330.7,3337.47,3340.38,3522.01,4850.77,4860.91,4864.13,5093.33,6503.34,6527.17,6530.87,6798.42,8329.05,8339.68,8339.78,8339.78])
            self.dishoutline=np.r_[x,-x[::-1]]/1000.0,np.r_[y,y[::-1]]/1000.0-self.dishdiameter/2.0
        elif (self.telescopename.lower()=='dva1'):
            self.blockdiameter=0.1#kesteven
            self.blockstrut=0
            self.dishdiameter=15.0
            self.focallength=7.2#kesteven 7.2#   5.25?
            self.mapsize=17.0
            self.gridsize=512#kesteven freq 12224# freq 12209
            self.xyzoffsets=[0.0,0.0,0.0]
            self.xmag=9.0#kesteven 9.0
            self.colmap=matplotlib.colors.ListedColormap(dvacolmap(),'sqr')#note override colourmap
            self.parabolaoffsetdev=[0.0,0.0]
            self.flipx=False
            self.flipy=False
            self.flipz=False
        elif (self.telescopename.lower()=='vla'):
            self.blockdiameter=1.2
            self.blockstrut=0
            self.dishdiameter=25.0
            self.focallength=7.5
            self.mapsize=30.0
            self.gridsize=512
            self.xyzoffsets=[0.0,0.0,0.0]
            self.xmag=1.0
            self.parabolaoffsetdev=[0.0,0.0]
            self.flipx=False
            self.flipy=False
            self.flipz=False
        elif (self.telescopename.lower()=='hartrao'):
            self.blockdiameter=1.2
            self.blockstrut=0
            self.dishdiameter=25.9
            self.focallength=10.9728#10.9728*4.886453416
            self.mapsize=30.0
            self.gridsize=512
            self.xyzoffsets=[0.0,0.0,0.0]
            self.xmag=4.886453416#positive for subreflector position errors instead of feed position errors
            self.parabolaoffsetdev=[0.0,0.0]
            self.flipx=False
            self.flipy=True
            self.flipz=True
            self.designpointingparams=np.array([0.0,0.0,0.0])
            self.designfeedparams=np.array([0.0,0.0,5.1816,0,0,0])
            self.designellipsoidparams=np.array([0.0,0.0,0.5*(10.9728+5.1816),2.1747602028047588,2.1747602028047588,1.911783832,0,0,0])
            self.designmainparams=np.array([0.0,0.0,0.0,10.9728,0.0,0.0,0.0])
            self.designparabolavertex_to_phasecenter_offset=np.array([0.0,0.0])            
            self.designsub='hyperboloid'
            # #hartrao hyperboloid:
            # A=1.911783832
            # C=2.8956
            # xs=sqrt(C**2-A**2)
            # 1=Z^2/A^2-R^2/(C^2-A^2)
            # R=linspace(-10,10,1000)
            # Z=A*sqrt(1./(C**2-A**2)*R**2+1.)
            # plot(R,Z+0.5*(10.9728+5.1816))
            # plot(R,-Z+0.5*(10.9728+5.1816))
        elif (self.telescopename.lower()=='vgos'):#from diagram in Mariet VGOS email 16/9/20202
            self.blockdiameter=1.55
            self.blockstrut=0
            self.dishdiameter=13.20
            self.focallength=3.7
            self.mapsize=17.0
            self.gridsize=512
            self.xyzoffsets=[0.0,0.0,0.0]
            self.xmag=1.0
            self.parabolaoffsetdev='vgos focus ring'
            self.flipx=False
            self.flipy=False
            self.flipz=False
        else:
            print('Warning: unknown telescope %s'%self.telescopename)
            
        if (blockdiameter!=None):
            self.blockdiameter=np.float64(blockdiameter)
        if (blockstrut!=None):
            self.blockstrut=blockstrut
        if (dishdiameter!=None):
            self.dishdiameter=np.float64(dishdiameter)
        if (focallength!=None):
            self.focallength=np.float64(focallength)
        if (mapsize!=None):
            self.mapsize=np.float64(mapsize)
        if (gridsize!=None):
            self.gridsize=np.int32(gridsize)
        if (xyzoffsets!=None):
            self.xyzoffsets=np.array(xyzoffsets,dtype='float')
        if (xmag!=None):
            self.xmag=xmag
        if (parabolaoffsetdev!=None):
            self.parabolaoffsetdev=parabolaoffsetdev
        if (flipx is not None):
            self.flipx=flipx
        if (flipy is not None):
            self.flipy=flipy
        if (flipz is not None):
            self.flipz=flipz

        if (self.dataset is None):
            self.gridsize=dataset['apert'].shape[0] 
            if 'mapsize' in dataset:
                self.mapsize=dataset['mapsize']

        self.ndftproc=ndftproc
        self.freq=self.freqMHz*1e6
        self.wavelength=299792458.0/self.freq
        self.unwrapmaskmap,self.unwrapmaskind=self.makeunwrapmask()#note uses mapsize
        x,y=np.meshgrid(np.linspace(-self.mapsize/2.0,self.mapsize/2.0,self.gridsize+1)[:-1],np.linspace(-self.mapsize/2.0,self.mapsize/2.0,self.gridsize+1)[:-1])
        r=np.sqrt(x**2+y**2);
        az=np.arctan2(y,x)*180.0/np.pi
#        self.maskmap=np.array(np.logical_or((r<(self.blockdiameter/2.0)),(r>self.dishdiameter/2.0)),dtype='int')
        if (blockazimuth!=None):
            if (self.feed=='H' or self.feed==0):
                self.maskmap=np.array((r<(self.blockdiameter/2.0)) |  (r>self.dishdiameter/2.0) | ((az<blockazimuth) & (az>-blockazimuth)) | (az>180.0-blockazimuth) | (az<-180.0+blockazimuth),dtype='int')
            else:
                self.maskmap=np.array((r<(self.blockdiameter/2.0)) |  (r>self.dishdiameter/2.0) | ((az>blockazimuth) & (az<180.0-blockazimuth)) | ((az<-blockazimuth) & (az>-180.0+blockazimuth)),dtype='int')
        else:
            self.maskmap=np.array((r<(self.blockdiameter/2.0)) |  (r>self.dishdiameter/2.0) ,dtype='int')
        if (self.blockstrut is not None):
            if (self.blockstrut>0):#+ blockage
                self.maskmap=np.logical_or(self.maskmap,((np.abs(x)<self.blockstrut/2.0) | (np.abs(y)<self.blockstrut/2.0)))
            elif (self.blockstrut<0):#diagonal blockage
                self.maskmap=np.logical_or(self.maskmap,((np.abs(x-y)<-self.blockstrut/2.0) | (np.abs(x+y)<-self.blockstrut/2.0)))            

        if (isinstance(self.fitampmap, (int, float, complex))):#then makes gaussian with edge taper of this value in dB
            x,y=np.meshgrid(np.linspace(-self.mapsize/2.0,self.mapsize/2.0,self.gridsize+1)[:-1],np.linspace(-self.mapsize/2.0,self.mapsize/2.0,self.gridsize+1)[:-1])
            r=np.sqrt(x**2+y**2);
            edge_taper_dB=self.fitampmap
            sigma2=-1.25*((self.dishdiameter)**2)/(np.log(10.)*edge_taper_dB)# from edge_taper_dB=10*np.log10(np.exp(-0.5*((self.dishdiameter/2.)**2)/sigma**2))
            self.fitampmap=(1-self.maskmap)*np.exp(-0.5*(r**2)/sigma2)

        if (flatregion!=None):
            self.flatmaskmap=np.array((x<flatregion[0]) | (x>flatregion[1]) | (y<flatregion[2]) | (y>flatregion[3]) ,dtype='int')
        else:
            self.flatmaskmap=np.array((r>self.dishdiameter/2.0) ,dtype='int')
        if (excluderegions!=None):
            self.flatmaskmap=self.flatmaskmap.astype('bool')
            for region in excluderegions:
                self.flatmaskmap|=np.array((x>region[0]) & (x<region[1]) & (y>region[2]) & (y<region[3]) ,dtype='bool')
            self.flatmaskmap=self.flatmaskmap.astype('int')

        if (self.dataset is None):
            self.apert=dataset['apert']
            self.analyse(feedoffset=feedoffset)
            return
            
            
            
        ll,mm,fullvis,beamoffsets,Gxgainlist,Gygainlist,Dxgainlist,Dygainlist=self.dataset.getvisslice(self.freqMHz,self.dMHz,self.scanantennaname,self.trackantennanames)
        #ll,mm,beamoffsets in radians
        beamoffsetI=beamoffsets[0][0]
        beamoffsetGx=beamoffsets[0][0]
        beamoffsetGy=beamoffsets[0][0]
        if (applypointing=='Gx'):#applies the offset determined for Gx to all polarisation products
            offsets=[beamoffsetGx[0],beamoffsetGx[1]]
        elif (applypointing=='Gy'):#applies the offset determined for Gy to all polarisation products
            offsets=[beamoffsetGy[0],beamoffsetGy[1]]
        elif (applypointing=='I'):#applies the offset determined for I to all polarisation products
            offsets=[beamoffsetI[0],beamoffsetI[1]]
        elif (type(applypointing)==list or type(applypointing)==np.ndarray):
            offsets=np.array(applypointing)*np.pi/180.0
        else:#do nothing
            offsets=[0.0,0.0]
        ll-=offsets[0]
        mm-=offsets[1]

        if (self.feedcombine is not None):
            gx,gy,dx,dy=fullvis[0]+0,fullvis[1]+0,fullvis[2]+0,fullvis[3]+0
            vis=feedcombine[0]*gx+feedcombine[1]*dx+feedcombine[2]*dy+feedcombine[3]*gy
            #normalise beam pattern at origin assuming its an emssbeam pattern
            ind_onaxis=np.nonzero((ll==0.0)*(mm==0.0))[0]#TODO this should be improved but ok for emss beam patterns
            if (len(ind_onaxis)):
                vis/=np.mean(vis[ind_onaxis])
        elif (self.feedtheta!=0):
            gx,gy,dx,dy=fullvis[0]+0,fullvis[1]+0,fullvis[2]+0,fullvis[3]+0
            poldistortion=[[np.exp(1j*self.feedphi)*(np.cos(self.feedepsilon)*np.cos(self.feedtheta)-1j*np.sin(self.feedepsilon)*np.sin(self.feedtheta)),np.exp(1j*self.feedphi)*(np.cos(self.feedepsilon)*np.sin(self.feedtheta)+1j*np.sin(self.feedepsilon)*np.cos(self.feedtheta))],[np.exp(-1j*self.feedphi)*(1j*np.sin(self.feedepsilon)*np.cos(self.feedtheta)-np.cos(self.feedepsilon)*np.sin(self.feedtheta)),np.exp(-1j*self.feedphi)*(1j*np.sin(self.feedepsilon)*np.sin(self.feedtheta)+np.cos(self.feedepsilon)*np.cos(self.feedtheta))]]
            [[Jxx,Jxy],[Jyx,Jyy]]=poldistortion
            if (self.feed=='H' or self.feed==0):
                vis=gx*Jxx+dx*Jyx#self.Gx[ich,:,:]=gx*Jxx+dx*Jyx
            elif (self.feed=='HV'):
                vis=dx*Jxx+gx*Jyx#self.Dx[ich,:,:]=dx*Jxx+gx*Jyx
            elif (self.feed=='VH'):
                vis=dy*Jyy+gy*Jxy#self.Dy[ich,:,:]=dy*Jyy+gy*Jxy
            else: #(self.feed=='V'):
                vis=gy*Jyy+dy*Jxy#self.Gy[ich,:,:]=gy*Jyy+dy*Jxy
        else:
            if (self.feed=='H' or self.feed==0):
                vis=fullvis[0]+0
            elif (self.feed=='HV'):
                vis=fullvis[2]+0
            elif (self.feed=='VH'):
                vis=fullvis[3]+0
            else: #(self.feed=='V'):
                vis=fullvis[1]+0
            
        if (gainadjustment!=None):
            vis*=gainadjustment
            
        # if (len(vis)!=4):
        #     vis=vis[0]
        # else:
        #     vis=0.5*(vis[0]+vis[1])
            #should rather determine suitable rotation based on the on-axis results, and derotate by this angle, ensuring that linear polarisation of target is aligned with rotated feed

        #correct visibilities for offsets in aperture plane
        dl,dm,dn=np.array(self.xyzoffsets)*(np.pi*2.0)/self.wavelength
        phaseadjustment=np.exp(1j*(dl*(ll)+dm*(mm)+dn*np.sqrt(1.0-(ll)**2-(mm)**2) ))
        vis=vis*phaseadjustment

        if (applyvisgrid is not None):
            applyvisgridsize=applyvisgrid.shape[0]
            x,y=np.meshgrid(np.linspace(-applyvisextent/2.0,applyvisextent/2.0,applyvisgridsize+1)[:-1],np.linspace(-applyvisextent/2.0,applyvisextent/2.0,applyvisgridsize+1)[:-1])
            xy=(x.reshape(-1)*np.pi/180.0,y.reshape(-1)*np.pi/180.0)
            adj=scipy.interpolate.griddata(xy, np.real(applyvisgrid.reshape(-1)), (ll,mm), method='linear', fill_value=0.0)+1j*scipy.interpolate.griddata(xy, np.imag(applyvisgrid.reshape(-1)), (ll,mm), method='linear', fill_value=0.0)
            vis=adj
        
        if (dovoronoi):
            self.weight=getweight(ll,mm)
            if (voronoimaxweight!=None):
                idx=np.nonzero(self.weight>voronoimaxweight)[0]
                self.weight[idx]=voronoimaxweight
            
        self.ll=ll
        self.mm=mm
        self.vis=vis
        if self.dodftgain:
            self.makebeam()
        else:
            if (self.ndftproc==None and dogpudft!=None):#by default use GPU if available
                self.apert=dogpudft(ll,mm,vis*self.weight,self.mapsize,self.gridsize,self.wavelength)
                # self.beam=vis
                # for cnt in range(1):
                #     self.apert=dogpudft(ll,mm,self.beam*self.weight,self.mapsize,self.gridsize,self.wavelength)
                #     self.beam=dogpuidft(ll,mm,self.apert,self.mapsize,self.gridsize,self.wavelength)

            elif (self.ndftproc==None or self.ndftproc>0):#otherwise, by default use multiple cores dft 
                if (self.ndftproc==None):
                    self.ndftproc=cpu_count()
                self.apert=domultidft(ll,mm,vis*self.weight,self.mapsize,self.gridsize,self.wavelength,self.ndftproc)
                # self.beam=vis
                # for cnt in range(1):
                #     self.apert=domultidft(ll,mm,self.beam*self.weight,self.mapsize,self.gridsize,self.wavelength,self.ndftproc)
                #     self.beam=domultiidft(ll,mm,self.apert,self.mapsize,self.gridsize,self.wavelength,self.ndftproc)
                
            else:#FFT
                self.lmextent=self.wavelength/self.mapsize*self.gridsize            
                if (0):#grid by supersampling# note there is an error in
                    maxl=max(np.max(np.abs(ll)),np.max(np.abs(mm)))
                    superfactor=16#power of 2
                    enlargefactor=1
                    while (self.lmextent/2.0/superfactor<maxl):
                        superfactor/=2
                        enlargefactor*=2
                    lmargin=np.linspace(-self.lmextent/2.0/superfactor,self.lmextent/2.0/superfactor,self.gridsize*enlargefactor+1)[:-1]
                    gridl,gridm=np.meshgrid(lmargin,lmargin)
                    supergridvis=np.array(mlab.griddata(ll,mm,np.real(vis),np.array(gridl),np.array(gridm),interp='linear')+1j*mlab.griddata(ll,mm,np.imag(vis),np.array(gridl),np.array(gridm),interp='linear'),dtype='complex')                
                    supergridvis=supergridvis.reshape(-1)
                    supergridvis[np.nonzero(np.isfinite(supergridvis)==0)]=0.0;#set any nan to 0
                    supergridvis=supergridvis.reshape([self.gridsize*enlargefactor,self.gridsize*enlargefactor])
                    gridvis=np.zeros([self.gridsize,self.gridsize],dtype='complex')
                    for isuper in range(superfactor*enlargefactor):
                        for jsuper in range(superfactor*enlargefactor):
                            gridvis[(self.gridsize-self.gridsize//superfactor)//2:(self.gridsize+self.gridsize//superfactor)//2,(self.gridsize-self.gridsize//superfactor)//2:(self.gridsize+self.gridsize//superfactor)//2]+=supergridvis[isuper::superfactor*enlargefactor,jsuper::superfactor*enlargefactor]
                else:
                    lmargin=np.linspace(-self.lmextent/2.0,self.lmextent/2.0,self.gridsize+1)[:-1]
                    gridl,gridm=np.meshgrid(lmargin,lmargin)
                    gridvis=np.array(mlab.griddata(ll,mm,np.real(vis),np.array(gridl),np.array(gridm),interp='linear')+1j*mlab.griddata(ll,mm,np.imag(vis),np.array(gridl),np.array(gridm),interp='linear'),dtype='complex')
                    gridvis=gridvis.reshape(-1)
                    gridvis[np.nonzero(np.isfinite(gridvis)==0)]=0.0;#set any nan to 0
                    gridvis=gridvis.reshape([self.gridsize,self.gridsize])                
                self.gridvis=gridvis
                self.apert=np.fft.ifftshift(np.fft.fft2(np.fft.fftshift(gridvis)))
                self.apert=apert[::-1,::-1]
        
            self.analyse(feedoffset=feedoffset)

    def makebeam(self,applypointing=None):
        #applypointing can be None, True, or pointing offset [dx,dy] in radians
        #note to convert nopointingphasegradient in degrees per cell to pointing offset in radians, do (to fix pointing error): 
        #makebeam(applypointing=-dfth.nopointingphasegradient*dfth.gridsize/dfth.mapsize*(dfth.wavelength/(2.0*np.pi))*np.pi/180)
        if (self.newweight is None):
            mask=1.0-self.unwrapmaskmap
            if (self.ndftproc==None and dogpudft!=None):
                m=np.real(dogpuidft(self.ll,self.mm,mask,self.mapsize,self.gridsize,self.wavelength))
                M=np.real(dogpudft(self.ll,self.mm,m,self.mapsize,self.gridsize,self.wavelength))
                WM=np.real(dogpudft(self.ll,self.mm,m*self.weight,self.mapsize,self.gridsize,self.wavelength))
            else:
                if (self.ndftproc==None):
                    self.ndftproc=cpu_count()
                m=np.real(domultiidft(self.ll,self.mm,mask,self.mapsize,self.gridsize,self.wavelength,self.ndftproc))
                M=np.real(domultidft(self.ll,self.mm,m,self.mapsize,self.gridsize,self.wavelength,self.ndftproc))
                WM=np.real(domultidft(self.ll,self.mm,m*self.weight,self.mapsize,self.gridsize,self.wavelength,self.ndftproc))
            #fit expected mas
            WW=1
            Y=mask.reshape(-1)*WW
            X=np.array([WM.reshape(-1),M.reshape(-1)])*WW
            XT=X.transpose()
            XXT=np.dot(X,XT)
            #Y=dot(C,X)
            YXT=np.dot(Y,XT)
            C=np.dot(YXT,np.linalg.pinv(XXT))
            self.newweight=C[0]*self.weight+C[1]
        if (self.ndftproc==None and dogpudft!=None):
            self.apert=dogpudft(self.ll,self.mm,self.vis*self.newweight,self.mapsize,self.gridsize,self.wavelength)
        else:
            if (self.ndftproc==None):
                self.ndftproc=cpu_count()
            self.apert=domultidft(self.ll,self.mm,self.vis*self.newweight,self.mapsize,self.gridsize,self.wavelength,self.ndftproc)
        if (applypointing is None):
            self.analyse()
        elif (applypointing is True):
            self.analyse()
            self.apert=self.ampmap*np.exp(1j*self.nopointingphasemap)
            self.analyse()
        else:
            x,y=np.meshgrid(np.linspace(-self.mapsize/2.0,self.mapsize/2.0,self.gridsize+1)[:-1],np.linspace(-self.mapsize/2.0,self.mapsize/2.0,self.gridsize+1)[:-1])
            wavenumber=2.0*np.pi/self.wavelength
            self.apert=self.applypointing(self.apert,applypointing)
            self.analyse()

    def applypointing(self,apert,applypointing_rad):
        x,y=np.meshgrid(np.linspace(-self.mapsize/2.0,self.mapsize/2.0,self.gridsize+1)[:-1],np.linspace(-self.mapsize/2.0,self.mapsize/2.0,self.gridsize+1)[:-1])
        wavenumber=2.0*np.pi/self.wavelength
        return np.abs(apert)*np.exp(1j*(np.angle(apert)+applypointing_rad[0]*wavenumber*x+applypointing_rad[1]*wavenumber*y))
        
        
    def analyse(self,feedoffset=None):
        self.ampmap=np.abs(self.apert)
        self.phasemap=np.angle(self.apert)
        self.unwrappedphasemap=unwrap(self.ampmap,self.phasemap,self.unwrapmaskmap)
        self.ampmodelmap=ampmodel(self.ampmap,self.blockdiameter,self.dishdiameter,self.mapsize,self.gridsize)
        self.nopointingphasemap,self.nopointingphaseoffset,self.nopointingphasegradient,dud,self.nopointingphaseoffsetstd,self.nopointingphasegradientstd,dud,self.nopointingfuncs=flatphase(self.ampmap if (self.fitampmap is None) else self.fitampmap,self.unwrappedphasemap,self.flatmaskmap,self.blockdiameter,self.dishdiameter,self.mapsize,self.gridsize,self.wavelength,self.focallength,self.xmag,feedoffset,self.parabolaoffset,self.flatmode,self.copolmap,self.crosspolmap)
        self.flatphasemap,self.phaseoffset,self.phasegradient,self.feedoffset,self.phaseoffsetstd,self.phasegradientstd,self.feedoffsetstd,self.funcs=flatphase(self.ampmap if (self.fitampmap is None) else self.fitampmap,self.unwrappedphasemap,self.flatmaskmap,self.blockdiameter,self.dishdiameter,self.mapsize,self.gridsize,self.wavelength,self.focallength,self.xmag,feedoffset,self.parabolaoffset,'flat',domiriad=self.domiriad)
        self.modelmap=self.unwrappedphasemap-self.flatphasemap
        self.nopointingmodelmap=self.unwrappedphasemap-self.nopointingphasemap
        self.nopointingdevmap=self.blank(getdeviation(self.nopointingphasemap,self.mapsize,self.gridsize,self.wavelength,self.focallength,self.parabolaoffsetdev))
        self.devmap=self.blank(getdeviation(self.flatphasemap,self.mapsize,self.gridsize,self.wavelength,self.focallength,self.parabolaoffsetdev))
        self.rms0_mm=self.halfpatherrorms(self.ampmap,self.nopointingphasemap)
        self.rms_mm=self.halfpatherrorms(self.ampmap,self.flatphasemap)
        self.gain(None,1.0)

    def analysefeed(self,feedoffset=None):
        self.ampmap=np.abs(self.apert)
        self.phasemap=np.angle(self.apert)
        self.unwrappedphasemap=unwrap(self.ampmap,self.phasemap,self.unwrapmaskmap)
        self.ampmodelmap=ampmodel(self.ampmap,self.blockdiameter,self.dishdiameter,self.mapsize,self.gridsize)
        self.nopointingphasemap,self.nopointingphaseoffset,self.nopointingphasegradient,dud,self.nopointingphaseoffsetstd,self.nopointingphasegradientstd,dud,self.nopointingfuncs=flatphase(self.ampmap if (self.fitampmap is None) else self.fitampmap,self.unwrappedphasemap,self.flatmaskmap,self.blockdiameter,self.dishdiameter,self.mapsize,self.gridsize,self.wavelength,self.focallength,self.xmag,feedoffset,self.parabolaoffset,self.flatmode,self.copolmap,self.crosspolmap)
        self.flatphasemap,self.phaseoffset,self.phasegradient,self.feedoffset,self.phaseoffsetstd,self.phasegradientstd,self.feedoffsetstd,self.funcs=flatphase(self.ampmap if (self.fitampmap is None) else self.fitampmap,self.unwrappedphasemap,self.flatmaskmap,self.blockdiameter,self.dishdiameter,self.mapsize,self.gridsize,self.wavelength,self.focallength,self.xmag,feedoffset,self.parabolaoffset,'feed')
        self.modelmap=self.unwrappedphasemap-self.flatphasemap
        self.nopointingmodelmap=self.unwrappedphasemap-self.nopointingphasemap
        self.nopointingdevmap=self.blank(getdeviation(self.nopointingphasemap,self.mapsize,self.gridsize,self.wavelength,self.focallength,self.parabolaoffsetdev))
        self.devmap=self.blank(getdeviation(self.flatphasemap,self.mapsize,self.gridsize,self.wavelength,self.focallength,self.parabolaoffsetdev))
        self.rms0_mm=self.halfpatherrorms(self.ampmap,self.nopointingphasemap)
        self.rms_mm=self.halfpatherrorms(self.ampmap,self.flatphasemap)
        self.gain(None,1.0)
        
    def makeunwrapmask(self):
        x,y=np.meshgrid(np.linspace(-self.mapsize/2.0,self.mapsize/2.0,self.gridsize+1)[:-1],np.linspace(-self.mapsize/2.0,self.mapsize/2.0,self.gridsize+1)[:-1])
        r=np.sqrt(x**2+y**2)
        #mask=np.array(np.logical_or((r<self.blockdiameter/2.0),(r>self.dishdiameter/2.0)),dtype='int').reshape(-1);
        mask=np.array((r>self.dishdiameter/2.0),dtype='int')
        mask[0,:]=1;mask[:,0]=1;mask[-1,:]=1;mask[:,-1]=1;#efficient way of preventing evaluations beyond domain limits
        mask=np.array(mask,dtype='int').reshape(-1);#1 means blocked, 0 means unclassified, 2 means classified, 3 means perimeter
        if (self.dishoutline is not None):
            x=x.reshape(-1)
            y=y.reshape(-1)
            mask=mask.reshape(-1)
            testind=np.nonzero(mask)[0]
            path=matplotlib.path.Path(list(zip(np.r_[self.dishoutline[0],self.dishoutline[0][0]],-np.r_[self.dishoutline[1],self.dishoutline[1][0]])))
            isinpoly=np.nonzero(path.contains_points(list(zip(x[testind],y[testind]))))[0]
            mask[testind[isinpoly]]=0
        maskind=np.nonzero(mask==0)[0]
        mask=mask.reshape([self.gridsize,self.gridsize])
        return mask,maskind

    def blank(self,phase,blankval=np.nan):
        vals=phase.reshape(-1)
        invalid=np.nonzero(self.unwrapmaskmap.reshape(-1))[0]
        vals[invalid]=blankval
        phase=vals.reshape([self.gridsize,self.gridsize])
        return phase
    
    #calculate measured and theoretical antenna gain in dB
    #freqscaling=1.0 at observing frequency
    def gain(self,blockdiameter=None,freqscaling=1.0):
        if (freqscaling=='k'):
            Lambda=0.0133
            freqscaling=self.wavelength/Lambda
            print('k-band')
        elif (freqscaling=='q'):
            Lambda=0.007
            freqscaling=self.wavelength/Lambda
            print('q-band')
        else:
            Lambda=self.wavelength
            F1=freqscaling
            
        cellsize=self.mapsize/self.gridsize
        fact=cellsize/Lambda
        if (blockdiameter==None):
            itmp=np.flatnonzero(self.maskmap==0)
        else:
            x,y=np.meshgrid(np.linspace(-self.mapsize/2.0,self.mapsize/2.0,self.gridsize+1)[:-1],np.linspace(-self.mapsize/2.0,self.mapsize/2.0,self.gridsize+1)[:-1])
            x=x.reshape(-1)
            y=y.reshape(-1)
            r=np.sqrt(x**2+y**2)
            itmp=np.nonzero((r<blockdiameter/2.0)+(r>self.dishdiameter/2.0)==0)[0]#note using override here for block diameter, which could=0 deliberately (for Kesteven it must equal blockdiameter)
            
        mtmp=(self.ampmap.reshape(-1)[itmp])*np.exp(1j*freqscaling*self.flatphasemap.reshape(-1)[itmp])#assuming focus and feed adjustments are made
        msum=np.sum(mtmp)
        mssum=np.sum(mtmp*np.conj(mtmp))
        self.gainbest=4.0*np.pi*fact*fact*np.abs(msum*np.conj(msum)/mssum)
        self.gainbest_dB=10.0*np.log10(self.gainbest)
        mtmp=(self.ampmap.reshape(-1)[itmp])*np.exp(1j*freqscaling*self.phasemap.reshape(-1)[itmp])#focus as is, without correcting for feed positioning errors
        msum=np.sum(mtmp)
        mssum=np.sum(mtmp*np.conj(mtmp))
        self.gainmeasured=4.0*np.pi*fact*fact*np.abs(msum*np.conj(msum)/mssum)
        self.gainmeasured_dB=10.0*np.log10(self.gainmeasured)
        mtmp=(self.ampmap.reshape(-1)[itmp])*np.exp(1j*freqscaling*self.modelmap.reshape(-1)[itmp])
        msum=np.sum(mtmp)
        mssum=np.sum(mtmp*np.conj(mtmp))
        self.gainmodel=4.0*np.pi*fact*fact*np.abs(msum*np.conj(msum)/mssum)
        self.gainmodel_dB=10.0*np.log10(self.gainmodel)
        mtmp=(self.ampmap.reshape(-1)[itmp])#effectively have perfect flat phase over aperture
        msum=np.sum(mtmp)
        mssum=np.sum(mtmp*np.conj(mtmp))
        self.gainnopanelerr=4.0*np.pi*fact*fact*np.abs(msum*np.conj(msum)/mssum)
        self.gainnopanelerr_dB=10.0*np.log10(self.gainnopanelerr)
        tsum=len(itmp)
        tssum=len(itmp)
        self.gainuniform=4.0*np.pi*fact*fact*np.abs(tsum*np.conj(tsum)/tssum)
        self.gainuniform_dB=10.0*np.log10(self.gainuniform)
        #self.eff_aperture=self.gainmeasured/self.gainuniform #identical to eff_illumination
        #self.eff_illumination_nopanelerror=self.gainnopanelerr/self.gainuniform #identical to eff_taper
        mtmp=(self.ampmodelmap.reshape(-1)[itmp])
        self.eff_taperampmodel=np.sum(np.abs(mtmp))**2/(len(itmp)*np.sum(np.abs(mtmp)**2))

        #focus as is without correcting for feed positioning errors, but including pointing correction            
        mtmp=(self.ampmap.reshape(-1)[itmp])*np.exp(1j*freqscaling*self.nopointingphasemap.reshape(-1)[itmp])
        self.eff0_spillover=np.sum(np.abs(mtmp)**2)/np.sum(np.abs(self.ampmap.reshape(-1))**2)
        self.eff0_illumination=np.abs(np.sum(mtmp))**2/(len(itmp)*np.sum(np.abs(mtmp)**2))
        self.eff0_taper=np.sum(np.abs(mtmp))**2/(len(itmp)*np.sum(np.abs(mtmp)**2))
        self.eff0_phase=np.abs(np.sum(mtmp))**2/np.sum(np.abs(mtmp))**2
        self.eff0_surface=np.exp(-(4.0*np.pi*(self.rms0_mm/1000.0)/Lambda)**2)

        #originally: gives results assuming focus adjustments are made
        mtmp=(self.ampmap.reshape(-1)[itmp])*np.exp(1j*freqscaling*self.flatphasemap.reshape(-1)[itmp])
        self.eff_spillover=np.sum(np.abs(mtmp)**2)/np.sum(np.abs(self.ampmap.reshape(-1))**2)
        self.eff_illumination=np.abs(np.sum(mtmp))**2/(len(itmp)*np.sum(np.abs(mtmp)**2))
        self.eff_taper=np.sum(np.abs(mtmp))**2/(len(itmp)*np.sum(np.abs(mtmp)**2))
        self.eff_phase=np.abs(np.sum(mtmp))**2/np.sum(np.abs(mtmp))**2
        self.eff_surface=np.exp(-(4.0*np.pi*(self.rms_mm/1000.0)/Lambda)**2)

    def printoffset(self):
        meantrackelev=np.mean(self.dataset.targetel)
        cellsize=self.mapsize/self.gridsize
        
        print('Phase offset %0.2f (%0.2f) [deg]'%(self.phaseoffset,self.phaseoffsetstd))
        print('Phase gradient x %0.2f (%0.2f) [deg/cell]'%(self.phasegradient[0],self.phasegradientstd[0]))
        print('Phase gradient y %0.2f (%0.2f) [deg/cell]'%(self.phasegradient[1],self.phasegradientstd[1]))
        print('Feed offset x %0.2f (%0.2f) [mm]'%(self.feedoffset[0],self.feedoffsetstd[0]))
        print('Feed offset y %0.2f (%0.2f) [mm]'%(self.feedoffset[1],self.feedoffsetstd[1]))
        print('Feed offset z %0.2f (%0.2f) [mm]'%(self.feedoffset[2],self.feedoffsetstd[2]))
    
        #Convert offsets to direction cosines
        PLM = -(self.wavelength*self.phasegradient/360.0)/cellsize
        FLM = -(0.001*self.feedoffset/self.focallength)*0.85
        #Convert to (Az,El) offsets in arcmin
        PAZ = -np.arcsin(PLM[0]/np.cos(meantrackelev))*180.0/np.pi*60.0
        PEL =  np.arcsin(PLM[1])*180.0/np.pi*60.0
        FAZ = -np.arcsin(FLM[0]/np.cos(meantrackelev))*180.0/np.pi*60.0
        FEL =  np.arcsin(FLM[1])*180.0/np.pi*60.0
        print('Equivalent pointing offsets:')
        print('Dish component in Az %0.2f arcmin'%(PAZ))
        print('Dish component in El %0.2f arcmin'%(PEL))
        print('Feed component in Az %0.2f arcmin'%(FAZ))
        print('Feed component in El %0.2f arcmin'%(FEL))
        print('Source component in Az %0.2f arcmin'%(PAZ+FAZ))
        print('Source component in El %0.2f arcmin'%(PEL+FEL))
        
    def printgain(self):
        print('Measured gain: %.2f dB'%(self.gainmeasured_dB))
        print('Predicted gain after focus adjustments: %.2f dB'%(self.gainbest_dB))
        print('Theoretical gain with uniform illumination: %.2f dB'%(self.gainuniform_dB))
        print('Gain with no phase errors: %.2f dB'%(self.gainnopanelerr_dB))
        print('Gain with modelled phase errors: %.2f dB'%(self.gainmodel_dB))
        print('Illumination efficiency: %f'%(self.eff0_illumination))
        print('Taper efficiency: %.3f'%(self.eff0_taper))
        print('Phase efficiency: %.3f'%(self.eff0_phase))
        print('Spillover efficiency: %.3f'%(self.eff0_spillover))
        print('Surface-error efficiency: %.3f'%(self.eff0_surface))
        
    def halfpatherrorms(self,amp,phase):
        itmp=np.flatnonzero(self.maskmap==0)
        ampm=(amp.reshape(-1))[itmp]
        phasem=(phase.reshape(-1))[itmp]*self.wavelength/(4.0*np.pi)
        WT=np.sum(ampm)
        MEAN=np.sum(ampm*phasem)/WT
        RMS=np.sqrt(np.sum(ampm*phasem**2)/WT-MEAN**2)
        return 1000.0*RMS#,1000.0*MEAN#in mm
                
    def plottri(self,flareangle,angleoffset,radius0,radius1,originy,ncols):
        for ip in range(ncols): 
            #bottom edge        
            plt.plot([radius0*np.sin((flareangle/2.0+angleoffset)*np.pi/180.0),radius0*np.sin((-flareangle/2.0+angleoffset)*np.pi/180.0)],[originy+radius0*np.cos((flareangle/2.0+angleoffset)*np.pi/180.0),originy+radius0*np.cos((-flareangle/2.0+angleoffset)*np.pi/180.0)],'k--')
            #top edge
            if (0):
                plt.plot([radius1*np.sin((flareangle/2.0+angleoffset)*np.pi/180.0),radius1*np.sin((-flareangle/2.0+angleoffset)*np.pi/180.0)],[originy+radius1*np.cos((flareangle/2.0+angleoffset)*np.pi/180.0),originy+radius1*np.cos((-flareangle/2.0+angleoffset)*np.pi/180.0)],'k--')
            #left edge
            # if (ip==0):
            #     plt.plot([radius0*np.sin((-flareangle/2.0+angleoffset)*np.pi/180.0),radius1*np.sin((-flareangle/2.0+angleoffset)*np.pi/180.0)],[originy+radius0*np.cos((-flareangle/2.0+angleoffset)*np.pi/180.0),originy+radius1*np.cos((-flareangle/2.0+angleoffset)*np.pi/180.0)],'k--')
            #right edge
            if (ip<ncols-1):
                plt.plot([radius0*np.sin((flareangle/2.0+angleoffset)*np.pi/180.0),radius1*np.sin((flareangle/2.0+angleoffset)*np.pi/180.0)],[originy+radius0*np.cos((flareangle/2.0+angleoffset)*np.pi/180.0),originy+radius1*np.cos((flareangle/2.0+angleoffset)*np.pi/180.0)],'k--')
            angleoffset+=flareangle
        
    def plotmeerkatedges(self):
        self.plottri(30,-60,0.212,2.380,-13.5/2,5)
        self.plottri(30,-60,2.380,4.700,-13.5/2,5)
        self.plottri(30,-60,4.700,6.640,-13.5/2,5)
        self.plottri(15,-45-7.5,6.640,8.560,-13.5/2,8)
        self.plottri(15,-45,8.560,10.330,-13.5/2,7)
        self.plottri(15,-30-7.5,10.330,11.970,-13.5/2,6)
        self.plottri(15,-15-7.5,11.970,13.500,-13.5/2,4)
        plt.plot(self.dishoutline[0],self.dishoutline[1],'k--')
        #self.plottri(15,-15-7.5,11.970,13.530,-13.5/2,4)


    def plot_hartrao_rings(self,rad,start,end,number):
        [r,theta] = np.meshgrid(rad,np.linspace(start,end,num=number))
        x = r*np.cos(theta)
        y = r*np.sin(theta)    
        plt.plot(x,y,'k-')  
    
    def plot_hartrao_lines(self,rad_out,rad_in,start,end,number):
        [r,theta] = np.meshgrid(rad_out,np.linspace(start,end,num=number))
        x_out = r*np.cos(theta)
        y_out = r*np.sin(theta)
        [r,theta] = np.meshgrid(rad_in,np.linspace(start,end,num=number))
        x_in = r*np.cos(theta)
        y_in = r*np.sin(theta)
        for i in range(1, np.size(x_in)):
            plt.plot([x_in[i], x_out[i]],[y_in[i], y_out[i]],'k-')
        
    def plothartraoedges(self):
        hartrao_rings_rad = np.array([  0.58863636,   1.86401515,   3.82613636,   6.08257576, 7.84848485,   9.2219697 ,  10.59545455,  11.77272727,  12.95      ]) #meters
        rnd = 2*np.pi
        ## Radial rings
        for i in range(0, 2): # Panel ring 0-1
            self.plot_hartrao_rings(hartrao_rings_rad[i],-rnd/48,rnd-rnd/48,13)
        for i in range(2, 4): # Panel rings 2-3
            self.plot_hartrao_rings(hartrao_rings_rad[i],-rnd/48,rnd-rnd/48,25)
        for i in range(4, 9): # Panel rings 4-8
            self.plot_hartrao_rings(hartrao_rings_rad[i],0,rnd,49)
    
        ## Radial lines      
        self.plot_hartrao_lines(hartrao_rings_rad[8],hartrao_rings_rad[0],-rnd/48,rnd-rnd/48,13) # radial lines from inner diameter
        self.plot_hartrao_lines(hartrao_rings_rad[8],hartrao_rings_rad[2],rnd/2/24,rnd+rnd/2/24,13) # radial lines from thick rings 
        self.plot_hartrao_lines(hartrao_rings_rad[8],hartrao_rings_rad[4],0,rnd,25) # radial lines for outer four rings
        
    def plot_ghana_rings(self,rad,start,end,number):
        [r,theta] = np.meshgrid(rad,np.linspace(start,end,num=number))
        x = r*np.cos(theta)
        y = r*np.sin(theta)
        plt.plot(x,y,'k-')

    def plot_ghana_lines(self,rad_out,rad_in,start,end,number):
        [r,theta] = np.meshgrid(rad_out,np.linspace(start,end,num=number))
        x_out = r*np.cos(theta)
        y_out = r*np.sin(theta)
        [r,theta] = np.meshgrid(rad_in,np.linspace(start,end,num=number))
        x_in = r*np.cos(theta)
        y_in = r*np.sin(theta)
        for i in range(1, np.size(x_in)):
            plt.plot([x_in[i], x_out[i]],[y_in[i], y_out[i]],'k-')

    def plotghanaedges(self):
        rings_rad_inches = np.array([66, 168, 267, 363, 456, 545, 631.5]) #inches
        rings_rad = rings_rad_inches*0.0254 #meters
        rnd = 2*np.pi

        ## Radial rings
        for i in range(0, 2): # Panel ring 0-1
            self.plot_ghana_rings(rings_rad[i],-rnd/24,rnd-rnd/24,13)
        for i in range(2, 7): # Panel rings 2-6
            self.plot_ghana_rings(rings_rad[i],0,rnd,49)

        ## Radial lines
        self.plot_ghana_lines(rings_rad[6],rings_rad[0],0,rnd,25) # radial lines from inner diameter
        self.plot_ghana_lines(rings_rad[6],rings_rad[2],-rnd/48,rnd-rnd/48,25) # radial lines for outer four rings

    @staticmethod
    def getSKApanels():
        return [[[-1.678369,-1.500006,-601.24707,-1249.915405,-1898.359863,-2496.945801,-1897.96228,-1249.111328,-600.819641],[14306.330078,16151.06543,15930.912109,15677.524414,15409.22168,15146.898438,14965.592773,14754.52832,14528.626953]],
                [[-1.500044,-1.500014,-601.560852,-1250.581055,-1898.159546,-2499.275391,-1898.13501,-1249.106445,-600.662903],[12329.03418,14302.657227,14067.367188,13797.832031,13513.100586,13234.568359,13037.834961,12810.308594,12567.431641]],
                [[-2498.307861,-2497.855225,-1899.219971,-1250.450684,-601.52948,-2.996297,-602.042053,-1250.685669,-1899.927979],[15145.12207,13237.616211,13515.046875,13800.21582,14069.700195,14304.569336,14526.767578,14752.817383,14963.96875]],
                [[-2501.383545,-2501.401123,-3100.985107,-3749.839844,-4399.451172,-4996.784668,-4485.147461,-3750.637939,-3102.214111],[13237.895508,15144.880859,14870.69043,14557.432617,14226.87207,13906.557617,13788.132813,13600.609375,13418.368164]],
                [[-2498.387695,-2497.004883,-1901.647705,-1253.055908,-603.65625,-2.953539,-604.003418,-1250.549561,-1902.11792],[13231.975586,11188.663086,11483.039063,11787.243164,12075.250977,12327.167969,12566.249023,12808.447266,13036.789063]],
                [[-1.499898,-1.5,-602.132019,-1251.582275,-1900.432861,-2500.919434,-1900.335449,-1251.362305,-610.057068],[10207.599609,12325.25293,12073.389648,11785.499023,11481.091797,11183.539063,10971.273438,10726.210938,10467.808594]],
                [[-2506.804688,-2501.42041,-2501.381348,-2501.412354,-2501.419189,-3100.707275,-3751.32373,-4400.758301,-5001.555664,-4402.587891,-3753.625977,-3105.580811],[11185.550781,11690.727539,12228.746094,12755.945313,13233.236328,12941.629883,12608.140625,12257.545898,11916.649414,11763.532227,11581.499023,11383.207031]],
                [[-4998.248047,-4997.959961,-4399.335938,-3750.402832,-3102.126709,-2505.279053,-3022.247559,-3665.049561,-4314.696777],[13904.646484,11921.125977,12260.759766,12611.068359,12943.24707,13234.088867,13392.357422,13575.169922,13744.094727]],
                [[-5001.275391,-5001.275391,-5600.658203,-6249.772461,-6899.95459,-7498.126465,-6966.730469,-6251.281738,-5603.255859],[11920.755859,13903.946289,13569.68457,13188.529297,12787.222656,12400.110352,12317.162109,12189.09375,12055.8125]],
                [[-2498.385742,-2498.385986,-1888.698364,-1250.764404,-601.451172,-3.006151,-601.621704,-1250.767212,-1901.016968],[11180.121094,8982.115234,9304.40918,9627.313477,9936.298828,10205.536133,10461.696289,10723.381836,10968.951172]],
                [[-1.499126,-1.499997,-600.14093,-1249.457397,-1894.110718,-2497.250977,-1898.233643,-1249.528687,-601.074951],[7924.450195,10203.586914,9934.283203,9625.297852,9300.592773,8979.982422,8750.6875,8485.447266,8202.418945]],
                [[-2501.385986,-2501.385986,-2501.397705,-2501.385986,-2503.387695,-3101.323242,-3752.960205,-4401.007813,-4999.532227,-4399.900391,-3750.80249,-3102.444336],[8981.513672,9525.974609,10101.783203,10668.723633,11182.919922,10872.173828,10515.662109,10141.779297,9778.413086,9610.586914,9412.149414,9196.617188]],
                [[-4998.275391,-4998.275391,-4401.979492,-3752.887451,-3104.370605,-2507.672852,-3104.133301,-3752.69458,-4401.404297],[11913.352539,9781.865234,10143.841797,10518.271484,10873.067383,11183.294922,11380.212891,11578.708984,11760.754883]],
                [[-5001.275391,-5001.275391,-5601.016602,-6251.515137,-6899.938965,-7497.05957,-6966.499023,-6250.711914,-5602.553223],[9782.199219,11912.549805,11559.762695,11152.53125,10724.459961,10309.592773,10219.821289,10078.984375,9931.746094]],
                [[-7499.665039,-7500.03418,-6879.10498,-6252.910156,-5604.71875,-5007.579102,-5519.955078,-6166.368652,-6815.675293],[12397.850586,10310.060547,10741.143555,11154.15332,11560.032227,11915.612305,12034.961914,12170.210938,12289.263672]],
                [[-1.499743,-1.499991,-599.660645,-1248.849731,-1897.941895,-2497.377197,-1908.0,-1249.140137,-600.437012],[5430.567871,7920.095215,7628.083984,7292.440918,6936.375,6588.467773,6341.866211,6047.01709,5736.225098]],
                [[-2498.385986,-2498.385986,-1900.193237,-1250.663452,-601.797913,-3.041598,-601.324768,-1250.481079,-1900.626831],[8977.647461,6590.873047,6938.070313,7294.397949,7629.880859,7922.280762,8199.710938,8483.043945,8748.854492]],
                [[-2501.427002,-2501.385986,-3099.352539,-3749.300537,-4398.640625,-4997.611816,-4398.666504,-3749.781006,-3099.962158],[6590.033203,8977.726563,8643.044922,8259.435547,7854.319824,7459.771484,7276.643066,7059.977051,6824.137695]],
                [[-4998.275391,-4998.322754,-4401.029785,-3751.36377,-3102.318115,-2503.279053,-3102.100586,-3750.644775,-4400.553223],[9775.40332,7462.23291,7855.652832,8261.008789,8644.12793,8979.459961,9193.766602,9409.329102,9608.081055]],
                [[-5001.275391,-5001.288574,-5001.322754,-5001.290527,-5004.851563,-5603.230469,-6250.819824,-6890.271484,-7497.429199,-6965.64502,-6249.419922,-5601.551758],[7460.941406,8035.123535,8642.401367,9238.34668,9775.102539,9393.082031,8957.038086,8501.429688,8043.293457,7944.461426,7789.473633,7628.031738]],
                [[-7500.037109,-7500.408203,-6908.663086,-6252.336914,-5603.951172,-5005.542969,-5519.09082,-6165.821289,-6815.191406],[10307.450195,8043.812012,8491.355469,8958.737305,9395.317383,9777.344727,9908.810547,10058.09082,10189.345703]],
                [[-1.499996,-1.500082,-598.7146,-1249.069702,-1898.171753,-2496.881104,-1897.430786,-1248.955078,-598.902649],[2643.990723,5425.793457,5104.248047,4731.775391,4335.467285,3946.314209,3666.413574,3340.990967,2989.953613]],
                [[-2498.385742,-2498.385986,-1900.098267,-1250.254028,-601.319519,-2.97318,-601.35376,-1250.954956,-1900.775513],[6585.864258,3948.671875,4337.555664,4734.335938,5105.992676,5428.265137,5733.549805,6044.817871,6335.73291]],
                [[-2501.386475,-2501.395752,-3100.274658,-3750.371338,-4399.870605,-4997.759277,-4398.589844,-3749.874756,-3099.599609],[3948.341797,6586.145996,6218.992188,5797.062988,5348.820313,4909.647461,4708.319336,4469.477539,4208.270996]],
                [[-4998.274902,-4998.275391,-4400.712891,-3750.579346,-3101.836914,-2503.419434,-3102.055664,-3750.904297,-4401.250977],[7457.149414,4912.5,5351.390137,5800.029297,6221.060547,6587.883789,6821.943359,7057.40918,7274.533203]],
                [[-5001.275391,-5001.233398,-5600.75293,-6249.850586,-6890.032715,-7497.797852,-6965.804688,-6249.606445,-5599.998535],[4910.776367,7457.325684,7040.300781,6561.216309,6057.288574,5546.825684,5438.772949,5270.014648,5093.28125]],
                [[-7500.408691,-7500.790039,-6892.905762,-6251.86377,-5603.419922,-5003.525391,-5602.73291,-6251.584473,-6891.087402],[8040.961426,5547.432617,6058.023438,6562.705078,7041.353516,7458.684082,7625.456543,7787.057129,7926.628906]],
                [[-1.501261,-1.500172,-599.943115,-1249.162354,-1889.546021,-2498.384033,-1898.009888,-1249.788452,-598.731689],[-665.806763,2638.608154,2269.617188,1838.96936,1379.118774,904.735718,574.60199,186.109131,-240.147018]],
                [[-2498.410889,-1891.77063,-1250.698242,-602.105774,-3.045157,-600.817383,-1250.007935,-1899.620239,-2498.385986],[908.698669,1381.33728,1841.637817,2271.901855,2641.276367,2987.515381,3338.072754,3664.039063,3943.619385]],
                [[-2501.385498,-3099.457031,-3748.427002,-4389.366211,-4998.273438,-4398.666992,-3749.781006,-3099.755371,-2501.421143],[3943.294189,3529.338623,3048.040527,2534.980713,2007.532959,1780.406616,1508.774292,1208.746948,906.321228]],
                [[-4998.273926,-4391.431641,-3749.99585,-3101.741943,-2502.894043,-3100.896484,-3749.337891,-4393.575684,-4998.273926],[2011.310913,2536.895996,3050.400879,3531.150635,3945.649902,4205.456055,4465.917969,4703.282715,4906.551758]],
                [[-5001.272949,-5610.411621,-6251.029785,-6883.158203,-7499.649902,-6899.926758,-6250.550781,-5600.579102,-5001.269531],[4906.986816,4429.654297,3890.642822,3319.261963,2722.964111,2584.54126,2411.378662,2213.440186,2008.618042]],
                [[-7501.193848,-6955.20166,-6317.143066,-5613.078613,-5003.86084,-5602.836426,-6251.500977,-6891.128906,-7500.780762],[2725.175537,3255.20166,3836.071289,4430.814941,4908.355957,5090.878418,5267.32959,5419.336426,5544.228027]],
                [[2496.945801,1898.359863,1249.915405,601.24707,1.500006,1.678369,600.819641,1249.111328,1897.96228],[15146.898438,15409.22168,15677.524414,15930.912109,16151.06543,14306.330078,14528.626953,14754.52832,14965.592773]],
                [[2499.275391,1898.159546,1250.581055,601.560852,1.500014,1.500044,600.662903,1249.106445,1898.13501],[13234.568359,13513.100586,13797.832031,14067.367188,14302.657227,12329.03418,12567.431641,12810.308594,13037.834961]],
                [[2.996297,601.52948,1250.450684,1899.219971,2497.855225,2498.307861,1899.927979,1250.685669,602.042053],[14304.569336,14069.700195,13800.21582,13515.046875,13237.616211,15145.12207,14963.96875,14752.817383,14526.767578]],
                [[4996.784668,4399.451172,3749.839844,3100.985107,2501.401123,2501.383545,3102.214111,3750.637939,4485.147461],[13906.557617,14226.87207,14557.432617,14870.69043,15144.880859,13237.895508,13418.368164,13600.609375,13788.132813]],
                [[2.953539,603.65625,1253.055908,1901.647705,2497.004883,2498.387695,1902.11792,1250.549561,604.003418],[12327.167969,12075.250977,11787.243164,11483.039063,11188.663086,13231.975586,13036.789063,12808.447266,12566.249023]],
                [[2500.919434,1900.432861,1251.582275,602.132019,1.5,1.499898,610.057068,1251.362305,1900.335449],[11183.539063,11481.091797,11785.499023,12073.389648,12325.25293,10207.599609,10467.808594,10726.210938,10971.273438]],
                [[5001.555664,4400.758301,3751.32373,3100.707275,2501.419189,2501.412354,2501.381348,2501.42041,2506.804688,3105.580811,3753.625977,4402.587891],[11916.649414,12257.545898,12608.140625,12941.629883,13233.236328,12755.945313,12228.746094,11690.727539,11185.550781,11383.207031,11581.499023,11763.532227]],
                [[2505.279053,3102.126709,3750.402832,4399.335938,4997.959961,4998.248047,4314.696777,3665.049561,3022.247559],[13234.088867,12943.24707,12611.068359,12260.759766,11921.125977,13904.646484,13744.094727,13575.169922,13392.357422]],
                [[7498.126465,6899.95459,6249.772461,5600.658203,5001.275391,5001.275391,5603.255859,6251.281738,6966.730469],[12400.110352,12787.222656,13188.529297,13569.68457,13903.946289,11920.755859,12055.8125,12189.09375,12317.162109]],
                [[3.006151,601.451172,1250.764404,1888.698364,2498.385986,2498.385742,1901.016968,1250.767212,601.621704],[10205.536133,9936.298828,9627.313477,9304.40918,8982.115234,11180.121094,10968.951172,10723.381836,10461.696289]],
                [[2497.250977,1894.110718,1249.457397,600.14093,1.499997,1.499126,601.074951,1249.528687,1898.233643],[8979.982422,9300.592773,9625.297852,9934.283203,10203.586914,7924.450195,8202.418945,8485.447266,8750.6875]],
                [[4999.532227,4401.007813,3752.960205,3101.323242,2503.387695,2501.385986,2501.397705,2501.385986,2501.385986,3102.444336,3750.80249,4399.900391],[9778.413086,10141.779297,10515.662109,10872.173828,11182.919922,10668.723633,10101.783203,9525.974609,8981.513672,9196.617188,9412.149414,9610.586914]],
                [[2507.672852,3104.370605,3752.887451,4401.979492,4998.275391,4998.275391,4401.404297,3752.69458,3104.133301],[11183.294922,10873.067383,10518.271484,10143.841797,9781.865234,11913.352539,11760.754883,11578.708984,11380.212891]],
                [[7497.05957,6899.938965,6251.515137,5601.016602,5001.275391,5001.275391,5602.553223,6250.711914,6966.499023],[10309.592773,10724.459961,11152.53125,11559.762695,11912.549805,9782.199219,9931.746094,10078.984375,10219.821289]],
                [[5007.579102,5604.71875,6252.910156,6879.10498,7500.03418,7499.665039,6815.675293,6166.368652,5519.955078],[11915.612305,11560.032227,11154.15332,10741.143555,10310.060547,12397.850586,12289.263672,12170.210938,12034.961914]],
                [[2497.377197,1897.941895,1248.849731,599.660645,1.499991,1.499743,600.437012,1249.140137,1908.0],[6588.467773,6936.375,7292.440918,7628.083984,7920.095215,5430.567871,5736.225098,6047.01709,6341.866211]],
                [[3.041598,601.797913,1250.663452,1900.193237,2498.385986,2498.385986,1900.626831,1250.481079,601.324768],[7922.280762,7629.880859,7294.397949,6938.070313,6590.873047,8977.647461,8748.854492,8483.043945,8199.710938]],
                [[4997.611816,4398.640625,3749.300537,3099.352539,2501.385986,2501.427002,3099.962158,3749.781006,4398.666504],[7459.771484,7854.319824,8259.435547,8643.044922,8977.726563,6590.033203,6824.137695,7059.977051,7276.643066]],
                [[2503.279053,3102.318115,3751.36377,4401.029785,4998.322754,4998.275391,4400.553223,3750.644775,3102.100586],[8979.459961,8644.12793,8261.008789,7855.652832,7462.23291,9775.40332,9608.081055,9409.329102,9193.766602]],
                [[7497.429199,6890.271484,6250.819824,5603.230469,5004.851563,5001.290527,5001.322754,5001.288574,5001.275391,5601.551758,6249.419922,6965.64502],[8043.293457,8501.429688,8957.038086,9393.082031,9775.102539,9238.34668,8642.401367,8035.123535,7460.941406,7628.031738,7789.473633,7944.461426]],
                [[5005.542969,5603.951172,6252.336914,6908.663086,7500.408203,7500.037109,6815.191406,6165.821289,5519.09082],[9777.344727,9395.317383,8958.737305,8491.355469,8043.812012,10307.450195,10189.345703,10058.09082,9908.810547]],
                [[2496.881104,1898.171753,1249.069702,598.7146,1.500082,1.499996,598.902649,1248.955078,1897.430786],[3946.314209,4335.467285,4731.775391,5104.248047,5425.793457,2643.990723,2989.953613,3340.990967,3666.413574]],
                [[2.97318,601.319519,1250.254028,1900.098267,2498.385986,2498.385742,1900.775513,1250.954956,601.35376],[5428.265137,5105.992676,4734.335938,4337.555664,3948.671875,6585.864258,6335.73291,6044.817871,5733.549805]],
                [[4997.759277,4399.870605,3750.371338,3100.274658,2501.395752,2501.386475,3099.599609,3749.874756,4398.589844],[4909.647461,5348.820313,5797.062988,6218.992188,6586.145996,3948.341797,4208.270996,4469.477539,4708.319336]],
                [[2503.419434,3101.836914,3750.579346,4400.712891,4998.275391,4998.274902,4401.250977,3750.904297,3102.055664],[6587.883789,6221.060547,5800.029297,5351.390137,4912.5,7457.149414,7274.533203,7057.40918,6821.943359]],
                [[7497.797852,6890.032715,6249.850586,5600.75293,5001.233398,5001.275391,5599.998535,6249.606445,6965.804688],[5546.825684,6057.288574,6561.216309,7040.300781,7457.325684,4910.776367,5093.28125,5270.014648,5438.772949]],
                [[5003.525391,5603.419922,6251.86377,6892.905762,7500.790039,7500.408691,6891.087402,6251.584473,5602.73291],[7458.684082,7041.353516,6562.705078,6058.023438,5547.432617,8040.961426,7926.628906,7787.057129,7625.456543]],
                [[2498.384033,1889.546021,1249.162354,599.943115,1.500172,1.501261,598.731689,1249.788452,1898.009888],[904.735718,1379.118774,1838.96936,2269.617188,2638.608154,-665.806763,-240.147018,186.109131,574.60199]],
                [[2498.385986,1899.620239,1250.007935,600.817383,3.045157,602.105774,1250.698242,1891.77063,2498.410889],[3943.619385,3664.039063,3338.072754,2987.515381,2641.276367,2271.901855,1841.637817,1381.33728,908.698669]],
                [[2501.421143,3099.755371,3749.781006,4398.666992,4998.273438,4389.366211,3748.427002,3099.457031,2501.385498],[906.321228,1208.746948,1508.774292,1780.406616,2007.532959,2534.980713,3048.040527,3529.338623,3943.294189]],
                [[4998.273926,4393.575684,3749.337891,3100.896484,2502.894043,3101.741943,3749.99585,4391.431641,4998.273926],[4906.551758,4703.282715,4465.917969,4205.456055,3945.649902,3531.150635,3050.400879,2536.895996,2011.310913]],
                [[5001.269531,5600.579102,6250.550781,6899.926758,7499.649902,6883.158203,6251.029785,5610.411621,5001.272949],[2008.618042,2213.440186,2411.378662,2584.54126,2722.964111,3319.261963,3890.642822,4429.654297,4906.986816]],
                [[7500.780762,6891.128906,6251.500977,5602.836426,5003.86084,5613.078613,6317.143066,6955.20166,7501.193848],[5544.228027,5419.336426,5267.32959,5090.878418,4908.355957,4430.814941,3836.071289,3255.20166,2725.175537]]]

    def plotskaedges(self):
        panels=self.getSKApanels()
        for i in range(len(panels)):
            plt.plot(np.r_[panels[i][0],panels[i][0][0]]/1000.,np.r_[panels[i][1],panels[i][1][0]]/1000-self.dishdiameter/2.-0.54,'k-',lw=0.5)
        
    def plot(self,plottype='dev',diff=None,clim=[None,None],doclf=True,docolorbar=True,plotextras=True):
        drawlimits=False
        drawoverlay=True
        im=None
        incrx=-1 if (self.flipy) else 1#note the transpose is actually plotted, hence flipx changes incry and flipy changed incrx
        incry=-1 if (self.flipx) else 1
        incrz=-1 if (self.flipz) else 1
        if (doclf):
            plt.clf()
        if (plottype=='nopointingdev'):
            if (diff!=None):
                im=plt.imshow(incrz*(self.nopointingdevmap[::incrx,::incry]-diff.nopointingdevmap[::incrx,::incry]),extent=[-self.mapsize/2.0,self.mapsize/2.0,-self.mapsize/2.0,self.mapsize/2.0],vmin=clim[0],vmax=clim[1],cmap=self.colmap,origin='lower')
                if (docolorbar):
                    cb=plt.colorbar()
                    cb.set_label('mm')
                if (self.telescopename.lower()=='xdm'):
                    plt.contour(np.linspace(-self.mapsize/2.0,self.mapsize/2.0,self.gridsize+1)[:-1],np.linspace(-self.mapsize/2.0,self.mapsize/2.0,self.gridsize+1)[:-1],incrz*(self.nopointingdevmap[::incrx,::incry]-diff.nopointingdevmap[::incrx,::incry]),levels=[-4,-3,-2,2,3,4],colors='k')
                else:
                    plt.contour(np.linspace(-self.mapsize/2.0,self.mapsize/2.0,self.gridsize+1)[:-1],np.linspace(-self.mapsize/2.0,self.mapsize/2.0,self.gridsize+1)[:-1],incrz*(self.nopointingdevmap[::incrx,::incry]-diff.nopointingdevmap[::incrx,::incry]),levels=[-4,-3,-2,-1,1,2,3,4],colors='k')
                plt.title('Surface difference deviation %s - %s '%(os.path.basename(self.filename),os.path.basename(diff.dataset.filename)))
            else:
                im=plt.imshow(incrz*self.nopointingdevmap[::incrx,::incry],extent=[-self.mapsize/2.0,self.mapsize/2.0,-self.mapsize/2.0,self.mapsize/2.0],vmin=clim[0],vmax=clim[1],cmap=self.colmap,origin='lower')
                if (docolorbar):
                    cb=plt.colorbar()
                    cb.set_label('mm')
                if (self.telescopename.lower()=='xdm'):
                    plt.contour(np.linspace(-self.mapsize/2.0,self.mapsize/2.0,self.gridsize+1)[:-1],np.linspace(-self.mapsize/2.0,self.mapsize/2.0,self.gridsize+1)[:-1],incrz*self.nopointingdevmap[::incrx,::incry],levels=[-4,-3,-2,2,3,4],colors='k')
                else:
                    plt.contour(np.linspace(-self.mapsize/2.0,self.mapsize/2.0,self.gridsize+1)[:-1],np.linspace(-self.mapsize/2.0,self.mapsize/2.0,self.gridsize+1)[:-1],incrz*self.nopointingdevmap[::incrx,::incry],levels=[-4,-3,-2,-1,1,2,3,4],colors='k')
                plt.title('Surface deviation map for %s'%(os.path.basename(self.filename)))
            plt.xlabel('meters')
            plt.ylabel('meters')
        elif (plottype=='dev'):
            if (diff!=None):
                im=plt.imshow(incrz*(self.devmap[::incrx,::incry]-diff.devmap[::incrx,::incry]),extent=[-self.mapsize/2.0,self.mapsize/2.0,-self.mapsize/2.0,self.mapsize/2.0],vmin=clim[0],vmax=clim[1],cmap=self.colmap,origin='lower')
                if (docolorbar):
                    cb=plt.colorbar()
                    cb.set_label('mm')
                if (self.telescopename.lower()=='xdm'):
                    plt.contour(np.linspace(-self.mapsize/2.0,self.mapsize/2.0,self.gridsize+1)[:-1],np.linspace(-self.mapsize/2.0,self.mapsize/2.0,self.gridsize+1)[:-1],incrz*(self.devmap[::incrx,::incry]-diff.devmap[::incrx,::incry]),levels=[-4,-3,-2,2,3,4],colors='k')
                else:
                    plt.contour(np.linspace(-self.mapsize/2.0,self.mapsize/2.0,self.gridsize+1)[:-1],np.linspace(-self.mapsize/2.0,self.mapsize/2.0,self.gridsize+1)[:-1],incrz*(self.devmap[::incrx,::incry]-diff.devmap[::incrx,::incry]),levels=[-4,-3,-2,-1,1,2,3,4],colors='k')
                plt.title('Surface difference deviation %s - %s '%(os.path.basename(self.filename),os.path.basename(diff.dataset.filename)))
            else:
                im=plt.imshow(incrz*self.devmap[::incrx,::incry],extent=[-self.mapsize/2.0,self.mapsize/2.0,-self.mapsize/2.0,self.mapsize/2.0],vmin=clim[0],vmax=clim[1],cmap=self.colmap,origin='lower')
                if (docolorbar):
                    cb=plt.colorbar()
                    cb.set_label('mm')
                if (self.telescopename.lower()=='xdm'):
                    plt.contour(np.linspace(-self.mapsize/2.0,self.mapsize/2.0,self.gridsize+1)[:-1],np.linspace(-self.mapsize/2.0,self.mapsize/2.0,self.gridsize+1)[:-1],incrz*self.devmap[::incrx,::incry],levels=[-4,-3,-2,2,3,4],colors='k')
                else:
                    plt.contour(np.linspace(-self.mapsize/2.0,self.mapsize/2.0,self.gridsize+1)[:-1],np.linspace(-self.mapsize/2.0,self.mapsize/2.0,self.gridsize+1)[:-1],incrz*self.devmap[::incrx,::incry],levels=[-4,-3,-2,-1,1,2,3,4],colors='k')
                plt.title('Surface deviation map for %s'%(os.path.basename(self.filename)))
            plt.xlabel('meters')
            plt.ylabel('meters')
        elif (plottype=='nopointing'):
            drawlimits=True
            if (diff!=None):
                im=plt.imshow(incrz*(self.nopointingphasemap[::incrx,::incry]-diff.nopointingphasemap[::incrx,::incry])/D2R,extent=[-self.mapsize/2.0,self.mapsize/2.0,-self.mapsize/2.0,self.mapsize/2.0],vmin=clim[0],vmax=clim[1],cmap=self.colmap,origin='lower')
                if (docolorbar):
                    cb=plt.colorbar()
                    cb.set_label('deg')
                plt.title('Phase difference map %s - %s '%(os.path.basename(self.filename),os.path.basename(diff.dataset.filename)))
            else:
                im=plt.imshow(incrz*self.nopointingphasemap[::incrx,::incry]/D2R,extent=[-self.mapsize/2.0,self.mapsize/2.0,-self.mapsize/2.0,self.mapsize/2.0],vmin=clim[0],vmax=clim[1],cmap=self.colmap,origin='lower')
                if (docolorbar):
                    cb=plt.colorbar()
                    cb.set_label('deg')
                plt.title('Phase map for %s'%(os.path.basename(self.filename)))
            plt.xlabel('meters')
            plt.ylabel('meters')
        elif (plottype=='nopointingmm'):
            drawlimits=True
            phasemm=self.nopointingphasemap*self.wavelength/(4.0*np.pi)*1000.0#in mm - half path distance in mm (i.e. div by 4 instead of 2)
            im=plt.imshow(incrz*phasemm[::incrx,::incry],extent=[-self.mapsize/2.0,self.mapsize/2.0,-self.mapsize/2.0,self.mapsize/2.0],vmin=clim[0],vmax=clim[1],cmap=self.colmap,origin='lower')
            if (docolorbar):
                cb=plt.colorbar()
                cb.set_label('mm')
            plt.title('Phase map for %s'%(os.path.basename(self.filename)))
            plt.xlabel('meters')
            plt.ylabel('meters')
        elif (plottype=='phase'):
            drawlimits=True
            if (diff!=None):
                im=plt.imshow(incrz*(self.phasemap[::incrx,::incry]-diff.phasemap[::incrx,::incry])/D2R,extent=[-self.mapsize/2.0,self.mapsize/2.0,-self.mapsize/2.0,self.mapsize/2.0],vmin=clim[0],vmax=clim[1],cmap=self.colmap,origin='lower')
                if (docolorbar):
                    cb=plt.colorbar()
                    cb.set_label('deg')
                plt.title('Phase difference map %s - %s '%(os.path.basename(self.filename),os.path.basename(diff.dataset.filename)))
            else:
                im=plt.imshow(incrz*self.phasemap[::incrx,::incry]/D2R,extent=[-self.mapsize/2.0,self.mapsize/2.0,-self.mapsize/2.0,self.mapsize/2.0],vmin=clim[0],vmax=clim[1],cmap=self.colmap,origin='lower')
                if (docolorbar):
                    cb=plt.colorbar()
                    cb.set_label('deg')
                plt.title('Phase map for %s'%(os.path.basename(self.filename)))
            plt.xlabel('meters')
            plt.ylabel('meters')
        elif (plottype=='phasemm'):
            drawlimits=True
            phasemm=incrz*self.flatphasemap*self.wavelength/(4.0*np.pi)*1000.0#in mm - half path distance in mm (i.e. div by 4 instead of 2)
            im=plt.imshow(phasemm[::incrx,::incry],extent=[-self.mapsize/2.0,self.mapsize/2.0,-self.mapsize/2.0,self.mapsize/2.0],vmin=clim[0],vmax=clim[1],cmap=self.colmap,origin='lower')
            if (docolorbar):
                cb=plt.colorbar()
                cb.set_label('mm')
            plt.title('Phase map for %s'%(os.path.basename(self.filename)))
            plt.xlabel('meters')
            plt.ylabel('meters')
        elif (plottype=='unwrap'):
            drawlimits=True
            if (diff!=None):
                im=plt.imshow(incrz*(self.unwrappedphasemap[::incrx,::incry]-diff.unwrappedphasemap[::incrx,::incry])/D2R,extent=[-self.mapsize/2.0,self.mapsize/2.0,-self.mapsize/2.0,self.mapsize/2.0],vmin=clim[0],vmax=clim[1],cmap=self.colmap,origin='lower')
                if (docolorbar):
                    cb=plt.colorbar()
                    cb.set_label('deg')
                plt.title('Unwrapped difference phase %s - %s '%(os.path.basename(self.filename),os.path.basename(diff.dataset.filename)))
            else:
                im=plt.imshow(incrz*self.unwrappedphasemap[::incrx,::incry]/D2R,extent=[-self.mapsize/2.0,self.mapsize/2.0,-self.mapsize/2.0,self.mapsize/2.0],vmin=clim[0],vmax=clim[1],cmap=self.colmap,origin='lower')
                if (docolorbar):
                    cb=plt.colorbar()
                    cb.set_label('deg')
                plt.title('Unwrapped phase map for %s'%(os.path.basename(self.filename)))
            plt.xlabel('meters')
            plt.ylabel('meters')
        elif (plottype=='unwrapmm'):
            unwrapmm=incrz*self.flatphasemap*self.wavelength/(4.0*np.pi)*1000.0#in mm - half path distance in mm (i.e. div by 4 instead of 2)
            drawlimits=True
            im=plt.imshow(unwrapmm[::incrx,::incry],extent=[-self.mapsize/2.0,self.mapsize/2.0,-self.mapsize/2.0,self.mapsize/2.0],vmin=clim[0],vmax=clim[1],cmap=self.colmap,origin='lower')
            if (docolorbar):
                cb=plt.colorbar()
                cb.set_label('mm')
            plt.title('Unwrapped phase map for %s'%(os.path.basename(self.filename)))
            plt.xlabel('meters')
            plt.ylabel('meters')
        elif (plottype=='flat'):
            drawlimits=True
            if (diff!=None):
                im=plt.imshow(incrz*(self.flatphasemap[::incrx,::incry]-diff.flatphasemap[::incrx,::incry])/D2R,extent=[-self.mapsize/2.0,self.mapsize/2.0,-self.mapsize/2.0,self.mapsize/2.0],vmin=clim[0],vmax=clim[1],cmap=self.colmap,origin='lower')
                if (docolorbar):
                    cb=plt.colorbar()
                    cb.set_label('deg')
                plt.title('Flattened difference phase %s - %s '%(os.path.basename(self.filename),os.path.basename(diff.dataset.filename)))
            else:
                im=plt.imshow(incrz*self.flatphasemap[::incrx,::incry]/D2R,extent=[-self.mapsize/2.0,self.mapsize/2.0,-self.mapsize/2.0,self.mapsize/2.0],vmin=clim[0],vmax=clim[1],cmap=self.colmap,origin='lower')
                if (docolorbar):
                    cb=plt.colorbar()
                    cb.set_label('deg')
                plt.title('Flattened phase map for %s'%(os.path.basename(self.filename)))
            plt.xlabel('meters')
            plt.ylabel('meters')
        elif (plottype=='flatmm'):
            drawlimits=True
            flatmm=incrz*self.flatphasemap*self.wavelength/(4.0*np.pi)*1000.0#in half path distance in mm (i.e. div by 4 instead of 2)
            #flatmm=getdeviation(self.flatphasemap,self.mapsize,self.gridsize,self.wavelength,self.focallength)
            im=plt.imshow(flatmm[::incrx,::incry],extent=[-self.mapsize/2.0,self.mapsize/2.0,-self.mapsize/2.0,self.mapsize/2.0],vmin=clim[0],vmax=clim[1],cmap=self.colmap,origin='lower')
            if (docolorbar):
                cb=plt.colorbar()
                cb.set_label('mm')
            plt.contour(np.linspace(-self.mapsize/2.0,self.mapsize/2.0,self.gridsize+1)[:-1],np.linspace(-self.mapsize/2.0,self.mapsize/2.0,self.gridsize+1)[:-1],flatmm[::incrx,::incry],levels=[-4,-3,-2,-1,1,2,3,4],colors='k')
            plt.title('Flattened phase map in mm for %s'%(os.path.basename(self.filename)))
            plt.xlabel('meters')
            plt.ylabel('meters')
        elif (plottype=='model'):
            drawlimits=True
            if (diff!=None):            
                im=plt.imshow(incrz*(self.modelmap[::incrx,::incry]-diff.modelmap[::incrx,::incry])/D2R,extent=[-self.mapsize/2.0,self.mapsize/2.0,-self.mapsize/2.0,self.mapsize/2.0],vmin=clim[0],vmax=clim[1],cmap=self.colmap,origin='lower')
                if (docolorbar):
                    cb=plt.colorbar()
                    cb.set_label('deg')
                plt.title('Model difference phase %s - %s '%(os.path.basename(self.filename),os.path.basename(diff.dataset.filename)))
            else:
                im=plt.imshow(incrz*self.modelmap[::incrx,::incry]/D2R,extent=[-self.mapsize/2.0,self.mapsize/2.0,-self.mapsize/2.0,self.mapsize/2.0],vmin=clim[0],vmax=clim[1],cmap=self.colmap,origin='lower')
                if (docolorbar):
                    cb=plt.colorbar()
                    cb.set_label('deg')
                plt.title('Model phase map for %s'%(os.path.basename(self.filename)))
            plt.xlabel('meters')
            plt.ylabel('meters')            
        elif (plottype=='amp'):
            drawlimits=True
            if (diff!=None):
                im=plt.imshow((self.ampmap[::incrx,::incry]-diff.ampmap[::incrx,::incry]),extent=[-self.mapsize/2.0,self.mapsize/2.0,-self.mapsize/2.0,self.mapsize/2.0],vmin=clim[0],vmax=clim[1],cmap=self.colmap,origin='lower')
                if (docolorbar):
                    plt.colorbar()        
                plt.title('Amplitude difference %s - %s '%(os.path.basename(self.filename),os.path.basename(diff.dataset.filename)))
            else:
                im=plt.imshow(self.ampmap[::incrx,::incry],extent=[-self.mapsize/2.0,self.mapsize/2.0,-self.mapsize/2.0,self.mapsize/2.0],vmin=clim[0],vmax=clim[1],cmap=self.colmap,origin='lower')
                if (docolorbar):
                    plt.colorbar()        
                plt.title('Amplitude map for %s'%(os.path.basename(self.filename)))
            plt.xlabel('meters')
            plt.ylabel('meters')
        elif (plottype=='mask'):
            im=plt.imshow(self.unwrapmaskmap[::incrx,::incry],extent=[-self.mapsize/2.0,self.mapsize/2.0,-self.mapsize/2.0,self.mapsize/2.0],vmin=clim[0],vmax=clim[1],cmap=self.colmap,origin='lower')
            if (docolorbar):
                plt.colorbar()        
            plt.title('Mask map for %s'%(os.path.basename(self.filename)))
            plt.xlabel('meters')
            plt.ylabel('meters')
        elif (plottype=='weight'):
            maxrad=np.max([np.max(self.ll),-np.min(self.ll),np.max(self.mm),-np.min(self.mm)])/D2R
            margin=np.linspace(-maxrad*D2R,maxrad*D2R,self.gridsize)
            newx,newy=np.meshgrid(margin,margin)
            xi=(newx,newy)
            nweight=scipy.interpolate.griddata(np.transpose(np.array([self.ll,self.mm])), self.weight, xi, method='linear')
            im=plt.imshow(nweight,extent=[-maxrad,maxrad,-maxrad,maxrad],vmin=clim[0],vmax=clim[1],cmap=self.colmap,origin='lower')
            if (docolorbar):
                plt.colorbar()
            plt.title('Weight used by DFT for %s'%(os.path.basename(self.filename)))
            plt.xlabel('degrees')
            plt.ylabel('degrees')
            drawoverlay=False
        elif (plottype=='weightmlab'):
            maxrad=np.max([np.max(self.ll),-np.min(self.ll),np.max(self.mm),-np.min(self.mm)])/D2R
            margin=np.linspace(-maxrad*D2R,maxrad*D2R,self.gridsize)
            nweight=mlab.griddata(self.ll,self.mm,self.weight,margin,margin)
            im=plt.imshow(nweight,extent=[-maxrad,maxrad,-maxrad,maxrad],vmin=clim[0],vmax=clim[1],cmap=self.colmap,origin='lower')
            if (docolorbar):
                plt.colorbar()        
            plt.title('Weight used by DFT for %s'%(os.path.basename(self.filename)))
            plt.xlabel('degrees')
            plt.ylabel('degrees')
            drawoverlay=False
        elif (plottype=='weightprofile'):
            rr=np.sqrt(self.ll**2+self.mm**2)/D2R
            plt.plot(rr,self.weight,'.')
            plt.title('Radial profile of weight used by DFT for %s'%(os.path.basename(self.filename)))
            plt.xlabel('degrees')
            plt.ylabel('Weight')
            drawoverlay=False
        elif (plottype=='voronoi'):
            l=self.ll/D2R
            m=self.mm/D2R
            v=scipy.spatial.Voronoi(np.array(list(zip(l,m))))
            minmaxrad=np.min([np.max(l),-np.min(l),np.max(m),-np.min(m)])
            rad=np.sqrt(l*l+m*m)
            imidrange=np.nonzero((rad>minmaxrad*0.3)*(rad<minmaxrad*0.8))[0]
            weight=np.zeros(l.shape,dtype='float')
            iperimeter=np.nonzero([1 if (ir==-1 or -1 in v.regions[ir] or len(v.regions[ir])==0) else 0 for ir in v.point_region])[0]
            perimorder=np.argsort(np.arctan2(l[iperimeter],m[iperimeter]))
            # vinside=matplotlib.nxutils.points_inside_poly(v.vertices,list(zip(l[iperimeter[perimorder]],m[iperimeter[perimorder]])))
            # outside=np.nonzero(vinside==False)[0]
            p = path.Path(list(zip(l[iperimeter[perimorder]],m[iperimeter[perimorder]])))
            outside = np.nonzero(~p.contains_points(v.vertices))[0]
            for iout in outside:
                v.vertices[iout]=[np.nan,np.nan]
            for i,ir in enumerate(v.point_region):
                if (ir==-1 or len(v.regions[ir])==0 or -1 in v.regions[ir]):
                    weight[i]=np.nan
                else:
                    pt=[v.vertices[iv] for iv in v.regions[ir]]
                    weight[i]=np.abs(area_of_polygon(pt))/float(len(np.nonzero(ir==v.point_region)[0]))#note pt must NOT be np array#divide by number of duplciate points
                    plt.plot(np.array(pt)[:,0],np.array(pt)[:,1])
            medianweight=np.median(weight[imidrange])
            weight[np.nonzero(np.isnan(weight))[0]]=medianweight
            weight=weight/medianweight
            for i in range(len(l)):
                plt.text(l[i],m[i],'%.2f'%(weight[i]),horizontalalignment='center',verticalalignment='center')
                
            plt.xlim([np.min(l),np.max(l)])
            plt.ylim([np.min(m),np.max(m)])
            plt.title('Voronoi tessellation used by DFT for %s'%(os.path.basename(self.filename)))
            plt.xlabel('degrees')
            plt.ylabel('degrees')
            drawoverlay=False
        if (plotextras and drawoverlay):#Draw dish and blockage limits
            if (self.telescopename.lower()[:7]=='meerkat'):
                self.plotmeerkatedges()
            elif (self.telescopename.lower()[:7]=='hartrao'):
                self.plothartraoedges()
            elif (self.telescopename.lower()[:5]=='ghana'):
                self.plotghanaedges()
            elif (self.telescopename.lower()[:3]=='ska'):
                self.plotskaedges()
        if (plotextras and drawlimits):#Draw dish and blockage limits
            diamangles=np.arange(0,np.pi*2,np.arctan(1.0/((0.5*self.dishdiameter/self.mapsize)*self.gridsize)))
            if (self.blockdiameter>0):
                blockangles=np.arange(0,np.pi*2,np.arctan(1.0/((0.5*self.blockdiameter/self.mapsize)*self.gridsize)))
                plt.plot(0.5*self.blockdiameter*np.cos(blockangles),0.5*self.blockdiameter*np.sin(blockangles),'--w')
            plt.plot(0.5*self.dishdiameter*np.cos(diamangles),0.5*self.dishdiameter*np.sin(diamangles),'--w')
        if (im is not None):
            plt.gca().set_aspect('equal') 
            plt.gca().autoscale(tight=True) 
    
    def tofits(self,filename=None):
        dx=self.mapsize/self.gridsize
        cards=[pyfits.Card('SIMPLE', True),pyfits.Card('BITPIX', 16),pyfits.Card('NAXIS', 3),pyfits.Card('NAXIS1', self.gridsize),pyfits.Card('NAXIS2', self.gridsize),pyfits.Card('NAXIS3', 2),pyfits.Card('BSCALE', 1.0),pyfits.Card('BZERO', 0.0),pyfits.Card('BUNIT', ' '),pyfits.Card('CRVAL1',0),pyfits.Card('CRVAL2',0),pyfits.Card('CRVAL3',0),pyfits.Card('CRPIX1',self.gridsize/2.0-1.0),pyfits.Card('CRPIX2',self.gridsize/2.0-1.0),pyfits.Card('CRPIX3',1.0/2.0),pyfits.Card('CDELT1',dx),pyfits.Card('CDELT2',dx),pyfits.Card('CDELT3',1.0),pyfits.Card('CTYPE1','TARGETX'),pyfits.Card('CTYPE2','TARGETY'),pyfits.Card('CTYPE3','MAP')]
        if (filename==None):
            filename=self.dataset.filenamebase+'.fits'
        pyfits.writeto(filename,np.array([self.ampmap,self.devmap]),pyfits.Header(cards),overwrite=True);


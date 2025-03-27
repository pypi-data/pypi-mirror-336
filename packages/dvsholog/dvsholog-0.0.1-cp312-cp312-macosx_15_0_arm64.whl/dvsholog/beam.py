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
import scikits.fitting as fitting
import astropy.io.fits as pyfits
import array
import scipy
import os,sys,time
from multiprocessing import Process, Queue, cpu_count
import katdal
import pickle
import optparse
import dvsholog
from .utilities import *

class BeamCube(object):
    """BeamCube object stores beam patterns for a range of frequencies for a single dish.
    """
    def __init__(self,dataset,dMHz=16,freqMHz=None,extent=None,gridsize=512,scanantennaname=None,trackantennanames=None,applypointing=None,xyzoffsets=None,interpmethod='linear',feedtheta=0,feedepsilon=0,feedphi=0,feedcombine=None):
        """Creates a BeamCube object from a holography dataset object.

        Parameters
        ----------
        dataset : dvsholog.Dataset object
            Dataset object from which to derive beam cube.
        dMHz : float
            Width of frequency range to use for averaging channels together, in MHz.
        freqMHz : float or list of floats
            Center frequencies of beam cube map slices, in MHz. If None, then these will automatically 
            be chosen such that they are dMHz apart.
        extent : float
            Diameter extent of beam, as scaled to fit onto the grid extent, in degrees. 
            If None, then the full data extent is used.
        gridsize : int
            If not None, override number of cells in map along one axis.
        scanantennaname : string
            Name of antenna for which to create aperture map. If None then the first scanning antenna is used.
        trackantennanames : list of strings
            Names of antennas to use as tracking antennas to create aperture map. If None, all tracking antennas will be used.
        applypointing : string or None        
            Specify kind of pointing correction to apply, can be 'Gx','Gy','I','Imaxf','center','centerperfreq','perfeed':
            'Gx' : applies the offset determined for Gx to all polarisation products
            'Gy' : applies the offset determined for Gy to all polarisation products
            'I' : applies the offset determined for I to all polarisation products
            'Imaxf' : applies the offset determined for I at max freq to all polarisation products
            'center' : applies the estimated dish pointing error, averaged over frequency
            'centerperfreq' : applies the estimated dish pointing error, per frequency slice
            'perfeed' : applies the Gx offset to Gx products, and Gy offset to Gy products
            Default is None, i.e. apply no pointing correction to beam.
        xyzoffsets : list of 3 floats
            If not None, override non-intersecting axis offsets of antenna, in meters.
        
        
        """
        self.feedtheta=feedtheta
        self.feedepsilon=feedepsilon
        self.feedphi=feedphi
        self.feedcombine=feedcombine
        self.dMHz=dMHz
        self.extent=extent
        self.interpmethod=interpmethod
        if (type(dataset)==dvsholog.aperture.ApertureMap):
            self.ApertureMap=dataset
            self.telescopename=dataset.telescopename
            self.filename=dataset.filename
            self.dataset=dataset.dataset
            self.scanantennaname=dataset.scanantennaname
            self.trackantennanames=dataset.trackantennanames
            self.freqgrid=np.array([dataset.freqMHz])
            nchan=1
        else:
            self.ApertureMap=None
            self.dataset=dataset
            self.filename=dataset.filename
            self.telescopename=dataset.telescopename
            self.scanantennaname,self.trackantennanames=dataset.parseantennanames(scanantennaname,trackantennanames)
            if (freqMHz==None):#then derive from dataset
                if (len(self.dataset.radialscan_centerfreq)==1):
                    self.freqgrid=self.dataset.radialscan_centerfreq/1e6
                else:
                    if (dMHz<0.0):
                        dMHz*=(self.dataset.h5.channel_freqs[1]-self.dataset.h5.channel_freqs[0])/1e6
                    cenfreqMHz=self.dataset.radialscan_centerfreq/1E6
                    refMHz=1800.0;
                    startMHz=refMHz+np.round(((cenfreqMHz[0])-refMHz)/dMHz)*dMHz#includes all valid channels
                    self.freqgrid=np.arange(startMHz,(cenfreqMHz[-1]-dMHz/2.0),-dMHz)#center frequencies to be evaluated            
            elif (np.shape(freqMHz)==()):
                self.freqgrid=np.array([freqMHz])
            else:
                self.freqgrid=np.array(freqMHz)
            nchan=len(self.freqgrid)
        if (self.telescopename.lower()=='kat7'):
            self.gridsize=512
            self.xyzoffsets=[0.0,0.325,0.84]
        elif (self.telescopename.lower()=='hirax'):
            self.gridsize=512
            self.xyzoffsets=[0.0,0.0,0.0]
        elif (self.telescopename.lower()=='xdm'):
            self.gridsize=512
            self.xyzoffsets=[0.0,0.0,1.44]
        elif (self.telescopename.lower()=='mopra'):
            self.gridsize=512
            self.xyzoffsets=[0.0,0.0,0.0]
        elif (self.telescopename.lower()=='kat7emss'):
            self.gridsize=512
            self.xyzoffsets=[0.0,0.0,0.0]
        elif (self.telescopename.lower()=='ska'):
            self.gridsize=512
            self.xyzoffsets=[0.0,0.0,0.0]
        elif (self.telescopename.lower()=='meerkataph'):
            self.gridsize=512
            self.xyzoffsets=[0.0,-1.55,-2.4762]
        elif (self.telescopename.lower()=='meerkat'):
            self.gridsize=512
            self.xyzoffsets=[0.0,-1.55,-2.4762]
        elif (self.telescopename.lower()=='dva1'):
            self.gridsize=512
            self.xyzoffsets=[0.0,0.0,0.0]
        elif (self.telescopename.lower()=='vla'):
            self.gridsize=512
            self.xyzoffsets=[0.0,0.0,0.0]
        elif (self.telescopename.lower()=='ghana'):
            self.gridsize=512
            self.xyzoffsets=[0.0,0.0,0.0]
        elif (self.telescopename.lower()=='hartrao'):
            self.gridsize=512
            self.xyzoffsets=[0.0,0.0,0.0]
        elif (self.telescopename.lower()=='vgos'):
            self.gridsize=512
            self.xyzoffsets=[0.0,0.0,0.0]
        else:
            print('Warning: unknown telescope %s'%self.telescopename)
        if (gridsize!=None):
            self.gridsize=np.int32(gridsize)
        if (xyzoffsets!=None):
            self.xyzoffsets=np.array(xyzoffsets,dtype='float')
        self.xyzoffsets=np.array(self.xyzoffsets)

        self.colmap=matplotlib.colors.ListedColormap(sqrcolmap(),'sqr')
        
        if (self.extent==None):
            self.extent=self.dataset.radialscan_extent/D2R
        self.margin=np.linspace(-self.extent/2.0,self.extent/2.0,self.gridsize+1)[:-1]
        self.Gx=np.zeros([nchan,self.gridsize,self.gridsize],dtype='complex')
        self.Gy=np.zeros([nchan,self.gridsize,self.gridsize],dtype='complex')
        self.beamoffsetI=np.zeros([nchan,2],dtype='float')
        self.beamoffsetGx=np.zeros([nchan,2],dtype='float')
        self.beamoffsetGy=np.zeros([nchan,2],dtype='float')
        self.beamwidthI=np.zeros([nchan,2],dtype='float')
        self.beamwidthGx=np.zeros([nchan,2],dtype='float')
        self.beamwidthGy=np.zeros([nchan,2],dtype='float')
        self.beamoffsetapplied=[]
        self.Dx=np.zeros([nchan,self.gridsize,self.gridsize],dtype='complex')
        self.Dy=np.zeros([nchan,self.gridsize,self.gridsize],dtype='complex')
        self.Gxgainlist=[]
        self.Gygainlist=[]
        self.Dxgainlist=[]
        self.Dygainlist=[]
        self.beamoffsetlist=[]
        if (type(dataset)==dvsholog.aperture.ApertureMap):
            self.Gxgainlist.append([])
            self.Gygainlist.append([])
            self.Dxgainlist.append([])
            self.Dygainlist.append([])
            self.beamoffsetI[0]=[0,0]
            self.beamoffsetGx[0]=[0,0]
            self.beamoffsetGy[0]=[0,0]
            self.beamwidthI[0]=[0,0]
            self.beamwidthGx[0]=[0,0]
            self.beamwidthGy[0]=[0,0]
            offsets=[[0.0,0.0],[0.0,0.0],[0.0,0.0],[0.0,0.0]]
            self.beamoffsetlist.append(offsets)
            self.beamoffsetapplied.append(offsets)
            lld,mmd=np.meshgrid(self.margin,self.margin)
            lld=lld.reshape(-1)
            mmd=mmd.reshape(-1)
            if (dataset.ndftproc is None and dogpudft is not None):
                beam=dogpuidft(lld*D2R,mmd*D2R,dataset.apert,dataset.mapsize,dataset.gridsize,dataset.wavelength).reshape([self.gridsize,self.gridsize])
            else:
                ndftproc=dataset.ndftproc
                if (ndftproc==None):
                    ndftproc=cpu_count()
                beam=domultiidft(lld*D2R,mmd*D2R,dataset.apert,dataset.mapsize,dataset.gridsize,dataset.wavelength,ndftproc).reshape([self.gridsize,self.gridsize])
            self.Gx[0,:,:],self.Gy[0,:,:],self.Dx[0,:,:],self.Dy[0,:,:]=beam,0*beam,0*beam,0*beam
        else:
            for ich,freq in enumerate(self.freqgrid):
                ll,mm,vis,beamoffsets,Gxgainlist,Gygainlist,Dxgainlist,Dygainlist=self.dataset.getvisslice(freq,self.dMHz,self.scanantennaname,self.trackantennanames,ich)            
                wavelength=self.dataset.speedoflight/(self.freqgrid[ich]*1e6)
                dl,dm,dn=np.array(self.xyzoffsets)*(np.pi*2.0)/wavelength
                vis=vis*np.exp(1j*(dl*(ll)+dm*(mm)+dn*np.sqrt(1.0-(ll)**2-(mm)**2) ))
                self.Gxgainlist.append(Gxgainlist)
                self.Gygainlist.append(Gygainlist)
                self.Dxgainlist.append(Dxgainlist)
                self.Dygainlist.append(Dygainlist)
                self.beamoffsetI[ich]=np.mean([beamoffset[0] for beamoffset in beamoffsets],axis=0)
                self.beamoffsetGx[ich]=np.mean([beamoffset[1] for beamoffset in beamoffsets],axis=0)
                self.beamoffsetGy[ich]=np.mean([beamoffset[2] for beamoffset in beamoffsets],axis=0)
                self.beamwidthI[ich]=np.mean([beamoffset[3] for beamoffset in beamoffsets],axis=0)
                self.beamwidthGx[ich]=np.mean([beamoffset[4] for beamoffset in beamoffsets],axis=0)
                self.beamwidthGy[ich]=np.mean([beamoffset[5] for beamoffset in beamoffsets],axis=0)
                self.beamoffsetlist.append(beamoffsets)
            for ich,freq in enumerate(self.freqgrid):
                if (applypointing=='Gx'):#applies the offset determined for Gx to all polarisation products
                    offsets=[[self.beamoffsetGx[ich,0]/D2R,self.beamoffsetGx[ich,1]/D2R],[self.beamoffsetGx[ich,0]/D2R,self.beamoffsetGx[ich,1]/D2R],[self.beamoffsetGx[ich,0]/D2R,self.beamoffsetGx[ich,1]/D2R],[self.beamoffsetGx[ich,0]/D2R,self.beamoffsetGx[ich,1]/D2R]]
                elif (applypointing=='Gy'):#applies the offset determined for Gy to all polarisation products
                    offsets=[[self.beamoffsetGy[ich,0]/D2R,self.beamoffsetGy[ich,1]/D2R],[self.beamoffsetGy[ich,0]/D2R,self.beamoffsetGy[ich,1]/D2R],[self.beamoffsetGy[ich,0]/D2R,self.beamoffsetGy[ich,1]/D2R],[self.beamoffsetGy[ich,0]/D2R,self.beamoffsetGy[ich,1]/D2R]]
                elif (applypointing=='I'):#applies the offset determined for I to all polarisation products
                    offsets=[[self.beamoffsetI[ich,0]/D2R,self.beamoffsetI[ich,1]/D2R],[self.beamoffsetI[ich,0]/D2R,self.beamoffsetI[ich,1]/D2R],[self.beamoffsetI[ich,0]/D2R,self.beamoffsetI[ich,1]/D2R],[self.beamoffsetI[ich,0]/D2R,self.beamoffsetI[ich,1]/D2R]]
                elif (applypointing=='Imaxf'):#applies the offset determined for I at max freq to all polarisation products
                    offsets=[[self.beamoffsetI[-1,0]/D2R,self.beamoffsetI[-1,1]/D2R],[self.beamoffsetI[-1,0]/D2R,self.beamoffsetI[-1,1]/D2R],[self.beamoffsetI[-1,0]/D2R,self.beamoffsetI[-1,1]/D2R],[self.beamoffsetI[-1,0]/D2R,self.beamoffsetI[-1,1]/D2R]]
                elif (applypointing=='center'):#applies the estimated dish pointing error, averaged over frequency
                    offsets=[[np.mean(self.beamoffsetGy[:,0])/D2R,np.mean(self.beamoffsetGx[:,1])/D2R],[np.mean(self.beamoffsetGy[:,0])/D2R,np.mean(self.beamoffsetGx[:,1])/D2R],[np.mean(self.beamoffsetGy[:,0])/D2R,np.mean(self.beamoffsetGx[:,1])/D2R],[np.mean(self.beamoffsetGy[:,0])/D2R,np.mean(self.beamoffsetGx[:,1])/D2R]]
                elif (applypointing=='centerperfreq'):#applies the estimated dish pointing error, per frequency
                    offsets=[[self.beamoffsetGy[ich,0]/D2R,self.beamoffsetGx[ich,1]/D2R],[self.beamoffsetGy[ich,0]/D2R,self.beamoffsetGx[ich,1]/D2R],[self.beamoffsetGy[ich,0]/D2R,self.beamoffsetGx[ich,1]/D2R],[self.beamoffsetGy[ich,0]/D2R,self.beamoffsetGx[ich,1]/D2R]]
                elif (applypointing=='perfeed'):#applies the Gx offset to Gx products, and Gy offset to Gy products
                    offsets=[[self.beamoffsetGx[ich,0]/D2R,self.beamoffsetGx[ich,1]/D2R],[self.beamoffsetGy[ich,0]/D2R,self.beamoffsetGy[ich,1]/D2R],[self.beamoffsetGx[ich,0]/D2R,self.beamoffsetGx[ich,1]/D2R],[self.beamoffsetGy[ich,0]/D2R,self.beamoffsetGy[ich,1]/D2R]]
                elif (type(applypointing)==list or type(applypointing)==np.ndarray):
                    if (type(applypointing[0])==list or type(applypointing[0])==np.ndarray):
                        offsets=[[-applypointing[0][0],-applypointing[0][1]],[-applypointing[1][0],-applypointing[1][1]],[-applypointing[2][0],-applypointing[2][1]],[-applypointing[3][0],-applypointing[3][1]]]
                    else:
                        offsets=[[-applypointing[0],-applypointing[1]],[-applypointing[0],-applypointing[1]],[-applypointing[0],-applypointing[1]],[-applypointing[0],-applypointing[1]]]
                else:#do nothing
                    offsets=[[0.0,0.0],[0.0,0.0],[0.0,0.0],[0.0,0.0]]
                self.beamoffsetapplied.append(offsets)
                if (type(dataset)==dvsholog.aperture.ApertureMap):
                    ll,mm,vis,beamoffsets,Gxgainlist,Gygainlist,Dxgainlist,Dygainlist=self.dataset.getvisslice(freq,self.dMHz,self.scanantennaname,self.trackantennanames)
                    wavelength=self.dataset.speedoflight/(self.freqgrid[ich]*1e6)
                    dl,dm,dn=np.array(self.xyzoffsets)*(np.pi*2.0)/wavelength
                    phaseadjustment=np.exp(1j*(dl*(ll)+dm*(mm)+dn*np.sqrt(1.0-(ll)**2-(mm)**2) ))
                    for ivis in range(len(vis)):
                        vis[ivis]*=phaseadjustment*dataset.weight
                    apertGx,apertGy,apertDx,apertDy=dogpudftfull(ll,mm,vis,dataset.mapsize,dataset.gridsize,wavelength)
                    x,y=np.meshgrid(np.linspace(-dataset.mapsize/2.0,dataset.mapsize/2.0,self.gridsize+1)[:-1],np.linspace(-dataset.mapsize/2.0,dataset.mapsize/2.0,self.gridsize+1)[:-1])
                    subsample=4
                    flatmask=dataset.maskmap[::subsample,::subsample].reshape(-1)
                    valid=np.nonzero(flatmask==0)[0]
                    apertGx=np.ascontiguousarray(apertGx[::subsample,::subsample].reshape(-1)[valid],dtype='complex64')
                    apertGy=np.ascontiguousarray(apertGy[::subsample,::subsample].reshape(-1)[valid],dtype='complex64')
                    apertDx=np.ascontiguousarray(apertDx[::subsample,::subsample].reshape(-1)[valid],dtype='complex64')
                    apertDy=np.ascontiguousarray(apertDy[::subsample,::subsample].reshape(-1)[valid],dtype='complex64')
                    flatx=np.ascontiguousarray(x[::subsample,::subsample].reshape(-1)[valid],dtype='float32')
                    flaty=np.ascontiguousarray(y[::subsample,::subsample].reshape(-1)[valid],dtype='float32')
                    divisions=1
                    aGx0=0;aGy0=0;aDx0=0;aDy0=0;
                    for idiv in range(divisions):
                        aGx,aGy,aDx,aDy    =dogpudftfull(flatx[idiv::divisions],flaty[idiv::divisions],[apertGx[idiv::divisions],apertGy[idiv::divisions],apertDx[idiv::divisions],apertDy[idiv::divisions]],self.dataset.radialscan_extent,self.gridsize,wavelength)
                        aGx0=aGx+aGx0
                        aGy0=aGy+aGy0
                        aDx0=aDx+aDx0
                        aDy0=aDy+aDy0
                    
                    self.Gx[ich,:,:],self.Gy[ich,:,:],self.Dx[ich,:,:],self.Dy[ich,:,:]=aGx0,aGy0,aDx0,aDy0
                elif (dataset.method!='offsetonly'):
                    ll,mm,vis,beamoffsets,Gxgainlist,Gygainlist,Dxgainlist,Dygainlist=self.dataset.getvisslice(freq,self.dMHz,scanantennaname,trackantennanames)            
                    wavelength=self.dataset.speedoflight/(self.freqgrid[ich]*1e6)
                    dl,dm,dn=np.array(self.xyzoffsets)*(np.pi*2.0)/wavelength
                    vis=vis*np.exp(1j*(dl*(ll)+dm*(mm)+dn*np.sqrt(1.0-(ll)**2-(mm)**2) ))
                    if (len(vis)==1):
                        beam=self.interpgrid(ll/D2R,mm/D2R,vis,self.beamoffsetapplied[ich])
                        self.Gx[ich,:,:],self.Gy[ich,:,:],self.Dx[ich,:,:],self.Dy[ich,:,:]=beam[0],0*beam[0],0*beam[0],0*beam[0]
                    elif (len(vis)==2):
                        self.Gx[ich,:,:],self.Dx[ich,:,:]=self.interpgrid(ll/D2R,mm/D2R,vis,self.beamoffsetapplied[ich])
                        self.Gy[ich,:,:],self.Dy[ich,:,:]=self.interpgrid(mm/D2R,-ll/D2R,vis,self.beamoffsetapplied[ich])
                    else:
                        self.Gx[ich,:,:],self.Gy[ich,:,:],self.Dx[ich,:,:],self.Dy[ich,:,:]=self.interpgrid(ll/D2R,mm/D2R,vis,self.beamoffsetapplied[ich])
        #applies poldistortion [exp(j*phi),0;0,exp(-j*phi)]*[cos(epsilon),j*sin(epsilon);j*sin(epsilon),cos(epsilon)]*[cos(theta),sin(theta);-sin(theta),cos(theta)]
        #[exp(j*phi)*(cos(epsilon)*cos(theta)-j*sin(epsilon)*sin(theta)),exp(j*phi)*(cos(epsilon)*sin(theta)+j*sin(epsilon)*cos(theta));exp(-j*phi)*(j*sin(epsilon)*cos(theta)-cos(epsilon)*sin(theta)),exp(-j*phi)*(j*sin(epsilon)*sin(theta)+cos(epsilon)*cos(theta))]
        if (self.feedcombine is not None):
            for ich in range(len(self.freqgrid)):
                gx,gy,dx,dy=self.Gx[ich,:,:]+0,self.Gy[ich,:,:]+0,self.Dx[ich,:,:]+0,self.Dy[ich,:,:]+0
                vis=feedcombine[0]*gx+feedcombine[1]*dx+feedcombine[2]*dy+feedcombine[3]*gy
                #TODO this should be improved, normalise at origin, assuming its an emss beam pattern
                vis/=vis[self.gridsize//2-1,self.gridsize//2-1]
                self.Gx[ich,:,:]=vis
                self.Dx[ich,:,:]=vis
                self.Dy[ich,:,:]=vis
                self.Gy[ich,:,:]=vis
        elif (self.feedtheta!=0):
            poldistortion=[[np.exp(1j*self.feedphi)*(np.cos(self.feedepsilon)*np.cos(self.feedtheta)-1j*np.sin(self.feedepsilon)*np.sin(self.feedtheta)),np.exp(1j*self.feedphi)*(np.cos(self.feedepsilon)*np.sin(self.feedtheta)+1j*np.sin(self.feedepsilon)*np.cos(self.feedtheta))],[np.exp(-1j*self.feedphi)*(1j*np.sin(self.feedepsilon)*np.cos(self.feedtheta)-np.cos(self.feedepsilon)*np.sin(self.feedtheta)),np.exp(-1j*self.feedphi)*(1j*np.sin(self.feedepsilon)*np.sin(self.feedtheta)+np.cos(self.feedepsilon)*np.cos(self.feedtheta))]]
            [[Jxx,Jxy],[Jyx,Jyy]]=poldistortion
            for ich in range(len(self.freqgrid)):
                gx,gy,dx,dy=self.Gx[ich,:,:]+0,self.Gy[ich,:,:]+0,self.Dx[ich,:,:]+0,self.Dy[ich,:,:]+0
                self.Gx[ich,:,:]=gx*Jxx+dx*Jyx
                self.Dx[ich,:,:]=dx*Jxx+gx*Jyx
                self.Dy[ich,:,:]=dy*Jyy+gy*Jxy
                self.Gy[ich,:,:]=gy*Jyy+dy*Jxy
            

    #fits and applies polynomial model to beam up to specified power level
    def fitpoly(self,fitdBlevel=-14,degree=6):
        ncoeff=polygetncoeff(degree)
        nmodelparams=ncoeff*2
        modelfunction=polydriftabs
        ngainintervals=1
        self.mGx=np.array(np.tile(np.nan,self.Gx.shape),dtype='complex')
        self.mGy=np.array(np.tile(np.nan,self.Gx.shape),dtype='complex')
        self.mDx=np.array(np.tile(np.nan,self.Gx.shape),dtype='complex')
        self.mDy=np.array(np.tile(np.nan,self.Gx.shape),dtype='complex')
        self.cGx=np.zeros([self.Gx.shape[0],nmodelparams])
        self.cGy=np.zeros([self.Gx.shape[0],nmodelparams])
        self.cDx=np.zeros([self.Gx.shape[0],nmodelparams])
        self.cDy=np.zeros([self.Gx.shape[0],nmodelparams])
        powbeam=0.5*(self.Gx[:,:,:]**2+self.Gy[:,:,:]**2)
        for ich in range(self.Gx.shape[0]):
            initialparams=np.r_[np.zeros(nmodelparams),np.ones(ngainintervals-1),np.zeros(ngainintervals-1)]
            fitptsI=np.nonzero(10.0*np.log10(np.abs(powbeam[ich,:,:].reshape(-1)))>fitdBlevel)[0]
            newx,newy=np.meshgrid(self.margin,self.margin)
            newx=newx.reshape(-1)
            newy=newy.reshape(-1)

            fitterGx=NonLinearLeastSquaresFit(modelfunction,initialparams)
            beamGx=self.Gx[ich,:,:].reshape(-1)
            fitterGx.fit([newx[fitptsI],newy[fitptsI],np.zeros(len(fitptsI)),ncoeff,degree],np.r_[np.real(beamGx[fitptsI]),np.imag(beamGx[fitptsI])])
            fitGx=fitterGx.eval([newx[fitptsI],newy[fitptsI],np.zeros(len(fitptsI)),ncoeff,degree])
            fitGx=fitGx[:len(fitptsI)]+1j*fitGx[len(fitptsI):]
            beamGx=np.array(np.tile(np.nan,self.Gx.shape[1:]).reshape(-1),dtype='complex')
            beamGx[fitptsI]=fitGx
            self.mGx[ich,:,:]=beamGx.reshape(self.Gx.shape[1:])
            self.cGx[ich,:]=fitterGx.params

            fitterGy=NonLinearLeastSquaresFit(modelfunction,initialparams)
            beamGy=self.Gy[ich,:,:].reshape(-1)
            fitterGy.fit([newx[fitptsI],newy[fitptsI],np.zeros(len(fitptsI)),ncoeff,degree],np.r_[np.real(beamGy[fitptsI]),np.imag(beamGy[fitptsI])])
            fitGy=fitterGy.eval([newx[fitptsI],newy[fitptsI],np.zeros(len(fitptsI)),ncoeff,degree])
            fitGy=fitGy[:len(fitptsI)]+1j*fitGy[len(fitptsI):]
            beamGy=np.array(np.tile(np.nan,self.Gx.shape[1:]).reshape(-1),dtype='complex')
            beamGy[fitptsI]=fitGy
            self.mGy[ich,:,:]=beamGy.reshape(self.Gx.shape[1:])
            self.cGy[ich,:]=fitterGy.params
            
            fitterDx=NonLinearLeastSquaresFit(modelfunction,initialparams)
            beamDx=self.Dx[ich,:,:].reshape(-1)
            fitterDx.fit([newx[fitptsI],newy[fitptsI],np.zeros(len(fitptsI)),ncoeff,degree],np.r_[np.real(beamDx[fitptsI]),np.imag(beamDx[fitptsI])])
            fitDx=fitterDx.eval([newx[fitptsI],newy[fitptsI],np.zeros(len(fitptsI)),ncoeff,degree])
            fitDx=fitDx[:len(fitptsI)]+1j*fitDx[len(fitptsI):]
            beamDx=np.array(np.tile(np.nan,self.Dx.shape[1:]).reshape(-1),dtype='complex')
            beamDx[fitptsI]=fitDx
            self.mDx[ich,:,:]=beamDx.reshape(self.Gx.shape[1:])
            self.cDx[ich,:]=fitterDx.params
            
            fitterDy=NonLinearLeastSquaresFit(modelfunction,initialparams)
            beamDy=self.Dy[ich,:,:].reshape(-1)
            fitterDy.fit([newx[fitptsI],newy[fitptsI],np.zeros(len(fitptsI)),ncoeff,degree],np.r_[np.real(beamDy[fitptsI]),np.imag(beamDy[fitptsI])])
            fitDy=fitterDy.eval([newx[fitptsI],newy[fitptsI],np.zeros(len(fitptsI)),ncoeff,degree])
            fitDy=fitDy[:len(fitptsI)]+1j*fitDy[len(fitptsI):]
            beamDy=np.array(np.tile(np.nan,self.Dx.shape[1:]).reshape(-1),dtype='complex')
            beamDy[fitptsI]=fitDy
            self.mDy[ich,:,:]=beamDy.reshape(self.Gx.shape[1:])
            self.cDy[ich,:]=fitterDy.params

    #fits cubic to data provided (limited range from total dataset, referred to be around origin)
    #and return node parameters (function value, and derivatives) at origin
    def fitbicubic(self,x,y,rebeam):
        initialparams=np.zeros(16)
        fitter=NonLinearLeastSquaresFit(cubefunc,initialparams)
        fitter.fit([x,y],rebeam)
        return fitter.params
        
    #performs piecewise bicubic modeling of calibrated beam
    #with nodes spaced appropriately
    #note there seem to be insufficient points in node regions to do fit everywhere of interest
    def modelbicubic(self,x,y,beams,offsets):
        self.nodespacing=0.8;#degrees
        self.nodemargin=np.arange(0,self.extent/2.0,self.nodespacing);
        self.nodemargin=np.r_[-self.nodemargin[:0:-1],self.nodemargin]
        nodex,nodey=np.meshgrid(self.nodemargin,self.nodemargin)
        nodex=nodex.reshape(-1)
        nodey=nodey.reshape(-1)
        newx,newy=np.meshgrid(self.margin,self.margin)
        newx=newx.reshape(-1)
        newy=newy.reshape(-1)
        gridbeam=[]
        for ibeam,cbeam in enumerate(beams):
            thisgrid=np.zeros([self.gridsize*self.gridsize],dtype='complex')
            for inode in range(len(nodex)):
                valid=np.nonzero(np.logical_and(np.abs(x-nodex[inode])<=self.nodespacing/2.0,np.abs(y-nodey[inode])<=self.nodespacing/2.0))[0]
                validgrid=np.nonzero(np.logical_and(np.abs(newx-nodex[inode])<=self.nodespacing/2.0,np.abs(newy-nodey[inode])<=self.nodespacing/2.0))[0]
                if (len(valid)>16):
                    reparams=self.fitbicubic(x[valid]-nodex[inode],y[valid]-nodey[inode],np.real(cbeam[valid]))
                    imparams=self.fitbicubic(x[valid]-nodex[inode],y[valid]-nodey[inode],np.imag(cbeam[valid]))                    
                    print(reparams,imparams)
                    thisgrid[validgrid]=np.array(cubefunc(reparams,[newx[validgrid]-nodex[inode],newy[validgrid]-nodey[inode]]),dtype='complex')+1j*np.array(cubefunc(imparams,[newx[validgrid]-nodex[inode],newy[validgrid]-nodey[inode]]),dtype='complex')
            gridbeam.append(thisgrid.reshape([self.gridsize,self.gridsize]))
        return gridbeam
        
#     def interpgrid(self,x,y,beams,offsets):
# #        return self.modelbicubic(x,y,beams,offsets)
#         newx,newy=np.meshgrid(self.margin,self.margin)
#         gridbeam=[]
#         offaxis=np.nonzero((x**2+y**2)>(self.dataset.radialscan_sampling/D2R)**2)[0]
#         onaxis=np.nonzero((x**2+y**2)<=(self.dataset.radialscan_sampling/D2R)**2)[0]
#         tx=np.r_[0.0,x[offaxis]]
#         ty=np.r_[0.0,y[offaxis]]
#         for ibeam,icbeam in enumerate(beams):
#             cbeam=np.r_[np.mean(icbeam[onaxis]),icbeam[offaxis]]
#             if (len(tx)==0):
#                 gridbeam.append(np.zeros([self.gridsize*self.gridsize],dtype='complex64'))
#             elif(self.interpmethod=='scipy'):
#                 points=np.transpose(np.array([tx-offsets[ibeam][0],ty-offsets[ibeam][1]]))
#                 xi=(newx,newy)
#                 method='linear'
#                 gridbeam.append(scipy.interpolate.griddata(points, np.real(cbeam), xi, method=method)+1j*scipy.interpolate.griddata(points, np.imag(cbeam), xi, method=method))
#             else:
#                 gridbeam.append(mlab.griddata(tx-offsets[ibeam][0],ty-offsets[ibeam][1],np.real(cbeam),np.array(newx),np.array(newy))+1j*mlab.griddata(tx-offsets[ibeam][0],ty-offsets[ibeam][1],np.imag(cbeam),np.array(newx),np.array(newy)))
#         return gridbeam

    def interpgrid(self,x,y,beams,offsets):
#        return self.modelbicubic(x,y,beams,offsets)
        newx,newy=np.meshgrid(self.margin,self.margin)
        gridbeam=[]
        offaxis=np.nonzero((x**2+y**2)>(self.dataset.radialscan_sampling/D2R)**2)[0]
        onaxis=np.nonzero((x**2+y**2)<=(self.dataset.radialscan_sampling/D2R)**2)[0]
        for ibeam,icbeam in enumerate(beams):
            tx=np.r_[0.0,x[offaxis]]
            ty=np.r_[0.0,y[offaxis]]
            cbeam=np.r_[np.mean(icbeam[onaxis]),icbeam[offaxis]]
            if (len(tx)==0):
                gridbeam.append(np.zeros([self.gridsize*self.gridsize],dtype='complex64'))
            elif(self.interpmethod=='scipy'):
                points=np.transpose(np.array([tx-offsets[ibeam][0],ty-offsets[ibeam][1]]))
                xi=(newx,newy)
                method='linear'
                #gridbeam.append(scipy.interpolate.griddata(points, np.real(cbeam), xi, method=method)+1j*scipy.interpolate.griddata(points, np.imag(cbeam), xi, method=method))
                reiminterp=scipy.interpolate.griddata(points, np.real(np.exp(1j*np.angle(cbeam))), xi, method=method)+1j*scipy.interpolate.griddata(points, np.imag(np.exp(1j*np.angle(cbeam))), xi, method=method)
                absinterp=scipy.interpolate.griddata(points, np.abs(cbeam), xi, method=method)*np.exp(1j*np.angle(reiminterp))
                gridbeam.append(absinterp)
            elif(self.interpmethod=='polar'):
                #convert into polar coordinates, and interpolate in that coordinate system
                newr=np.sqrt(newx**2+newy**2)
                newq=np.arctan2(newy,newx)
                tr=np.sqrt((tx-offsets[ibeam][0])**2+(ty-offsets[ibeam][1])**2)
                tq=np.arctan2((ty-offsets[ibeam][1]),(tx-offsets[ibeam][0]))
                top=np.nonzero(tq>np.pi-0.5)[0]
                bottom=np.nonzero(tq<-np.pi+0.5)[0]
                tr=np.r_[np.zeros(len(self.margin)/2),tr[1:],tr[top],tr[bottom]]
                tq=np.r_[np.linspace(-np.pi-0.5,np.pi+0.5,len(self.margin)/2),tq[1:],tq[top]-np.pi*2,tq[bottom]+np.pi*2]
                tq/=6.0
                newq/=6.0
                cbeam=np.r_[np.tile(cbeam[0],len(self.margin)/2),cbeam[1:],cbeam[top],cbeam[bottom]]
                points=np.transpose(np.array([tr,tq]))
                xi=(newr,newq)
                method='linear'
                #gridbeam.append(scipy.interpolate.griddata(points, np.real(cbeam), xi, method=method)+1j*scipy.interpolate.griddata(points, np.imag(cbeam), xi, method=method))
                reiminterp=scipy.interpolate.griddata(points, np.real(np.exp(1j*np.angle(cbeam))), xi, method=method)+1j*scipy.interpolate.griddata(points, np.imag(np.exp(1j*np.angle(cbeam))), xi, method=method)
                absinterp=scipy.interpolate.griddata(points, np.abs(cbeam), xi, method=method)*np.exp(1j*np.angle(reiminterp))
                gridbeam.append(absinterp)
            else:   
                # tx,ty,cbeam=self.averageduplicates(tx,ty,cbeam)#note clumsy here to overwrite tx,ty then iterate again for next beam
                gridbeam.append(mlab.griddata(tx-offsets[ibeam][0],ty-offsets[ibeam][1],np.real(cbeam),np.array(newx),np.array(newy))+1j*mlab.griddata(tx-offsets[ibeam][0],ty-offsets[ibeam][1],np.imag(cbeam),np.array(newx),np.array(newy)))
        return gridbeam
    
    def averageduplicates(self,x,y,data):
        tol=0.0#self.dataset.radialscan_sampling/D2R
        nx=np.array(x)
        ny=np.array(y)
        ndata=np.array(data)
        i=0
        while(i<len(nx)):
            same=np.nonzero(np.sqrt((nx[i]-nx)**2+(ny[i]-ny)**2)<=tol)[0]
            if (len(same)>0):
                ndata[i]=np.mean(ndata[same])#should perhaps do abs&unwrapped(phase) means
                nx[i]=np.mean(nx[same])
                ny[i]=np.mean(ny[same])#note this moves around the coordinates too!
                if (same[0]!=i):
                    print('Unexpected %d not equal to first element %d'%(i,same[0]))
                keep=list(set(range(len(nx)))-set(same[1:]))
                ndata=ndata[keep]
                nx=nx[keep]
                ny=ny[keep]
            i+=1
        return nx,ny,ndata
        
    def interpline(self,x,y,beams,offsets,theta):
        newx=np.linspace(self.margin[0],self.margin[-1],self.gridsize)
        newy=[0.0]
        theta=theta*np.pi/180.0
        costheta=np.cos(theta)
        sintheta=np.sin(theta)
        gridbeam=[]
        
        offaxis=np.nonzero((x**2+y**2)>(self.dataset.radialscan_sampling/D2R)**2)[0]
        onaxis=np.nonzero((x**2+y**2)<=(self.dataset.radialscan_sampling/D2R)**2)[0]
        for ibeam,icbeam in enumerate(beams):
            tx=np.r_[0.0,x[offaxis]]
            ty=np.r_[0.0,y[offaxis]]
            cbeam=np.r_[np.mean(icbeam[onaxis]),icbeam[offaxis]]
            ox=tx-offsets[ibeam][0]
            oy=ty-offsets[ibeam][1]
            xx=ox*costheta+oy*sintheta
            yy=-ox*sintheta+oy*costheta
            if (len(x)==0):
                gridbeam.append(np.zeros([self.gridsize*self.gridsize],dtype='complex64'))
            elif(self.interpmethod=='scipy'):
                points=np.transpose(np.array([xx,yy]))
                xi=(newx,newy)
                method='linear'
                # gridbeam.append(scipy.interpolate.griddata(points, np.real(cbeam), xi, method=method)+1j*scipy.interpolate.griddata(points, np.imag(cbeam), xi, method=method))
                reiminterp=scipy.interpolate.griddata(points, np.real(np.exp(1j*np.angle(cbeam))), xi, method=method)+1j*scipy.interpolate.griddata(points, np.imag(np.exp(1j*np.angle(cbeam))), xi, method=method)
                absinterp=scipy.interpolate.griddata(points, np.abs(cbeam), xi, method=method)*np.exp(1j*np.angle(reiminterp))
                gridbeam.append(absinterp)
            else:
                # xx,yy,cbeam=self.averageduplicates(xx,yy,cbeam)#note clumsy here to overwrite tx,ty then iterate again for next beam
                gridbeam.append(mlab.griddata(xx,yy,np.real(cbeam),np.array(newx),np.array(newy))+1j*mlab.griddata(xx,yy,np.imag(cbeam),np.array(newx),np.array(newy)))
        return gridbeam

    def plotoffset(self,ich):
        R2D=180.0/np.pi
        plt.plot([0,0],[-0.5,0.5],':k')
        plt.plot([-0.5,0.5],[0,0],':k')
        
        plt.plot([self.beamoffsetGx[ich,0]*R2D-self.beamoffsetapplied[ich][0][0]-0.05,self.beamoffsetGx[ich,0]*R2D-self.beamoffsetapplied[ich][0][0]+0.05],[self.beamoffsetGx[ich,1]*R2D-self.beamoffsetapplied[ich][0][1]-0.05,self.beamoffsetGx[ich,1]*R2D-self.beamoffsetapplied[ich][0][1]+0.05],'g')
        plt.plot([self.beamoffsetGx[ich,0]*R2D-self.beamoffsetapplied[ich][0][0]-0.05,self.beamoffsetGx[ich,0]*R2D-self.beamoffsetapplied[ich][0][0]+0.05],[self.beamoffsetGx[ich,1]*R2D-self.beamoffsetapplied[ich][0][1]+0.05,self.beamoffsetGx[ich,1]*R2D-self.beamoffsetapplied[ich][0][1]-0.05],'g')

        plt.plot([self.beamoffsetGy[ich,0]*R2D-self.beamoffsetapplied[ich][1][0]-0.05,self.beamoffsetGy[ich,0]*R2D-self.beamoffsetapplied[ich][1][0]],[self.beamoffsetGy[ich,1]*R2D-self.beamoffsetapplied[ich][1][1]+0.05,self.beamoffsetGy[ich,1]*R2D-self.beamoffsetapplied[ich][1][1]],'b')
        plt.plot([self.beamoffsetGy[ich,0]*R2D-self.beamoffsetapplied[ich][1][0]+0.05,self.beamoffsetGy[ich,0]*R2D-self.beamoffsetapplied[ich][1][0]],[self.beamoffsetGy[ich,1]*R2D-self.beamoffsetapplied[ich][1][1]+0.05,self.beamoffsetGy[ich,1]*R2D-self.beamoffsetapplied[ich][1][1]],'b')
        plt.plot([self.beamoffsetGy[ich,0]*R2D-self.beamoffsetapplied[ich][1][0],self.beamoffsetGy[ich,0]*R2D-self.beamoffsetapplied[ich][1][0]],[self.beamoffsetGy[ich,1]*R2D-self.beamoffsetapplied[ich][1][1],self.beamoffsetGy[ich,1]*R2D-self.beamoffsetapplied[ich][1][1]-0.05*np.sqrt(2)],'b')
        
        # plt.plot([self.beamoffsetGy[:,0]*R2D,self.beamoffsetGy[:,0]*R2D],[self.beamoffsetGx[:,1]*R2D-0.5,self.beamoffsetGx[:,1]*R2D+0.5],'g')#Gy's x component and Gx's y component is used
        # plt.plot([self.beamoffsetGy[:,0]*R2D-0.5,self.beamoffsetGy[:,0]*R2D+0.5],[self.beamoffsetGx[:,1]*R2D,self.beamoffsetGx[:,1]*R2D],'g')#Gy's x component and Gx's y component is used
        
    def movie(self,stokes='I',component='pow',iquv=[1,0,0,0],clim=[None,None]):
        for ich in range(len(self.freqgrid)):
            self.plot(stokes,component,iquv,ich,True,clim=clim)
            time.sleep(0.5)
        
    def plotcut(self,stokes='I',component='pow',iquv=[1,0,0,0],ich=0,doclf=True,clim=[None,None],dashed='',theta=0):
        R2arcmin=180.0/np.pi*60
        if (self.ApertureMap!=None):
            ich=0#produce beam from aperture, sampled on grid
            # ll,mm,vis,beamoffsets,Gxgainlist,Gygainlist,Dxgainlist,Dygainlist=dataset.dataset.getvisslice(dataset.freqMHz,self.dMHz,self.scanantennaname,self.trackantennanames,0)
            newx=np.linspace(self.margin[0],self.margin[-1],self.gridsize)
            newy=np.zeros(self.gridsize)
            costheta=np.cos(theta*np.pi/180.0)
            sintheta=np.sin(theta*np.pi/180.0)
            #note here assumed (possibly incorrectly! that offsets are zero)
            ox=newx#-offsets[ibeam][0]
            oy=newy#-offsets[ibeam][1]
            xx=ox*costheta+oy*sintheta
            yy=-ox*sintheta+oy*costheta
            localGx,localGy,localDx,localDy=self.ApertureMap.getmodelbeam(xx*D2R,yy*D2R)
            localGx=localGx.reshape(-1)
            localGy=localGy.reshape(-1)
            localDx=localDx.reshape(-1)
            localDy=localDy.reshape(-1)
        else:
            ll,mm,vis,beamoffsets,Gxgainlist,Gygainlist,Dxgainlist,Dygainlist=self.dataset.getvisslice(self.freqgrid[ich],self.dMHz,self.scanantennaname,self.trackantennanames)
            wavelength=self.dataset.speedoflight/(self.freqgrid[ich]*1e6)
            dl,dm,dn=np.array(self.xyzoffsets)*(np.pi*2.0)/wavelength
            vis=vis*np.exp(1j*(dl*(ll)+dm*(mm)+dn*np.sqrt(1.0-(ll)**2-(mm)**2) ))
            if (len(vis)==1):
                beam=self.interpline(ll/D2R,mm/D2R,vis,self.beamoffsetapplied[ich],theta)
                localGx,localGy,localDx,localDy=beam[0],0*beam[0],0*beam[0],0*beam[0]
            elif (len(vis)==2):
                localGx,localDx=self.interpline(ll/D2R,mm/D2R,vis,self.beamoffsetapplied[ich],theta)
                localGy,localDy=self.interpline(mm/D2R,-ll/D2R,vis,self.beamoffsetapplied[ich],theta)
            else:
                localGx,localGy,localDx,localDy=self.interpline(ll/D2R,mm/D2R,vis,self.beamoffsetapplied[ich],theta)
        if (doclf):
            plt.clf()
        if (stokes=='I'):
            Quant=0.5*(np.abs(localGx)**2+np.abs(localGy)**2+np.abs(localDx)**2+np.abs(localDy)**2)
            Quant=np.sqrt(Quant)
        elif (stokes=='Gx'):
            Quant=localGx
        elif (stokes=='Gy'):
            Quant=localGy
        elif (stokes=='Dx'):
            Quant=localDx
        elif (stokes=='Dy'):
            Quant=localDy
        elif (stokes=='instrumental'):
            E_xx= localGx
            E_xy= localDy
            E_yx= localDx
            E_yy= localGy
            unpolI = 0.5 * (np.abs(E_xx) ** 2 + np.abs(E_xy) ** 2 + np.abs(E_yx) ** 2 + np.abs(E_yy) ** 2)
            unpolQ = 0.5 * (np.abs(E_xx) ** 2 + np.abs(E_xy) ** 2 - np.abs(E_yx) ** 2 - np.abs(E_yy) ** 2)
            unpolU = (E_xx * E_yx.conj() + E_xy * E_yy.conj()).real
            unpolV = (E_xx * E_yx.conj() + E_xy * E_yy.conj()).imag
            instrumental=np.sqrt(np.abs(unpolQ)**2+np.abs(unpolU)**2+np.abs(unpolV)**2)/np.abs(unpolI)
            Quant=100*instrumental
            
        Quant=Quant.reshape(-1)
        #note Quant is a voltage quantity
                        
        #assumes origin at center of grid
        if (component=='pow'):            
            plt.plot(np.linspace(self.margin[0],self.margin[-1],self.gridsize),20.0*np.log10(np.abs(Quant)))
            plt.axis('tight')
            plt.title('Power beam cut for %s'%(os.path.basename(self.dataset if (type(self.dataset)==str) else self.filename))+':'+self.scanantennaname+' '+str(self.freqgrid[ich])+'MHz')
            plt.xlabel('degrees')
            plt.ylabel('Power')
        elif (component=='amp' or component=='abs' or component=='mag'):
            plt.plot(np.linspace(self.margin[0],self.margin[-1],self.gridsize),np.abs(Quant))
            #x=np.linspace(self.margin[0],self.margin[-1],self.gridsize)
            sigma2fwhm=2.0 * np.sqrt(2.0 * np.log(2.0))
            sigma=(np.mean(self.beamwidthI[ich])/sigma2fwhm)*180.0/np.pi
            plt.plot(self.margin,np.sqrt(np.exp(-0.5*(self.margin/sigma)**2)),':k')
            plt.axis('tight')
            plt.title('Amplitude beam for %s'%(os.path.basename(self.dataset if (type(self.dataset)==str) else self.filename))+':'+self.scanantennaname+' '+str(self.freqgrid[ich])+'MHz')
            plt.xlabel('degrees')
            plt.ylabel('Amplitude')
        elif (component=='phase' or component=='arg' or component =='angle'):
            plt.plot(np.linspace(self.margin[0],self.margin[-1],self.gridsize),np.angle(Quant)/D2R)
            plt.axis('tight')
            plt.title('Phase beam for %s'%(os.path.basename(self.dataset if (type(self.dataset)==str) else self.filename))+':'+self.scanantennaname+' '+str(self.freqgrid[ich])+'MHz')
            plt.xlabel('degrees')
            plt.ylabel('Phase')
        elif (component=='real' or component=='re'):
            plt.plot(np.linspace(self.margin[0],self.margin[-1],self.gridsize),np.real(Quant))
            plt.axis('tight')
            plt.title('Real beam for %s'%(os.path.basename(self.dataset if (type(self.dataset)==str) else self.filename))+':'+self.scanantennaname+' '+str(self.freqgrid[ich])+'MHz')
            plt.xlabel('degrees')
            plt.ylabel('real')
        elif (component=='imag' or component=='im'):
            plt.plot(np.linspace(self.margin[0],self.margin[-1],self.gridsize),np.imag(Quant))
            plt.axis('tight')
            plt.title('Imag beam for %s'%(os.path.basename(self.dataset if (type(self.dataset)==str) else self.filename))+':'+self.scanantennaname+' '+str(self.freqgrid[ich])+'MHz')
            plt.xlabel('degrees')
            plt.ylabel('imag')
        
        plt.draw()
        return Quant
        
    #reads off/interpolate value of offset at freq 
    #the x value is taken from Gy, the y value is taken from Gx
    def offset(self,atfreq):
        #returns interpolated coordinate, and mean over freq
        sind=np.argsort(self.freqgrid)
        return [np.interp(atfreq,self.freqgrid[sind],self.beamoffsetGy[sind,0]),np.interp(atfreq,self.freqgrid[sind],self.beamoffsetGx[sind,1])],[np.mean(self.beamoffsetGy[:,0]),np.mean(self.beamoffsetGx[:,1])]
        
        
    def plot(self,stokes='I',component='pow',iquv=[1,0,0,0],ich=0,doclf=True,clim=[None,None],dashed='',forcepointingoffset=None,plotextras=True):
        extents=[self.margin[0],self.margin[-1],self.margin[0],self.margin[-1]]
        levels = np.linspace(-60.0, 0.0, 21)
        R2arcmin=180.0/np.pi*60
        if (doclf):
            plt.clf()
        if (stokes=='gain'):
            plt.subplot(2,2,1);
            self.plot('gaingx',component,doclf=False,dashed=dashed);
            plt.subplot(2,2,2);
            self.plot('gaindx',component,doclf=False,dashed=dashed);
            plt.subplot(2,2,3);
            self.plot('gaindy',component,doclf=False,dashed=dashed);
            plt.subplot(2,2,4);
            self.plot('gaingy',component,doclf=False,dashed=dashed);
            plt.legend([self.dataset.radialscan_allantenna[it] for it in self.dataset.trackantennas])
            #plt.legend(np.tile([self.dataset.radialscan_allantenna[it] for it in self.dataset.trackantennas],2))
            plt.gcf().text(0.5,0.975,component+' '+self.filename+': '+self.scanantennaname+' track:'+str(self.trackantennanames),horizontalalignment='center',verticalalignment='top')
            return
        if (stokes=='gaingx' or stokes=='gaingy' or stokes=='gaindx' or stokes=='gaindy'):            
            if (stokes=='gaingx'):
                quant=self.Gxgainlist[ich]
            elif (stokes=='gaingy'):
                quant=self.Gygainlist[ich]
            elif (stokes=='gaindx'):
                quant=self.Dxgainlist[ich]
            elif (stokes=='gaindy'):
                quant=self.Dygainlist[ich]
                
            for itrack in range(len(quant)):
                if (component=='pow'):
                    plt.plot(self.dataset.rawtime[self.dataset.time_range]-self.dataset.rawtime[self.dataset.time_range[0]],20.0*np.log10(np.abs(quant[itrack])),dashed)
                elif (component=='abs' or component=='mag' or component=='amp'):
                    plt.plot(self.dataset.rawtime[self.dataset.time_range]-self.dataset.rawtime[self.dataset.time_range[0]],np.abs(quant[itrack]),dashed)
                elif (component=='real'):
                    plt.plot(self.dataset.rawtime[self.dataset.time_range]-self.dataset.rawtime[self.dataset.time_range[0]],np.real(quant[itrack]),dashed)
                elif (component=='imag'):
                    plt.plot(self.dataset.rawtime[self.dataset.time_range]-self.dataset.rawtime[self.dataset.time_range[0]],np.imag(quant[itrack]),dashed)
                elif (component=='angle' or component=='phase'):
                    plt.plot(self.dataset.rawtime[self.dataset.time_range]-self.dataset.rawtime[self.dataset.time_range[0]],np.angle(quant[itrack])/D2R,dashed)
            plt.draw()
            return
        elif (stokes=='pointings'):#per trackantenna
            for itrack in range(len(self.beamoffsetlist[0])):
                plt.subplot(2,2,1)
                offGx=np.array(self.beamoffsetlist)[:,itrack,1,:]
                offGy=np.array(self.beamoffsetlist)[:,itrack,2,:]
                plt.plot(self.freqgrid,(offGx[:,0]-D2R*np.array(self.beamoffsetapplied)[:,0,0])*R2arcmin)
                plt.xlabel('frequency')
                plt.ylabel('Gx X pointing error [arcmin]')
                plt.subplot(2,2,2)
                plt.plot(self.freqgrid,(offGx[:,1]-D2R*np.array(self.beamoffsetapplied)[:,0,1])*R2arcmin)
                plt.xlabel('frequency')
                plt.ylabel('Gx Y pointing error [arcmin]')
                plt.subplot(2,2,3)
                plt.plot(self.freqgrid,(offGy[:,0]-D2R*np.array(self.beamoffsetapplied)[:,1,0])*R2arcmin)
                plt.xlabel('frequency')
                plt.ylabel('Gy X pointing error [arcmin]')
                plt.subplot(2,2,4)
                plt.plot(self.freqgrid,(offGy[:,1]-D2R*np.array(self.beamoffsetapplied)[:,1,1])*R2arcmin)
                plt.xlabel('frequency')
                plt.ylabel('Gy Y pointing error [arcmin]')
            plt.subplot(2,2,2)
            plt.legend([self.dataset.radialscan_allantenna[it] for it in self.dataset.trackantennas])
            fig=plt.gcf();
            fig.text(0.5,0.975,self.filename+': '+self.scanantennaname+' track:'+str(self.trackantennanames),horizontalalignment='center',verticalalignment='top')
            plt.draw()
            return
        elif (stokes=='pointing'):
            if (forcepointingoffset!=None):
                plt.subplot(2,2,1)
                plt.plot(self.freqgrid,(self.beamoffsetGx[:,0]-forcepointingoffset[0])*R2arcmin,'b')
                plt.plot(self.freqgrid,(self.beamoffsetGy[:,0]-forcepointingoffset[0])*R2arcmin,'r')
                plt.plot(self.freqgrid,(self.beamoffsetI[:,0]-forcepointingoffset[0])*R2arcmin,'g')
                plt.xlabel('frequency')
                plt.ylabel('X pointing error [arcmin]')
                plt.subplot(2,2,2)
                plt.plot(self.freqgrid,(self.beamoffsetGx[:,1]-forcepointingoffset[1])*R2arcmin,'b')
                plt.plot(self.freqgrid,(self.beamoffsetGy[:,1]-forcepointingoffset[1])*R2arcmin,'r')
                plt.plot(self.freqgrid,(self.beamoffsetI[:,1]-forcepointingoffset[1])*R2arcmin,'g')
                plt.xlabel('frequency')
                plt.ylabel('Y pointing error [arcmin]')
            else:
                plt.subplot(2,2,1)
                plt.plot(self.freqgrid,(self.beamoffsetGx[:,0]-D2R*np.array(self.beamoffsetapplied)[:,0,0])*R2arcmin,'b')
                plt.plot(self.freqgrid,(self.beamoffsetGy[:,0]-D2R*np.array(self.beamoffsetapplied)[:,1,0])*R2arcmin,'r')
                plt.plot(self.freqgrid,(self.beamoffsetI[:,0]-0.5*D2R*(np.array(self.beamoffsetapplied)[:,0,0]+np.array(self.beamoffsetapplied)[:,1,0]))*R2arcmin,'g')
                plt.xlabel('frequency')
                plt.ylabel('X pointing error [arcmin]')
                plt.subplot(2,2,2)
                plt.plot(self.freqgrid,(self.beamoffsetGx[:,1]-D2R*np.array(self.beamoffsetapplied)[:,0,1])*R2arcmin,'b')
                plt.plot(self.freqgrid,(self.beamoffsetGy[:,1]-D2R*np.array(self.beamoffsetapplied)[:,1,1])*R2arcmin,'r')
                plt.plot(self.freqgrid,(self.beamoffsetI[:,1]-0.5*D2R*(np.array(self.beamoffsetapplied)[:,0,1]+np.array(self.beamoffsetapplied)[:,1,1]))*R2arcmin,'g')
                plt.xlabel('frequency')
                plt.ylabel('Y pointing error [arcmin]')
            plt.subplot(2,2,3)
            plt.plot(self.freqgrid,self.beamwidthGx[:,0]*R2arcmin,'b')
            plt.plot(self.freqgrid,self.beamwidthGy[:,0]*R2arcmin,'r')
            plt.plot(self.freqgrid,self.beamwidthI[:,0]*R2arcmin,'g')
            plt.xlabel('frequency')
            plt.ylabel('X beam width [arcmin]')
            plt.subplot(2,2,4)
            plt.plot(self.freqgrid,self.beamwidthGx[:,1]*R2arcmin,'b')
            plt.plot(self.freqgrid,self.beamwidthGy[:,1]*R2arcmin,'r')
            plt.plot(self.freqgrid,self.beamwidthI[:,1]*R2arcmin,'g')
            plt.legend(['Gx','Gy','I'])
            plt.xlabel('frequency')
            plt.ylabel('Y beam width [arcmin]')
            fig=plt.gcf();
            fig.text(0.5,0.975,self.filename+': '+self.scanantennaname+' track:'+str(self.trackantennanames),horizontalalignment='center',verticalalignment='top')
            plt.draw()
            return
        elif (stokes=='beamwidth'):
            t=np.linspace(0,2.0*np.pi,180)
            x=0.5*np.sin(t)
            y=0.5*np.cos(t)
            for ifreq,freq in enumerate(self.freqgrid):
                plt.plot(self.beamwidthGx[ifreq,0]*x*R2arcmin,self.beamwidthGx[ifreq,1]*y*R2arcmin,'b')
                plt.plot(self.beamwidthGy[ifreq,0]*x*R2arcmin,self.beamwidthGy[ifreq,1]*y*R2arcmin,'r')
            plt.xlabel('Horizontal width [arcmin]')
            plt.ylabel('Vertical width [arcmin]')
            plt.title(self.filename+': '+self.scanantennaname+' beam width H (blue) and V (red) feed')
            return
        elif (stokes=='squint'):
            dx=(self.beamoffsetGx[:,0]-self.beamoffsetGy[:,0])*R2arcmin
            dy=(self.beamoffsetGx[:,1]-self.beamoffsetGy[:,1])*R2arcmin
            plt.plot(dx,dy,'.-')
            # for ifr,freq in enumerate(self.freqgrid):
            #     plt.text(dx[ifr],dy[ifr],'%d'%(freq))
            plt.xlabel('Horizontal squint [arcmin]')
            plt.ylabel('Vertical squint [arcmin]')
            plt.title(self.filename+': '+self.scanantennaname+' beam squint H feed wrt V feed')
            return
        elif (stokes=='squints'):#per trackantenna
            for itrack in range(len(self.beamoffsetlist[0])):
                offGx=np.array(self.beamoffsetlist)[:,itrack,1,:]
                offGy=np.array(self.beamoffsetlist)[:,itrack,2,:]
                plt.plot((offGx[:,0]-offGy[:,0])*R2arcmin,(offGx[:,1]-offGy[:,1])*R2arcmin,'.-')
            plt.legend([self.dataset.radialscan_allantenna[it] for it in self.dataset.trackantennas])
            plt.xlabel('Horizontal squint [arcmin]')
            plt.ylabel('Vertical squint [arcmin]')
            plt.title(self.filename+': '+self.scanantennaname+' beam squint H feed wrt V feed')
            return            
        elif (stokes=='squintcomp'):
            plt.plot((self.beamoffsetGy[:,0])*R2arcmin,(self.beamoffsetGx[:,1])*R2arcmin,'.-b')
            plt.xlabel('Horizontal [arcmin]')
            plt.ylabel('Vertical [arcmin]')
            plt.title(self.filename+': '+self.scanantennaname+' beam center')
            return
        elif (stokes=='squintcomps'):#per trackantenna
            for itrack in range(len(self.beamoffsetlist[0])):
                offGx=np.array(self.beamoffsetlist)[:,itrack,1,:]
                offGy=np.array(self.beamoffsetlist)[:,itrack,2,:]
                plt.plot((offGy[:,0])*R2arcmin,(offGx[:,1])*R2arcmin,'.-')
            plt.legend([self.dataset.radialscan_allantenna[it] for it in self.dataset.trackantennas])
            plt.xlabel('Horizontal [arcmin]')
            plt.ylabel('Vertical [arcmin]')
            plt.title(self.filename+': '+self.scanantennaname+' beam center')
            return
        elif (stokes=='instrumental'):
            E_xx= self.Gy[ich]
            E_xy= self.Dy[ich]
            E_yx= self.Dx[ich]
            E_yy= self.Gx[ich]
            unpolI = 0.5 * (np.abs(E_xx) ** 2 + np.abs(E_xy) ** 2 + np.abs(E_yx) ** 2 + np.abs(E_yy) ** 2)
            unpolQ = 0.5 * (np.abs(E_xx) ** 2 + np.abs(E_xy) ** 2 - np.abs(E_yx) ** 2 - np.abs(E_yy) ** 2)
            unpolU = (E_xx * E_yx.conj() + E_xy * E_yy.conj()).real
            unpolV = (E_xx * E_yx.conj() + E_xy * E_yy.conj()).imag
            instrumental=np.sqrt(np.abs(unpolQ)**2+np.abs(unpolU)**2+np.abs(unpolV)**2)/np.abs(unpolI)
            plt.imshow(100*instrumental,cmap='jet',extent=extents)
            plt.contour(np.abs(unpolI[:,:]),extent=extents,levels=[np.max(unpolI)/2.0],colors='k',linestyles='dashed')
            return instrumental            
        elif (stokes=='mueller' or stokes=='jones' or stokes=='IQUV'):
            E_xx= self.Gy[ich]
            E_xy= self.Dy[ich]
            E_yx= self.Dx[ich]
            E_yy= self.Gx[ich]

            # Calculate Jones and Mueller matrices from voltage patterns of feeds
            # Form conjugate of E-Jones matrix
            J_E_c = np.array([[E_xx, E_xy], [E_yx, E_yy]]).conj()
            # Form Kronecker product of J_E x J_E.conj()
            JJ_E = np.vstack([np.hstack([E_xx * J_E_c, E_xy * J_E_c]),
                             np.hstack([E_yx * J_E_c, E_yy * J_E_c])])
            # Coherency -> Stokes transform
            stokesFromCoh = np.array([[1,  0,  0,  1],
                                      [1,  0,  0, -1],
                                      [0,  1,  1,  0],
                                      [0, -1j, 1j, 0]], dtype='complex128')
            # Stokes -> coherency transform (inverse of above)
            cohFromStokes = 0.5 * np.array([[1,  1, 0,  0],
                                            [0,  0, 1,  1j],
                                            [0,  0, 1, -1j],
                                            [1, -1, 0,  0]], dtype='complex128')
            # Convert to Stokes coordinate frame to get E-Mueller matrix
            # A single-dish Mueller matrix is always real - the imag part is identically zero
            M_E = np.tensordot(np.tensordot(stokesFromCoh, JJ_E, axes=(1, 0)),
                               cohFromStokes, axes=(1, 0)).transpose([0, 3, 1, 2]).real
            #
            # Calculate full Stokes response to unity-power unpolarised source; checked same as if iquv=[1,0,0,0]
            # unpolI = 0.5 * (np.abs(E_xx) ** 2 + np.abs(E_xy) ** 2 + np.abs(E_yx) ** 2 + np.abs(E_yy) ** 2)
            # unpolQ = 0.5 * (np.abs(E_xx) ** 2 + np.abs(E_xy) ** 2 - np.abs(E_yx) ** 2 - np.abs(E_yy) ** 2)
            # unpolU = (E_xx * E_yx.conj() + E_xy * E_yy.conj()).real
            # unpolV = (E_xx * E_yx.conj() + E_xy * E_yy.conj()).imag
            # # Calculate full Stokes response to unity-power right-handed circularly polarised source (e.g. satellite) ; checked same as if iquv=[1,0,0,1]
            #check in 2023 suggests below is actually for LCP iquv[1,0,0,-1]:
            # rcpI = 0.5 * (np.abs(E_xx - 1.0j * E_xy) ** 2 + np.abs(E_yx - 1.0j * E_yy) ** 2)
            # rcpQ = 0.5 * (np.abs(E_xx - 1.0j * E_xy) ** 2 - np.abs(E_yx - 1.0j * E_yy) ** 2)
            # rcpU = ((E_xx - 1.0j * E_xy) * (E_yx - 1.0j * E_yy).conj()).real
            # rcpV = ((E_xx - 1.0j * E_xy) * (E_yx - 1.0j * E_yy).conj()).imag
            # lcpI = 0.5 * (np.abs(E_xx + 1.0j * E_xy) ** 2 + np.abs(E_yx + 1.0j * E_yy) ** 2)
            # lcpQ = 0.5 * (np.abs(E_xx + 1.0j * E_xy) ** 2 - np.abs(E_yx + 1.0j * E_yy) ** 2)
            # lcpU = ((E_xx + 1.0j * E_xy) * (E_yx + 1.0j * E_yy).conj()).real
            # lcpV = ((E_xx + 1.0j * E_xy) * (E_yx + 1.0j * E_yy).conj()).imag
            if (stokes=='IQUV'):
                IQUV=0*M_E[:,0,:,:]
                for irow,row in enumerate(['I','Q','U','V']):
                    for icol,col in enumerate(['I','Q','U','V']):
                        IQUV[irow,:,:]+=M_E[irow,icol,:,:]*iquv[icol]
                    a=plt.subplot(2,2,irow+1)
                    E=IQUV[irow,:,:];
                    E_dB=10.0*np.log10(np.abs(E))
                    # Remove -infs (keep above lowest contour level to prevent white patches in contourf)
                    E_dB[E_dB < levels.min() + 0.01] = levels.min() + 0.01
                    # Also keep below highest contour level for the same reason
                    E_dB[E_dB > levels.max() - 0.01] = levels.max() - 0.01
                    cset = plt.contourf(self.margin, self.margin, E_dB, levels)
                    matplotlib.rc('contour', negative_linestyle='solid')
                    # Positive beam patterns are straightforward
                    if E.min() >= 0.0:
                        plt.contour(self.margin, self.margin, E_dB, levels, colors='k', linewidths=0.5)
                    else:
                        # Indicate positive parts with solid contours
                        E_dB_pos = E_dB.copy()
                        E_dB_pos[E < 0.0] = levels.min() + 0.01
                        plt.contour(self.margin, self.margin, E_dB_pos, levels, colors='k', linewidths=0.5)
                        # Indicate negative parts with dashed contours
                        E_dB_neg = E_dB.copy()
                        E_dB_neg[E > 0.0] = levels.min() + 0.01
                        matplotlib.rc('contour', negative_linestyle='dashed')
                        plt.contour(self.margin, self.margin, E_dB_neg, levels, colors='k', linewidths=0.5)
                    if (irow==0):
                        a.set_ylabel('I', rotation='horizontal')
                        a.set(xlabel='', xticks=[])
                    elif (irow==1):
                        a.set_ylabel('Q', rotation='horizontal')
                        a.set(xlabel='', xticks=[], yticks=[])
                    elif (irow==2):
                        a.set_ylabel('U', rotation='horizontal')
                        a.set(xlabel='l')
                    else:
                        a.set_ylabel('V', rotation='horizontal')
                        a.set(xlabel='l',yticks=[])
                    plt.axis('image')    
                plt.gcf().text(0.5, 0.925, 'Stokes response for Target Stokes IQUV=[%g,%g,%g,%g]'%(iquv[0],iquv[1],iquv[2],iquv[3]), ha='center', size='x-large')
                plt.subplots_adjust(left=0.1, right=0.85, bottom=0.1, top=0.9, wspace=0.1, hspace=0.05)
                plt.colorbar(cset, cax=plt.axes([0.895, 0.1, 0.02, 0.8]), format='%d')
                plt.gcf().text(0.96, 0.5, 'dB')
                # plt.gcf().set_size_inches((7.0, 6.0))                
                plt.draw()
                return IQUV
            elif (stokes=='jones'):
                jones= np.array([[E_xx, E_xy], [E_yx, E_yy]])
                for irow in range(2):
                    for icol in range(2):
                        a=plt.subplot(2,2,icol+irow*2+1)
                        E=jones[irow,icol,:,:];
                        E_dB=10.0*np.log10(np.abs(E))
                        # Remove -infs (keep above lowest contour level to prevent white patches in contourf)
                        E_dB[E_dB < levels.min() + 0.01] = levels.min() + 0.01
                        # Also keep below highest contour level for the same reason
                        E_dB[E_dB > levels.max() - 0.01] = levels.max() - 0.01
                        cset = plt.contourf(self.margin, self.margin, E_dB, levels)
                        matplotlib.rc('contour', negative_linestyle='solid')
                        # Positive beam patterns are straightforward
                        if E.real.min() >= 0.0:
                            plt.contour(self.margin, self.margin, E_dB, levels, colors='k', linewidths=0.5)
                        else:
                            # Indicate positive parts with solid contours
                            E_dB_pos = E_dB.copy()
                            E_dB_pos[E.real < 0.0] = levels.min() + 0.01
                            plt.contour(self.margin, self.margin, E_dB_pos, levels, colors='k', linewidths=0.5)
                            # Indicate negative parts with dashed contours
                            E_dB_neg = E_dB.copy()
                            E_dB_neg[E.real > 0.0] = levels.min() + 0.01
                            matplotlib.rc('contour', negative_linestyle='dashed')
                            plt.contour(self.margin, self.margin, E_dB_neg, levels, colors='k', linewidths=0.5)
                        if (irow==0 and icol==0):
                            a.set_ylabel('Gx', rotation='horizontal')
                            a.set(xlabel='', xticks=[])
                        elif (irow==0 and icol==1):
                            a.set_ylabel('Dx', rotation='horizontal')
                            a.set(xlabel='', xticks=[], yticks=[])
                        elif (irow==1 and icol==0):
                            a.set_ylabel('Dy', rotation='horizontal')
                            a.set(xlabel='l')
                        else:
                            a.set_ylabel('Gy', rotation='horizontal')
                            a.set(xlabel='l',yticks=[])
                        plt.axis('image')    
                plt.gcf().text(0.5, 0.925, 'Jones matrix', ha='center', size='x-large')
                plt.subplots_adjust(left=0.1, right=0.85, bottom=0.1, top=0.9, wspace=0.1, hspace=0.05)
                plt.colorbar(cset, cax=plt.axes([0.895, 0.1, 0.02, 0.8]), format='%d')
                plt.gcf().text(0.96, 0.5, 'dB')
                # plt.gcf().set_size_inches((7.0, 6.0))                
                plt.draw()
                return jones
            else:
                for irow,row in enumerate(['I','Q','U','V']):
                    for icol,col in enumerate(['I','Q','U','V']):
                        a=plt.subplot(4,4,icol+irow*4+1)
                        E=M_E[irow,icol,:,:]
                        E_dB=10.0*np.log10(np.abs(E))
                        # Remove -infs (keep above lowest contour level to prevent white patches in contourf)
                        E_dB[E_dB < levels.min() + 0.01] = levels.min() + 0.01
                        # Also keep below highest contour level for the same reason
                        E_dB[E_dB > levels.max() - 0.01] = levels.max() - 0.01
                        cset = plt.contourf(self.margin, self.margin, E_dB, levels)
                        matplotlib.rc('contour', negative_linestyle='solid')
                        # Positive beam patterns are straightforward
                        if E.min() >= 0.0:
                            plt.contour(self.margin, self.margin, E_dB, levels, colors='k', linewidths=0.5)
                        else:
                            # Indicate positive parts with solid contours
                            E_dB_pos = E_dB.copy()
                            E_dB_pos[E < 0.0] = levels.min() + 0.01
                            plt.contour(self.margin, self.margin, E_dB_pos, levels, colors='k', linewidths=0.5)
                            # Indicate negative parts with dashed contours
                            E_dB_neg = E_dB.copy()
                            E_dB_neg[E > 0.0] = levels.min() + 0.01
                            matplotlib.rc('contour', negative_linestyle='dashed')
                            plt.contour(self.margin, self.margin, E_dB_neg, levels, colors='k', linewidths=0.5)
                        if irow!=3:
                            a.set(xlabel='', xticks=[])
                        else:
                            if (icol==0):
                                a.set(xlabel='I')
                            elif (icol==1):
                                a.set(xlabel='Q')
                            elif (icol==2):
                                a.set(xlabel='U')
                            else:
                                a.set(xlabel='V')
                        if icol!=0:
                            a.set(ylabel='', yticks=[])
                        else:
                            if (irow==0):
                                a.set_ylabel('I', rotation='horizontal')
                            elif (irow==1):
                                a.set_ylabel('Q', rotation='horizontal')
                            elif (irow==2):
                                a.set_ylabel('U', rotation='horizontal')
                            else:
                                a.set_ylabel('V', rotation='horizontal')
                        plt.axis('image')
                plt.gcf().text(0.5, 0.925, 'Beam Mueller Matrix', ha='center', size='x-large')
                plt.subplots_adjust(left=0.1, right=0.85, bottom=0.1, top=0.9, wspace=0.1, hspace=0.05)
                plt.colorbar(cset, cax=plt.axes([0.895, 0.1, 0.02, 0.8]), format='%d')
                plt.gcf().text(0.96, 0.5, 'dB')                
                plt.draw()
                return M_E
        if (stokes=='I'):
            Quant=0.5*(np.abs(self.Gx)**2+np.abs(self.Gy)**2+np.abs(self.Dx)**2+np.abs(self.Dy)**2)
            Quant=np.sqrt(Quant)
        elif (stokes=='Gx'):
            Quant=self.Gx
        elif (stokes=='Gy'):
            Quant=self.Gy
        elif (stokes=='Dx'):
            Quant=self.Dx
        elif (stokes=='Dy'):
            Quant=self.Dy
        elif (stokes=='mI'):
            Quant=0.5*(np.abs(self.mGx)**2+np.abs(self.mGy)**2+np.abs(self.mDx)**2+np.abs(self.mDy)**2)
            Quant=np.sqrt(Quant)
        elif (stokes=='mGx'):
            Quant=self.mGx
        elif (stokes=='mGy'):
            Quant=self.mGy
        elif (stokes=='mDx'):
            Quant=self.mDx
        elif (stokes=='mDy'):
            Quant=self.mDy
        #IQuant=np.sqrt(np.abs(self.Gx)**2 + np.abs(self.Gy)**2 + np.abs(self.Dx)**2 + np.abs(self.Dy)**2)/2.0
        if (stokes[0]=='m'):
            IQuant=(np.abs(self.mGx)+np.abs(self.mGy))/2.0
        else:
            IQuant=(np.abs(self.Gx)+np.abs(self.Gy))/2.0
        if (component=='pow'):
            im=plt.imshow(20.0*np.log10(np.abs(Quant[ich,:,:])),extent=extents,cmap=self.colmap,origin='lower',vmin=clim[0],vmax=clim[1])
            if (plotextras):
                plt.contour(np.abs(IQuant[ich,:,:]),extent=extents,levels=[1.0/np.sqrt(2.0)],colors='k',linestyles='dashed')            
                self.plotoffset(ich)
            plt.axis('tight')
            cb=plt.colorbar(im)
            cb.set_label('dB')
            plt.title('Power beam for %s'%(os.path.basename(self.dataset if (type(self.dataset)==str) else self.filename))+':'+self.scanantennaname+' '+str(self.freqgrid[ich])+'MHz')
            plt.xlabel('degrees')
            plt.ylabel('degrees')
        elif (component=='amp' or component=='abs' or component=='mag'):
            im=plt.imshow(np.abs(Quant[ich,:,:]),extent=extents,cmap=self.colmap,origin='lower',vmin=clim[0],vmax=clim[1])
            if (plotextras):
                plt.contour(np.abs(IQuant[ich,:,:]),extent=extents,levels=[1.0/np.sqrt(2.0)],colors='k',linestyles='dashed')            
                self.plotoffset(ich)
            plt.axis('tight')
            plt.colorbar(im)
            plt.title('Amplitude beam for %s'%(os.path.basename(self.dataset if (type(self.dataset)==str) else self.filename))+':'+self.scanantennaname+' '+str(self.freqgrid[ich])+'MHz')
            plt.xlabel('degrees')
            plt.ylabel('degrees')
        elif (component=='phase' or component=='arg' or component =='angle'):
            im=plt.imshow(np.angle(Quant[ich,:,:])/D2R,extent=extents,cmap=self.colmap,origin='lower',vmin=clim[0],vmax=clim[1])
            if (plotextras):
                plt.contour(np.abs(IQuant[ich,:,:]),extent=extents,levels=[1.0/np.sqrt(2.0)],colors='k',linestyles='dashed')            
                self.plotoffset(ich)
            plt.axis('tight')
            cb=plt.colorbar(im)
            cb.set_label('deg')
            plt.title('Phase beam for %s'%(os.path.basename(self.dataset if (type(self.dataset)==str) else self.filename))+':'+self.scanantennaname+' '+str(self.freqgrid[ich])+'MHz')
            plt.xlabel('degrees')
            plt.ylabel('degrees')
        elif (component=='real' or component=='re'):
            im=plt.imshow(np.real(Quant[ich,:,:]),extent=extents,cmap=self.colmap,origin='lower',vmin=clim[0],vmax=clim[1])
            if (plotextras):
                plt.contour(np.abs(IQuant[ich,:,:]),extent=extents,levels=[1.0/np.sqrt(2.0)],colors='k',linestyles='dashed')            
                self.plotoffset(ich)
            plt.axis('tight')
            plt.colorbar(im)
            plt.title('Real beam for %s'%(os.path.basename(self.dataset if (type(self.dataset)==str) else self.filename))+':'+self.scanantennaname+' '+str(self.freqgrid[ich])+'MHz')
            plt.xlabel('degrees')
            plt.ylabel('degrees')
        elif (component=='imag' or component=='im'):
            im=plt.imshow(np.imag(Quant[ich,:,:]),extent=extents,cmap=self.colmap,origin='lower',vmin=clim[0],vmax=clim[1])
            if (plotextras):
                plt.contour(np.abs(IQuant[ich,:,:]),extent=extents,levels=[1.0/np.sqrt(2.0)],colors='k',linestyles='dashed')            
                self.plotoffset(ich)
            plt.axis('tight')
            plt.colorbar(im)
            plt.title('Imag beam for %s'%(os.path.basename(self.dataset if (type(self.dataset)==str) else self.filename))+':'+self.scanantennaname+' '+str(self.freqgrid[ich])+'MHz')
            plt.xlabel('degrees')
            plt.ylabel('degrees')
        
        if (im is not None):
            plt.gca().set_aspect('equal') 
            plt.gca().autoscale(tight=True) 
        plt.draw()
        return
    
    def tofits(self,stokes='I',component='pow',ich=None,filename=None):
        if (stokes=='I'):
            Quant=0.5*(np.abs(self.Gx)**2+np.abs(self.Gy)**2+np.abs(self.Dx)**2+np.abs(self.Dy)**2)
            Quant=np.sqrt(Quant)
        elif (stokes=='Gx'):
            Quant=self.Gx
        elif (stokes=='Gy'):
            Quant=self.Gy
        elif (stokes=='Dx'):
            Quant=self.Dx
        elif (stokes=='Dy'):
            Quant=self.Dy
        if (component=='pow'):
            im=20.0*np.log10(np.abs(Quant[:,:,:]))
        elif (component=='amp' or component=='abs' or component=='mag'):
            im=np.abs(Quant[:,:,:])
        elif (component=='phase' or component=='arg' or component =='angle'):
            im=np.angle(Quant[:,:,:])/D2R
        elif (component=='real' or component=='re'):
            im=np.real(Quant[:,:,:])
        elif (component=='imag' or component=='im'):
            im=np.imag(Quant[:,:,:])
        dx=np.float64(self.extent)/np.float64(self.gridsize)
        if (len(self.freqgrid)>1 and ich==None):
            thedMHz=np.float64(self.freqgrid[1]-self.freqgrid[0])
            thefreq0=self.freqgrid[0]
        elif (ich!=None):            
            thedMHz=1.0
            thefreq0=self.freqgrid[ich]
        else:
            thedMHz=1.0
            thefreq0=self.freqgrid[0]
        cards=[pyfits.Card('SIMPLE', True),pyfits.Card('BITPIX', 16),pyfits.Card('NAXIS', 3),pyfits.Card('NAXIS1', self.gridsize),pyfits.Card('NAXIS2', self.gridsize),pyfits.Card('NAXIS3', 2),pyfits.Card('BSCALE', 1.0),pyfits.Card('BZERO', 0.0),pyfits.Card('BUNIT', ' '),pyfits.Card('CRVAL1',0),pyfits.Card('CRVAL2',0),pyfits.Card('CRVAL3',thefreq0),pyfits.Card('CRPIX1',self.gridsize/2.0-1.0),pyfits.Card('CRPIX2',self.gridsize/2.0-1.0),pyfits.Card('CRPIX3',1),pyfits.Card('CDELT1',dx),pyfits.Card('CDELT2',dx),pyfits.Card('CDELT3',thedMHz),pyfits.Card('CUNIT1','DEG'),pyfits.Card('CUNIT2','DEG'),pyfits.Card('CUNIT3','MHZ'),pyfits.Card('CTYPE1','TARGETX'),pyfits.Card('CTYPE2','TARGETY'),pyfits.Card('CTYPE3','FREQ')]
        if (filename==None):
            filename=self.dataset.filenamebase+'_'+stokes+'_'+component+'.fits'
        if (ich==None):
            pyfits.writeto(filename,im,pyfits.Header(cards),overwrite=True);
        else:
            pyfits.writeto(filename,im[ich,:,:],pyfits.Header(cards),overwrite=True);
            
    

#Solving for gains first using all cross baselines, then fitting gaussians, needs more than 2 antennas, the more the better, and all baselines.

#solve for onaxis full polarisation jones matrix of tracking antenna with gain variation, and scanning antenna pointing offsets, 
#by fitting gaussians to Gx,Gy minising the fit and simultaneously minimize the total power in the Dx terms. One could assume that the onaxis Dx terms remain constant





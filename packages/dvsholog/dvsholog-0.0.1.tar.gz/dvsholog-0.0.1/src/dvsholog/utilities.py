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
from scikits.fitting import NonLinearLeastSquaresFit, PiecewisePolynomial1DFit, Spline2DScatterFit, GaussianFit, LinearLeastSquaresFit
import scikits.fitting as fitting
from scipy.interpolate import BSpline, splrep, splev
import astropy.io.fits as pyfits
import array
import scipy
import scipy.spatial
import scipy.io
import os,sys,time
import json
import base64
from multiprocessing import Process, Queue, cpu_count
from matplotlib import path
import katdal
import pickle
import optparse
from scipy.special import factorial, comb as binomial
import types
import copy
from katdal.sensordata import to_str
from .cffi_code import ffi, lib

D2R=np.pi/180.0

PY3 = sys.version_info[0] == 3

#msavez and mload replace np.savez and np.load
#  coded by Ludwig Schwardt, by email Thu, Mar 25, 2021
# See https://stackoverflow.com/a/27948073/942503
def numpy_to_json(obj):
    """Convert NumPy arrays to JSON objects and scalars to native types."""
    if isinstance(obj, np.ndarray):
        if obj.dtype == object:
            return obj.tolist()
        data_b64 = to_str(base64.b64encode(np.ascontiguousarray(obj).data))
        return dict(__ndarray__=data_b64, dtype=str(obj.dtype), shape=obj.shape)
    elif isinstance(obj, np.generic):
        return obj.item()
    else:
        raise TypeError('Object of type {} is not JSON serializable'
                        .format(obj.__class__.__name__))


# See https://stackoverflow.com/a/27948073/942503
def json_to_numpy(dct):
    """Reconstruct NumPy ndarray from JSON object / dict."""
    if isinstance(dct, dict) and '__ndarray__' in dct:
        data_b64 = dct['__ndarray__']
        if PY3:
            data_b64 = data_b64.encode()
        data = base64.b64decode(data_b64)
        return np.frombuffer(data, dct['dtype']).reshape(dct['shape'])
    return dct


def msavez(file, **kwargs):
    """Numpy savez alternative that replaces pickle with JSON and supports native strings."""
    out = {}
    for key in kwargs:
        x = np.asarray(kwargs[key])
        if x.dtype == object:
            # Turn non-scalar arrays into lists to get JSON encoded
            x = json.dumps(x.tolist(), default=numpy_to_json)
            # Always store JSON objects as Unicode strings, even on Python 2.
            # There is no Unicode in existing Py2 datasets, so it identifies these objects.
            if not PY3:
                x = x.decode()
        elif x.dtype.kind == 'U':
            # Always store normal strings as bytes, even on Python 3 (to_str will fix it)
            x = np.char.encode(x)
        out[key] = x
    np.savez(file, **out)


def mload(file):
    """Numpy load alternative that replaces pickle with JSON and supports native strings."""
    out = {}
    npz = np.load(file, allow_pickle=True, encoding='latin1')
    for key in npz:
        x = npz[key]
        if not x.ndim:
            kind = x.dtype.kind
            x = x.item()
            if kind == 'U':
                # Identify scalar Unicode array as a JSON string
                x = json.loads(x, object_hook=json_to_numpy)
        # Convert all strings to the native version
        out[key] = to_str(x)
    return out


#do not check if GPU available
dogpuidft=None
dogpuidftfull=None
dogpudft=None
dogpudftfull=None

#dva colour
def dvacolmap():
    ind=range(256)
    A=np.ones(256)
    R=np.interp(ind,np.array([0,55,143,237,284,328,368,514,607,703,792,847,889,937],dtype='float')*255.0/937.0,np.array([200, 200, 250, 252, 237, 183, 41,19, 25, 20, 3, 134, 118, 0],dtype='float')/255)[::-1]
    G=np.interp(ind,np.array([0,50,137,187,282,325,375,514,564,609,655,702,748,794,891,917,937],dtype='float')*255.0/937.0,np.array([200,9,13,154,236,251,252,150,169,169,153,123,29,20,15,3,0],dtype='float')/255)[::-1]
    B=np.interp(ind,np.array([0,50,163,188,282,325,379,514,570,612,661,746,800,891,937],dtype='float')*255.0/937.0,np.array([200,20,30,40,50,50,45,24,138,173,219,217,165,133,0],dtype='float')/255)[::-1]
    return np.array([R,G,B,A]).transpose()
    
#generates sqr colour map
def sqrcolmap():
    ind=range(256)
    A=np.ones(256)
    R=np.interp(ind,[0,74,123,255],[0,0,1,1])             #R 0 until 74, up to 1 at 123
    G=np.interp(ind,[0,12,38,123,183,255],[0,0,1,1,0,1])  #G 0 until 12, up to 1 until 38, then stay until 123, down to 0 at 183, up to 1 at 255
    B=np.interp(ind,[0,12,38,74,183,255],[0,1,1,0,0,1])   #B 0 up to 1 at 12, stay at 1 until 38, down to 0 at 73, stay at 0 until 183, up to 1 at 255
    return np.array([R,G,B,A]).transpose()

#dot product eg x.shape=[1000,2,2],y.shape=[1000,2,2] np.sum(np.transpose(x,(0,2,1))[:, :, :, np.newaxis] * y[:, :, np.newaxis, :], axis=-3)
#assumes shape eg [1,2,2] or [100,2,2] or [2,2]
def dodot(mxlist):
    rhs=mxlist[-1]
    if (len(rhs.shape)==2):
        rhs=rhs[np.newaxis]
    for lhs in mxlist[-2::-1]:
        if (len(lhs.shape)==2):
            lhs=lhs[np.newaxis]
        rhs=np.sum(np.transpose(lhs,(0,2,1))[:, :, :, np.newaxis] * rhs[:, :, np.newaxis, :], axis=-3)
    return rhs

#same as katpoint.projection._sphere_to_plane_common(az0=scanaz,el0=scanel,az=targetaz,el=targetel) with ll=ortho_x,mm=-ortho_y
def sphere_to_plane_holography(targetaz,targetel,scanaz,scanel):
    #produces direction cosine coordinates from scanning antenna azimuth,elevation coordinates
    #see _coordinate options.py for derivation
    ll=np.cos(targetel)*np.sin(targetaz-scanaz)
    mm=np.cos(targetel)*np.sin(scanel)*np.cos(targetaz-scanaz)-np.cos(scanel)*np.sin(targetel)
    return ll,mm
    
#NOT same as for katpoint.projection.plane_to_sphere because katpoint is solving for target azel instead of scan azel
def plane_to_sphere_holography(targetaz,targetel,ll,mm):
    scanaz=targetaz-np.arcsin(np.clip(ll/np.cos(targetel),-1.0,1.0))
    scanel=np.arcsin(np.clip((np.sqrt(1.0-ll**2-mm**2)*np.sin(targetel)+np.sqrt(np.cos(targetel)**2-ll**2)*mm)/(1.0-ll**2),-1.0,1.0))
    return scanaz,scanel

#print with aligned columns: insert spaces at $ such that column align at @ (remove these special characters before printing)
#if a number follows @ directly then align on nearby decimal point
def formatprint(stringlist):
    maxalign=0
    while maxalign != -1:
        align=[]
        maxalign=-1
        for line in stringlist:
            alignoffsets=line.replace('$','').split('@')
            if (len(alignoffsets)>1):
                if (alignoffsets[1][0].isdigit() or alignoffsets[1][0]=='-'):
                    off=alignoffsets[1].find('.')
                    align.append((1 if off<0 else off)+len(alignoffsets[0]))
                else:
                    align.append(len(alignoffsets[0]))
                if (align[-1]>maxalign):
                    maxalign=align[-1]
        for iline,line in enumerate(stringlist):
            if (len(align)>iline):
                splitline=line.split('@')
                splitline[0]=splitline[0].replace('$',' '*(maxalign-(align[iline])))
                if (len(splitline)>1):
                    splitline[1]=splitline[0]+splitline[1]
                    stringlist[iline]='@'.join(splitline[1:])
                else:
                    stringlist[iline]=splitline[0]
    for line in stringlist:
        print(line)

def unwrap(amp,phase,mask):
    shp=np.shape(phase)
    gridsize=np.int32(shp[0])
    twopi=2.0*np.pi
        
    amp=np.array(amp,dtype=np.double).reshape(-1)
    nmax=np.max(amp)
    if nmax==0 or not np.isfinite(nmax):
        print('Invalid amp')
        return phase
    phase=np.array(phase,dtype=np.double).reshape(-1)
    mask=np.array(mask,dtype=np.intc)+0
    mask[0,:]=1;mask[:,0]=1;mask[-1,:]=1;mask[:,-1]=1;
    mask=np.array(mask,dtype=np.intc).reshape(-1);
    ijp=np.argmax((amp*(mask==0)))
    mask[ijp]=2#set mask to classified
    initperimeter=np.array([ijp-1,ijp+1,ijp-gridsize,ijp+gridsize])
    mask[initperimeter]=3#set mask to perimeter
    sper=np.argsort(amp[initperimeter])
    lenperimeter=len(sper)
    flatperimeter=np.zeros(np.shape(mask),dtype=np.intc)
    flatperimeter[:lenperimeter]=initperimeter[sper]
    pi=np.pi
    
    c_flatperimeter=ffi.from_buffer("int[]", flatperimeter, require_writable=True)
    c_amp=ffi.from_buffer("double[]", amp, require_writable=False)
    c_phase=ffi.from_buffer("double[]", phase, require_writable=True)
    c_mask=ffi.from_buffer("int[]", mask, require_writable=True)
    lib.c_unwrap(lenperimeter, c_flatperimeter, gridsize, c_amp, c_phase, c_mask, pi, twopi)
    return phase.reshape(shp)

#fits model to surface deflection
#expecting phase in radians
#xmag=1 implies prime focus; otherwise subreflector assumed
def flatphase(weight,phase,mask,blockdiameter,dishdiameter,mapsize,gridsize,wavelength,focallength,xmag,feedoffset=None,parabolaoffset=None,flatmode='flat',copol=None,crosspol=None,domiriad=True,externpathlengthlist=None,externxyzfeedoffsetsmmlist=None):
    try:
        x,y=np.meshgrid(np.linspace(-mapsize/2.0,mapsize/2.0,gridsize+1)[:-1],np.linspace(-mapsize/2.0,mapsize/2.0,gridsize+1)[:-1])
        xc,yc=np.meshgrid(np.linspace(-gridsize/2.0,gridsize/2.0,gridsize+1)[:-1],np.linspace(-gridsize/2.0,gridsize/2.0,gridsize+1)[:-1])
        x=x.reshape(-1)
        y=y.reshape(-1)
        xc=xc.reshape(-1)
        yc=yc.reshape(-1)
        if (parabolaoffset!=None):
            x-=parabolaoffset[0]
            y-=parabolaoffset[1]
            xc-=parabolaoffset[0]*gridsize/mapsize
            yc-=parabolaoffset[1]*gridsize/mapsize
        r=np.sqrt(x**2+y**2)
        rc=np.sqrt(xc**2+yc**2)
        if (rc[gridsize//2+gridsize*gridsize//2]==0):#should be the case
            rc[gridsize//2+gridsize*gridsize//2]=1#avoid division by 0
        else:
            rc[np.nonzero(rc==0)[0]]=1#foolproof avoid division by 0
        cellsize=mapsize/gridsize
        fp=focallength/cellsize
        
        xp=xc
        yp=yc
        rp=rc
        funcs=None
        q = rp / (fp * 2.0);
        s = 1.0 / (q * q + 1.0);
        #see 'small displacements in parabolic reflectors' by john ruze, 1969
        if (xmag==1.0):#prime focus
            xf = 2.0*(xp/rp)*q*s;
            yf = 2.0*(yp/rp)*q*s;
            zf = -(1.0 - q*q)*s;
            funcs=xp,yp,xf,yf,zf
        elif(xmag>0.0):#Cassegrain subreflector;miriad#this calculates offset for subreflector
            qp=q/xmag
            sp=1.0/(1.0+qp*qp)
            xf=2.0*(xp/rp)*(q*s-qp*sp)#cassegrain subreflector#miriad code this is qp*sp
            if domiriad:
                yf=2.0*(yp/rp)*(q*s-qp*qp)#cassegrain subreflector#miriad code this is qp*qp
            else:
                yf=2.0*(yp/rp)*(q*s-qp*sp)#cassegrain subreflector#miriad code this is qp*qp
            zf=-(1.0 - q*q)*s - (1.0 - qp*qp)*sp#cassegrain subreflector
            funcs=xp,yp,xf,yf,zf
        else:
            #Paper by Lamb in "Verification of Ruze Formulas By Comparison with Ray-Tracing" points out that Ruze's formulas are normalized 
            #to have zero path length on axis, and that that is not a suitable form if you wish to project to the reflector surfaces. 
            #The un-normalized path lengths, which are the actual path lengths from the aperture plane, are simply obtained be dropping the leading "1"s.
            qp=q/np.abs(xmag)
            sp=1.0/(1.0+qp*qp)
            xf = 2.0*(xp/rp)*qp*sp;#this calculates offset for feed (of cassegrain or gregorian antenna)
            yf = 2.0*(yp/rp)*qp*sp;
            zf = -(1.0 - qp*qp)*sp;
            axf = focallength*(rp/fp  +2.0*(xp/rp)*q*s)
            ayf = focallength*(rp/fp  +2.0*(yp/rp)*q*s)
            xfg=2.0*(xp/rp)*(q*s+qp*sp)#gregorian subreflector
            yfg=2.0*(yp/rp)*(q*s+qp*sp)#gregorian subreflector
            zfg=-(1.0 - q*q)*s - (1.0 - qp*qp)*sp#gregorian subreflector
            xfc=2.0*(xp/rp)*(q*s-qp*sp)#cassegrain subreflector
            yfc=2.0*(yp/rp)*(q*s-qp*sp)#cassegrain subreflector
            axfg = np.abs(10)*(xp/rp)*(q*s+xmag*qp*sp)#abs(xmag)?
            ayfg = np.abs(10)*(yp/rp)*(q*s+xmag*qp*sp)
            iaxfg = np.abs(10)*(xp/rp)*(q*s+1.0/xmag*qp*sp)
            iayfg = np.abs(10)*(yp/rp)*(q*s+1.0/xmag*qp*sp)
            funcs=xp,yp,xf,yf,zf,xfg,yfg,zfg,axfg,ayfg,iaxfg,iayfg
            #debug
    
        if (flatmode=='funcs'):
            return funcs

        # valid=np.nonzero(~np.array(mask.reshape(-1),dtype='bool'))[0]#note ~ does not work correctly on integer array, only on bool
        valid=np.nonzero(~np.logical_or(np.array(mask.reshape(-1),dtype='bool'),weight.reshape(-1)==0))[0]#note ~ does not work correctly on integer array, only on bool
        #original valid=np.nonzero((r<blockdiameter/2.0)+(r>dishdiameter/2.0)==0)[0]
        R=np.zeros([6])
        D=np.zeros([6,6])
        wt=weight.reshape(-1)+0#because python sux
        wt/=np.max(wt)
        ph=phase.reshape(-1)*180.0/np.pi

        if (feedoffset is not None):#applies supplied feedoffset to phase
            X=np.array([np.ones(np.shape(xp)),xp,yp,xf,yf,zf]).transpose()
            initmodel=np.dot(X,np.array([0,0,0,feedoffset[0],feedoffset[1],feedoffset[2]])/(1000*wavelength/360.0));
            ph-=initmodel
            xf*=0.0#disable feed offset component in calculation
            yf*=0.0
            zf*=0.0
        else:
            initmodel=0
        if externpathlengthlist is not None and externxyzfeedoffsetsmmlist is not None:
            # externpathlengthlist=[dft.unwrappedphasemap*dft.wavelength/(2.0*np.pi) for dft in dfts]
            # externxyzfeedoffsetsmmlist=xyzfeedoffsets=[[0,0,0],[0,2,0],[0,0,2]]            
            # pathlength=wavelength*unwrapped_phase_rad/(2.0*np.pi)#in meters
            # externoxyz=np.array([[1.,xyz[0],xyz[1],xyz[2]] for xyz in externxyzfeedoffsetsmmlist]).T#[4xm] where m is number of supplied equations
            externoxyz=np.array([np.r_[xyz,1.] for xyz in externxyzfeedoffsetsmmlist]).T#[4xm] where m is number of supplied equations
            externpath=np.array([path.reshape(-1) for path in externpathlengthlist]).T#[gsgsxm]
            normalisedpath=np.dot(externpath,np.linalg.pinv(externoxyz))
            newfuncs=[normalisedpath[:,i]*1000 for i in range(normalisedpath.shape[1])]#in meters
            # comment only: xf,yf,zf,phoff=[normalisedpath[:,i].reshape([gridsize,gridsize])/wavelength*2.*np.pi*180./np.pi for i in range(normalisedpath.shape[1])]#in degrees
            # xf,yf,zf,phoff=xf.reshape(-1),yf.reshape(-1),zf.reshape(-1),phoff.reshape(-1)
            allfuncs=[np.ones(xp.shape),xp,yp]
            allfuncs.extend(newfuncs)
            W=np.sqrt(np.abs(wt[valid]))
            X=np.array([fun[valid] for fun in allfuncs]).transpose()
            rv=np.linalg.lstsq(W[:,np.newaxis]*X,W*ph[valid])
            x_=rv[0]
            vx=0*x_#not calculated
            X=np.array(allfuncs).transpose()
            model=np.dot(X,x_)
            funcs=allfuncs[1:]
        elif (0):#equivalent to below without calculation of stdev
            W=np.sqrt(np.abs(wt[valid]))
            X=np.array([np.ones(np.shape(xp[valid])),xp[valid],yp[valid],xf[valid],yf[valid],zf[valid]]).transpose()
            rv=np.linalg.lstsq(W[:,np.newaxis]*X,W*ph[valid])
            x_=rv[0]
            vx=0*x_#not calculated
            X=np.array([np.ones(np.shape(xp)),xp,yp,xf,yf,zf]).transpose()
            model=np.dot(X,x_);
        elif (flatmode=='feed'):#equivalent to below with calculation of stdev
            print('flatmode=feed')
            W=np.sqrt(np.abs(wt[valid]))
            X=np.array([xf[valid],yf[valid],zf[valid]]).transpose()
            fitter=fitting.LinearLeastSquaresFit()
            fitter.fit(np.transpose(X),np.transpose(ph[valid]),(np.shape(X)[1]**2)/W)
            x_=np.r_[0,0,0,fitter.params];
            vx=np.r_[0,0,0,np.diag(fitter.cov_params)]#there is still some scale factor discrepancy here
            X=np.array([np.ones(np.shape(xp)),xp,yp,xf,yf,zf]).transpose()
            model=np.dot(X,x_);
        elif (flatmode=='feed pointing'):#equivalent to below with calculation of stdev
            print('flatmode=feed pointing')
            W=np.sqrt(np.abs(wt[valid]))
            X=np.array([np.ones(np.shape(xp[valid])),xp[valid],yp[valid],xf[valid],yf[valid],zf[valid]]).transpose()
            fitter=fitting.LinearLeastSquaresFit()
            fitter.fit(np.transpose(X),np.transpose(ph[valid]),(np.shape(X)[1]**2)/W)
            x_=fitter.params;
            vx=np.diag(fitter.cov_params)#there is still some scale factor discrepancy here
            X=np.array([np.ones(np.shape(xp)),xp,yp,xf,yf,zf]).transpose()
            model=np.dot(X,x_);
        elif (flatmode=='pointing co cross' and (copol is not None) and (crosspol is not None)):#equivalent to below with calculation of stdev
            print('flatmode=pointing co cross')
            W=np.sqrt(np.abs(wt[valid]))
            X=np.array([np.ones(np.shape(xp[valid])),xp[valid],yp[valid],copol.reshape(-1)[valid],crosspol.reshape(-1)[valid]]).transpose()
            fitter=fitting.LinearLeastSquaresFit()
            fitter.fit(np.transpose(X),np.transpose(ph[valid]),(np.shape(X)[1]**2)/W)
            X=np.array([np.ones(np.shape(xp)),xp,yp,copol.reshape(-1),crosspol.reshape(-1)]).transpose()
            x_=fitter.params;
            model=np.dot(X,x_);
            x_=np.r_[fitter.params[:3],0,0,0];
            vx=np.r_[np.diag(fitter.cov_params[:3]),0,0,0]#there is still some scale factor discrepancy here        
        elif (flatmode=='feed pointing co cross' and (copol is not None) and (crosspol is not None)):#equivalent to below with calculation of stdev
            print('flatmode=feed pointing co cross')
            W=np.sqrt(np.abs(wt[valid]))
            X=np.array([np.ones(np.shape(xp[valid])),xp[valid],yp[valid],xf[valid],yf[valid],zf[valid],copol.reshape(-1)[valid],crosspol.reshape(-1)[valid]]).transpose()
            fitter=fitting.LinearLeastSquaresFit()
            fitter.fit(np.transpose(X),np.transpose(ph[valid]),(np.shape(X)[1]**2)/W)
            X=np.array([np.ones(np.shape(xp)),xp,yp,xf,yf,zf,copol.reshape(-1),crosspol.reshape(-1)]).transpose()
            x_=fitter.params;
            model=np.dot(X,x_);
            x_=fitter.params[:6];
            vx=np.diag(fitter.cov_params)[:6]#there is still some scale factor discrepancy here
        elif (flatmode=='pointingonly'):
            print('flatmode=pointingonly')
            W=np.sqrt(np.abs(wt[valid]))
            X=np.array([np.ones(np.shape(xp[valid])),xp[valid],yp[valid]]).transpose()
            fitter=fitting.LinearLeastSquaresFit()
            fitter.fit(np.transpose(X),np.transpose(ph[valid]),(np.shape(X)[1]**2)/W)
            x_=np.r_[fitter.params,0,0,0];
            vx=np.r_[np.diag(fitter.cov_params),0,0,0]#there is still some scale factor discrepancy here        
            X=np.array([np.ones(np.shape(xp)),xp,yp,xf,yf,zf]).transpose()
            model=np.dot(X,x_);
        elif (flatmode=='subreflectortilt'):
            print('flatmode=subreflectortilt')
            W=np.sqrt(np.abs(wt[valid]))
            X=np.array([np.ones(np.shape(xp[valid])),xp[valid],yp[valid],xf[valid],yf[valid],zf[valid],axfg[valid],ayfg[valid]]).transpose()
            rv=np.linalg.lstsq(W[:,np.newaxis]*X,W*ph[valid])
            x_=rv[0]
            vx=0*x_#not calculated
            X=np.array([np.ones(np.shape(xp)),xp,yp,xf,yf,zf,axfg,ayfg]).transpose()
            model=np.dot(X,x_);
        elif (1):
            print('flatmode=flat')
            W=np.sqrt(np.abs(wt[valid]))
            X=np.array([np.ones(np.shape(xp[valid])),xp[valid],yp[valid],xf[valid],yf[valid],zf[valid]]).transpose()
            fitter=fitting.LinearLeastSquaresFit()
            fitter.fit(np.transpose(X),np.transpose(ph[valid]),(np.shape(X)[1]**2)/W)
            x_=fitter.params;
            vx=np.diag(fitter.cov_params)#there is still some scale factor discrepancy here with std estimate
            X=np.array([np.ones(np.shape(xp)),xp,yp,xf,yf,zf]).transpose()
            model=np.dot(X,x_);

        newphase=copy.deepcopy(phase).reshape(-1)*180.0/np.pi;    
        newphase-=model+initmodel
        newphase=newphase.reshape([gridsize,gridsize]);
        phaseoffset=x_[0]#in degrees
        phaseoffsetstd=np.sqrt(vx[0])#in degrees
        phasegradient=np.array([x_[1],x_[2]])# in degrees per cell
        phasegradientstd=np.sqrt([vx[1],vx[2]])# in degrees per cell
        if (feedoffset==None):
            feedoffset=np.array([x_[3],x_[4],x_[5]])*1000*wavelength/360.0;#in mm
            feedoffsetstd=np.sqrt([vx[3],vx[4],vx[5]])*1000*wavelength/360.0;#stdev in mm
        else:
            feedoffset=np.array(feedoffset)
            feedoffsetstd=np.array([0,0,0]);#stdev in mm
    
        return newphase*np.pi/180.0,phaseoffset,phasegradient,feedoffset,phaseoffsetstd,phasegradientstd,feedoffsetstd,funcs
    except:
        print('Error evaluating flatphase')
        return phase,np.nan,np.array([np.nan,np.nan]),np.array([np.nan,np.nan,np.nan]),np.nan,np.array([np.nan,np.nan]),np.array([np.nan,np.nan,np.nan]),None

def getdeviation(phase_rad,mapsize,gridsize,wavelength,focallength,parabolaoffset=[0.0,0.0]):    
    x,y=np.meshgrid(np.linspace(-mapsize/2.0,mapsize/2.0,gridsize+1)[:-1],np.linspace(-mapsize/2.0,mapsize/2.0,gridsize+1)[:-1])
    if isinstance(parabolaoffset,type('')) and parabolaoffset == 'vgos focus ring':
        x=x.reshape(-1)
        y=y.reshape(-1)
        r=np.sqrt(x**2+y**2)-1.55/2.
    else:
        x=x.reshape(-1)-parabolaoffset[0]
        y=y.reshape(-1)-parabolaoffset[1]
        r=np.sqrt(x**2+y**2)
    pathlength=wavelength*phase_rad/(2.0*np.pi)#in meters
    deviation=pathlength/(4.0*focallength)*np.sqrt(r.reshape([gridsize,gridsize])**2+4.0*focallength**2)#in meters
    return deviation*1000.0#in millimeters

def putdeviation(deviation_mm,mapsize,gridsize,wavelength,focallength,parabolaoffset=[0.0,0.0]):
    deviation=deviation_mm/1000.0#mm to meters
    x,y=np.meshgrid(np.linspace(-mapsize/2.0,mapsize/2.0,gridsize+1)[:-1],np.linspace(-mapsize/2.0,mapsize/2.0,gridsize+1)[:-1])
    if isinstance(parabolaoffset,type('')) and parabolaoffset == 'vgos focus ring':
        x=x.reshape(-1)
        y=y.reshape(-1)
        r=np.sqrt(x**2+y**2)-1.55/2.
    else:
        x=x.reshape(-1)-parabolaoffset[0]
        y=y.reshape(-1)-parabolaoffset[1]
        r=np.sqrt(x**2+y**2)
    pathlength=deviation*(4.0*focallength)/np.sqrt(r.reshape([gridsize,gridsize])**2+4.0*focallength**2)#in meters
    phase_rad=pathlength*(2.0*np.pi)/wavelength
    return phase_rad

#calculates surface deviation on hyperboloid subreflector instead of mainreflector
def getcassegraindeviation(phase_rad,mapsize,gridsize,wavelength,designfeedparams,designellipsoidparams,parabolaoffset=[0.0,0.0]):
    x,y=np.meshgrid(np.linspace(-mapsize/2.0,mapsize/2.0,gridsize+1)[:-1],np.linspace(-mapsize/2.0,mapsize/2.0,gridsize+1)[:-1])
    x=x.reshape(-1)-parabolaoffset[0]
    y=y.reshape(-1)-parabolaoffset[1]
    r=np.sqrt(x**2+y**2)
    pathlength=wavelength*phase_rad/(2.0*np.pi)#in meters

    z0=designellipsoidparams[2]-designfeedparams[2]#such that bottom focus of ellipsoid is at origin
    rs=designellipsoidparams[3]
    zs=designellipsoidparams[5]
    z=np.sqrt(1+(r**2)/(rs**2))*zs+z0
    dz=((zs**2)*r)/((rs**2)*(z-z0))
    leng=np.sqrt(dz**2+1)
    deviation=pathlength*(leng*(r*dz-z))/(2.0*np.sqrt(r**2+z**2))#in meters
    return deviation*1000.0#in millimeters

def getweight(l,m):
    # t00=time.time()
    weight=np.zeros(len(l),dtype='float')
    v=scipy.spatial.Voronoi(np.array(list(zip(l,m))))
    minmaxrad=np.min([np.max(l),-np.min(l),np.max(m),-np.min(m)])
    rad=np.sqrt(l*l+m*m)
    imidrange=np.nonzero((rad>minmaxrad*0.3)*(rad<minmaxrad*0.9))[0]
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
    medianweight=np.nanmedian(weight[imidrange])
    if True:#use neighbours weight to fill in perimeter weights
        for i,ir in enumerate(v.point_region):
            if np.isnan(weight[i]):
                m0=np.nonzero(v.ridge_points[:,0]==i)[0]
                m1=np.nonzero(v.ridge_points[:,1]==i)[0]
                i_neigh=np.r_[v.ridge_points[m0,1],v.ridge_points[m1,0]]
                weight[i]=np.nanmean([weight[i_neigh]]) if (len(i_neigh)) else medianweight
    weight[np.nonzero(np.isnan(weight))[0]]=medianweight
    weight=weight/medianweight
    # t01=time.time()
    # print('Tesselation in %.1fs medianweight %f'%(t01-t00,medianweight))
    return weight

def c_cinnerdft(l,m,rebeam,imbeam,x,y,num,queue):
    aperturereal=np.zeros(x.shape,dtype='double').reshape(-1)
    apertureimag=np.zeros(x.shape,dtype='double').reshape(-1)
    c_rebeam=ffi.from_buffer("double[]", rebeam, require_writable=False)
    c_imbeam=ffi.from_buffer("double[]", imbeam, require_writable=False)
    c_aperturereal=ffi.from_buffer("double[]", aperturereal, require_writable=True)
    c_apertureimag=ffi.from_buffer("double[]", apertureimag, require_writable=True)
    c_l=ffi.from_buffer("double[]", l, require_writable=False)
    c_m=ffi.from_buffer("double[]", m, require_writable=False)
    c_x=ffi.from_buffer("double[]", x, require_writable=False)
    c_y=ffi.from_buffer("double[]", y, require_writable=False)

    lib.c_cpu_dft_code(c_aperturereal,c_apertureimag,c_l,c_m,c_rebeam,c_imbeam,c_x,c_y,len(x),len(l))
    queue.put([num,aperturereal,apertureimag])

def c_cinneridft(l,m,aperturereal,apertureimag,x,y,num,queue):
    rebeam=np.zeros(l.shape,dtype='double').reshape(-1)
    imbeam=np.zeros(l.shape,dtype='double').reshape(-1)

    c_rebeam=ffi.from_buffer("double[]", rebeam, require_writable=True)
    c_imbeam=ffi.from_buffer("double[]", imbeam, require_writable=True)
    c_aperturereal=ffi.from_buffer("double[]", aperturereal, require_writable=False)
    c_apertureimag=ffi.from_buffer("double[]", apertureimag, require_writable=False)
    c_l=ffi.from_buffer("double[]", l, require_writable=False)
    c_m=ffi.from_buffer("double[]", m, require_writable=False)
    c_x=ffi.from_buffer("double[]", x, require_writable=False)
    c_y=ffi.from_buffer("double[]", y, require_writable=False)

    lib.c_cpu_idft_code(c_aperturereal,c_apertureimag,c_l,c_m,c_rebeam,c_imbeam,c_x,c_y,len(x),len(l))
    queue.put([num,rebeam,imbeam])

def domultiidft(l,m,aperturemap,mapsize,gridsize,wavelength,nproc,aperturemapvalidindices=None):
    xmargin=np.linspace(-mapsize/2.0,mapsize/2.0,gridsize+1)[:-1]
    x,y=np.meshgrid(xmargin,xmargin)
    x=2.0*np.pi/wavelength*x.reshape(-1)
    y=2.0*np.pi/wavelength*y.reshape(-1)
    aperturereal=np.array(np.real(aperturemap),dtype='double')
    apertureimag=np.array(np.imag(aperturemap),dtype='double')
    beam=np.zeros(len(l),dtype='complex')
    if (aperturemapvalidindices is not None):
        x=x[aperturemapvalidindices]
        y=y[aperturemapvalidindices]
        aperturereal=aperturereal.reshape(-1)[aperturemapvalidindices]
        apertureimag=apertureimag.reshape(-1)[aperturemapvalidindices]
    ndata=len(beam)
    if (nproc>=ndata):
        nproc=ndata;
    print('Starting (double) Inverse Direct Fourier Transform using %d processes'%nproc)
    t0=time.time()
    limits=np.array(np.linspace(0,ndata,nproc+1,endpoint=True),dtype='int')
    startindex=limits[:-1]
    endindex=limits[1:]
    queue=Queue()
    
    if (1):
        procs=[]
        for num in range(nproc):
            currange=range(startindex[num],endindex[num])
            Process(target=c_cinneridft, args=(l[currange],m[currange],aperturereal,apertureimag,x,y,num,queue)).start()
        for num in range(nproc):
            qv=queue.get()
            currange=range(startindex[qv[0]],endindex[qv[0]])#beware num!=qv[0] necessarily because order could have changed
            beam[currange]=qv[1]+1j*qv[2]
        # psf=0.0
        # for num in range(nproc):
        #     qv=queue.get()
        #     aperturemap+=qv[1]
        #     psf+=qv[2]
    t1=time.time()
    print('iDFT time: %.1fs'%(t1-t0))
    return beam


#performs direct fourier transform onto a grid
#x,y in degrees, location of points for cbeam
#apextent in meters, gridsize number of pixels on side
def domultidft(l,m,beam,mapsize,gridsize,wavelength,nproc,aperturemapvalidindices=None):
    xmargin=np.linspace(-mapsize/2.0,mapsize/2.0,gridsize+1)[:-1]
    x,y=np.meshgrid(xmargin,xmargin)
    x=2.0*np.pi/wavelength*x.reshape(-1)
    y=2.0*np.pi/wavelength*y.reshape(-1)
    rebeam=np.array(np.real(beam),dtype='double')
    imbeam=np.array(np.imag(beam),dtype='double')
    if (aperturemapvalidindices is not None):
        x=x[aperturemapvalidindices]
        y=y[aperturemapvalidindices]

    ndata=len(beam)
    if (nproc>=ndata):
        nproc=ndata;
    print('Starting (double) Direct Fourier Transform using %d processes'%nproc)
    t0=time.time()
    limits=np.array(np.linspace(0,ndata,nproc+1,endpoint=True),dtype='int')
    startindex=limits[:-1]
    endindex=limits[1:]
    queue=Queue()
    
    if (1):
        procs=[]
        for num in range(nproc):
            currange=range(startindex[num],endindex[num])
            Process(target=c_cinnerdft, args=(l[currange],m[currange],rebeam[currange],imbeam[currange],x,y,num,queue)).start()
        aperturemap=np.zeros(gridsize*gridsize,dtype=np.complex128)
        if (aperturemapvalidindices is not None):
            for num in range(nproc):
                qv=queue.get()
                aperturemap[aperturemapvalidindices]+=qv[1]+1j*qv[2]
        else:
            for num in range(nproc):
                qv=queue.get()
                aperturemap+=qv[1]+1j*qv[2]
        # psf=0.0
        # for num in range(nproc):
        #     qv=queue.get()
        #     aperturemap+=qv[1]
        #     psf+=qv[2]
    t1=time.time()
    print('DFT time: %.1fs'%(t1-t0))
    return aperturemap.reshape([gridsize,gridsize])
    # return aperturemap/psf

def mintotalpower(params,g,d):
    re,im=params
    nd=d+(re+im*1j)*g
    return np.sum(np.abs(nd)**2)

def maxtotalpower(params,g,d,reim):
    re,im=params
    ng=g+(re+im*1j)*(d+reim*g)
    return -np.sum(np.abs(ng)**2)#minimize neg total power== maximise total power

def ellipsecost(params,x,y,f):
    x0,y0,rx,ry=params
    #adds up all the complex values inside ellipse, and maximize this value
    inside=np.nonzero((((x-x0)/(rx))**2+((y-y0)/(ry))**2)<1.0)[0]
    nett=np.abs(np.sum(f[inside]))#take absolute of complex summation
    return -nett#maximize nett=minimize -nett
    
def gaussianxydriftfit(params,indep):
    x,y,t,ngainintervals=indep
    gains=params[:ngainintervals*4]+1j*params[ngainintervals*4:ngainintervals*8]
    X1gains=gains[:ngainintervals]
    Y1gains=gains[ngainintervals:ngainintervals*2]
    X2gains=gains[ngainintervals*2:ngainintervals*3]
    Y2gains=gains[ngainintervals*3:ngainintervals*4]
    #Xx0,Xy0,Yx0,Yy0,Xsx,Xsy,Ysx,Ysy,rD1x,iD1x,rD1y,iD1y,rD2x,iD2x,rD2y,iD2y=params[ngainintervals*8:]
    Xx0,Xy0,Yx0,Yy0,Xsx,Xsy,Ysx,Ysy,rD2x,iD2x,rD2y,iD2y=params[ngainintervals*8:]

    D1x=X1gains[0]
    D1y=Y1gains[0]
    # D1x=rD1x+1j*iD1x
    # D1y=rD1y+1j*iD1y
    D2x=rD2x+1j*iD2x
    D2y=rD2y+1j*iD2y
    X1gains[0]=1.0
    Y1gains[0]=1.0

    g1xx=np.interp(t,np.linspace(t[0],t[-1],len(X1gains)),np.real(X1gains))+1j*np.interp(t,np.linspace(t[0],t[-1],len(X1gains)),np.imag(X1gains))
    g1yy=np.interp(t,np.linspace(t[0],t[-1],len(Y1gains)),np.real(Y1gains))+1j*np.interp(t,np.linspace(t[0],t[-1],len(Y1gains)),np.imag(Y1gains))
    g2xx=np.interp(t,np.linspace(t[0],t[-1],len(X2gains)),np.real(X2gains))+1j*np.interp(t,np.linspace(t[0],t[-1],len(X2gains)),np.imag(X2gains))
    g2yy=np.interp(t,np.linspace(t[0],t[-1],len(Y2gains)),np.real(Y2gains))+1j*np.interp(t,np.linspace(t[0],t[-1],len(Y2gains)),np.imag(Y2gains))
    
    Exx=(np.exp(-0.5*(((x-Xx0)/Xsx)**2+((y-Xy0)/Xsy)**2))**2)
    Eyy=(np.exp(-0.5*(((x-Yx0)/Ysx)**2+((y-Yy0)/Ysy)**2))**2)
    # Exy=rXY*(x-Xx0)*(y-Xy0)+1j*iXY*(x-Xx0)*(y-Xy0)
    # Eyx=rYX*(x-Yx0)*(y-Yy0)+1j*iYX*(x-Yx0)*(y-Yy0)
    Exy=0
    Eyx=0
    # Exy=rXY*(x-Xx0)*(y-Xy0)+r1XY*(x-Xx0)+r2XY*(y-Xy0)+1j*iXY*(x-Xx0)*(y-Xy0)+i1XY*(x-Xx0)+i2XY*(y-Xy0)
    # Eyx=rYX*(x-Yx0)*(y-Yy0)+r1YX*(x-Yx0)+r2YX*(y-Yy0)+1j*iYX*(x-Yx0)*(y-Yy0)+i1YX*(x-Yx0)+i2YX*(y-Yy0)
    
    Vxx=g1xx*(Exx*g2xx+Exy*g2xx*D2x)+g1xx*D1x*(Eyx*g2xx+Eyy*g2xx*D2x)
    Vxy=g1xx*(Exx*g2yy*D2y+Exy*g2yy)+g1xx*D1x*(Eyx*g2yy*D2y+Eyy*g2yy)
    Vyx=g1yy*D1y*(Exx*g2xx+Exy*g2xx*D2x)+g1yy*(Eyx*g2xx+Eyy*g2xx*D2x)
    Vyy=g1yy*D1y*(Exx*g2yy*D2y+Exy*g2yy)+g1yy*(Eyx*g2yy*D2y+Eyy*g2yy)
    
    return np.r_[np.real(Vxx),np.imag(Vxx),np.real(Vyy),np.imag(Vyy),np.real(Vxy),np.imag(Vxy),np.real(Vyx),np.imag(Vyx)]

#also solve for complex leakage components
#for o
#data should=zeros
#this is for one antenna, need to solve simultaneously for all track ants
def gaussleakagedrift(params,indep):
    x,y,t,xx,xy,yx,yy=indep
    x0=params[0]
    y0=params[1]
    sx=params[2]
    sy=params[3]
    dx=params[4]+1j*params[5]#repeated per trackantenna
    dy=params[6]+1j*params[7]#repeated per trackantenna
    gains=params[8:]         #repeated per trackantenna
    return (np.abs(xx+dx*xy+dy*yx+dx*dy*yy)/np.interp(t,np.linspace(t[0],t[-1],len(gains)),gains)-np.exp(-0.5*(((x-x0)/sx)**2+((y-y0)/sy)**2)))

#assumes all antennas have same time flags
def gaussleakagedriftall(params,indep):
    x,y,t,xx,xy,yx,yy=indep
    ntrack=len(xx)
    ngain=(len(params)-4)/ntrack-4
    modelresult=np.zeros(len(xx[0])*ntrack)
    for itrack in range(ntrack):
        modelresult[itrack*len(xx[0]):(itrack+1)*len(xx[0])]=gaussleakagedrift(np.r_[params[:4],params[4+itrack*(ngain+4):4+(itrack+1)*(ngain+4)]],[x,y,t,xx[itrack],xy[itrack],yx[itrack],yy[itrack]])
    return modelresult

def gaussdriftuvr(params,indep):
    x,y,t,u,v,resu,resv,resp=indep
    x0=params[0]
    y0=params[1]
    sx=params[2]
    sy=params[3]
    gains=params[4:]
    return (np.exp(-0.5*(((x-x0)/sx)**2+((y-y0)/sy)**2)))*np.exp(-0.5*((u/resu)**2+(v/resv)**2-(resp*u/resu)*(v/resv) ))* np.interp(t,np.linspace(t[0],t[-1],len(gains)),gains)

def gaussdrift(params,indep):
    x,y,t=indep
    x0=params[0]
    y0=params[1]
    sx=params[2]
    sy=params[3]
    gains=params[4:]
    return (np.exp(-0.5*(((x-x0)/sx)**2+((y-y0)/sy)**2))) * np.interp(t,np.linspace(t[0],t[-1],len(gains)),gains)

def weightedgaussdrift(params,indep):
    x,y,t,w=indep
    x0=params[0]
    y0=params[1]
    sx=params[2]
    sy=params[3]
    gains=params[4:]
    return w*(np.exp(-0.5*(((x-x0)/sx)**2+((y-y0)/sy)**2))) * np.interp(t,np.linspace(t[0],t[-1],len(gains)),gains)

def gauss(params,indep):
    x,y=indep
    x0=params[0]
    y0=params[1]
    sx=params[2]
    sy=params[3]
    gain=params[4]
    return gain*(np.exp(-0.5*(((x-x0)/sx)**2+((y-y0)/sy)**2)))

def beampow(params,indep):
    x,y=indep
    x0=params[0]
    y0=params[1]
    gain=params[2]
    asim=params[3]
    c1,c2,c3,c4,c5=params[4]*10e3,params[5]*10e7,params[6]*10e10,params[7]*10e13,params[8]*10e16
    r=(x-x0)**2+asim*(y-y0)**2
    return gain*(1.0+c1*r+c2*r**2+c3*r**3+c4*r**4+c5*r**5)

def beampowindep(params,indep):
    x,y=indep
    x0=params[0]
    y0=params[1]
    gain=params[2]
    a1,a2,a3,a4,a5=params[3],params[4],params[5],params[6],params[7]
    c1,c2,c3,c4,c5=params[8]*10e3,params[9]*10e7,params[10]*10e10,params[11]*10e13,params[12]*10e16
    r1=(x-x0)**2+a1*(y-y0)**2
    r2=(x-x0)**2+a2*(y-y0)**2
    r3=(x-x0)**2+a3*(y-y0)**2
    r4=(x-x0)**2+a4*(y-y0)**2
    r5=(x-x0)**2+a5*(y-y0)**2
    return gain*(1.0+c1*r1+c2*r2**2+c3*r3**3+c4*r4**4+c5*r5**5)

def beampowindepm(params,indep):
    x,y=indep
    x0=params[0]
    y0=params[1]
    gain=params[2]
    a1,a2,a3,a4,a5,a6,a7,a8,a9=params[3],params[4],params[5],params[6],params[7],params[8],params[9],params[10],params[11]
    c1,c2,c3,c4,c5,c6,c7,c8,c9=params[12]*10e3,params[13]*10e7,params[14]*10e10,params[15]*10e13,params[16]*10e16,params[17]*10e19,params[18]*10e20,params[19]*10e23,params[20]*10e26
    r1=(x-x0)**2+a1*(y-y0)**2
    r2=(x-x0)**2+a2*(y-y0)**2
    r3=(x-x0)**2+a3*(y-y0)**2
    r4=(x-x0)**2+a4*(y-y0)**2
    r5=(x-x0)**2+a5*(y-y0)**2
    r6=(x-x0)**2+a6*(y-y0)**2
    r7=(x-x0)**2+a7*(y-y0)**2
    r8=(x-x0)**2+a8*(y-y0)**2
    r9=(x-x0)**2+a9*(y-y0)**2
    return gain*(1.0+c1*r1+c2*r2**2+c3*r3**3+c4*r4**4+c5*r5**5+c6*r6**6+c7*r7**7+c8*r8**8+c9*r9**9)
        
#set data=zeros
#this optimization is done independently per track-scan antenna pair
#inverts rawGx,rawGy,rawDx,rawDy ensuring identity matrix at x0,y0 and subtracting Gaussian
def gaussfitinvertstokesI(params,indep):
    x,y,Gx,Gy,Dx,Dy,meanGxgain,meanGygain,meanDxgain,meanDygain,gxparams,gyparams,dxparams,dyparams,ncoeff,degree=indep#the raw values at coordinates
    x0=params[0]
    y0=params[1]
    sx=params[2]
    sy=params[3]
    #evaluate raw data function at x0,y0 (or interpolate)
    nmodelparams=ncoeff*2
    Gx0=polydrift(gxparams[:nmodelparams],[[x0],[y0],[0.0],ncoeff,degree])
    Gx0=Gx0[:1]+1j*Gx0[1:]
    Gy0=polydrift(gyparams[:nmodelparams],[[x0],[y0],[0.0],ncoeff,degree])
    Gy0=Gy0[:1]+1j*Gy0[1:]
    Dx0=polydrift(dxparams[:nmodelparams],[[x0],[y0],[0.0],ncoeff,degree])
    Dx0=Dx0[:1]+1j*Dx0[1:]
    Dy0=polydrift(dyparams[:nmodelparams],[[x0],[y0],[0.0],ncoeff,degree])
    Dy0=Dy0[:1]+1j*Dy0[1:]
    
    mGx=meanGxgain*Gx
    mGy=meanGygain*Gy
    mDx=meanDxgain*Dx
    mDy=meanDygain*Dy
    gGx0=meanGxgain*Gx0
    gGy0=meanGygain*Gy0
    gDx0=meanDxgain*Dx0
    gDy0=meanDygain*Dy0

    det=(gGx0*gGy0-gDx0*gDy0)
    #this sets the value at the prescribed origin to zero using the model offset
    aGx=(mGx*gGy0-mDx*gDy0)/det
    aDx=(mDx*gGx0-mGx*gDx0)/det
    aDy=(mDy*gGy0-mGy*gDy0)/det
    aGy=(mGy*gGx0-mDy*gDx0)/det
    
    calImodeldata=0.5*(np.abs(aGx)**2+np.abs(aGy)**2+np.abs(aDx)**2+np.abs(aDy)**2)
    
    return np.sqrt(calImodeldata)-np.exp(-0.5*(((x-x0)/sx)**2+((y-y0)/sy)**2))

#set data=zeros
#this optimization is done independently per track-scan antenna pair
#inverts rawGx,rawGy,rawDx,rawDy ensuring identity matrix at x0,y0 and subtracting Gaussian
def gaussfitinvertstokesGx(params,indep):
    x,y,Gx,Gy,Dx,Dy,meanGxgain,meanGygain,meanDxgain,meanDygain,gxparams,gyparams,dxparams,dyparams,ncoeff,degree=indep#the raw values at coordinates
    x0=params[0]
    y0=params[1]
    sx=params[2]
    sy=params[3]
    #evaluate raw data function at x0,y0 (or interpolate)
    nmodelparams=ncoeff*2
    Gx0=polydrift(gxparams[:nmodelparams],[[x0],[y0],[0.0],ncoeff,degree])
    Gx0=Gx0[:1]+1j*Gx0[1:]
    Gy0=polydrift(gyparams[:nmodelparams],[[x0],[y0],[0.0],ncoeff,degree])
    Gy0=Gy0[:1]+1j*Gy0[1:]
    Dx0=polydrift(dxparams[:nmodelparams],[[x0],[y0],[0.0],ncoeff,degree])
    Dx0=Dx0[:1]+1j*Dx0[1:]
    Dy0=polydrift(dyparams[:nmodelparams],[[x0],[y0],[0.0],ncoeff,degree])
    Dy0=Dy0[:1]+1j*Dy0[1:]
    
    mGx=meanGxgain*Gx
    mGy=meanGygain*Gy
    mDx=meanDxgain*Dx
    mDy=meanDygain*Dy
    gGx0=meanGxgain*Gx0
    gGy0=meanGygain*Gy0
    gDx0=meanDxgain*Dx0
    gDy0=meanDygain*Dy0

    det=(gGx0*gGy0-gDx0*gDy0)
    #this sets the value at the prescribed origin to zero using the model offset
    aGx=(mGx*gGy0-mDx*gDy0)/det
    aDx=(mDx*gGx0-mGx*gDx0)/det
    aDy=(mDy*gGy0-mGy*gDy0)/det
    aGy=(mGy*gGx0-mDy*gDx0)/det
        
    return np.abs(aGx)-np.exp(-0.5*(((x-x0)/sx)**2+((y-y0)/sy)**2))

def gaussfitinvertstokesGy(params,indep):
    x,y,Gx,Gy,Dx,Dy,meanGxgain,meanGygain,meanDxgain,meanDygain,gxparams,gyparams,dxparams,dyparams,ncoeff,degree=indep#the raw values at coordinates
    x0=params[0]
    y0=params[1]
    sx=params[2]
    sy=params[3]
    #evaluate raw data function at x0,y0 (or interpolate)
    nmodelparams=ncoeff*2
    Gx0=polydrift(gxparams[:nmodelparams],[[x0],[y0],[0.0],ncoeff,degree])
    Gx0=Gx0[:1]+1j*Gx0[1:]
    Gy0=polydrift(gyparams[:nmodelparams],[[x0],[y0],[0.0],ncoeff,degree])
    Gy0=Gy0[:1]+1j*Gy0[1:]
    Dx0=polydrift(dxparams[:nmodelparams],[[x0],[y0],[0.0],ncoeff,degree])
    Dx0=Dx0[:1]+1j*Dx0[1:]
    Dy0=polydrift(dyparams[:nmodelparams],[[x0],[y0],[0.0],ncoeff,degree])
    Dy0=Dy0[:1]+1j*Dy0[1:]
    
    mGx=meanGxgain*Gx
    mGy=meanGygain*Gy
    mDx=meanDxgain*Dx
    mDy=meanDygain*Dy
    gGx0=meanGxgain*Gx0
    gGy0=meanGygain*Gy0
    gDx0=meanDxgain*Dx0
    gDy0=meanDygain*Dy0

    det=(gGx0*gGy0-gDx0*gDy0)
    #this sets the value at the prescribed origin to zero using the model offset
    aGx=(mGx*gGy0-mDx*gDy0)/det
    aDx=(mDx*gGx0-mGx*gDx0)/det
    aDy=(mDy*gGy0-mGy*gDy0)/det
    aGy=(mGy*gGx0-mDy*gDx0)/det
        
    return np.abs(aGy)-np.exp(-0.5*(((x-x0)/sx)**2+((y-y0)/sy)**2))

#nmodelparams=2
def constdrift(params,indep):
    x,y,t=indep
    ngains=(len(params)-2)//2
    rep=params[:1]
    imp=params[1:2]
    regains=params[2:2+ngains]
    imgains=params[2+ngains:]
    staticmodel=np.complex(rep[0],imp[0])
    crv=staticmodel* (np.interp(t,np.linspace(t[0],t[-1],len(regains)+1),np.r_[1,regains])+1j*np.interp(t,np.linspace(t[0],t[-1],len(imgains)+1),np.r_[0,imgains]))
    return np.r_[np.real(crv),np.imag(crv)]

#nmodelparams=6
def lindrift(params,indep):
    x,y,t=indep
    ngains=(len(params)-6)//2
    rep=params[:3]
    imp=params[3:6]
    regains=params[6:6+ngains]
    imgains=params[6+ngains:]
    staticmodel=np.complex(rep[0],imp[0])*(x)+np.complex(rep[1],imp[1])*(y)+np.complex(rep[2],imp[2])
    crv=staticmodel* (np.interp(t,np.linspace(t[0],t[-1],len(regains)+1),np.r_[1,regains])+1j*np.interp(t,np.linspace(t[0],t[-1],len(imgains)+1),np.r_[0,imgains]))
    return np.r_[np.real(crv),np.imag(crv)]

#nmodelparams=20
def cubedrift(params,indep):
    x,y,t=indep
    ngains=(len(params)-20)//2
    rep=params[:10]
    imp=params[10:20]
    regains=params[20:20+ngains]
    imgains=params[20+ngains:]
    staticmodel=np.complex(rep[0],imp[0])*(x**3)+np.complex(rep[1],imp[1])*(y**3)+np.complex(rep[2],imp[2])*((x**2)*y)+np.complex(rep[3],imp[3])*((y**2)*x)+np.complex(rep[4],imp[4])*(x**2)+np.complex(rep[5],imp[5])*(y**2)+np.complex(rep[6],imp[6])*(x*y)+np.complex(rep[7],imp[7])*(x)+np.complex(rep[8],imp[8])*(y)+np.complex(rep[9],imp[9])
    crv=staticmodel* (np.interp(t,np.linspace(t[0],t[-1],len(regains)+1),np.r_[1,regains])+1j*np.interp(t,np.linspace(t[0],t[-1],len(imgains)+1),np.r_[0,imgains]))
    return np.r_[np.real(crv),np.imag(crv)]

def errorfunc(params,indep):
    #[cos(f)*cos(e)*cos(q)+sin(f)*sin(e)*sin(q)+1j*(sin(f)*cos(e)*cos(q)-cos(f)*sin(e)*sin(q)),cos(f)*cos(e)*sin(q)-sin(f)*sin(e)*cos(q)+j*(sin(f)*cos(e)*sin(q)+cos(f)*sin(e)*cos(q));sin(e)*cos(q)*sin(f)-cos(e)*sin(q)*cos(f)+j*(sin(e)*cos(q)*cos(f)+cos(e)*sin(q)*sin(f)),sin(e)*sin(q)*sin(f)+cos(e)*cos(q)*cos(f)+j*(sin(e)*sin(q)*cos(f)-cos(e)*cos(q)*sin(f))]
    f,e,q=params
    sinf,sine,sinq=np.sin(f),np.sin(e),np.sin(q)
    cosf,cose,cosq=np.cos(f),np.cos(e),np.cos(q)
    [a,b,c,d]=[cosf*cose*cosq+sinf*sine*sinq+1j*(sinf*cose*cosq-cosf*sine*sinq),cosf*cose*sinq-sinf*sine*cosq+1j*(sinf*cose*sinq+cosf*sine*cosq),sine*cosq*sinf-cose*sinq*cosf+1j*(sine*cosq*cosf+cose*sinq*sinf),sine*sinq*sinf+cose*cosq*cosf+1j*(sine*sinq*cosf-cose*cosq*sinf)]
    return a.real,b.real,c.real,d.real,a.imag,b.imag,c.imag,d.imag
    
def calfunc(params,indep):
    V=indep[0]
    G=np.array(params[:4]+1j*np.r_[0,params[4:],0]).reshape([2,2])
    GH=G.transpose().conj()
    invG=np.linalg.inv(G)
    invGH=np.linalg.inv(GH)
    res=dodot([G,GH,V,invGH,invG])
    return np.r_[np.real(res).reshape(-1),np.imag(res).reshape(-1)]
    
def polydrift(params,indep):
    x,y,t,ncoeff,degree=indep
    ngains=len(params)//2-ncoeff
    rep=params[:ncoeff]
    imp=params[ncoeff:ncoeff*2]
    regains=params[ncoeff*2:ncoeff*2+ngains]
    imgains=params[ncoeff*2+ngains:]
    staticmodel=np.zeros(np.shape(x),dtype='complex')
    cx=np.ones(np.shape(x))
    icoeff=0
    for idx in range(degree+1):
        cy=np.ones(np.shape(x))
        for idy in range(degree+1):
            if (idx+idy<=degree):
                cxy=cx*cy
                staticmodel+=np.complex(rep[-1-icoeff],imp[-1-icoeff])*cxy
                icoeff+=1
                cy*=y
            else:
                break
        cx*=x
    # interpgains=np.interp(t,np.linspace(t[0],t[-1],len(regains)+1),np.r_[1,regains])+1j*np.interp(t,np.linspace(t[0],t[-1],len(imgains)+1),np.r_[0,imgains])
    # interpgains/=np.mean(interpgains)#ensures average amp is 1 and phase is 0; instead of first value
    # crv=staticmodel* interpgains
    crv=staticmodel* (np.interp(t,np.linspace(t[0],t[-1],len(regains)+1),np.r_[1,regains])+1j*np.interp(t,np.linspace(t[0],t[-1],len(imgains)+1),np.r_[0,imgains]))
    return np.r_[np.real(crv),np.imag(crv)]

def polydriftabs(params,indep):
    x,y,t,ncoeff,degree=indep
    ngains=len(params)//2-ncoeff
    rep=params[:ncoeff]
    imp=params[ncoeff:ncoeff*2]
    absgains=params[ncoeff*2:ncoeff*2+ngains]
    phgains=params[ncoeff*2+ngains:]
    staticmodel=np.zeros(np.shape(x),dtype='complex')
    cx=np.ones(np.shape(x))
    icoeff=0
    for idx in range(degree+1):
        cy=np.ones(np.shape(x))
        for idy in range(degree+1):
            if (idx+idy<=degree):
                cxy=cx*cy
                staticmodel+=np.complex(rep[-1-icoeff],imp[-1-icoeff])*cxy
                icoeff+=1
                cy*=y
            else:
                break
        cx*=x
    # interpgains=np.interp(t,np.linspace(t[0],t[-1],len(regains)+1),np.r_[1,regains])+1j*np.interp(t,np.linspace(t[0],t[-1],len(imgains)+1),np.r_[0,imgains])
    # interpgains/=np.mean(interpgains)#ensures average amp is 1 and phase is 0; instead of first value
    # crv=staticmodel* interpgains
    crv=staticmodel* (np.interp(t,np.linspace(t[0],t[-1],len(absgains)+1),np.r_[1,absgains])*np.exp(1j*np.interp(t,np.linspace(t[0],t[-1],len(phgains)+1),np.r_[0,phgains])))
    return np.r_[np.real(crv),np.imag(crv)]

#fits phase of visibilities (allowing for wraps), and evaluates at center of intervalfrom and intervalto to allow interpolation
#typically called for a cross product, hh and vv pols only.
def getunwrappedmodelphase(timestamps,visibilities,intervalfrom,intervalto,corr_products):
    sep=10
    # data=[]
    vals=np.zeros([len(intervalfrom),visibilities.shape[2]],dtype=np.float)
    medianval=np.zeros(visibilities.shape[2],dtype=np.float)
    for ipol in range(visibilities.shape[2]):
        for iint in range(len(intervalto)):
            #should possibly rather take average (along time) of difference (in freq) of phase angle
            mdata=np.angle(np.mean(visibilities[intervalfrom[iint]:intervalto[iint]-1,:,ipol],axis=0))
            # mdata=np.angle(np.mean(visibilities[intervalfrom[iint]:intervalto[iint]-1,2000:3000,ipol],axis=0))
            # if (ipol==1):
            #     data.append(np.mean(visibilities[intervalfrom[iint]:intervalto[iint]-1,:,ipol],axis=0))
            mydiff=(np.remainder((mdata[sep:]-mdata[:-sep])+np.pi,np.pi*2.0)-np.pi)/sep
            [minstdx,midx0,maxstdx]=np.percentile(mydiff,[15.75,50,84.25])
            minstd=np.min([midx0-minstdx,maxstdx-midx0])
            minval=midx0-minstd*2.0
            maxval=midx0+minstd*2.0
            valid=np.nonzero(np.logical_and(mydiff>minval,mydiff<maxval))[0]
            vals[iint,ipol]=np.median(mydiff[valid])
        medianval[ipol]=np.median(vals[:,ipol])
        print('ipol %d %s %f %f'%ipol,corr_products[ipol],medianval[ipol],np.std(vals[:,ipol]))
    
    # np.save('data',np.array(data))
    return np.mean(medianval)#average over pol

def getunwrappedmodelphasefft(timestamps,visibilities,intervalfrom,intervalto,corr_products):
    sep=10
    # data=[]
    vals=np.zeros([len(intervalfrom),visibilities.shape[2]],dtype=np.float)
    medianval=np.zeros(visibilities.shape[2],dtype=np.float)
    for ipol in range(visibilities.shape[2]):
        iint=0
        phase=np.angle(np.mean(visibilities[intervalfrom[iint]:intervalto[iint]-1,:,ipol],axis=0))
        lag=np.fft.fftshift(abs(np.fft.fft(np.exp(1j*phase))))
        phaseangle=float(np.argmax(lag)-len(lag)/2)/float(len(lag))*360.0*np.pi/180.0
        medianval[ipol]=phaseangle
        print('ipol %d %s %f %f'%ipol,corr_products[ipol],medianval[ipol],np.std(vals[:,ipol]))
    
    # np.save('data',np.array(data))
    return np.mean(medianval)#average over pol


def polygetncoeff(degree):
    icoeff=0
    for idx in range(degree+1):
        for idy in range(degree+1):
            if (idx+idy<=degree):
                icoeff+=1
            else:
                break
    return icoeff
    
    
def cubefunc(params,indep):
    x,y=indep
    a=params
    return (x**3)*(a[0]+a[1]*y+a[2]*y**2+a[3]*y**3)+x**2*(a[4]+a[5]*y+a[6]*y**2+a[7]*y**3)+x*(a[8]+a[9]*y+a[10]*y**2+a[11]*y**3)+(a[12]+a[13]*y+a[14]*y**2+a[15]*y**3)
    
def crosspower(params,indep):
    mGx,mDx,mDy,mGy=indep
    Gx0,Dx0,Dy0,Gy0,Gx0j,Dx0j,Dy0j,Gy0j=params
    Gx0=Gx0+1j*Gx0j
    Dx0=Dx0+1j*Dx0j
    Dy0=Dy0+1j*Dy0j
    Gy0=Gy0+1j*Gy0j
    newGx=(mGx*Gy0-mDx*Dy0)
    newDx=(mDx*Gx0-mGx*Dx0)
    newDy=(mDy*Gy0-mGy*Dy0)
    newGy=(mGy*Gx0-mDy*Dx0)
    return np.sqrt(np.sqrt((np.sum(np.abs(newDx)**2)+np.sum(np.abs(newDy)**2))/(np.sum(np.abs(newGx)**2)+np.sum(np.abs(newGy)**2))))
    
def cosinepower(params,indep):
    r=indep
    a0=params[0]
    s0=params[1]
    ampmodel=np.clip(a0*np.cos(np.clip(r/s0,-np.pi/2.0,np.pi/2.0))**2.0,0,np.inf)
    return ampmodel

def ampmodel(ampmap,blockdiameter,dishdiameter,mapsize,gridsize):
    x,y=np.meshgrid(np.linspace(-mapsize/2.0,mapsize/2.0,gridsize+1)[:-1],np.linspace(-mapsize/2.0,mapsize/2.0,gridsize+1)[:-1])
    r=np.sqrt(x**2+y**2);
    valid=np.nonzero(r.reshape(-1)>=blockdiameter/2.0)[0]
    data=ampmap.reshape(-1)[valid]
    indep=[r.reshape(-1)[valid]]
    initialparams=[1,1]
    fitter=NonLinearLeastSquaresFit(cosinepower,initialparams)
    fitter.fit(indep,data)
    ampmodel=fitter.eval(r.reshape(-1)).reshape(np.shape(r))
    return ampmodel
    
#vertices must be a list of coordinates, will not work correctly if it is a 2d np array
def area_of_polygon(vertices):
    pairs = list(zip(vertices, vertices[1:] + vertices[0:1]))
    return sum(x1 * y2 - y1 * x2 for (x1, y1), (x2, y2) in pairs) / 2
    

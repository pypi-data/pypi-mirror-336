#Copyright National Research Foundation (SARAO), 2005-2025. All Rights Reserved.
#Author: Mattieu de Villiers (email: mattieu@sarao.ac.za)
"""
    Copyright National Research Foundation (SARAO), 2005-2025. All Rights Reserved.
    Author: Mattieu de Villiers (email: mattieu@sarao.ac.za)

    This scripting code has been adapted by aph@ska.ac.za from the original report by mattieu@ska.ac.za: original at
    http://kat-imager.kat.ac.za:8888/notebooks/RTS_reduction_results/3.1-Aperture_Phase_Efficiency/Ku-band%20holography%20report.ipynb
"""
from pylab import *
import pylab as plt # kathlog need this for some debug plots
from matplotlib.backends.backend_pdf import PdfPages
import time
import os
import traceback
import socket
import numpy as np
import scipy as sp
import dvsholog
import katdal
import io
from .utilities import meerkatflatphase
# from .spreadsheet import Spreadsheet
matplotlib.use('PDF')


reportURL = lambda reportfilename: 'http://kat-imager.kat.ac.za:8888/files/RTS_reduction_results/3.1-Aperture_Phase_Efficiency/'+reportfilename

def tilt_beams(dataset, feedtilt_deg, hv, xyzoffsets,clipextent,gridsize):
    """
       Generate received patterns to appear to have been radiated by the specified source.
       @param dataset: dataset with "receive" beam patterns in linear basis [HH, HV, VH, VV]
       @param feedtilt_deg: rotation of the "up" feed to align with the "north" direction of the source signal in degrees. positive values rotates from north to east (i.e. counter clock wise for southern observer).
       @param hv: equivalent linear pol source/input signal as (H,V); e.g. [1,1] or [1,0] - gets normalized.
       @return: ApertureMaps & BeamCubes based on the patterns in dataset
    """
    # Clockwise rotation (V->H) of received linear pol signal relative to the feed
    # e_in = [e_in_h, e_in_v]
    # h_pol = e_in_h*cos+e_in_v*sin
    # v_pol = -e_in_h*sin+e_in_v*cos
    # Therefore r_h = g_hh*h_pol + g_hv*v_pol = g_hh*(e_in_h*cos+e_in_v*sin) + g_hv*(-e_in_h*sin+e_in_v*cos)
    #           r_v = g_vv*v_pol + g_vh*h_pol = g_vv*(-e_in_h*sin+e_in_v*cos) + g_vh*(e_in_h*cos+e_in_v*sin)
    # Identical result from alternative derivation as per Hamaker, Bregman & Sault
    s = np.sin(feedtilt_deg*np.pi/180.)
    c = np.cos(feedtilt_deg*np.pi/180.)
    # Normalize the reference signal
    h,v = [x/(np.abs(hv[0])**2+np.abs(hv[1])**2)**.5 for x in hv]
    # dvsholog feedcombine represents vector for dot product = feedcombine . [ghh,ghv,gvh,gvv]
    beam_ch = dvsholog.BeamCube(dataset,interpmethod='scipy',xyzoffsets=xyzoffsets,extent=clipextent,feedcombine=[h*c+v*s, -h*s+v*c, 0,0])
    beam_cv = dvsholog.BeamCube(dataset,interpmethod='scipy',xyzoffsets=xyzoffsets,extent=clipextent,feedcombine=[0,0, h*c+v*s, -h*s+v*c])
    beam_dummy = dvsholog.BeamCube(dataset,interpmethod='scipy',xyzoffsets=xyzoffsets,extent=clipextent,feedcombine=[h*c+v*s, -h*s+v*c, 0,0])
    dft_ch = dvsholog.ApertureMap(dataset,gridsize=gridsize,xyzoffsets=xyzoffsets,feedcombine=[h*c+v*s, -h*s+v*c, 0,0])
    dft_cv = dvsholog.ApertureMap(dataset,gridsize=gridsize,xyzoffsets=xyzoffsets,feedcombine=[0,0, h*c+v*s, -h*s+v*c])
    dft_dummy = dvsholog.ApertureMap(dataset,gridsize=gridsize,xyzoffsets=xyzoffsets,feedcombine=[h*c+v*s, -h*s+v*c, 0,0])
    return {'dfth':dft_ch,'dftv':dft_cv,'beamh':beam_ch,'beamv':beam_cv,'dft_dummy':dft_dummy,'beam_dummy':beam_dummy}


def load_simulation_conj(emssfilename,freq,feedtilt_deg,beaconpol,clipextent,gridsize):
    """@param feedtilt_deg: CCW rotation relative to observer's "up" of source's "up" when looking at it"""
    xyzoffsets = [0,0,0] if (freq > 10000) else [0,-13.5/2.0,0] # EMSS used a different reference point for the Ku-band patterns.
    dataset_Lin = dvsholog.Dataset(emssfilename,'meerkat',freqMHz=freq,method='raw',clipextent=clipextent)
    
    # IEEE source coordinate frame for waves from source with +z direction towards antenna, linear basis
    srchv = {'RCP':[1,-1j], 'LCP':[1,1j], 'H':[1,0], 'V':[0,1]}[beaconpol]
    
    # A. Simulated patterns have +z from the antenna to the far field.
    #    Conjugation changes the direction of travel (+z); to maintain IEEE definition of RCP, the angle sign needs to invert.
    # B. More motivation for flips:
    #    Fourier transform theorem: if aperture(r,phi) <-> farfield(theta,phi)
    #               then conjugate(aperture(r,phi)) <-> farfield(theta,-phi)
    #               also conjugate(farfield(theta,phi)) <-> aperture(r,-phi)
    #    Since ll = r*sin(phi) and mm = r*cos(phi) conjugation requires flipping ll.
    #    Holography measures patterns in offset look angles on the sky - these angles are
    #    negative that of the offset angle in the patterns.
    #      We rather flip the simulated patterns to agree with the measured patterns.
    #      Simulated patterns have +ll eastward and +mm downward (to NCP, IEEE definition)
    #      while measured patterns have +D_crossEl eastward and +D_El upward so we have to flip mm.
    dataset_Lin.visibilities = [np.conj(v) for v in dataset_Lin.visibilities]
    dataset_Lin.ll = -dataset_Lin.ll # Cross-elevation flips left-right
    dataset_Lin.mm = -dataset_Lin.mm # Elevation orientation flips upside down
    results = tilt_beams(dataset_Lin, feedtilt_deg, srchv, xyzoffsets=xyzoffsets, clipextent=clipextent,gridsize=gridsize)
    return results


#loads measurement as flagged/selected in dataset
def load_selected_measurement(dataset,ichan,clipextent,gridsize,dMHz=0.01): # ichan is permitted to have a fractional part
    #H and V feeds on m063 was swapped (incorrectly) from 24/9/2015 to 28/10/2015
    swappedfeed=((dataset.radialscan_allantenna[dataset.scanantennas[0]]=='m063' and dataset.rawtime[0]>time.mktime((2015, 9, 24, 9,0,0,0,0,0)) and dataset.rawtime[0]<time.mktime((2015, 10, 28, 9,0,0,0,0,0))) or (dataset.radialscan_allantenna[dataset.scanantennas[0]]=='m046' and dataset.rawtime[0]>time.mktime((2017, 11, 23, 0,0,0,0,0,0)) and dataset.rawtime[0]<time.mktime((2017, 11, 26, 0,0,0,0,0,0))))
    
    xmag=-1.35340292717 # APH improved (dvsholog's sign convention) From eq 20 of Rusch et al M = Feq/F_mainreflector = |1-e^2|/((1+e^2)-2*e*cos(beta)), e=0.2916641,beta=45.4746deg
    xyzoffsets=[0.0,-(-5.200+13.5/2.),-1.000-((13.5/2.)**2/(4*5.48617)-0.600)] # APH improved Better 'z' precision than default 'meerkat' set which is ~0.5mm! x=horizontal=no offset; y=vertical=el_axis_to_centre_on_main_reflector (neg); z=az_axis_to_cenre_on_main_reflector
    freqMHz=(dataset.h5.freqs[int(ichan)]+dataset.h5.channel_width*(ichan-int(ichan)))/1e6
    scanant=dataset.radialscan_allantenna[dataset.scanantennas[0]]
    
    # There seems almost no difference between ApertureMap 'HV'&'VH' and 'H'&'V' -- it used to be calibation suceeded most often on HV&VH.
    # In principle prefer H&V  which matches BeamCube's feedcombine and also the mapping used by tilt_beams().
    # Using ApertureMap's feedcombine=[0,1.0,0,0] instead of the equiv feed='HV' crashes the kernel due to fragile normalization.
    dfth=dvsholog.ApertureMap(dataset,scanantennaname=scanant,freqMHz=freqMHz,dMHz=dMHz,feed='H',gridsize=gridsize,xmag=xmag, xyzoffsets=xyzoffsets) # APH 08/2016 changed from HV to H because all aperture maps had H & V swapped incorrectly
    dftv=dvsholog.ApertureMap(dataset,scanantennaname=scanant,freqMHz=freqMHz,dMHz=dMHz,feed='V',gridsize=gridsize,xmag=xmag, xyzoffsets=xyzoffsets) # APH 08/2016 changed from VH to V
    beamh=dvsholog.BeamCube(dataset,scanantennaname=scanant,freqMHz=freqMHz,dMHz=dMHz,interpmethod='scipy',extent=clipextent,feedcombine=[1.0,0,0,0],applypointing='perfeed') # APH changed from original "Gx" -- perfeed is correct for "error beam" assessment
    beamv=dvsholog.BeamCube(dataset,scanantennaname=scanant,freqMHz=freqMHz,dMHz=dMHz,interpmethod='scipy',extent=clipextent,feedcombine=[0,0,0,1.0],applypointing='perfeed') # APH changed from original "Gx" -- perfeed is correct for "error beam" assessment

    dfth.subphase,dfth.subparam,dfth.subpatherrormodels=meerkatflatphase(dfth.ampmap,dfth.unwrappedphasemap,dfth.flatmaskmap,dfth.mapsize,dfth.gridsize,dfth.wavelength,flatmode='sub',geometryerrors=[('phaseoffset',None,'deg'),('pointx',None,'deg/cell'),('pointy',None,'deg/cell'),('subx',None,'mm'),('suby',None,'mm'),('subz',None,'mm'),('subroty',None,'deg')])
    dftv.subphase,dftv.subparam,dftv.subpatherrormodels=meerkatflatphase(dftv.ampmap,dftv.unwrappedphasemap,dftv.flatmaskmap,dftv.mapsize,dftv.gridsize,dftv.wavelength,flatmode='sub',geometryerrors=[('phaseoffset',None,'deg'),('pointx',None,'deg/cell'),('pointy',None,'deg/cell'),('subx',None,'mm'),('suby',None,'mm'),('subz',None,'mm'),('subroty',None,'deg')])

    if swappedfeed:
        dfth, dftv, beamh, beamv = dftv, dfth, beamv, beamh
    
    results = {'time_avg_str':dataset.env_time[0],'time_min':dataset.rawtime[dataset.time_range[0]],
               'time_max':dataset.rawtime[dataset.time_range[-1]],
               'time_avg':0.5*(dataset.rawtime[dataset.time_range[0]]+dataset.rawtime[dataset.time_range[-1]]),
               'el_avg':dataset.env_el[0],'el_min':dataset.env_el[1],'el_max':dataset.env_el[2],
               'sun_avg':dataset.env_sun[0],'sun_min':dataset.env_sun[1],'sun_max':dataset.env_sun[2],
               'dfth':dfth,'dftv':dftv,'beamh':beamh,'beamv':beamv,'filename':dataset.filename,'targetname':dataset.target.name,
               'scanantenna':dataset.radialscan_allantenna[dataset.scanantennas[0]],
               'trackantenna':dataset.radialscan_allantenna[dataset.trackantennas[0]]}
    try: # Avoid crashing if it's just enviro data that's missing
        results.update({'temp_avg':dataset.env_temp[0],'temp_min':dataset.env_temp[1],'temp_max':dataset.env_temp[2],
                        'wind_avg':dataset.env_wind[0],'wind_min':dataset.env_wind[1],'wind_max':dataset.env_wind[2]})
    except Exception as e:
        print("No environmental temperature or wind data available - continuing with 0's! %s" % (traceback.format_exc()))
        null = 0*dataset.env_el[0] # Optimal conditions, but suspiciously so
        results.update({'temp_avg':null,'temp_min':null,'temp_max':null,
                        'wind_avg':null,'wind_min':null,'wind_max':null})
    return results


def flag_old0cycles(dataset):
    """ Same return signature as dataset.findcycles(), which doesn't work on some of the old single cycle scans.
        CAUTION: this flags everything up to the last "track" """
    dataset.flagdata() # Reset all flags
    T0 = dataset.h5.timestamps[0]
    s0 = 0
    for s in dataset.h5.scans():
        if (s[1] == 'track'):
            s0 = s[0]+1
    print("Flagging all scans prior to last 'track' at scan #%d" % s0)
    scans = range(s0,len(list(dataset.h5.scans())))
    dataset.h5.select(scans=scans)
    # Start & stop offsets in hrs & number of scans
    cycles = ([(dataset.h5.timestamps[0]-T0)/(60*60.0)] ,[(dataset.h5.timestamps[-1]-dataset.h5.timestamps[0])/(60*60.0)], [len(scans)])
    return cycles

def load_measurement(filename,centerfreq,ichan,clipextent,gridsize,icycle,icycleoffset,ignoreantennas=[],maxcycles=999,timestart_hrs=0,timeduration_hrs=1e300,dMHz=0.01):
    """loads measurements and environmental conditions into database
       icycle can be None, 'all', int or list of ints marking specific cycles; ichan is permitted to have a fractional part"""
    try:
        h5=katdal.open(filename)
        scanantennas=h5.obs_params['scan_ants'].split(',')
        scanantennas=np.sort(list(set(scanantennas)-set(ignoreantennas))).tolist()
        scanantname=scanantennas[0]
    except:
        dataset=dvsholog.Dataset(filename,'meerkat',katdal_centre_freq=None if (centerfreq is None) else (centerfreq*1e9),method='gainrawabs',ignoreantennas=ignoreantennas,onaxissampling=0.01)
        scanantname=dataset.radialscan_allantenna[dataset.scanantennas[0]]
    #dataset=dvsholog.Dataset(filename,'meerkat',katdal_centre_freq=None if (centerfreq is None) else (centerfreq*1e9),method='gainrawabs',scanantname=scanantname,ignoreantennas=ignoreantennas,onaxissampling=0.01)
    #temporary fix for timing offset!!!! REMOVE TODO
    dataset=dvsholog.Dataset(filename,'meerkat',timingoffset=-0.25,katdal_centre_freq=None if (centerfreq is None) else (centerfreq*1e9),method='gainrawabs',scanantname=scanantname,ignoreantennas=ignoreantennas,onaxissampling=0.01)
    # 'rawonaxis' & 'polproducts' only for the first pair of antennas. Original 'L-band%20holography%20report.ipyn' has only what's in the second half of this code.
    if (len(dataset.trackantennas)>1 or len(dataset.scanantennas)>1):
        print('WARNING: using more than 1 trackantennas or scanantennas may lead to incorrect results. Not currently supported.')
        print('scanantennas'+','.join([dataset.radialscan_allantenna[i] for i in dataset.scanantennas]))
        print('trackantennas: '+','.join([dataset.radialscan_allantenna[i] for i in dataset.trackantennas]))
        return
    
    if (icycle is None):
        cycles=[]
    else:
        # Identify cycles & try to work around typical failure modes
        print('using timestart_hrs',timestart_hrs,'timeduration_hrs',timeduration_hrs,'icycleoffset',icycleoffset)
        # Try different combinations to find the one that best detects cycles
        cyclestart,cyclestop,nscanspercycle= [], [], 9e9
        for _onradial,_flagslew in [([0.5, 0.75],False), ([0.25,0.5],False), ([0.05,0.2],False), ([0.05,0.2],True)]: # Defaults then progressivley more robust against poor pointing
            print('trying flagslew',_flagslew,'onradial',_onradial)
            dataset.flagdata(timestart_hrs=timestart_hrs,timeduration_hrs=timeduration_hrs, ignoreantennas=ignoreantennas,flagslew=_flagslew)
            _cyclestart,_cyclestop,_nscanspercycle=dataset.findcycles(cycleoffset=icycleoffset,onradial=_onradial,doplot=True)
            if (len(_cyclestart) > len(cyclestart)) or (len(_cyclestart) == len(cyclestart) and _nscanspercycle > nscanspercycle): # Best so far
                onradial,flagslew=_onradial,_flagslew
                cyclestart,cyclestop,nscanspercycle=_cyclestart,_cyclestop,_nscanspercycle
        if (len(cyclestart)>0):
            print('Proceeding with cycles detected using flagslew',flagslew,'onradial',onradial)
        else:
            print('No cycles found, trying to interpret data as for old-style single cycles')
            cyclestart,cyclestop,nscanspercycle=flag_old0cycles(dataset)
            flagslew = False
            dataset.flagdata(timestart_hrs=timestart_hrs,timeduration_hrs=timeduration_hrs, ignoreantennas=ignoreantennas,flagslew=flagslew)
        assert len(cyclestart)>0, "Failed to find any cycles. Consider changing cycle & time offsets in registry."
        
        cycles=list(zip(cyclestart,cyclestop))
        if (type(icycle)==int):
            cycles=[cycles[icycle]]
        elif (type(icycle)==np.ndarray or type(icycle)==list):
            cycles=[cycles[c] for c in icycle]
        #else: #icycle=='all'
            
    corrprod_to_index = dict([(tuple(cp), ind) for cp, ind in zip(dataset.h5.corr_products, range(len(dataset.h5.corr_products)))])
    trackant = dataset.radialscan_allantenna[dataset.trackantennas[0]]
    scanant = dataset.radialscan_allantenna[dataset.scanantennas[0]]
    polprods = [("%s%s"%(scanant,p[0].lower()), "%s%s"%(trackant,p[1].lower())) for p in dataset.pols_to_use] # Fixed by kathlog convention: [HH,HV,VH,VV]
    try:
        cpindices = [corrprod_to_index[p] for p in polprods]
        polproducts = [pol[0]+'-'+pol[1] for pol in polprods]
    except KeyError as e: # For some reason the ordering matters and some times it is different
        cpindices = [corrprod_to_index[(p[1],p[0])] for p in polprods]
        polproducts = [pol[1]+'-'+pol[0] for pol in polprods]
    
    results=[]
    rawonaxis=[] # APH refactored rawonaxis to be loaded as (cycles x [prods x dumps_cycle]) rather than (prods x dumps_allcycles)
    if (len(cycles)>0):
        for ic in range(min([len(cycles),maxcycles])):
            print('--------------------------------------------\nProcessing cycle %d of %d\n'%(ic+1,len(cycles)))
            cycle=cycles[ic]
            dataset.flagdata(timestart_hrs=cycle[0],timeduration_hrs=cycle[1]-cycle[0],clipextent=clipextent,ignoreantennas=ignoreantennas,flagslew=flagslew)
            results.append(load_selected_measurement(dataset,ichan,clipextent,gridsize,dMHz))
            # APH refactored
            dataset.h5.select(reset="",dumps=np.array((np.array((dataset.ll)**2+(dataset.mm)**2<(dataset.radialscan_sampling)**2,dtype='int')),dtype='bool'));
            rawonaxis.append([dataset.h5.vis[:,round(ichan),iprod].squeeze() for iprod in cpindices])
    else:
        results.append(load_selected_measurement(dataset,ichan,clipextent,gridsize,dMHz))
        # APH refactored
        dataset.h5.select(reset="",dumps=np.array((np.array((dataset.ll)**2+(dataset.mm)**2<(dataset.radialscan_sampling)**2,dtype='int')),dtype='bool'));
        rawonaxis.append([dataset.h5.vis[:,round(ichan),iprod].squeeze() for iprod in cpindices])
    
    # Re-order so that rawonaxis is (prods x [cycles x dumps_cycle])
    rawonaxis = np.moveaxis(rawonaxis,0,1)
    return results,rawonaxis,polproducts


col_no = lambda col_alpha: ([chr(ord('a')+i) for i in range(26)] + ['a'+chr(ord('a')+i) for i in range(26)]).index(col_alpha.lower())
def hyperlink(URL, text):
    return '=HYPERLINK("%s","%s")'%(URL,text)    
def hyperlinktext(hyperlink): # Separate out the text from a google sheets hyperlink, if it is
    try:
        return hyperlink.split('"')[-2] # Google sheets requires use of "; the last group is the closing brakcets.
    except:
        return hyperlink

# def loadifiles(gspreadsheet,ifiles,gridsize,clipextent,maxcycles=999,dMHz=0.01):
#     """
#         @param gspreadsheet: a compatible object with columns A-G containing "h5file,centerfreq,h5channel,beaconpol,beacontilt,emssfreq,emssfile". columns AE..AH may contain "icycleoffset,maxcycles,time_start,time_duration".
#         @param maxcycles: max number of cycles to load of any file; default 999.
#         @return: rawprods, results, rawonaxis, iindices, nofitflags, concat_filenames, beaconpol, tilt, emssfreq, emssresults
#         Note: only iindices is nested like ifiles, the rest is "flat"
#     """
#     results=[]
#     rawonaxis=[[],[],[],[]]
#     iindices=[]
#
#     concat_filenames=''
#     for ifile in ifiles:
#         try: # Avoid unnecessarily losing everything if something goes wrong
#             grows=gspreadsheet.get_row(None,ifile)
#             filename,centerfreq,channel,beaconpol,tilt,emssfreq,emssfilename=grows[col_no('A'):col_no('G')+1]
#             filename = str(hyperlinktext(filename)) # Separate from hyperlink, if it is
#             try: # Spreadsheet overrides only if present
#                 _icycleoffset,_maxcycles,_timestart_hrs,_timeduration_hrs = grows[col_no('AE'):col_no('AH')+1]
#                 icycleoffset = int(_icycleoffset) if _icycleoffset else 0
#                 maxcycles = min([maxcycles, int(_maxcycles) if _maxcycles else maxcycles])
#                 timestart_hrs=float(_timestart_hrs) if (len(_timestart_hrs)) else 0.0
#                 timeduration_hrs=float(_timeduration_hrs) if len(_timeduration_hrs) else 1e300
#             except: # Defaults if not overridden in spreadsheet
#                 icycleoffset = 0
#                 maxcycles = 100
#                 timestart_hrs = 0
#                 timeduration_hrs = 1e300
#             print("Employing icycleoffset=%d & maxcycles=%d" % (icycleoffset,maxcycles))
#             ignoreantennas=[] if (len(grows)<=col_no('J')) else grows[col_no('J')].split(',')
#             centerfreq=float(centerfreq) if centerfreq else None
#             channel=float(channel)
#             emssfreq=float(emssfreq)
#             tilt=float(tilt)
#             basefilename=os.path.splitext(os.path.basename(filename))[0]
#             thisresult,thisrawonaxis,rawprods=load_measurement(filename,centerfreq,channel,clipextent,gridsize,'all',icycleoffset,ignoreantennas,maxcycles,timestart_hrs,timeduration_hrs,dMHz=dMHz)
#         except Exception as e:
#             print("Error loading %d, continuing with next.\n\t(%s)" % (ifile,traceback.format_exc()))
#             continue
#         # Only take results onboard if no errors encountered this far
#         concat_filenames=basefilename if (len(concat_filenames)==0) else concat_filenames+'_'+basefilename
#         for iprod in range(len(thisrawonaxis)):
#             rawonaxis[iprod].extend(thisrawonaxis[iprod]) # Flat
#         iindices.append(range(len(results),len(results)+len(thisresult)))
#         results.extend(thisresult) # Flat
#
#     print("\nLoading simulated beams")
#     emssresults=load_simulation_conj(emssfilename,emssfreq,tilt,beaconpol,clipextent,gridsize)
#
#     print("\nFitting smooth beams...")
#     fitbeams([emssresults])
#     nofitflags = fitbeams(results)
#
#     return rawprods, results, rawonaxis, iindices, nofitflags, concat_filenames, beaconpol, tilt, emssfreq, emssresults


def fitbeams(results):
    """
        Fit beam models, and flag cycles that cannot be fitted.
        @return: notfitted_flags - with same shape as results.
    """
    notfitted = []
    for _c,_r in enumerate(results):
        try:
            _r['beamh'].fitpoly()
            _r['beamv'].fitpoly()
            notfitted.append(False)
        except Exception as e:
            print("Failed to fit beam model for cycle %d @ %s: %s"%(_c,_r['time_avg_str'],traceback.format_exc()))
            notfitted.append(True)
    return np.asarray(notfitted)


def thresh_and_flag(rawonaxis, results, iindices, maxdelta=1, cascade_keep=None):
    """
        Applies a per-cycle threshold based on the stddev/median of onaxis results compared to the entire set.
        @param maxdelta: the max fraction that the on-axis noise-to-signal is permitted to increase relative to the 30th percentile, to not be discarded; default 1 (sigma@30th, 2sigma@cutoff).
        @param cascade_keep: if given (same shape as results), AND these togeter with threshold flags; default None.
        @return: kept(rawonaxis), kept(results), discarded(results), kept(iindices), SNR_onaxis -- as views on the input data.
    """
    def flagdropoutcycles(rawonaxis,mu_onaxis,maxdelta):
        """
            Generate flags for cycles where the on axis stddev/median exceeds the specified fraction above the threshold.
            @param mu_onaxis: threshold by product
            @return boolean keep flags against rawonaxis cycles
        """
        if (maxdelta > 0):
            _onaxis = np.asarray([[np.std(np.abs(_c))/np.median(np.abs(_c)) for _c in _p] for _p in rawonaxis]) # product x cycle
            keep = np.asarray([_onaxis[_p,:]/mu_onaxis[_p]-1 for _p in range(len(mu_onaxis))]) # product x cycle
            print("Cycles relative to threshold:\n" + str(keep))
            keep = keep < maxdelta # product x cycle
            print("Good data:\n" + str(keep))
            keep = [np.all(keep[:,_r]) for _r in range(len(rawonaxis[0]))] # Only keep if all products are good
        else:
            keep = [True]*len(rawonaxis[0])
        return np.asarray(keep)

    # Calculate thresholds across all cycles as 30th percentile
    mu_onaxis = [[],[],[],[]]
    for indices in iindices:
        thisrawonaxis = [np.take(r,indices,axis=0) for r in rawonaxis] # product x cycle x samples
        for _p in range(len(mu_onaxis)):
            mu_onaxis[_p].extend([np.std(np.abs(_c))/np.median(np.abs(_c)) for _c in thisrawonaxis[_p]])
    mu_onaxis = np.percentile(mu_onaxis,30,axis=1) # product (collapse cycles)
    
    # Filter cycles
    keptresults=[]
    badresults=[]
    keptrawonaxis=[[],[],[],[]]
    keptiindices=[]
    for indices in iindices:
        thisresult = np.take(results,indices,axis=0)
        thisrawonaxis = [np.take(r,indices,axis=0) for r in rawonaxis]
        keep = flagdropoutcycles(thisrawonaxis,mu_onaxis,maxdelta)
        if (cascade_keep is not None):
            keep = np.logical_and(keep, np.take(cascade_keep,indices,axis=0))
        print("Keeping cycles: " + str(keep))
        thisrawonaxis = [np.take(_r,np.nonzero(keep)[0],axis=0) for _r in thisrawonaxis]
        badresults.extend(np.take(thisresult,np.nonzero(~keep)[0]))
        thisresult = np.take(thisresult,np.nonzero(keep)[0])
        for iprod in range(len(thisrawonaxis)):
            keptrawonaxis[iprod].extend(thisrawonaxis[iprod])
        keptiindices.append(range(len(keptresults),len(keptresults)+len(thisresult)))
        keptresults.extend(thisresult)
    return keptrawonaxis, keptresults, badresults, keptiindices, [int(1/mu+.5) for mu in mu_onaxis] # nominal SNR per product


# def updateifiles(gspreadsheet,ifiles,iindices,isoptimal,isnominal,results,h_feedoffset_xyz,v_feedoffset_xyz,h_errbmpks,v_errbmpks,h_rmserrbm,v_rmserrbm,h_subroty,v_subroty,snr_onaxis,reportfilename=None):
#     """@param gspreadsheet: a compatible object.
#       Results will be written into columns K:AD (APE : sub roll) (the spreadsheet must have columns at least up to AI)
#     """
#     for ifile,indices in zip(ifiles,iindices):
#         filename=gspreadsheet.get_value(None,ifile,1)
#         if (reportfilename and len(np.ravel(indices)) > 0): # Add hyperlink to report
#             cell = hyperlink(reportURL(reportfilename),hyperlinktext(filename))
#         else: # Remove hyperlink to report
#             cell = hyperlinktext(filename)
#         gspreadsheet.update_row(None,[cell],ifile,0)
#
#         cell_list=['' for c in range(20)]
#         if (len(np.ravel(indices)) > 0):
#             take = lambda x: np.take(x,indices) # Select only results for this ifile
#             _optimal, _nominal = take(isoptimal), take(isnominal)
#             _spec = _optimal+_nominal
#             takespec = take
#             if (_spec.searchsorted(True) >= 0): # Enough results to unambiguously select only results under spec conditions
#                 takespec = lambda x: np.take(x,indices)[_spec==True]
#             if (len(takespec(results)) == 0):
#                 takespec = take
#             cell_list[0]=take(results)[0]['scanantenna']#antenna
#             cell_list[1]='%d'%(len(np.nonzero(_optimal)[0]))#optimal
#             cell_list[2]='%d'%(len(np.nonzero(_nominal)[0]))#nominal
#             values = [np.mean([result['dftv'].eff0_phase,result['dfth'].eff0_phase]) for result in takespec(results)]
#             cell_list[3]='%.1f'%(np.min(values)*100) # Maps to max RMS
#             cell_list[4]='%.1f'%(np.percentile(values, 5)*100) # Maps to 95% RMS
#             values = [np.mean([result['dftv'].rms0_mm,result['dfth'].rms0_mm]) for result in takespec(results)]
#             cell_list[5]='%.2f'%(np.percentile(values, 95))
#             cell_list[6]='%.2f'%(np.max(values))
#             values = np.r_[take(h_feedoffset_xyz[0]),take(v_feedoffset_xyz[0])] # feed X
#             cell_list[7]='%.1f'%(np.mean(values))
#             cell_list[8]='%.1f'%(np.percentile(np.abs(values-np.mean(values)), 95))
#             values = np.r_[take(h_feedoffset_xyz[1]),take(v_feedoffset_xyz[1])] # feed Y
#             cell_list[9]='%.1f'%(np.mean(values))
#             cell_list[10]='%.1f'%(np.percentile(np.abs(values-np.mean(values)), 95))
#             values = np.r_[take(h_feedoffset_xyz[2]),take(v_feedoffset_xyz[2])] # feed Z
#             cell_list[11]='%.1f'%(np.mean(values))
#             cell_list[12]='%.1f'%(np.percentile(np.abs(values-np.mean(values)), 95))
#             values = takespec(h_errbmpks)
#             cell_list[13]='%.1f'%(np.max(values))
#             cell_list[14]='%.1f'%(100.0*len(values[values<4.05])/len(values)) # Spec threshold 4%
#             values = takespec(v_errbmpks)
#             cell_list[15]='%.1f'%(np.max(values))
#             cell_list[16]='%.1f'%(100.0*len(values[values<4.05])/len(values)) # Spec threshold 4%
#             cell_list[17]='%.1f'%(np.max(h_rmserrbm)*100) #max of pattern -- one RMS over these ifiles!
#             cell_list[18]='%.1f'%(np.max(v_rmserrbm)*100) #max of pattern -- one RMS over these ifiles!
#             cell_list[19]='%.2f'%(np.mean([np.mean(h_subroty),np.mean(v_subroty)])) #subreflector roll angle
#             gspreadsheet.update_row(None,cell_list,ifile,col_no('K'))
#
#             gspreadsheet.update_row(None,[str(snr_onaxis)],ifile,col_no('AI')) # Nominal signal-to-noise per product
#         else: # No valid cycles for this file
#             gspreadsheet.update_row(None,['','0','0'],ifile,col_no('K'))
#

def plot_envelope(x,y_avg,y_min,y_max):
    x=np.r_[x[0]-0.0001,x,x[-1]+0.0001]
    y_avg=np.r_[np.nan,y_avg,np.nan]
    y_min=np.r_[np.nan,y_min,np.nan]
    y_max=np.r_[np.nan,y_max,np.nan]
    sx=argsort(x)
    plot(x[sx],y_avg[sx],'k')
    fill_between(x[sx],y_min[sx],y_max[sx],facecolor='k',alpha=0.1)

def plot_line(x,y,colour,**kwargs):
    x=np.r_[np.min(x)-0.0001,x,np.max(x)+0.0001]
    y=np.r_[np.nan,y,np.nan]
    sx=argsort(x)
    plot(x[sx],y[sx],colour,**kwargs)

def plot_highlights(x, dx, ishighlighted,ymin,ymax,colour,alpha=0.1):
    xfrom=None
    xto=None
    x=np.r_[x[0]-0.0001,x,x[-1]+0.0001]
    ishighlighted=np.r_[0,ishighlighted,0]
    for ix in argsort(x):
        if (ishighlighted[ix]):
            if (xfrom==None):
                xfrom=x[ix]-dx/2.0
            xto=x[ix]+dx/2.0
        else:
            if (xfrom!=None):
                fill([xfrom,xfrom,xto,xto],[ymin,ymax,ymax,ymin],colour,alpha=alpha,edgecolor=None)
            xfrom=None
            xto=None
    if (xfrom!=None):
        fill([xfrom,xfrom,xto,xto],[ymin,ymax,ymax,ymin],colour,alpha=alpha,edgecolor=None)

printx=0
printy=1.0
printcolwidths=[]
def printline(coltexts,setprintcolwidths=None,setprinty=None):
    global printx,printy,printcolwidths
    printlineheight=-0.02
    if (setprintcolwidths is not None):
        printcolwidths=setprintcolwidths
    if (setprinty is not None):
        printy=setprinty
    if (type(coltexts) is not list):
        coltexts=[coltexts]
    for c in range(len(coltexts)):
        if (c<len(printcolwidths)):
            text(printx+printcolwidths[c]/40.0,printy,coltexts[c],fontsize=8)
        else:
            text(printx,printy,coltexts[c],fontsize=8)
    printy+=printlineheight

def norm_centre(map2d, modelmap2d=None): # Normalize ABS(map2d) with the central (peak) value
    m,n = map2d.shape
    map2d = np.abs(map2d) # We are concerned with power beams after all
    
    _m, _n = np.meshgrid(np.arange(m), np.arange(n))
    centre = (_m-m/2.)**2+(_n-n/2.)**2 <= 9 # APH refactored, unchanged 02/2017. [3^2->29 pixels, 2^2->13 pixels]
    
    ## Used prior to Sept 2016, but too simplistic in the presence of gridding & noise
    #C = np.max(map2d[centre])
    
    ## Introduced by APH 26/09/2016, the following is more robust against centering errors and noise
    x = np.percentile(map2d[centre],90) # Consider only the 10% largest values around the centre (e.g. 4 out of 29)
    C = np.mean(map2d[map2d>=x]) # Mean of the few highest values around the centre
    
    map2d = map2d/C # Normalized
    return map2d
    ## Introduced in Feb 2017 to avoid introducing compression due to averaging the peak, when there's high SNR and small grid
    if modelmap2d is not None: # Normalize in best-fit sense
        centre = (_m-m/2.)**2+(_n-n/2.)**2 <= (n/4.)**2 # Inner 16th of the map
        modelcentre = np.abs(modelmap2d[centre])
        p = sp.optimize.fmin(lambda p: np.sum((p[0]*map2d[centre] - modelcentre)**2), [1], disp=False)
        print("Refining beam by x%g to fit model"% p[0])
        map2d *= p[0]
    
    return map2d

def geterrorbeam(thisbeam,modelbeam,contourdB=-12): # Assumes all are centred on same grid
    gridsize = modelbeam.shape[0]
    modelbeam = norm_centre(modelbeam)
    thisbeam = norm_centre(thisbeam)
    powbeam=20.0*np.log10(np.abs(modelbeam)).reshape(-1)
    dbeam=(np.abs(thisbeam)**2-np.abs(modelbeam)**2).reshape(-1)
    valid12dB=np.nonzero(powbeam>=contourdB)[0]
    dbeam[np.nonzero(np.isnan(dbeam))[0]]=0.0 # Error beams are 0 outside of area of interest
    errorbeam=dbeam.reshape([gridsize,gridsize])
    if (len(valid12dB)<1):
        maxbeam=np.nan
        stdbeam=np.nan
    else:
        maxbeam=np.max(np.abs(errorbeam).reshape(-1)[valid12dB])
        stdbeam=np.std(errorbeam.reshape(-1)[valid12dB])
    return errorbeam,maxbeam,stdbeam

def rmserrorbeam(errorbeams,modelbeam,contourdB=-12): # Assumes all are centred on same grid
    powbeam=20.0*np.log10(np.abs(norm_centre(modelbeam))).reshape(-1)
    valid12dB=np.nonzero(powbeam>=contourdB)[0]
    rmserrorbeam = (np.sum([eb**2 for eb in errorbeams], axis=0)/float(len(errorbeams)))**.5
    return rmserrorbeam

def calc_rmserrorbeam(allbeamG,modelbeamG):
    """
        Computes the singular RMS pattern of the point-wise RMS over all error beams wrt. the model beam.
        Assumes all beams are centred on the same grid.
        
        Example: rmsbeam = calc_rmserrorbeam([r['beamh'].mGx[0,:,:] for r in results],
                                             norm_centre(np.mean([r['beamh'].mGx[0,:,:] for r in results],axis=0)))
        
        @param allbeamG: a list of 2D beam patterns.
        @param modelbeamG: the model to use to compute the error beam patterns (2D array).
        @return: the RMS pattern (2D array) which is 0. outside the area of interest
    """
    errbeams = [geterrorbeam(beamG,modelbeamG)[0] for beamG in allbeamG]
    rmserrbeam = rmserrorbeam(errbeams,modelbeamG)
    return rmserrbeam


def HOD(rawtime, tzoffset):
    """
        @param rawtime: raw timestamp ito UTC.
        @return: hour of day in local time [0,24] with timezone offset from UTC as specified. 
    """
    tgm = time.gmtime(rawtime) # Don't use time.localtime() since servers are sometimes at UTC
    return ((tgm[3] + tgm[4]/60.0 + tgm[5]/3600.0 + tzoffset) % 24)

# def uploadimages(results,emssresults,isoptimalind,gspreadsheet):
#     fformat='jpg'
#     antennaname=results[0]['scanantenna'].lower()
#     antnumber=int(antennaname[1:])
#     row=antnumber/10+1
#     col_offset=antnumber%10
#     dummydft=emssresults['dft_dummy']
#
#     plt.figure(100,figsize=(8,6),dpi=80)
#     plt.clf()
#     dft_avgh=np.mean([results[ind]['dfth'].nopointingdevmap for ind in isoptimalind],axis=0)
#     dummydft.nopointingdevmap=dft_avgh
#     dummydft.plot('nopointingdev',clim=[-1,1],doclf=True,docolorbar=False)
#     plt.xlim([-7.5,7.5])
#     plt.ylim([-7.5,7.5])
#     plt.xlabel('')
#     plt.ylabel('')
#     plt.gca().get_xaxis().set_visible(False)
#     plt.gca().get_yaxis().set_visible(False)
#     plt.gca().axis('off')
#     plt.title(antennaname,fontsize=30)
#     buf = io.BytesIO()
#     plt.savefig(buf, format=fformat,bbox_inches='tight')
#     buf.seek(0)
#     if (results[0]['targetname']=='INTELSAT 22 (IS-22)'):
#         gdir=dvsholog.GoogleDirectory(directoryid='15H93GMKzAOpD_66e06D9Lw2KKmAN-hr9')#IS-22 (H)
#         fileid=gdir.upload(antennaname+'.'+fformat,buf)
#         gspreadsheet.update_row('IS-22 (H)',['=IMAGE(SUBSTITUTE("https://drive.google.com/open?id='+fileid+'","https://drive.google.com/open?id=","https://docs.google.com/uc?export=download&id="))'],row,col_offset)
#     elif (results[0]['targetname']=='INTELSAT NEW DAWN'):
#         gdir=dvsholog.GoogleDirectory(directoryid='1ddm10O3_xYrxbQt6Znre8k2Ivv4sDd_c')#ISND (H)
#         fileid=gdir.upload(antennaname+'.'+fformat,buf)
#         gspreadsheet.update_row('ISND (H)',['=IMAGE(SUBSTITUTE("https://drive.google.com/open?id='+fileid+'","https://drive.google.com/open?id=","https://docs.google.com/uc?export=download&id="))'],row,col_offset)
#     buf.close()
#
#     plt.figure(100,figsize=(8,6),dpi=80)
#     plt.clf()
#     dft_avgh=np.mean([results[ind]['dfth'].devmap for ind in isoptimalind],axis=0)
#     dummydft.devmap=dft_avgh
#     dummydft.plot('dev',clim=[-1,1],doclf=True,docolorbar=False)
#     plt.xlim([-7.5,7.5])
#     plt.ylim([-7.5,7.5])
#     plt.xlabel('')
#     plt.ylabel('')
#     plt.gca().get_xaxis().set_visible(False)
#     plt.gca().get_yaxis().set_visible(False)
#     plt.gca().axis('off')
#     plt.title(antennaname,fontsize=30)
#     buf = io.BytesIO()
#     plt.savefig(buf, format=fformat,bbox_inches='tight')
#     buf.seek(0)
#     if (results[0]['targetname']=='INTELSAT 22 (IS-22)'):
#         gdir=dvsholog.GoogleDirectory(directoryid='1CWaGQDHFnHMsOmjN0kfYBtjtPn_otFWp')#IS-22 (H, no offset)
#         fileid=gdir.upload(antennaname+'.'+fformat,buf)
#         gspreadsheet.update_row('IS-22 (H, no offset)',['=IMAGE(SUBSTITUTE("https://drive.google.com/open?id='+fileid+'","https://drive.google.com/open?id=","https://docs.google.com/uc?export=download&id="))'],row,col_offset)
#     elif (results[0]['targetname']=='INTELSAT NEW DAWN'):
#         gdir=dvsholog.GoogleDirectory(directoryid='1NpKXRSrSvHrhLQ2K0fIgOECH-0wceQJr')#ISND (H, no offset)
#         fileid=gdir.upload(antennaname+'.'+fformat,buf)
#         gspreadsheet.update_row('ISND (H, no offset)',['=IMAGE(SUBSTITUTE("https://drive.google.com/open?id='+fileid+'","https://drive.google.com/open?id=","https://docs.google.com/uc?export=download&id="))'],row,col_offset)
#     buf.close()


def generate_report(rawprods,results,discardedresults,rawonaxis,beaconpol,tilt,emssfreq,emssresults,reportfilename,dMHz=0.01,targetfreqGHz=None,
                    bestfitbeams=None, eval_reflection=None, tzoffset=2, sunspec_lim=0,windspec_lim=13.4,sunwindspec_lim=(0,99)):
    """New report as to be proposed by aph@ska.ac.za 05/2016
        @param bestfitbeams: if specified and (h, v, label), these are the polynomial fit reference complex patterns to use instead of the average of the current dataset; default None. label may have two parts separated by | e.g. "short|verbose".
        @param eval_reflection: True to add two pages with exploratory analysis of reflection efficiency; default None i.e. only do so if scan resolution < 0.6 m.
        @param tzoffset: hours by which observation's local time is offset from UTC (override server timezone); default +2.
        @param sunspec_lim: greatest sun-boresight angle marking degraded conditions; default 0 deg.
        @param windspec_lim: greatest gusting wind speed not qualifying as degraded conditions; default 13.4 m/s.
        @param sunwindspec_lim: (sun-boresight angle, gust wind speed) which, if both occur simultaneously, marks degraded conditions; default (0 deg, 99 m/s).
        @return: ...., peaks of error beams against MODEL H & V, RMS error beams against MODEL H & V, bestfit beams H & V, subrot_y H & V
    """
    if (len(results) == 0):
        print("No unflagged results to report on!")
        return
    print(reportURL(reportfilename))
    dummybeam=emssresults['beam_dummy']
    dummydft=emssresults['dft_dummy']
    ebextent = 3 * (1.2*(300/emssfreq)/13.5) * (180/np.pi) # Error beam plots limited to ~second null assuming circular aperture diam 13.5m
    # Scale to specified frequency for reporting
    for result in results:
        freqscaling = targetfreqGHz/(result['dfth'].freqMHz/1e3) if targetfreqGHz else 1.0
        result['dfth'].gain(freqscaling=freqscaling)
        result['dftv'].gain(freqscaling=freqscaling)
    
    plt.close('all') # Avoid trouble when re-using numbered figures.
    with PdfPages(reportfilename) as pdf:
        warnings = [] # Populated with text lines to print on page 1
        
        temp_avg=np.array([result['temp_avg'] for result in results])
        temp_min=np.array([result['temp_min'] for result in results])
        temp_max=np.array([result['temp_max'] for result in results])
        wind_avg=np.array([result['wind_avg'] for result in results])
        wind_min=np.array([result['wind_min'] for result in results])
        wind_max=np.array([result['wind_max'] for result in results])
        el_avg=np.array([result['el_avg'] for result in results])
        sun_avg=np.array([result['sun_avg'] for result in results])
        cellsize=results[0]['dfth'].mapsize/results[0]['dfth'].gridsize
        conv=(results[0]['dfth'].wavelength/360.0)/cellsize
        h_az_pointing=[-np.arcsin(conv*result['dfth'].nopointingphasegradient[0]/np.cos(result['el_avg']*np.pi/180.0))*180.0/np.pi*60.0*60.0 for result in results]
        h_el_pointing=[np.arcsin(conv*result['dfth'].nopointingphasegradient[1])*180.0/np.pi*60.0*60.0 for result in results]
        v_az_pointing=[-np.arcsin(conv*result['dftv'].nopointingphasegradient[0]/np.cos(result['el_avg']*np.pi/180.0))*180.0/np.pi*60.0*60.0 for result in results]
        v_el_pointing=[np.arcsin(conv*result['dftv'].nopointingphasegradient[1])*180.0/np.pi*60.0*60.0 for result in results]
        hour_of_day=np.array([HOD(result['time_avg'], tzoffset) for result in results]) # APH corrected timezone (kat servers are GMT+0!)
        
        # Note: all "i..." indices are against EVERYTHING e.g. 'results'. Use take(..,i...) to get subsets
        take = lambda res,indices: np.asarray([res[ind] for ind in indices])
        issunwind=(sun_avg<sunwindspec_lim[0])*(wind_max>sunwindspec_lim[1])
        isoptimal=(np.logical_or(hour_of_day < 5,hour_of_day > 19)*(wind_max<=4.1)*(wind_avg<=2.9)*(temp_min>=-5)*(temp_max<=35))*(np.logical_not(issunwind))
        isnominal=((wind_max<=windspec_lim)*(wind_avg<=9.8)*(temp_min>=-5)*(temp_max<=40)*(sun_avg>sunspec_lim))*(np.logical_not(isoptimal))*(np.logical_not(issunwind))
        isoptimalind=np.nonzero(isoptimal)[0]
        isspecind=np.nonzero(isoptimal|isnominal)[0]
        if (len(isspecind) == 0):
            isspecind = [True]*len(results)
            warnings.append("all results recorded outside of specified environmental conditions!")
        
        indof = lambda res, val: np.argwhere(np.asarray(res)==val).squeeze()
        eff_combined=np.asarray([result['dfth'].eff0_phase+result['dftv'].eff0_phase for result in results])
        iworst = indof(eff_combined,np.min(take(eff_combined,isspecind)))
        ibest = indof(eff_combined,np.max(take(eff_combined,isspecind)))
        
        # "Analytical" reference results
        h_modelaper = emssresults['dfth']
        v_modelaper = emssresults['dftv']
        h_modelbeam = emssresults['beamh']
        v_modelbeam = emssresults['beamv']
        
        # "Empirical" reference results
        if (bestfitbeams): # Best fit beams passed to this function, assumed high SNR. Must be {h 2D, v 2D, label}
            h_bestfitbeam = bestfitbeams[0]
            v_bestfitbeam = bestfitbeams[1]
            h_bestfitbeamr = h_bestfitbeam # "...beamr" are only used for plots of RAW error patterns - not passed to this function.
            v_bestfitbeamr = v_bestfitbeam
            _bestfit_ = bestfitbeams[-1].split("|")[0] if "|" in bestfitbeams[-1] else "prescribed"
        else: # Best fit beams calculated from averages of data being analysed
            # The "typical beam" is best represented by the average over "all in spec conditions" than the average over "only optimal"
            h_bestfitbeam = norm_centre(np.mean([results[ind]['beamh'].mGx[0,:,:] for ind in isspecind],axis=0))
            v_bestfitbeam = norm_centre(np.mean([results[ind]['beamv'].mGx[0,:,:] for ind in isspecind],axis=0))
            # RAW beams, will be noisy if number of cycles is small but it's only used for plots.
            h_bestfitbeamr = norm_centre(np.mean([results[ind]['beamh'].Gx[0,:,:] for ind in isspecind],axis=0))
            v_bestfitbeamr = norm_centre(np.mean([results[ind]['beamv'].Gx[0,:,:] for ind in isspecind],axis=0))
            _bestfit_ = "average(spec)"
        
        # Error patterns for all results, all based on __fitted beams__
        h_errbm = [geterrorbeam(result['beamh'].mGx[0,:,:],h_modelbeam.mGx[0,:,:]) for result in results]
        v_errbm = [geterrorbeam(result['beamv'].mGx[0,:,:],v_modelbeam.mGx[0,:,:]) for result in results]
        h_errba = [geterrorbeam(result['beamh'].mGx[0,:,:],h_bestfitbeam) for result in results]
        v_errba = [geterrorbeam(result['beamv'].mGx[0,:,:],v_bestfitbeam) for result in results]
        # Singular RMS patterns under all "spec" conditions
        h_rmserrbm = rmserrorbeam([h_errbm[ind][0] for ind in isspecind], h_modelbeam.mGx[0,:,:])
        v_rmserrbm = rmserrorbeam([v_errbm[ind][0] for ind in isspecind], v_modelbeam.mGx[0,:,:])
        h_rmserrba = rmserrorbeam([h_errba[ind][0] for ind in isspecind], h_bestfitbeam)
        v_rmserrba = rmserrorbeam([v_errba[ind][0] for ind in isspecind], v_bestfitbeam)
        
        # Worst error beams for each pol separately
        iworsterr_emss = [indof([eb[1] for eb in h_errbm],np.max(take([eb[1] for eb in h_errbm],isspecind))),
                          indof([eb[1] for eb in v_errbm],np.max(take([eb[1] for eb in v_errbm],isspecind)))]
        iworsterr_avg = [indof([eb[1] for eb in h_errba],np.max(take([eb[1] for eb in h_errba],isspecind))),
                         indof([eb[1] for eb in v_errba],np.max(take([eb[1] for eb in v_errba],isspecind)))]
        # Best error beam considering both pols at same time. APH added 01/2017
        eb = [(h[1]**2+v[1]**2) for h,v in zip(h_errbm,v_errbm)]
        ibesterr = indof(eb,np.min(take(eb,isspecind)))
        
        _opt_ = "average(optimal)"
        if (len(isoptimalind)==0):
            _opt_ = "best[errbm](spec)" # APH changed [eff] to [errbm] 01/2017
            isoptimalind = [ibesterr] # ^^^ changed ibest to ibesterr
            warnings.append('no optimal cycles!!! Using '+_opt_+' instead of average(optimal)')
        
        ### Front page with vital stats summaries ##############################################
        fig=figure(1,figsize=(8.27, 11.69), dpi=100)
        clf()
        gca().set_axis_off()
        printline('dvsholog version: %s'%(dvsholog.__version__),setprinty=1.0)
        printline('Processed on: %s'%(time.ctime()))
        printline('')
        
        scanant = results[0]['scanantenna']
        printline('Scan antenna: %s'%(scanant))
        printline('Reference antenna: %s'%(results[0]['trackantenna']))
        printline('')
        
        scanext = results[0]['beamh'].dataset.findsampling(results[0]['beamh'].dataset.ll,results[0]['beamh'].dataset.mm,results[0]['beamh'].dataset.flagmask)[1]
        printline('Scan extent clipped to %.1f deg, aperture plane resolution ~ %.2f m'%(scanext*180/np.pi,1.2*(300/emssfreq)/scanext))
        if (eval_reflection is None):
            eval_reflection = (1.2*(300/emssfreq)/scanext) <= 0.6
        if not eval_reflection:
            printline('    Omitting reflection / diffraction analysis.')
        
        printline('Target(s):')
        for tg in set(['%s, %.1fMHz (%d channels around %d), %s pol beacon at %.1f degrees tilt'%((r['targetname'],r['dfth'].freqMHz)+(lambda ch:(len(ch),np.mean(ch)))(r['dfth'].dataset.getchannelindices(r['dfth'].freqMHz,dMHz))+(beaconpol,tilt-180.0)) for r in results]):
            printline('    '+tg)
        printline('Filename(s):')
        uniquedatasets = set([r["beamh"].dataset for r in results])
        for d in uniquedatasets:
            printline('    %s (%.1f deg extent)'%(d.filename,d.findsampling(d.ll,d.mm,0*d.flagmask)[1]*180/np.pi)) # TODO better un-flagging
        printline('From %s until %s'%(time.ctime(np.min([result['time_min'] for result in results])),time.ctime(np.max([result['time_max'] for result in results]))))
        printline('    All times quoted in this report are %s'%time.tzname[time.daylight]) # Valid for time.ctime
        
        cycleduration=(results[0]['time_max']-results[0]['time_min'])/60.0/60.0#in hours
        printline('Number of good cycles: %d (%d discarded), cycle duration: %d [minutes]'%(len(results),len(discardedresults),cycleduration*60))
        printline('    of which %d optimal, %d nominal, %d not considered for "spec"'%(len(np.nonzero(isoptimal)[0]),len(np.nonzero(isnominal)[0]),len(results)-len(isspecind)))
        for warn in warnings:
            printline('WARNING: '+warn)
        
        # Singular average patterns under "optimal" conditions
        beam_avgh = norm_centre(np.mean([results[ind]['beamh'].Gx[0,:,:] for ind in isoptimalind],axis=0))
        beam_avgv = norm_centre(np.mean([results[ind]['beamv'].Gx[0,:,:] for ind in isoptimalind],axis=0))
        beam_avghm = norm_centre(np.mean([results[ind]['beamh'].mGx[0,:,:] for ind in isoptimalind],axis=0))
        beam_avgvm = norm_centre(np.mean([results[ind]['beamv'].mGx[0,:,:] for ind in isoptimalind],axis=0))
        
        printline('Best fit reference for error beams:')
        printline('    '+_bestfit_+('' if (bestfitbeams is None) else (' = '+bestfitbeams[-1].split("|")[-1])))
        printline('')
        
        printline(['Ambient temperture: "mean (min to max)"','%.1f (%.1f to %.1f)'%(np.mean(temp_avg),np.min(temp_avg),np.max(temp_avg)),'[$^o$C]'],setprintcolwidths=[0,22,38])
        printline(['Wind speed:','%.1f (%.1f to %.1f, gust %.1f)'%(np.mean(wind_avg),np.min(wind_avg),np.max(wind_avg),np.max(wind_max)),'[mps]'])
        printline(['Elevation:','%.1f (%.1f to %.1f)'%(np.mean(el_avg),np.min(el_avg),np.max(el_avg)),'[degrees]'])
        printline(['Sun angle:','%.1f (%.1f to %.1f)'%(np.mean(sun_avg),np.min(sun_avg),np.max(sun_avg)),'[degrees]'])
        printline('')
        
        # b[2] or [-1] = stddev over pattern
        h_err_beamemss=[b[-1]*100.0 for b in h_errbm]
        v_err_beamemss=[b[-1]*100.0 for b in v_errbm]
        h_err_beam=[b[-1]*100.0 for b in h_errba]
        v_err_beam=[b[-1]*100.0 for b in v_errba]
        # b[1] == max over pattern
        h_err_beamemssmax=[b[1]*100.0 for b in h_errbm]
        v_err_beamemssmax=[b[1]*100.0 for b in v_errbm]
        h_err_beammax=[b[1]*100.0 for b in h_errba]
        v_err_beammax=[b[1]*100.0 for b in v_errba]
        
        # Further data for all results
        h_feedoffsetx=[result['dfth'].feedoffset[0] for result in results]
        h_feedoffsety=[result['dfth'].feedoffset[1] for result in results]
        h_feedoffsetz=[result['dfth'].feedoffset[2] for result in results]
        v_feedoffsetx=[result['dftv'].feedoffset[0] for result in results]
        v_feedoffsety=[result['dftv'].feedoffset[1] for result in results]
        v_feedoffsetz=[result['dftv'].feedoffset[2] for result in results]
        
        h_subroty=[dict([en[:2] for en in result['dfth'].subparam])['subroty'] for result in results]
        v_subroty=[dict([en[:2] for en in result['dftv'].subparam])['subroty'] for result in results]

        h_eff_phase = [result['dfth'].eff0_phase*100.0 for result in results]
        v_eff_phase = [result['dftv'].eff0_phase*100.0 for result in results]
        h_rms = [result['dfth'].rms0_mm for result in results]
        v_rms = [result['dftv'].rms0_mm for result in results]
        
        printline(['','H measurement','V Measurement'],setprintcolwidths=[0,17,28])
        printline(['Az pointing error: "mean (min to max)"','%.1f (%.1f to %.1f)'%(np.mean(h_az_pointing),np.min(h_az_pointing),np.max(h_az_pointing)),'%.1f (%.1f to %.1f)'%(np.mean(v_az_pointing),np.min(v_az_pointing),np.max(v_az_pointing)),'[arcsec]'],setprintcolwidths=[0,17,28,38])
        printline(['El pointing error:','%.1f (%.1f to %.1f)'%(np.mean(h_el_pointing),np.min(h_el_pointing),np.max(h_el_pointing)),'%.1f (%.1f to %.1f)'%(np.mean(v_el_pointing),np.min(v_el_pointing),np.max(v_el_pointing)),'[arcsec]'])
        printline('')
        
        printline(['X Feed offset:','%.1f (%.1f to %.1f)'%(np.mean(h_feedoffsetx),np.min(h_feedoffsetx),np.max(h_feedoffsetx)),'%.1f (%.1f to %.1f)'%(np.mean(v_feedoffsetx),np.min(v_feedoffsetx),np.max(v_feedoffsetx)),'[mm]'])
        printline(['Y Feed offset:','%.1f (%.1f to %.1f)'%(np.mean(h_feedoffsety),np.min(h_feedoffsety),np.max(h_feedoffsety)),'%.1f (%.1f to %.1f)'%(np.mean(v_feedoffsety),np.min(v_feedoffsety),np.max(v_feedoffsety)),'[mm]'])
        printline(['Z Feed offset:','%.1f (%.1f to %.1f)'%(np.mean(h_feedoffsetz),np.min(h_feedoffsetz),np.max(h_feedoffsetz)),'%.1f (%.1f to %.1f)'%(np.mean(v_feedoffsetz),np.min(v_feedoffsetz),np.max(v_feedoffsetz)),'[mm]'])

        printline(['Sub roll:','%.2f (%.2f to %.2f)'%(np.mean(h_subroty),np.min(h_subroty),np.max(h_subroty)),'%.2f (%.2f to %.2f)'%(np.mean(v_subroty),np.min(v_subroty),np.max(v_subroty)),'[deg]'])
        printline('')
        
        errbm_pass = lambda peaks: 100.0*len(peaks[peaks<4.05])/len(peaks) # Spec threshold 4%
        printline(['Error beam wrt model: "mean (peak) | Pr(<4%)"','%.1f (%.1f) | %.1f'%(np.max(take(h_err_beamemss,isspecind)),np.max(take(h_err_beamemssmax,isspecind)),errbm_pass(take(h_err_beamemssmax,isspecind))),'%.1f (%.1f) | %.1f'%(np.max(take(v_err_beamemss,isspecind)),np.max(take(v_err_beamemssmax,isspecind)),errbm_pass(take(v_err_beamemssmax,isspecind))),'[%]'])
        printline(['Error beam wrt '+_bestfit_+': "mean (peak)"','%.1f (%.1f)'%(np.max(take(h_err_beam,isspecind)),np.max(take(h_err_beammax,isspecind))),'%.1f (%.1f)'%(np.max(take(v_err_beam,isspecind)),np.max(take(v_err_beammax,isspecind))),'[%]'])
        # nzmean: When there's just 1 result, "xx w.r.t average" == 0 and some special checks are required
        nzmean = lambda data: np.mean(data[data>0]) if (np.max(data)>0) else np.nan
        printline(['RMS error beam wrt model:','%.1f (%.1f)'%(nzmean(h_rmserrbm)*100,np.max(h_rmserrbm)*100),'%.1f (%.1f)'%(nzmean(v_rmserrbm)*100,np.max(v_rmserrbm)*100),'[%]'])
        printline(['RMS error beam wrt '+_bestfit_+':','%.1f (%.1f)'%(nzmean(h_rmserrba)*100,np.max(h_rmserrba)*100),'%.1f (%.1f)'%(nzmean(v_rmserrba)*100,np.max(v_rmserrba)*100),'[%]'])
        printline('')
        
        printline(['Equivalent RMS at %.1fGHz:'%(results[0]['dfth'].freqMHz/1e3 if (targetfreqGHz is None) else targetfreqGHz),'%.2f (%.2f to %.2f)'%(np.mean(h_rms),np.min(h_rms),np.max(h_rms)),'%.2f (%.2f to %.2f)'%(np.mean(v_rms),np.min(v_rms),np.max(v_rms)),'[mm]'])
        printline(['Aperture phase eff at %.1fGHz:'%(results[0]['dfth'].freqMHz/1e3 if (targetfreqGHz is None) else targetfreqGHz),'%.1f (%.1f to %.1f)'%(np.mean(h_eff_phase),np.min(h_eff_phase),np.max(h_eff_phase)),'%.1f (%.1f to %.1f)'%(np.mean(v_eff_phase),np.min(v_eff_phase),np.max(v_eff_phase)),'[%]'])
        fig.set_size_inches([8.27,11.69])
        pdf.savefig()

        ### Summary plots of results ###########################################################
        fig=figure(2,figsize=(8.27, 11.69), dpi=100)
        clf()
        subplot(5,2,2)
        plot_envelope(hour_of_day,[result['temp_avg'] for result in results],[result['temp_min'] for result in results], [result['temp_max'] for result in results])
        xlim([0,24])
        ylabel('Temperature [$^{o}$C]')
        title('Ambient temperature')
        subplot(5,2,1)
        plot_envelope(hour_of_day,[result['wind_avg'] for result in results],[result['wind_min'] for result in results], [result['wind_max'] for result in results])
        xlim([0,24])
        ylabel('Speed [mps]')
        title('Wind speed')
        subplot(5,2,3)
        plot_envelope(hour_of_day,[result['sun_avg'] for result in results],[result['sun_min'] for result in results], [result['sun_max'] for result in results])
        xlim([0,24])
        ylabel('Sun angle [degrees]')
        title('Sun proximity to boresight')
        subplot(5,2,4)
        plot_envelope(hour_of_day,[result['el_avg'] for result in results],[result['el_min'] for result in results], [result['el_max'] for result in results])
        xlim([0,24])
        ylabel('Elevation [degrees]')
        title('Elevation')
        subplot(5,2,6)
        plot_line(hour_of_day,[-result['beamh'].beamoffsetGx[0][0]/np.cos(result['el_avg']*np.pi/180.0)*180.0/np.pi*60.0*60.0 for result in results],'b,')
        plot_line(hour_of_day,[result['beamh'].beamoffsetGx[0][1]*180.0/np.pi*60.0*60.0 for result in results],'g,')
        plot_line(hour_of_day,[-result['beamv'].beamoffsetGx[0][0]/np.cos(result['el_avg']*np.pi/180.0)*180.0/np.pi*60.0*60.0 for result in results],'b+',markersize=3)
        plot_line(hour_of_day,[result['beamv'].beamoffsetGx[0][1]*180.0/np.pi*60.0*60.0 for result in results],'g+',markersize=3)
        plot_line(hour_of_day,[-np.arcsin(conv*result['dfth'].nopointingphasegradient[0]/np.cos(result['el_avg']*np.pi/180.0))*180.0/np.pi*60.0*60.0 for result in results],'b.')
        plot_line(hour_of_day,[np.arcsin(conv*result['dfth'].nopointingphasegradient[1])*180.0/np.pi*60.0*60.0 for result in results],'g.')
        plot_line(hour_of_day,[-np.arcsin(conv*result['dftv'].nopointingphasegradient[0]/np.cos(result['el_avg']*np.pi/180.0))*180.0/np.pi*60.0*60.0 for result in results],'bx',markersize=3)
        plot_line(hour_of_day,[np.arcsin(conv*result['dftv'].nopointingphasegradient[1])*180.0/np.pi*60.0*60.0 for result in results],'gx',markersize=3)
        xlim([0,24])
        leg=legend(['H\'s Az (BP)','H\'s El (BP)','V\'s Az (BP)','V\'s El (BP)',
                'H\'s Az (AP)','H\'s El (AP)','V\'s Az (AP)','V\'s El (AP)'],fontsize=8,loc='best')
        leg.get_frame().set_alpha(0.75)
        ylabel('Pointing error [arcsec]')
        title('Pointing error')
        subplot(5,2,5)
        plot_line(hour_of_day,h_feedoffsetx,'b.')
        plot_line(hour_of_day,h_feedoffsety,'g.')
        plot_line(hour_of_day,h_feedoffsetz,'r.')
        plot_line(hour_of_day,v_feedoffsetx,'bv',markersize=3)
        plot_line(hour_of_day,v_feedoffsety,'gv',markersize=3)
        plot_line(hour_of_day,v_feedoffsetz,'rv',markersize=3)
        xlim([0,24])
        leg=legend(['H\'s x','H\'s y','H\'s z','V\'s x','V\'s y','V\'s z'],fontsize=8,loc='best')
        leg.get_frame().set_alpha(0.75)
        ylabel('Feed offsets [mm]')
        title('Feed offsets')    
        subplot(5,2,7)
        plot_line(hour_of_day,h_err_beamemss,'k.')
        plot_line(hour_of_day,v_err_beamemss,'kv',markersize=3)
        # plot_line(hour_of_day,np.max([h_err_beamemssmax,v_err_beamemssmax],axis=0),'k,')
        plot_line(hour_of_day,h_err_beamemssmax,'k_')
        plot_line(hour_of_day,v_err_beamemssmax,'k|')
        plot_highlights(hour_of_day, cycleduration, isoptimal,0.0, 4.0,colour='g',alpha=0.1)
        plot_highlights(hour_of_day, cycleduration, isnominal,0.0, 4.0,colour='g',alpha=0.05)
        plot_highlights(hour_of_day, cycleduration, isoptimal,4.0, 10.0,colour='r',alpha=0.1)
        plot_highlights(hour_of_day, cycleduration, isnominal,4.0, 10.0,colour='r',alpha=0.05)
        xlim([0,24])
        ylim([0,10])
        ylabel('Error beam [%]')
        title('Error beam wrt model')
        subplot(5,2,9)
        plot_line(hour_of_day,h_err_beam,'k.')
        plot_line(hour_of_day,v_err_beam,'kv',markersize=3)
        # plot_line(hour_of_day,np.max([h_err_beammax,v_err_beammax],axis=0),'k,')
        plot_line(hour_of_day,h_err_beammax,'k_')
        plot_line(hour_of_day,v_err_beammax,'k|')
        plot_highlights(hour_of_day, cycleduration, isoptimal,0.0, 4.0,colour='g',alpha=0.1)
        plot_highlights(hour_of_day, cycleduration, isnominal,0.0, 4.0,colour='g',alpha=0.05)
        plot_highlights(hour_of_day, cycleduration, isoptimal,4.0, 10.0,colour='r',alpha=0.1)
        plot_highlights(hour_of_day, cycleduration, isnominal,4.0, 10.0,colour='r',alpha=0.05)
        xlim([0,24])
        ylim([0,10])
        xlabel('Local hour of day',fontsize=10)
        ylabel('Error beam [%]')
        title('Error beam wrt '+_bestfit_)
        subplot(5,2,8)
        plot_line(hour_of_day,h_rms,'k.')
        plot_line(hour_of_day,v_rms,'kv',markersize=3)
        plot_highlights(hour_of_day, cycleduration, isoptimal,0.3, 0.6,colour='g',alpha=0.1)
        plot_highlights(hour_of_day, cycleduration, isnominal,0.3, 0.6,colour='g',alpha=0.05)
        plot_highlights(hour_of_day, cycleduration, isoptimal,0.6, 1.1,colour='r',alpha=0.1)
        plot_highlights(hour_of_day, cycleduration, isnominal,0.6, 1.1,colour='r',alpha=0.05)
        xlim([0,24])
        ylim([0.3,1.1])
        ylabel('RMS [mm]')
        title('Aperture plane phase RMS')
        subplot(5,2,10)
        plot_line(hour_of_day,h_eff_phase,'k.')
        plot_line(hour_of_day,v_eff_phase,'kv',markersize=3)
        plot_highlights(hour_of_day, cycleduration, isoptimal,91.0, 100.0,colour='g',alpha=0.1)
        plot_highlights(hour_of_day, cycleduration, isnominal,91.0, 100.0,colour='g',alpha=0.05)
        plot_highlights(hour_of_day, cycleduration, isoptimal,70.0, 91.0,colour='r',alpha=0.1)
        plot_highlights(hour_of_day, cycleduration, isnominal,70.0, 91.0,colour='r',alpha=0.05)
        xlim([0,24])
        leg=legend(['H','V'],fontsize=8,loc='best')
        leg.get_frame().set_alpha(0.75)
        xlabel('Local hour of day',fontsize=10)
        ylabel('Efficiency [%]')
        title('Aperture phase efficiency at %gGHz'%(results[0]['dfth'].freqMHz/1e3 if (targetfreqGHz is None) else targetfreqGHz))
        suptitle(results[0]['filename']+': '+ scanant,fontsize=8,x=0.5,y=0.998)
        fig.tight_layout()
        fig.set_size_inches([8.27,11.69])
        pdf.savefig()

        ### Power beams ########################################################################
        beamextent = [h_modelbeam.margin[0],h_modelbeam.margin[-1],h_modelbeam.margin[0],h_modelbeam.margin[-1]]
        fig=figure(3,figsize=(12, 10), dpi=100)
        clf()
        subplot(2,2,1)
        h_modelbeam.plot('Gx','pow',clim=[-90,0],doclf=False)
        plt.contour(np.abs(h_modelbeam.Gx[0,:,:]),extent=beamextent,levels=[10.**(-12.0/20.0)],colors='k',linestyles='dashed')
        xlabel('')
        title('H model %g MHz'%(emssfreq))
        subplot(2,2,2)
        v_modelbeam.plot('Gx','pow',clim=[-90,0],doclf=False)
        plt.contour(np.abs(v_modelbeam.Gx[0,:,:]),extent=beamextent,levels=[10.**(-12.0/20.0)],colors='k',linestyles='dashed')
        xlabel('')
        ylabel('')
        title('V model %g MHz'%(emssfreq))
        subplot(2,2,3)
        dummybeam.Gx[0,:,:]=beam_avgh
        dummybeam.plot('Gx','pow',clim=[-90,0],doclf=False)
        plt.contour(np.abs(beam_avgh),extent=beamextent,levels=[10.**(-12.0/20.0)],colors='k',linestyles='dashed')
        title('H %s %.2f MHz'%(_opt_,results[0]['dfth'].freqMHz))
        subplot(2,2,4)
        dummybeam.Gx[0,:,:]=beam_avgv
        dummybeam.plot('Gx','pow',clim=[-90,0],doclf=False)
        plt.contour(np.abs(beam_avgv),extent=beamextent,levels=[10.**(-12.0/20.0)],colors='k',linestyles='dashed')
        ylabel('')
        title('V %s %.2f MHz'%(_opt_,results[0]['dfth'].freqMHz))
        suptitle('Power beams\n'+results[0]['filename']+': '+ scanant,fontsize=12,x=0.5,y=0.99)
        pdf.savefig()

        ### RMS error beams ####################################################################
        fig = figure(4,figsize=(12, 10), dpi=100)
        clf()
        ebcontours = np.arange(0.5,5,0.5)
        subplot(2,2,1)
        dummybeam.Gx[0,:,:]=h_rmserrbm*100
        dummybeam.plot('Gx','amp',doclf=False,plotextras=False,clim=[0,5.])
        plt.contour(h_rmserrbm*100,extent=beamextent,levels=ebcontours,colors='k')
        ax=plt.gca();im=ax.images;cb=im[-1].colorbar;cb.set_label('%')
        title('H RMS wrt model\n(max %.2f%%, mean %.2f%%)'%(np.max(h_rmserrbm*100),nzmean(h_rmserrbm*100)))
        xlim([-ebextent/2.,ebextent/2.])
        ylim([-ebextent/2.,ebextent/2.])
        subplot(2,2,2)
        dummybeam.Gx[0,:,:]=v_rmserrbm*100
        dummybeam.plot('Gx','amp',doclf=False,plotextras=False,clim=[0,5.])
        plt.contour(v_rmserrbm*100,extent=beamextent,levels=ebcontours,colors='k')
        ax=plt.gca();im=ax.images;cb=im[-1].colorbar;cb.set_label('%')
        title('V RMS wrt model\n(max %.2f%%, mean %.2f%%)'%(np.max(v_rmserrbm*100),nzmean(v_rmserrbm*100)))
        xlim([-ebextent/2.,ebextent/2.])
        ylim([-ebextent/2.,ebextent/2.])
        
        subplot(2,2,3)
        dummybeam.Gx[0,:,:]=h_rmserrba*100
        dummybeam.plot('Gx','amp',doclf=False,plotextras=False,clim=[0,5.])
        plt.contour(h_rmserrba*100,extent=beamextent,levels=ebcontours,colors='k')
        ax=plt.gca();im=ax.images;cb=im[-1].colorbar;cb.set_label('%')
        title('H RMS wrt '+_bestfit_+'\n(max %.2f%%, mean %.2f%%)'%(np.max(h_rmserrba*100),nzmean(h_rmserrba*100)))
        xlim([-ebextent/2.,ebextent/2.])
        ylim([-ebextent/2.,ebextent/2.])
        subplot(2,2,4)
        dummybeam.Gx[0,:,:]=v_rmserrba*100
        dummybeam.plot('Gx','amp',doclf=False,plotextras=False,clim=[0,5.])
        plt.contour(v_rmserrba*100,extent=beamextent,levels=ebcontours,colors='k')
        ax=plt.gca();im=ax.images;cb=im[-1].colorbar;cb.set_label('%')
        title('V RMS wrt '+_bestfit_+'\n(max %.2f%%, mean %.2f%%)'%(np.max(v_rmserrba*100),nzmean(v_rmserrba*100)))
        xlim([-ebextent/2.,ebextent/2.])
        ylim([-ebextent/2.,ebextent/2.])
        suptitle('RMS of all error beams (fitted beams) taken over optimal & nominal cycles\n'+results[0]['filename']+': '+ scanant,fontsize=12,x=0.5,y=0.99)
        pdf.savefig()
        
        ### Error beam w.r.t. model & w.r.t average ############################################
        for fno,(what,refh,refv,refhm,refvm,iworst_) in enumerate([
                ["model",h_modelbeam.Gx[0,:,:],v_modelbeam.Gx[0,:,:],h_modelbeam.mGx[0,:,:],v_modelbeam.mGx[0,:,:],iworsterr_emss],
                [_bestfit_,h_bestfitbeamr,v_bestfitbeamr,h_bestfitbeam,v_bestfitbeam,iworsterr_avg]]):
            # Error beams as average(best) relative to either model or average(spec)
            errorbeamGx,maxGx,stdGx=geterrorbeam(beam_avgh,refh)
            errorbeamGy,maxGy,stdGy=geterrorbeam(beam_avgv,refv)
            filterederrorbeamGx,maxGx,stdGx=geterrorbeam(beam_avghm,refhm)
            filterederrorbeamGy,maxGy,stdGy=geterrorbeam(beam_avgvm,refvm)
            stdmGx=np.nanstd((errorbeamGx-filterederrorbeamGx).reshape(-1))
            stdmGy=np.nanstd((errorbeamGy-filterederrorbeamGy).reshape(-1))

            fig=figure(5+fno,figsize=(12, 10), dpi=100)
            clf()
            subplot(2,4,1)
            dummybeam.Gx[0,:,:]=np.abs(filterederrorbeamGx)*100.
            dummybeam.plot('Gx','amp',doclf=False,plotextras=False,clim=[0,10.])
            plt.contour(np.abs(beam_avgh),extent=beamextent,levels=[10.**(-12.0/20.0)],colors='k',linestyles='dashed')
            ax=plt.gca();im=ax.images;cb=im[-1].colorbar;cb.remove();
            xlabel('')
            title('H fitted (best)\n(max %.2f%%, std %.2f%%)'%(maxGx*100.,stdGx*100.))
            xlim([-ebextent/2.,ebextent/2.])
            ylim([-ebextent/2.,ebextent/2.])
            subplot(2,4,2)
            dummybeam.Gx[0,:,:]=np.abs(filterederrorbeamGy)*100.
            dummybeam.plot('Gx','amp',doclf=False,plotextras=False,clim=[0,10.])
            plt.contour(np.abs(beam_avgv),extent=beamextent,levels=[10.**(-12.0/20.0)],colors='k',linestyles='dashed')
            ax=plt.gca();im=ax.images;cb=im[-1].colorbar;cb.remove();
            xlabel('')
            ylabel('')
            title('V fitted (best)\n(max %.2f%%, std %.2f%%)'%(maxGy*100.,stdGy*100.))
            xlim([-ebextent/2.,ebextent/2.])
            ylim([-ebextent/2.,ebextent/2.])
            subplot(2,4,5)
            dummybeam.Gx[0,:,:]=np.abs(errorbeamGx)*100.
            dummybeam.plot('Gx','amp',doclf=False,plotextras=False,clim=[0,10.])
            plt.contour(np.abs(beam_avgh),extent=beamextent,levels=[10.**(-12.0/20.0)],colors='k',linestyles='dashed')
            ax=plt.gca();im=ax.images;cb=im[-1].colorbar;cb.remove();
            title('H raw (best)\n(stdev %.2f%% wrt fitted)'%(stdmGx*100.))
            xlim([-ebextent/2.,ebextent/2.])
            ylim([-ebextent/2.,ebextent/2.])
            subplot(2,4,6)
            dummybeam.Gx[0,:,:]=np.abs(errorbeamGy)*100.
            dummybeam.plot('Gx','amp',doclf=False,plotextras=False,clim=[0,10.])
            plt.contour(np.abs(beam_avgv),extent=beamextent,levels=[10.**(-12.0/20.0)],colors='k',linestyles='dashed')
            ax=plt.gca();im=ax.images;cb=im[-1].colorbar;cb.remove();
            ylabel('')
            title('V raw (best)\n(stdev %.2f%% wrt fitted)'%(stdmGy*100.))
            xlim([-ebextent/2.,ebextent/2.])
            ylim([-ebextent/2.,ebextent/2.])

            # APH added columns to show worst(norm+opt) in addition to above avg(opt)
            try:
                h_worst = geterrorbeam(results[iworst_[0]]['beamh'].Gx[0,:,:],refh)
                v_worst = geterrorbeam(results[iworst_[1]]['beamv'].Gx[0,:,:],refv)
                h_worstm = geterrorbeam(results[iworst_[0]]['beamh'].mGx[0,:,:],refhm)
                v_worstm = geterrorbeam(results[iworst_[1]]['beamv'].mGx[0,:,:],refvm)
            except:
                h_worst=np.tile(np.nan,refh.shape),np.nan,np.nan
                v_worst=h_worst
                h_worstm=h_worst
                v_worstm=h_worst
            subplot(2,4,3)
            dummybeam.Gx[0,:,:]=np.abs(h_worstm[0])*100.
            dummybeam.plot('Gx','amp',doclf=False,plotextras=False,clim=[0,10.])
            plt.contour(np.abs(beam_avgh),extent=beamextent,levels=[10.**(-12.0/20.0)],colors='k',linestyles='dashed')
            ax=plt.gca();im=ax.images;cb=im[-1].colorbar;cb.remove();
            xlabel('')
            ylabel('')
            title('H fitted (worst)\n(max %.2f%%, std %.2f%%)'%(h_worstm[1]*100.,h_worstm[2]*100.))
            xlim([-ebextent/2.,ebextent/2.])
            ylim([-ebextent/2.,ebextent/2.])
            subplot(2,4,4)
            dummybeam.Gx[0,:,:]=np.abs(v_worstm[0])*100.
            dummybeam.plot('Gx','amp',doclf=False,plotextras=False,clim=[0,10.])
            ax=plt.gca();im=ax.images;cb=im[-1].colorbar;cb.set_label('%')
            plt.contour(np.abs(beam_avgv),extent=beamextent,levels=[10.**(-12.0/20.0)],colors='k',linestyles='dashed')
            xlabel('')
            ylabel('')
            title('V fitted (worst)\n(max %.2f%%, std %.2f%%)'%(v_worstm[1]*100.,v_worstm[2]*100.))
            xlim([-ebextent/2.,ebextent/2.])
            ylim([-ebextent/2.,ebextent/2.])
            subplot(2,4,7)
            dummybeam.Gx[0,:,:]=np.abs(h_worst[0])*100.
            dummybeam.plot('Gx','amp',doclf=False,plotextras=False,clim=[0,10.])
            plt.contour(np.abs(beam_avgh),extent=beamextent,levels=[10.**(-12.0/20.0)],colors='k',linestyles='dashed')
            ax=plt.gca();im=ax.images;cb=im[-1].colorbar;cb.remove();
            ylabel('')
            title('H raw (worst)')
            xlim([-ebextent/2.,ebextent/2.])
            ylim([-ebextent/2.,ebextent/2.])
            subplot(2,4,8)
            dummybeam.Gx[0,:,:]=np.abs(v_worst[0])*100.
            dummybeam.plot('Gx','amp',doclf=False,plotextras=False,clim=[0,10.])
            ax=plt.gca();im=ax.images;cb=im[-1].colorbar;cb.set_label('%')
            plt.contour(np.abs(beam_avgv),extent=beamextent,levels=[10.**(-12.0/20.0)],colors='k',linestyles='dashed')
            ylabel('')
            title('V raw (worst)')
            xlim([-ebextent/2.,ebextent/2.])
            ylim([-ebextent/2.,ebextent/2.])

            suptitle(('Error beams wrt '+what+' for: best = '+_opt_+'; worst = worst[errbm per pol](spec)\n')+results[0]['filename']+': '+ scanant,fontsize=12,x=0.5,y=0.99)
            pdf.savefig()
        
        ### Aperture amplitude maps ############################################################
        fig=figure(6+fno,figsize=(12, 10), dpi=100)
        clf()
        subplot(2,2,1)
        h_modelaper.plot('amp',doclf=False)
        xlabel('')
        title('H model %g MHz'%(emssfreq))
        subplot(2,2,2)
        v_modelaper.plot('amp',doclf=False)
        xlabel('')
        ylabel('')
        title('V model %g MHz'%(emssfreq))
        subplot(2,2,3)
        dummydft.ampmap=np.mean([results[ind]['dfth'].ampmap for ind in isoptimalind],axis=0)
        dummydft.plot('amp',doclf=False)
        title('H '+_opt_)
        subplot(2,2,4)
        dummydft.ampmap=np.mean([results[ind]['dftv'].ampmap for ind in isoptimalind],axis=0)
        dummydft.plot('amp',doclf=False)
        ylabel('')
        title('V '+_opt_)
        suptitle('Aperture plane amplitude maps (illumination)\n'+results[0]['filename']+': '+ scanant,fontsize=12,x=0.5,y=0.99)
        pdf.savefig()
        
        ### Diffraction / reflection analysis for best maps ####################################
        if eval_reflection:
            r_apmaps = [norm_centre(np.abs(results[ibest]['dfth'].ampmap))/norm_centre(np.abs(h_modelaper.ampmap)),
                        norm_centre(np.abs(results[ibest]['dftv'].ampmap))/norm_centre(np.abs(v_modelaper.ampmap))]
            amp_clim = [0,2]
            figure(7+fno,figsize=(12,10), dpi=100)
            clf()
            subplot(2,2,1)
            h_eff_reflect = analyse_reflection([r['dfth'] for r in results], h_modelaper, areafrac=0.9)
            dummydft.ampmap = r_apmaps[0]
            dummydft.plot('amp',clim=amp_clim,doclf=False)
            title('H-pol best[eff] '+time.ctime(results[ibest]['time_avg'])[11:16])
            subplot(2,2,2)
            v_eff_reflect = analyse_reflection([r['dftv'] for r in results], v_modelaper, areafrac=0.9)
            dummydft.ampmap = r_apmaps[1]
            dummydft.plot('amp',clim=amp_clim,doclf=False)
            ylabel('')
            title('V-pol best[eff] '+time.ctime(results[ibest]['time_avg'])[11:16])
            subplot(2,2,3)
            dummydft.ampmap = (r_apmaps[0] + r_apmaps[1]) / 2.
            dummydft.plot('amp',clim=amp_clim,doclf=False)
            ylabel('')
            title('Average H&V above')
            subplot(2,2,4)
            dummydft.ampmap = r_apmaps[0] - r_apmaps[1]
            dummydft.plot('amp',clim=[-amp_clim[1]/4.,amp_clim[1]/4.],doclf=False)
            ylabel('')
            title('Difference H-V above')
            suptitle('Reflecting efficiencies for %s\nH-pol = [%s]%%\nV-pol = [%s]%%\n%s'%(results[0]['filename']+': '+scanant,
                ",".join(map(lambda e:"%.1f"%(e*100),h_eff_reflect)),",".join(map(lambda e:"%.1f"%(e*100),v_eff_reflect)),'CAUTION! Results not corrected for misalignment. Illustrative maps of |Illum measured|/|Illum modelled| below.'), fontsize=12,x=0.5,y=0.99)
            pdf.savefig()
            fno += 1
        
        ### Aperture deviation maps AS REALIZED ################################################
        dev_clim = [-5,5] if emssfreq < 3000 else [-1,1] # [mm]. Diffraction adds ripples below 3 GHz
        delta_clim = [d/4. for d in dev_clim]
        fig=figure(7+fno,figsize=(12, 14), dpi=100)
        clf()
        subplot(4,3,1)
        h_modelaper.plot('nopointingdev',clim=dev_clim,doclf=False)
        xlabel('')
        title('H model %g MHz'%(emssfreq))
        subplot(4,3,2)
        v_modelaper.plot('nopointingdev',clim=dev_clim,doclf=False)
        xlabel('')
        ylabel('')
        title('V model %g MHz'%(emssfreq))
        subplot(4,3,3)
        v_modelaper.plot('nopointingdev',diff=h_modelaper,clim=delta_clim,doclf=False)
        xlabel('')
        ylabel('')
        title('H-V model %g MHz'%(emssfreq))
        
        subplot(4,3,4)
        dft_avgh=np.mean([results[ind]['dfth'].nopointingdevmap for ind in isoptimalind],axis=0)
        dummydft.nopointingdevmap=dft_avgh
        dummydft.plot('nopointingdev',clim=dev_clim,doclf=False)
        xlabel('')
        title('H (best)')
        subplot(4,3,5)
        dft_avgv=np.mean([results[ind]['dftv'].nopointingdevmap for ind in isoptimalind],axis=0)
        dummydft.nopointingdevmap=dft_avgv
        dummydft.plot('nopointingdev',clim=dev_clim,doclf=False)
        xlabel('')
        ylabel('')
        title('V (best)')
        subplot(4,3,6)
        dummydft.nopointingdevmap=dft_avgv-dft_avgh
        dummydft.plot('nopointingdev',clim=delta_clim,doclf=False)
        xlabel('')
        ylabel('')
        title('H-V (best)')
        
        subplot(4,3,7)
        results[iworst]['dfth'].plot('nopointingdev',clim=dev_clim,doclf=False)
        xlabel('')
        title('H (worst)')
        subplot(4,3,8)
        results[iworst]['dftv'].plot('nopointingdev',clim=dev_clim,doclf=False)
        xlabel('')
        ylabel('')
        title('V (worst)')
        subplot(4,3,9)
        results[iworst]['dftv'].plot('nopointingdev',diff=results[iworst]['dfth'],clim=delta_clim,doclf=False)
        xlabel('')
        ylabel('')
        title('H-V (worst) @ '+time.ctime(results[iworst]['time_avg'])[11:16])
        
        subplot(4,3,10)
        results[iworst]['dfth'].plot('nopointingdev',clim=delta_clim,diff=results[ibest]['dfth'],doclf=False)
        title('H worst - H best')
        subplot(4,3,11)
        results[iworst]['dftv'].plot('nopointingdev',clim=delta_clim,diff=results[ibest]['dftv'],doclf=False)
        ylabel('')
        title('V worst - V best')
        subplot(4,3,12)
        dummydft.nopointingdevmap=(results[iworst]['dftv'].nopointingdevmap-results[ibest]['dftv'].nopointingdevmap)-(results[iworst]['dfth'].nopointingdevmap-results[ibest]['dfth'].nopointingdevmap)
        dummydft.plot('nopointingdev',clim=delta_clim,doclf=False)
        ylabel('')
        title('Difference of left')
        suptitle('Total path length deviation maps normal to main reflector surface, corrected only for pointing\n'+\
                 'best = '+_opt_+'; worst = worst[eff](spec)\n'+results[0]['filename']+': '+ scanant,fontsize=12,x=0.5,y=0.99)
        pdf.savefig()

        ### Aperture deviation maps EXPECTED AFTER OPTIMAL ALIGNMENT ###########################
        delta_clim = [d/4. for d in dev_clim]
        fig=figure(8+fno,figsize=(12, 14), dpi=100)
        clf()
        subplot(4,3,1)
        dft_avgh=np.mean([results[ind]['dfth'].devmap for ind in isoptimalind],axis=0)
        dummydft.devmap=dft_avgh
        dummydft.plot('dev',clim=dev_clim,doclf=False)
        xlabel('')
        title('H (best) FEED still incl')
        subplot(4,3,2)
        dft_avgv=np.mean([results[ind]['dftv'].devmap for ind in isoptimalind],axis=0)
        dummydft.devmap=dft_avgv
        dummydft.plot('dev',clim=dev_clim,doclf=False)
        xlabel('')
        ylabel('')
        title('V (best) FEED still incl')
        subplot(4,3,3)
        dummydft.devmap=dft_avgv-dft_avgh
        dummydft.plot('dev',clim=delta_clim,doclf=False)
        xlabel('')
        ylabel('')
        title('H-V (best) FEED still incl')

        subplot(4,3,4)
        dft_avgh=np.mean([results[ind]['dfth'].devmap for ind in isoptimalind],axis=0)
        dummydft.devmap=dft_avgh-h_modelaper.devmap
        dummydft.plot('dev',clim=dev_clim,doclf=False)
        xlabel('')
        title('H (best)')
        subplot(4,3,5)
        dft_avgv=np.mean([results[ind]['dftv'].devmap for ind in isoptimalind],axis=0)
        dummydft.devmap=dft_avgv-v_modelaper.devmap
        dummydft.plot('dev',clim=dev_clim,doclf=False)
        xlabel('')
        ylabel('')
        title('V (best)')
        subplot(4,3,6)
        dummydft.devmap=(dft_avgv-v_modelaper.devmap)-(dft_avgh-h_modelaper.devmap)
        dummydft.plot('dev',clim=delta_clim,doclf=False)
        xlabel('')
        ylabel('')
        title('H-V (best)')
        
        subplot(4,3,7)
        dummydft.devmap=results[iworst]['dfth'].devmap-h_modelaper.devmap
        dummydft.plot('dev',clim=dev_clim,doclf=False)
        xlabel('')
        title('H (worst)')
        subplot(4,3,8)
        dummydft.devmap=results[iworst]['dftv'].devmap-v_modelaper.devmap
        dummydft.plot('dev',clim=dev_clim,doclf=False)
        xlabel('')
        ylabel('')
        title('V (worst)')
        subplot(4,3,9)
        dummydft.devmap=(results[iworst]['dftv'].devmap-v_modelaper.devmap)-(results[iworst]['dfth'].devmap-h_modelaper.devmap)
        dummydft.plot('dev',clim=delta_clim,doclf=False)
        xlabel('')
        ylabel('')
        title('H-V (worst) @ '+time.ctime(results[iworst]['time_avg'])[11:16])
        
        subplot(4,3,10)
        results[iworst]['dfth'].plot('dev',clim=delta_clim,diff=results[ibest]['dfth'],doclf=False)
        title('H worst - H best')
        subplot(4,3,11)
        results[iworst]['dftv'].plot('dev',clim=delta_clim,diff=results[ibest]['dftv'],doclf=False)
        ylabel('')
        title('V worst - V best')
        subplot(4,3,12)
        dummydft.devmap=(results[iworst]['dftv'].devmap-results[ibest]['dftv'].devmap)-(results[iworst]['dfth'].devmap-results[ibest]['dfth'].devmap)
        dummydft.plot('dev',clim=delta_clim,doclf=False)
        ylabel('')
        title('Difference of left')
        suptitle('Total path length deviation maps normal to main reflector surface, corrected for pointing & OFFSETS & FEED PATTERN\n'+\
                 'best = '+_opt_+'; worst = worst[eff](spec)\n'+results[0]['filename']+': '+ scanant,fontsize=12,x=0.5,y=0.99)
        pdf.savefig()
        
        ### On-axis calibration measurements ###################################################
        figure(9+fno,figsize=(12,10), dpi=100)
        clf()
        subplot(2,1,1)
        plot(np.abs(np.concatenate(rawonaxis[0])),'r')
        plot(np.abs(np.concatenate(rawonaxis[1])),'g')
        plot(np.abs(np.concatenate(rawonaxis[2])),'c')
        plot(np.abs(np.concatenate(rawonaxis[3])),'b')
        legend(rawprods)
        title('Amplitude stability')
        ylabel('Amplitude [counts]')
        xlabel('Samples')
        subplot(2,1,2)
        plot(np.unwrap(np.angle(np.concatenate(rawonaxis[0])))*180.0/np.pi,'r')
        plot(np.unwrap(np.angle(np.concatenate(rawonaxis[1])))*180.0/np.pi,'g')
        plot(np.unwrap(np.angle(np.concatenate(rawonaxis[2])))*180.0/np.pi,'c')
        plot(np.unwrap(np.angle(np.concatenate(rawonaxis[3])))*180.0/np.pi,'b')
        title('Phase stability')
        ylabel('Phase [degrees]')
        xlabel('Samples')
        legend(rawprods)
        suptitle('Unprocessed on-axis beacon signals\n%s, %.1fMHz (channel %d), %s pol beacon at %.1f degrees tilt\n%s: %s'%(results[0]['targetname'],results[0]['dfth'].freqMHz,np.mean(results[0]['dfth'].dataset.getchannelindices(results[0]['dfth'].freqMHz,dMHz)),beaconpol,tilt-180.0,results[0]['filename'],scanant),fontsize=12,x=0.5,y=0.99)
        pdf.savefig()

        d = pdf.infodict()
        d['Title'] = 'RTS holography report'
        d['Author'] = socket.gethostname()
        d['Subject'] = 'Holography reflector phase efficiency and error beam report'
        d['Keywords'] = 'rts holography'
        d['CreationDate'] = datetime.datetime.today()
        d['ModDate'] = datetime.datetime.today()
    
    return isoptimalind, isoptimal, isnominal, results, [h_feedoffsetx, h_feedoffsety, h_feedoffsetz], [v_feedoffsetx, v_feedoffsety, v_feedoffsetz], h_err_beamemssmax, v_err_beamemssmax, h_rmserrbm[h_rmserrbm>0], v_rmserrbm[v_rmserrbm>0], h_bestfitbeam, v_bestfitbeam, h_subroty, v_subroty


def analyse_reflection(apermeasured, apermodel, areafrac=1.0):
    """
        Calculates reflection efficiency as the ratio of taper efficiency measured to that modelled with ideal solid reflectors.
        @param apermeasured: aperture plane (complex) illumination pattern. Either single or multiple.
        @param areafrac: the fraction of the (central) area to evaluate; default 100%
        @return: eff_reflection (either single or multiple).
    
    """
    # Original analysis was based on smoothed aperture plane illumination maps
    #apermeasured.analysediffraction() # Caution: generates two figures!
    #return apermeasured.eff_taper_diff
    
    # Analysis relative to high fidelity predicted aperture plane illumination maps
    # For this we neglect aperture plane phase -- phase effects are reflected in phase efficiency!
    x,y = np.meshgrid(np.linspace(-apermodel.mapsize/2.0,apermodel.mapsize/2.0,apermodel.gridsize+1)[:-1],np.linspace(-apermodel.mapsize/2.0,apermodel.mapsize/2.0,apermodel.gridsize+1)[:-1])
    r = np.sqrt(x**2+y**2)
    idxfit = np.logical_and(r>=apermodel.blockdiameter/2.0,r<areafrac*apermodel.dishdiameter/2.0)
    
    taper_model = np.sum(np.abs(apermodel.ampmap[idxfit]))**2 / np.sum(np.abs(apermodel.ampmap[idxfit])**2)
    try:
        eff_reflect = []
        for meas in apermeasured:
            eff_reflect.append( np.sum(np.abs(meas.ampmap[idxfit]))**2 / np.sum(np.abs(meas.ampmap[idxfit])**2) / taper_model )
    except: # Only a single measurement
        eff_reflect = np.sum(np.abs(apermeasured.ampmap[idxfit]))**2 / np.sum(np.abs(apermeasured.ampmap[idxfit])**2) / taper_model
    
    return eff_reflect

    
### TO BE DEPRECATED ########################################################################
def x_generate_report(rawprods,results,discardedresults,rawonaxis,beaconpol,tilt,emssfreq,emssresults,reportfilename,targetfreqGHz=None):
    """As currently in use by
    http://kat-imager.kat.ac.za:8888/notebooks/RTS_reduction_results/3.1-Aperture_Phase_Efficiency/Ku-band%20holography%20report.ipynb"""
    if (len(results) == 0):
        print("No unflagged results to report on!")
        return

    print('http://kat-imager.kat.ac.za:8888/files/RTS_reduction_results/3.1-Aperture_Phase_Efficiency/'+reportfilename)
    dummybeam=emssresults['beam_dummy']
    dummydft=emssresults['dft_dummy']
    ebextent = 3 * (1.2*(300/emssfreq)/13.5) * (180/np.pi) # Error beam plots limited to ~second null assuming circular aperture diam 13.5m
    # Scale to specified frequency for reporting
    for result in results:
        freqscaling = targetfreqGHz/(result['dfth'].freqMHz/1e3) if targetfreqGHz else 1.0
        result['dfth'].gain(freqscaling=freqscaling)
        result['dftv'].gain(freqscaling=freqscaling)
    
    with PdfPages(reportfilename) as pdf:
        temp_avg=np.array([result['temp_avg'] for result in results])
        temp_min=np.array([result['temp_min'] for result in results])
        temp_max=np.array([result['temp_max'] for result in results])
        wind_avg=np.array([result['wind_avg'] for result in results])
        wind_min=np.array([result['wind_min'] for result in results])
        wind_max=np.array([result['wind_max'] for result in results])
        el_avg=np.array([result['el_avg'] for result in results])
        sun_avg=np.array([result['sun_avg'] for result in results])
        cellsize=results[0]['dfth'].mapsize/results[0]['dfth'].gridsize
        conv=(results[0]['dfth'].wavelength/360.0)/cellsize
        h_az_pointing=[-np.arcsin(conv*result['dfth'].nopointingphasegradient[0]/np.cos(result['el_avg']*np.pi/180.0))*180.0/np.pi*60.0*60.0 for result in results]
        h_el_pointing=[np.arcsin(conv*result['dfth'].nopointingphasegradient[1])*180.0/np.pi*60.0*60.0 for result in results]
        v_az_pointing=[-np.arcsin(conv*result['dftv'].nopointingphasegradient[0]/np.cos(result['el_avg']*np.pi/180.0))*180.0/np.pi*60.0*60.0 for result in results]
        v_el_pointing=[np.arcsin(conv*result['dftv'].nopointingphasegradient[1])*180.0/np.pi*60.0*60.0 for result in results]
        hour_of_day=np.array([time.localtime(result['time_avg'])[3]+time.localtime(result['time_avg'])[4]/60.0+time.localtime(result['time_avg'])[5]/(60.0*60.0) for result in results]) # APH THIS IS WRONG, kat servers are in GMT+0!
        #result with best and worst phase efficiency
        eff_combined=[result['dfth'].eff0_phase+result['dftv'].eff0_phase for result in results]
        iworst=argmin(eff_combined)
        ibest=argmax(eff_combined)
        isoptimal=(np.logical_or(hour_of_day < 5,hour_of_day > 19)*(wind_max<=4.1)*(wind_avg<=2.9)*(temp_min>=-5)*(temp_max<=35))
        isnominal=((wind_max<=13.4)*(wind_avg<=9.8)*(temp_min>=-5)*(temp_max<=40))*(logical_not(isoptimal))
        isoptimalind=np.nonzero(isoptimal)[0]
        cycleduration=(results[0]['time_max']-results[0]['time_min'])/60.0/60.0#in hours
        fig=figure(1,figsize=(8.27, 11.69), dpi=100)
        clf()
        gca().set_axis_off()
        printline('dvsholog version: %s'%(dvsholog.__version__),setprinty=1.0)
        if (len(isoptimalind)==0):
            printline('WARNING: no optimal cycles!!! using best instead of optimal')
            isoptimalind=[ibest]

        emssresults['beamh'].fitpoly()
        emssresults['beamv'].fitpoly()
        [result['beamh'].fitpoly() for result in results]
        [result['beamv'].fitpoly() for result in results]
        beam_avghall=np.mean([result['beamh'].Gx[0,:,:] for result in results],axis=0)
        beam_avgvall=np.mean([result['beamv'].Gx[0,:,:] for result in results],axis=0)
        beam_avgh=np.mean([results[ind]['beamh'].Gx[0,:,:] for ind in isoptimalind],axis=0)
        beam_avgv=np.mean([results[ind]['beamv'].Gx[0,:,:] for ind in isoptimalind],axis=0)
        beam_avghallm=np.mean([result['beamh'].mGx[0,:,:] for result in results],axis=0)
        beam_avgvallm=np.mean([result['beamv'].mGx[0,:,:] for result in results],axis=0)
        beam_avghm=np.mean([results[ind]['beamh'].mGx[0,:,:] for ind in isoptimalind],axis=0)
        beam_avgvm=np.mean([results[ind]['beamv'].mGx[0,:,:] for ind in isoptimalind],axis=0)
        h_err_beamemss=[geterrorbeam(result['beamh'].mGx[0,:,:],emssresults['beamh'].mGx[0,:,:])[1]*100.0 for result in results]
        v_err_beamemss=[geterrorbeam(result['beamv'].mGx[0,:,:],emssresults['beamv'].mGx[0,:,:])[1]*100.0 for result in results]
        h_err_beam=[geterrorbeam(result['beamh'].mGx[0,:,:],beam_avghallm)[1]*100.0 for result in results]
        v_err_beam=[geterrorbeam(result['beamv'].mGx[0,:,:],beam_avgvallm)[1]*100.0 for result in results]
        h_feedoffsetx=[result['dfth'].feedoffset[0] for result in results]
        h_feedoffsety=[result['dfth'].feedoffset[1] for result in results]
        h_feedoffsetz=[result['dfth'].feedoffset[2] for result in results]
        v_feedoffsetx=[result['dftv'].feedoffset[0] for result in results]
        v_feedoffsety=[result['dftv'].feedoffset[1] for result in results]
        v_feedoffsetz=[result['dftv'].feedoffset[2] for result in results]
        h_subroty=[dict([en[:2] for en in result['dfth'].subparam])['subroty'] for result in results]
        v_subroty=[dict([en[:2] for en in result['dftv'].subparam])['subroty'] for result in results]

        errorbeamGx,maxGx,stdGx=geterrorbeam(beam_avgh,emssresults['beamh'].Gx[0,:,:])
        errorbeamGy,maxGy,stdGy=geterrorbeam(beam_avgv,emssresults['beamv'].Gx[0,:,:])
        filterederrorbeamGx,maxGx,stdGx=geterrorbeam(beam_avghm,emssresults['beamh'].mGx[0,:,:])
        filterederrorbeamGy,maxGy,stdGy=geterrorbeam(beam_avgvm,emssresults['beamv'].mGx[0,:,:])

        stdGx=np.nanstd((errorbeamGx-filterederrorbeamGx).reshape(-1))
        stdGy=np.nanstd((errorbeamGy-filterederrorbeamGy).reshape(-1))

        printline('Report filename: %s'%(reportfilename))
        printline('Filename: %s'%(results[0]['filename']))
        printline('Scan antenna: %s'%(results[0]['scanantenna']))
        printline('From %s until %s'%(time.ctime(np.min([result['time_min'] for result in results])),time.ctime(np.max([result['time_max'] for result in results]))))
        printline('Number of cycles: %d, cycle duration: %d [minutes]'%(len(results),cycleduration*60))
        printline('of which %d optimal, %d nominal, %d discarded'%(len(np.nonzero(isoptimal)[0]),len(np.nonzero(isnominal)[0]),len(discardedresults)))
        printline('Target: %s, %.1fMHz (channel %d), %s pol beacon at %.1f degrees tilt'%(results[0]['targetname'],results[0]['dfth'].freqMHz,results[0]['dfth'].dataset.getchannelindices(results[0]['dfth'].freqMHz,0.0001),beaconpol,tilt-180.0))
        printline(['Ambient temperture:','%.1f (%.1f to %.1f)'%(np.mean(temp_avg),np.min(temp_avg),np.max(temp_avg)),'[$^o$C]'],setprintcolwidths=[0,19,38])
        printline(['Wind speed:','%.1f (%.1f to %.1f, gust %.1f)'%(np.mean(wind_avg),np.min(wind_avg),np.max(wind_avg),np.max(wind_max)),'[mps]'])
        printline(['Elevation:','%.1f (%.1f to %.1f)'%(np.mean(el_avg),np.min(el_avg),np.max(el_avg)),'[degrees]'])
        printline(['Sun angle:','%.1f (%.1f to %.1f)'%(np.mean(sun_avg),np.min(sun_avg),np.max(sun_avg)),'[degrees]'])
        printline(['','H measurement','V Measurement'],setprintcolwidths=[0,13,26])
        printline(['Az pointing error:','%.1f (%.1f to %.1f)'%(np.mean(h_az_pointing),np.min(h_az_pointing),np.max(h_az_pointing)),'%.1f (%.1f to %.1f)'%(np.mean(v_az_pointing),np.min(v_az_pointing),np.max(v_az_pointing)),'[arcsec]'],setprintcolwidths=[0,13,26,38])
        printline(['El pointing error:','%.1f (%.1f to %.1f)'%(np.mean(h_el_pointing),np.min(h_el_pointing),np.max(h_el_pointing)),'%.1f (%.1f to %.1f)'%(np.mean(v_el_pointing),np.min(v_el_pointing),np.max(v_el_pointing)),'[arcsec]'])
        printline(['X Feed offset:','%.1f (%.1f to %.1f)'%(np.mean(h_feedoffsetx),np.min(h_feedoffsetx),np.max(h_feedoffsetx)),'%.1f (%.1f to %.1f)'%(np.mean(v_feedoffsetx),np.min(v_feedoffsetx),np.max(v_feedoffsetx)),'[mm]'])
        printline(['Y Feed offset:','%.1f (%.1f to %.1f)'%(np.mean(h_feedoffsety),np.min(h_feedoffsety),np.max(h_feedoffsety)),'%.1f (%.1f to %.1f)'%(np.mean(v_feedoffsety),np.min(v_feedoffsety),np.max(v_feedoffsety)),'[mm]'])
        printline(['Z Feed offset:','%.1f (%.1f to %.1f)'%(np.mean(h_feedoffsetz),np.min(h_feedoffsetz),np.max(h_feedoffsetz)),'%.1f (%.1f to %.1f)'%(np.mean(v_feedoffsetz),np.min(v_feedoffsetz),np.max(v_feedoffsetz)),'[mm]'])
        printline(['Sub roll:','%.2f (%.2f to %.2f)'%(np.mean(h_subroty),np.min(h_subroty),np.max(h_subroty)),'%.2f (%.2f to %.2f)'%(np.mean(v_subroty),np.min(v_subroty),np.max(v_subroty)),'[deg]'])

        printline(['Error beam wrt model:','%.1f (%.1f to %.1f)'%(np.nanmean(h_err_beamemss),np.nanmin(h_err_beamemss),np.nanmax(h_err_beamemss)),'%.1f (%.1f to %.1f)'%(np.nanmean(v_err_beamemss),np.nanmin(v_err_beamemss),np.nanmax(v_err_beamemss)),'[%]'])
        printline(['Error beam wrt average:','%.1f (%.1f to %.1f)'%(np.nanmean(h_err_beam),np.nanmin(h_err_beam),np.nanmax(h_err_beam)),'%.1f (%.1f to %.1f)'%(np.nanmean(v_err_beam),np.nanmin(v_err_beam),np.nanmax(v_err_beam)),'[%]'])
        printline(['RMS at %.1fGHz:'%(results[0]['dfth'].freqMHz/1e3 if (targetfreqGHz is None) else targetfreqGHz),'%.2f (%.2f to %.2f)'%(np.mean([result['dfth'].rms0_mm for result in results]),np.min([result['dfth'].rms0_mm for result in results]),np.max([result['dfth'].rms0_mm for result in results])),'%.2f (%.2f to %.2f)'%(np.mean([result['dftv'].rms0_mm for result in results]),np.min([result['dftv'].rms0_mm for result in results]),np.max([result['dftv'].rms0_mm for result in results])),'[mm]'])
        printline(['Phase eff at %.1fGHz:'%(results[0]['dfth'].freqMHz/1e3 if (targetfreqGHz is None) else targetfreqGHz),'%.1f (%.1f to %.1f)'%(np.mean([result['dfth'].eff0_phase*100.0 for result in results]),np.min([result['dfth'].eff0_phase*100.0 for result in results]),np.max([result['dfth'].eff0_phase*100.0 for result in results])),'%.1f (%.1f to %.1f)'%(np.mean([result['dftv'].eff0_phase*100.0 for result in results]),np.min([result['dftv'].eff0_phase*100.0 for result in results]),np.max([result['dftv'].eff0_phase*100.0 for result in results])),'[%]'])
        fig.set_size_inches([8.27,11.69])
        pdf.savefig()

        fig=figure(2,figsize=(8.27, 11.69), dpi=100)
        clf()
        subplot(5,2,1)
        plot_envelope(hour_of_day,[result['temp_avg'] for result in results],[result['temp_min'] for result in results], [result['temp_max'] for result in results])
        xlim([0,24])
        ylabel('Temperature [$^{o}$C]')
        title('Ambient temperature')
        subplot(5,2,2)
        plot_envelope(hour_of_day,[result['wind_avg'] for result in results],[result['wind_min'] for result in results], [result['wind_max'] for result in results])
        xlim([0,24])
        ylabel('Speed [mps]')
        title('Wind speed')
        subplot(5,2,3)
        plot_envelope(hour_of_day,[result['sun_avg'] for result in results],[result['sun_min'] for result in results], [result['sun_max'] for result in results])
        xlim([0,24])
        ylabel('Sun angle [degrees]')
        title('Sun proximity to boresight')
        subplot(5,2,4)
        plot_envelope(hour_of_day,[result['el_avg'] for result in results],[result['el_min'] for result in results], [result['el_max'] for result in results])
        xlim([0,24])
        ylabel('Elevation [degrees]')
        title('Elevation')
        subplot(5,2,5)
        plot_line(hour_of_day,[-result['beamh'].beamoffsetGx[0][0]/np.cos(result['el_avg']*np.pi/180.0)*180.0/np.pi*60.0*60.0 for result in results],'b:')
        plot_line(hour_of_day,[result['beamh'].beamoffsetGx[0][1]*180.0/np.pi*60.0*60.0 for result in results],'g:')
        plot_line(hour_of_day,[-result['beamv'].beamoffsetGx[0][0]/np.cos(result['el_avg']*np.pi/180.0)*180.0/np.pi*60.0*60.0 for result in results],'b-.')
        plot_line(hour_of_day,[result['beamv'].beamoffsetGx[0][1]*180.0/np.pi*60.0*60.0 for result in results],'g-.')
        plot_line(hour_of_day,[-np.arcsin(conv*result['dfth'].nopointingphasegradient[0]/np.cos(result['el_avg']*np.pi/180.0))*180.0/np.pi*60.0*60.0 for result in results],'b')
        plot_line(hour_of_day,[np.arcsin(conv*result['dfth'].nopointingphasegradient[1])*180.0/np.pi*60.0*60.0 for result in results],'g')
        plot_line(hour_of_day,[-np.arcsin(conv*result['dftv'].nopointingphasegradient[0]/np.cos(result['el_avg']*np.pi/180.0))*180.0/np.pi*60.0*60.0 for result in results],'b--')
        plot_line(hour_of_day,[np.arcsin(conv*result['dftv'].nopointingphasegradient[1])*180.0/np.pi*60.0*60.0 for result in results],'g--')
        xlim([0,24])
        leg=legend(['H\'s Az (BP)','H\'s El (BP)','V\'s Az (BP)','V\'s El (BP)',
                'H\'s Az (AP)','H\'s El (AP)','V\'s Az (AP)','V\'s El (AP)'],fontsize=8,loc='best')
        leg.get_frame().set_alpha(0.75)
        ylabel('Pointing error [arcsec]')
        title('Pointing error')
        subplot(5,2,6)
        plot_line(hour_of_day,h_feedoffsetx,'b')
        plot_line(hour_of_day,h_feedoffsety,'g')
        plot_line(hour_of_day,h_feedoffsetz,'r')
        plot_line(hour_of_day,v_feedoffsetx,'b--')
        plot_line(hour_of_day,v_feedoffsety,'g--')
        plot_line(hour_of_day,v_feedoffsetz,'r--')
        xlim([0,24])
        leg=legend(['H\'s x','H\'s y','H\'s z','V\'s x','V\'s y','V\'s z'],fontsize=8,loc='best')
        leg.get_frame().set_alpha(0.75)
        ylabel('Feed offsets [mm]')
        title('Feed offsets')    
        subplot(5,2,7)
        plot_line(hour_of_day,h_err_beamemss,'k')
        plot_line(hour_of_day,v_err_beamemss,'k--')
        plot_highlights(hour_of_day, cycleduration, isoptimal,0.0, 1.0,colour='g',alpha=0.1)
        plot_highlights(hour_of_day, cycleduration, isnominal,0.0, 1.0,colour='g',alpha=0.05)
        plot_highlights(hour_of_day, cycleduration, isoptimal,1.0, 10.0,colour='r',alpha=0.1)
        plot_highlights(hour_of_day, cycleduration, isnominal,1.0, 10.0,colour='r',alpha=0.05)
        xlim([0,24])
        ylim([0,10])
        ylabel('Error beam [%]')
        title('Error beam wrt model')
        subplot(5,2,8)
        plot_line(hour_of_day,h_err_beam,'k')
        plot_line(hour_of_day,v_err_beam,'k--')
        plot_highlights(hour_of_day, cycleduration, isoptimal,0.0, 1.0,colour='g',alpha=0.1)
        plot_highlights(hour_of_day, cycleduration, isnominal,0.0, 1.0,colour='g',alpha=0.05)
        plot_highlights(hour_of_day, cycleduration, isoptimal,1.0, 10.0,colour='r',alpha=0.1)
        plot_highlights(hour_of_day, cycleduration, isnominal,1.0, 10.0,colour='r',alpha=0.05)
        xlim([0,24])
        ylim([0,10])
        ylabel('Error beam [%]')
        title('Error beam wrt average')
        subplot(5,2,9)
        plot_line(hour_of_day,[result['dfth'].rms0_mm for result in results],'k')
        plot_line(hour_of_day,[result['dftv'].rms0_mm for result in results],'k--')
        plot_highlights(hour_of_day, cycleduration, isoptimal,0.3, 1.0,colour='g',alpha=0.1)
        plot_highlights(hour_of_day, cycleduration, isnominal,0.3, 1.0,colour='g',alpha=0.05)
        plot_highlights(hour_of_day, cycleduration, isoptimal,1.0,1.1,colour='r',alpha=0.1)
        plot_highlights(hour_of_day, cycleduration, isnominal,1.0,1.1,colour='r',alpha=0.05)
        xlim([0,24])
        ylim([0.3,1.1])
        xlabel('Hour of day after '+time.ctime(results[0]['time_min']),fontsize=10)
        ylabel('RMS [mm]')
        title('Aperture plane phase RMS')
        subplot(5,2,10)
        plot_line(hour_of_day,[result['dfth'].eff0_phase*100.0 for result in results],'k')
        plot_line(hour_of_day,[result['dftv'].eff0_phase*100.0 for result in results],'k--')
        plot_highlights(hour_of_day, cycleduration, isoptimal,91.0, 100.0,colour='g',alpha=0.1)
        plot_highlights(hour_of_day, cycleduration, isnominal,91.0, 100.0,colour='g',alpha=0.05)
        plot_highlights(hour_of_day, cycleduration, isoptimal,70.0,91.0,colour='r',alpha=0.1)
        plot_highlights(hour_of_day, cycleduration, isnominal,70.0,91.0,colour='r',alpha=0.05)
        xlim([0,24])
        leg=legend(['H','V'],fontsize=8,loc='best')
        leg.get_frame().set_alpha(0.75)
        xlabel('Hour of day after '+time.ctime(results[0]['time_min']),fontsize=10)
        ylabel('Efficiency [%]')
        title('Aperture phase efficiency at '+str(results[0]['dfth'].freqMHz/1e3 if (targetfreqGHz is None) else targetfreqGHz)+'GHz')
        suptitle(results[0]['filename']+': '+ results[0]['scanantenna'],fontsize=8,x=0.5,y=0.998)
        fig.tight_layout()
        fig.set_size_inches([8.27,11.69])
        pdf.savefig()

        fig=figure(3,figsize=(12, 10), dpi=100)
        clf()
        subplot(2,2,1)
        emssresults['beamh'].plot('Gx','pow',clim=[-90,0],doclf=False)
        plt.contour(np.abs(emssresults['beamh'].Gx[0,:,:]/emssresults['beamh'].Gx[0,emssresults['beamh'].gridsize//2,emssresults['beamh'].gridsize//2]),extent=[emssresults['beamh'].margin[0],emssresults['beamh'].margin[-1],emssresults['beamh'].margin[0],emssresults['beamh'].margin[-1]],levels=[10.**(-12.0/20.0)],colors='k',linestyles='dashed')
        xlabel('')
        title('H model %g MHz'%(emssfreq))
        subplot(2,2,2)
        emssresults['beamv'].plot('Gx','pow',clim=[-90,0],doclf=False)
        plt.contour(np.abs(emssresults['beamv'].Gx[0,:,:]/emssresults['beamv'].Gx[0,emssresults['beamh'].gridsize//2,emssresults['beamh'].gridsize//2]),extent=[emssresults['beamh'].margin[0],emssresults['beamh'].margin[-1],emssresults['beamh'].margin[0],emssresults['beamh'].margin[-1]],levels=[10.**(-12.0/20.0)],colors='k',linestyles='dashed')
        xlabel('')
        ylabel('')
        title('V model %g MHz'%(emssfreq))
        subplot(2,2,3)
        dummybeam.Gx[0,:,:]=beam_avgh
        dummybeam.plot('Gx','pow',clim=[-90,0],doclf=False)
        plt.contour(np.abs(beam_avgh/beam_avgh[emssresults['beamh'].gridsize//2,emssresults['beamh'].gridsize//2]),extent=[emssresults['beamh'].margin[0],emssresults['beamh'].margin[-1],emssresults['beamh'].margin[0],emssresults['beamh'].margin[-1]],levels=[10.**(-12.0/20.0)],colors='k',linestyles='dashed')
        title('H average for optimal')
        subplot(2,2,4)
        dummybeam.Gx[0,:,:]=beam_avgv
        dummybeam.plot('Gx','pow',clim=[-90,0],doclf=False)
        plt.contour(np.abs(beam_avgv/beam_avgv[emssresults['beamh'].gridsize//2,emssresults['beamh'].gridsize//2]),extent=[emssresults['beamh'].margin[0],emssresults['beamh'].margin[-1],emssresults['beamh'].margin[0],emssresults['beamh'].margin[-1]],levels=[10.**(-12.0/20.0)],colors='k',linestyles='dashed')
        ylabel('')
        title('V average for optimal')
        suptitle('Power beams\n'+results[0]['filename']+': '+ results[0]['scanantenna'],fontsize=12,x=0.5,y=0.99)
        pdf.savefig()

        fig=figure(4,figsize=(12, 10), dpi=100)
        clf()
        subplot(2,2,1)
        dummybeam.Gx[0,:,:]=np.abs(filterederrorbeamGx)*100.
        dummybeam.plot('Gx','amp',doclf=False,plotextras=False,clim=[0,10.])
        ax=plt.gca();im=ax.images;cb=im[-1].colorbar;cb.set_label('%')
        plt.contour(np.abs(beam_avgh/beam_avgh[emssresults['beamh'].gridsize//2,emssresults['beamh'].gridsize//2]),extent=[emssresults['beamh'].margin[0],emssresults['beamh'].margin[-1],emssresults['beamh'].margin[0],emssresults['beamh'].margin[-1]],levels=[10.**(-12.0/20.0)],colors='k',linestyles='dashed')
        xlabel('')
        title('H fitted error beam (max %.2f%%)'%(maxGx*100.))
        xlim([-ebextent/2.,ebextent/2.])
        ylim([-ebextent/2.,ebextent/2.])
        subplot(2,2,2)
        dummybeam.Gx[0,:,:]=np.abs(filterederrorbeamGy)*100.
        dummybeam.plot('Gx','amp',doclf=False,plotextras=False,clim=[0,10.])
        ax=plt.gca();im=ax.images;cb=im[-1].colorbar;cb.set_label('%')
        plt.contour(np.abs(beam_avgv/beam_avgv[emssresults['beamh'].gridsize//2,emssresults['beamh'].gridsize//2]),extent=[emssresults['beamh'].margin[0],emssresults['beamh'].margin[-1],emssresults['beamh'].margin[0],emssresults['beamh'].margin[-1]],levels=[10.**(-12.0/20.0)],colors='k',linestyles='dashed')
        xlabel('')
        ylabel('')
        title('V fitted error beam (max %.2f%%)'%(maxGy*100.))
        xlim([-ebextent/2.,ebextent/2.])
        ylim([-ebextent/2.,ebextent/2.])
        subplot(2,2,3)
        dummybeam.Gx[0,:,:]=np.abs(errorbeamGx)*100.
        dummybeam.plot('Gx','amp',doclf=False,plotextras=False,clim=[0,10.])
        ax=plt.gca();im=ax.images;cb=im[-1].colorbar;cb.set_label('%')
        plt.contour(np.abs(beam_avgh/beam_avgh[emssresults['beamh'].gridsize//2,emssresults['beamh'].gridsize//2]),extent=[emssresults['beamh'].margin[0],emssresults['beamh'].margin[-1],emssresults['beamh'].margin[0],emssresults['beamh'].margin[-1]],levels=[10.**(-12.0/20.0)],colors='k',linestyles='dashed')
        title('H error beam (stdev %.2f%% wrt fitted)'%(stdGx*100.))
        xlim([-ebextent/2.,ebextent/2.])
        ylim([-ebextent/2.,ebextent/2.])
        subplot(2,2,4)
        dummybeam.Gx[0,:,:]=np.abs(errorbeamGy)*100.
        dummybeam.plot('Gx','amp',doclf=False,plotextras=False,clim=[0,10.])
        ax=plt.gca();im=ax.images;cb=im[-1].colorbar;cb.set_label('%')
        plt.contour(np.abs(beam_avgv/beam_avgv[emssresults['beamh'].gridsize//2,emssresults['beamh'].gridsize//2]),extent=[emssresults['beamh'].margin[0],emssresults['beamh'].margin[-1],emssresults['beamh'].margin[0],emssresults['beamh'].margin[-1]],levels=[10.**(-12.0/20.0)],colors='k',linestyles='dashed')
        ylabel('')
        title('V error beam (stdev %.2f%% wrt fitted)'%(stdGy*100.))
        xlim([-ebextent/2.,ebextent/2.])
        ylim([-ebextent/2.,ebextent/2.])
        suptitle('Error beams average for optimal\n'+results[0]['filename']+': '+ results[0]['scanantenna'],fontsize=12,x=0.5,y=0.99)
        pdf.savefig()

        fig=figure(5,figsize=(12, 10), dpi=100)
        clf()
        subplot(2,2,1)
        emssresults['dfth'].plot('amp',doclf=False)
        xlabel('')
        title('H model %g MHz'%(emssfreq))
        subplot(2,2,2)
        emssresults['dftv'].plot('amp',doclf=False)
        xlabel('')
        ylabel('')
        title('V model %g MHz'%(emssfreq))
        subplot(2,2,3)
        dummydft.ampmap=np.mean([results[ind]['dfth'].ampmap for ind in isoptimalind],axis=0)
        dummydft.plot('amp',doclf=False)
        title('H average for optimal')
        subplot(2,2,4)
        dummydft.ampmap=np.mean([results[ind]['dftv'].ampmap for ind in isoptimalind],axis=0)
        dummydft.plot('amp',doclf=False)
        ylabel('')
        title('V average for optimal')
        suptitle('Aperture plane amplitude maps (illumination)\n'+results[0]['filename']+': '+ results[0]['scanantenna'],fontsize=12,x=0.5,y=0.99)
        pdf.savefig()

        fig=figure(6,figsize=(12, 14), dpi=100)
        clf()
        subplot(4,3,1)
        emssresults['dfth'].plot('nopointingdev',clim=[-1,1],doclf=False)
        xlabel('')
        title('H model %g MHz'%(emssfreq))
        subplot(4,3,2)
        emssresults['dftv'].plot('nopointingdev',clim=[-1,1],doclf=False)
        xlabel('')
        ylabel('')
        title('V model %g MHz'%(emssfreq))
        subplot(4,3,3)
        emssresults['dftv'].plot('nopointingdev',diff=emssresults['dfth'],clim=[-1,1],doclf=False)
        xlabel('')
        ylabel('')
        title('H-V model %g MHz'%(emssfreq))
        subplot(4,3,4)
        dft_avgh=np.mean([results[ind]['dfth'].nopointingdevmap for ind in isoptimalind],axis=0)
        dummydft.nopointingdevmap=dft_avgh
        dummydft.plot('nopointingdev',clim=[-5.0,5.0],doclf=False)
        xlabel('')
        title('H average for optimal')
        subplot(4,3,5)
        dft_avgv=np.mean([results[ind]['dftv'].nopointingdevmap for ind in isoptimalind],axis=0)
        dummydft.nopointingdevmap=dft_avgv
        dummydft.plot('nopointingdev',clim=[-5.0,5.0],doclf=False)
        xlabel('')
        ylabel('')
        title('V average for optimal')
        subplot(4,3,6)
        dummydft.nopointingdevmap=dft_avgv-dft_avgh
        dummydft.plot('nopointingdev',clim=[-1.0,1.0],doclf=False)
        xlabel('')
        ylabel('')
        title('H-V for optimal')
        subplot(4,3,7)
        results[ibest]['dfth'].plot('nopointingdev',clim=[-5,5],doclf=False)
        xlabel('')
        title('H at '+time.ctime(results[ibest]['time_avg'])[11:16])
        subplot(4,3,8)
        results[ibest]['dftv'].plot('nopointingdev',clim=[-5,5],doclf=False)
        xlabel('')
        ylabel('')
        title('V at '+time.ctime(results[ibest]['time_avg'])[11:16])
        subplot(4,3,9)
        results[ibest]['dftv'].plot('nopointingdev',diff=results[ibest]['dfth'],clim=[-1,1],doclf=False)
        xlabel('')
        ylabel('')
        title('H-V at '+time.ctime(results[ibest]['time_avg'])[11:16])
        subplot(4,3,10)
        results[iworst]['dfth'].plot('nopointingdev',clim=[-1,1],diff=results[ibest]['dfth'],doclf=False)
        title('H at '+time.ctime(results[ibest]['time_avg'])[11:16]+' - H at '+time.ctime(results[iworst]['time_avg'])[11:16])
        subplot(4,3,11)
        results[iworst]['dftv'].plot('nopointingdev',clim=[-1,1],diff=results[ibest]['dftv'],doclf=False)
        ylabel('')
        title('V at '+time.ctime(results[ibest]['time_avg'])[11:16]+' - V at '+time.ctime(results[iworst]['time_avg'])[11:16])
        subplot(4,3,12)
        dummydft.nopointingdevmap=(results[iworst]['dftv'].nopointingdevmap-results[ibest]['dftv'].nopointingdevmap)-(results[iworst]['dfth'].nopointingdevmap-results[ibest]['dfth'].nopointingdevmap)
        dummydft.plot('nopointingdev',clim=[-0.5,0.5],doclf=False)
        ylabel('')
        title('Difference of left')
        suptitle('Main reflector surface deviation maps\n'+results[0]['filename']+': '+ results[0]['scanantenna'],fontsize=12,x=0.5,y=0.99)
        pdf.savefig()

        figure(7,figsize=(12,10), dpi=100)
        clf()
        subplot(2,1,1)
        plot(np.abs(np.concatenate(rawonaxis[0])),'r')
        plot(np.abs(np.concatenate(rawonaxis[1])),'g')
        plot(np.abs(np.concatenate(rawonaxis[2])),'c')
        plot(np.abs(np.concatenate(rawonaxis[3])),'b')
        legend(rawprods)
        title('Amplitude stability')
        ylabel('Amplitude [counts]')
        xlabel('Samples')
        subplot(2,1,2)
        plot(np.unwrap(np.angle(np.concatenate(rawonaxis[0])))*180.0/np.pi,'r')
        plot(np.unwrap(np.angle(np.concatenate(rawonaxis[1])))*180.0/np.pi,'g')
        plot(np.unwrap(np.angle(np.concatenate(rawonaxis[2])))*180.0/np.pi,'c')
        plot(np.unwrap(np.angle(np.concatenate(rawonaxis[3])))*180.0/np.pi,'b')
        title('Phase stability')
        ylabel('Phase [degrees]')
        xlabel('Samples')
        legend(rawprods)
        suptitle('Unprocessed on-axis beacon signals\n%s, %.1fMHz (channel %d), %s pol beacon at %.1f degrees tilt\n%s: %s'%(results[0]['targetname'],results[0]['dfth'].freqMHz,results[0]['dfth'].dataset.getchannelindices(results[0]['dfth'].freqMHz,0.0001),beaconpol,tilt-180.0,results[0]['filename'],results[0]['scanantenna']),fontsize=12,x=0.5,y=0.99)
        pdf.savefig()

        d = pdf.infodict()
        d['Title'] = 'RTS holography report'
        d['Author'] = socket.gethostname()
        d['Subject'] = 'Holography reflector phase efficiency and error beam report'
        d['Keywords'] = 'rts holography'
        d['CreationDate'] = datetime.datetime.today()
        d['ModDate'] = datetime.datetime.today()
    
    return isoptimal, isnominal, results, [h_feedoffsetx, h_feedoffsety, h_feedoffsetz], [v_feedoffsetx, v_feedoffsety, v_feedoffsetz], h_err_beamemss, v_err_beamemss, h_err_beamemss, v_err_beamemss, None, None # Last two to be signature compatible with "generate_report()"



### Example of use ##########################################################################
# if __name__ == "__main__":
#
#     gspreadsheet=Spreadsheet('RTS ku band holography registry')
#     ifiles = [13]
#     rawprods, results, rawonaxis, iindices, nofitflags, concat_filenames, beaconpol, tilt, emssfreq, emssresults = loadifiles(gspreadsheet,ifiles,gridsize=512,clipextent=1,targetfreqGHz=14.5)
#
#     results, discardedresults, rawonaxis, iindices, snr = thresh_and_flag(results,rawonaxis,iindices,maxdelta=0.1,cascade_keep=~nofitflags)
#
#     isoptimalind, isoptimal, isnominal, results, h_feedoffset_xyz, v_feedoffset_xyz, h_err_beamemss, v_err_beamemss, h_subroty, v_subroty = generate_report( rawprods,results,discardedresults,rawonaxis,beaconpol,tilt,emssfreq,emssresults,'ku_report_%s_%s.pdf'%((results+discardedresults)[0]['scanantenna'],concat_filenames), sunspec_lim=30, windspec_lim=10)
#
#     uploadimages(results,emssresults,isoptimalind,gspreadsheet)
#     updateifiles(gspreadsheet,"J",ifiles,iindices,isoptimal,isnominal,results,h_feedoffset_xyz,v_feedoffset_xyz,h_err_beamemss,v_err_beamemss, h_subroty, v_subroty, snr)

import pysiaf
import pandas as pd
import pdb
import matplotlib.pyplot as plt
import numpy as np
from astropy.io import ascii, fits
from astropy.table import Table

siaf = pysiaf.Siaf('NIRCam')

apListSW =  ['NRCA1_FULL', 'NRCA2_FULL', 'NRCA3_FULL', 'NRCA4_FULL']#,
#           'NRCB1_FULL', 'NRCB2_FULL', 'NRCB3_FULL', 'NRCB4_FULL']
apListLW = ['NRCA5_FULL']#, 'NRCB5_FULL']
waveList = ['SW','LW']
apListAll = [apListSW,apListLW]

subarrayListSW = ['NRCA1_GRISMTS256', 'NRCA1_GRISMTS128',
                  'NRCA1_GRISMTS64', 'NRCA3_GRISMTS256', 'NRCA3_GRISMTS128',
                  'NRCA3_GRISMTS64']
subarrayListLW = ['NRCA5_GRISM256_F322W2', 'NRCA5_GRISM128_F322W2', 'NRCA5_GRISM64_F322W2']#,
                  # 'NRCA5_GRISM256_F277W', 'NRCA5_GRISM128_F277W', 'NRCA5_GRISM64_F277W',
                  # 'NRCA5_GRISM256_F356W', 'NRCA5_GRISM128_F356W', 'NRCA5_GRISM64_F356W',
                  # 'NRCA5_GRISM256_F444W', 'NRCA5_GRISM128_F444W', 'NRCA5_GRISM64_F444W',
                  # 'NRCA5_GRISM_F322W2', 'NRCA5_GRISM_F277W', 'NRCA5_GRISM_F356W',
                  # 'NRCA5_GRISM_F444W']

subarrayListAll = [subarrayListSW, subarrayListLW]

def make_csv():
    table_path = '../spectra_locations/'
    baseName = 'spectra_locations_science_pixel_coordinates'
    dat = pd.read_excel(table_path+baseName+'.xlsx')
    dat.to_csv('data/'+baseName+'.csv',index=False)

def reversibility(orig='sci',new='tel'):
    """ Test the reversibility  """
    orig_x = np.array([3, 2043])
    orig_y = np.array([1939, 1938])
    print("Original coordinates:")
    print(orig_x)
    print(orig_y)
    ap = siaf['NRCA1_FULL']
    
    method_forward = "{}_to_{}".format(orig,new)
    method_to_call = getattr(ap,method_forward)
    x2, y2 = method_to_call(orig_x,orig_y)
    
    method_reverse = "{}_to_{}".format(new,orig)
    method_to_call = getattr(ap,method_reverse)
    new_x, new_y = method_to_call(x2,y2)

    print("Recovered coordinates")
    print(new_x)
    print(new_y)

def show_spectra(axArr,yShift=0,xShift=0):
    dat = ascii.read('data/spectra_locations_science_pixel_coordinates.csv')
    outDat = Table()
    outDat['Spectra Description'] = dat['Spectra Description']
    outDat['telx1'] = np.nan
    outDat['tely1'] = np.nan
    outDat['telx2'] = np.nan
    outDat['tely2'] = np.nan
    outDat['Detector'] = np.array('',dtype='S16')
    outDat['Sci X1'] = np.nan
    outDat['Sci Y1'] = np.nan
    outDat['Sci X2'] = np.nan
    outDat['Sci Y2'] = np.nan
    
    for rowInd,sp in enumerate(dat):
        if sp['Detector Name'] != 0.0:
            detectorKey = 'NRC{}_FULL'.format(sp['Detector Name'])
            oneAp = siaf[detectorKey]
            xVals = np.array([sp['X at Max V2'],sp['X at Min V2']])
            yVals = np.array([sp['Y at Max V2'],sp['Y at Min V2']])
            tel_x, tel_y = oneAp.sci_to_tel(xVals,yVals)
            if detectorKey in apListLW:
                ax = axArr[1]
            else:
                ax = axArr[0]
            tel_x = tel_x + xShift
            tel_y = tel_y + yShift
            ax.plot(tel_x,tel_y,'o',color='black',markersize=2,linestyle='-')
            ax.text(tel_x[0],tel_y[0],sp['Spectra Description'],fontsize=4)
            
            # datShifted = dat[['Spectra Description','Detector Name']]
            # if sp['Detector Name'] == 'A5':
            #     new_sci_x, new_sci_y = oneAp.tel_to_sci(tel_x,tel_y)
            #     print("Shifted Y values on A5 = {}".format(new_sci_y))
                
            outDat['telx1'][rowInd] = np.round(tel_x[0],2)
            outDat['tely1'][rowInd] = np.round(tel_y[0],2)
            outDat['telx2'][rowInd] = np.round(tel_x[1],2)
            outDat['tely2'][rowInd] = np.round(tel_y[1],2)
            
            if sp['Spectra Description'] == 'Grism':
                newDetector = 'NRCA5_FULL'
            else:
                if tel_x[1] > 80:
                    newDetector = 'NRCA1_FULL'
                else:
                    newDetector = 'NRCA3_FULL'
            
            newAp = siaf[newDetector]
            outDat['Detector'][rowInd] = newDetector
            newSci_x, newSci_y = newAp.tel_to_sci(tel_x,tel_y)
            outDat['Sci X1'][rowInd] = np.round(newSci_x[0],2)
            outDat['Sci Y1'][rowInd] = np.round(newSci_y[0],2)
            outDat['Sci X2'][rowInd] = np.round(newSci_x[1],2)
            outDat['Sci Y2'][rowInd] = np.round(newSci_y[1],2)
            #if sp['Spectra Description'] == 'DHS 7':
            #    pdb.set_trace()
            
    outDat.write('data/spec_locations_tel_coor_yshift_{}.csv'.format(yShift),overwrite=True)

def show_detectors(axArr):
    for waveInd,apList in enumerate(apListAll):
        ax = axArr[waveInd]
        for oneApName in apList:
            oneAp = siaf[oneApName]
            oneAp.plot(ax=ax,fill=False)
            cornerTuple = oneAp.corners('tel')
            ax.text(cornerTuple[0][3],cornerTuple[1][3],
                    oneApName.split('_FULL')[0],va='bottom',fontsize=8)
#            pdb.set_trace()
        ax.set_title(waveList[waveInd])

def show_subarrays(axArr):
    for waveInd, subarrayList in enumerate(subarrayListAll):
        for oneApName in subarrayList:
            oneAp = siaf[oneApName]
            oneAp.plot(ax=axArr[waveInd],fill=True)
            oneAp.plot_frame_origin('sci',ax=axArr[waveInd])

def show_layout(yShift=0):
    
    fig, axArr = plt.subplots(1,2,sharey=True)
    #sci_x = 
    show_detectors(axArr)
    show_subarrays(axArr)
    show_spectra(axArr,yShift=yShift)
    
    ## there are some weird transformation things happening with xlim that are fixed here
    # for oneAx in axArr:
    #      oneAx.set_ylim(-650,-350)
    #      oneAx.set_xlim(160,0)
    fig.savefig('plots/spectra_layout_yshift_{}_arcsec.pdf'.format(yShift),
                bbox_inches='tight')
    plt.close(fig)
    
def all_field_points():
    show_layout(yShift=0) ## CV3 measured field point
    show_layout(yShift=-61.6) ## subarray field point
    
    
if __name__ == "__main__":
    all_field_points()
    
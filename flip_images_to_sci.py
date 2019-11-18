import numpy as np
import glob
import os
from astropy.io import fits, ascii
import pynrc
import pynrc.maths.coords

defaultList = '../example_slopes/g2v_cen_6011125535/original_orientation/*.fits'
defaultOutputPath = '../example_slopes/g2v_cen_6011125535/flipped_to_sci/'
def do_flips(fileList=defaultList,
             outPath=defaultOutputPath):
    
    """ Flip the images to science orientation"""
    globbedList = glob.glob(fileList)
    for oneFile in globbedList:
        HDUList = fits.open(oneFile)
        dat = HDUList[0].data
        head = HDUList[0].header
        newImg = pynrc.maths.coords.det_to_sci(dat[0],head['SCA_ID'])
        head['REORIENT'] = (True,"Re-oriented to science orientation?")
        outHDU = fits.PrimaryHDU(newImg,head)
        
        outName = os.path.basename(oneFile)
        outHDU.writeto(os.path.join(outPath,outName),overwrite=False)
        HDUList.close()
        

import argparse
import h5py
from tifffile import imwrite, imread
import re
import os
import sys
import numpy as np

import matplotlib.pyplot as plt

import rawpy
import imageio
import PIL

f = 'FL24_EXP2_20181029T183004_371_260729937.raw'


def raw_to_array(filename, res=16):

    with open(filename, 'rb') as file_:
        file_.seek(15, os.SEEK_SET)
        arr = np.fromfile(file_, dtype=np.dtype('<i2'))
        arr = arr.reshape([960, 1278])
        arr = np.fliplr(arr)
        arr = np.flipud(arr)
        imwrite(filename[0:-3]+'tif', arr, arr.shape, dtype=np.dtype('i2'))
        # plt.imshow(arr)
        # plt.show()


"""
file_=open(f, 'rb')
file_.seek(15, os.SEEK_SET)
arr = np.fromfile(file_, dtype=np.dtype('<i2'))
arr.shape
arr = arr.reshape([960, 1278])
arr = np.fliplr(arr)
arr = np.flipud(arr)

imwrite('templ.tif', err,err.shape,dtype=np.dtype('i1'))
imwrite('temp.tif', arr,arr.shape,dtype=np.dtype('i2'))
brr = imread('temp.tif')
initial = imread('FL24_EXP2_20181029T183004_371_260729937.tif')
corrected = imread('FL24_EXP2_20181029T183004_371_260729937LE.tif')
plt.imshow(arr)
plt.show()
plt.imshow(brr)
plt.show()
plt.imshow(initial)
plt.show()
plt.imshow(corrected)
plt.show()"""


def Create_filelist(full_path):

    if not os.path.isdir(full_path):

        return [full_path]

    else:
        all_files = [full_path + '\\' + f for f in os.listdir(full_path) if(
            os.path.isfile(f) and os.path.splitext(f)[1] == '.raw')]

    return all_files


def conv(path):
    count = 0
    for i in Create_filelist(path):
        raw_to_array(i)
        count += 1

    print(f'converted {count} files')


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Convert raw to tiff ',
                                     # usage='Any text you want\n',
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     epilog=""" """)

    parser.add_argument('Path', metavar='Path', type=str,
                        help='Path to folder or file to  be converted')
    args = parser.parse_args()
    conv(args.Path)

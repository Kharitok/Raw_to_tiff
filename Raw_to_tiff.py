import argparse
import os
import re
import sys


import numpy as np
from tifffile import imread, imwrite


def raw_to_array(filename, downscale=False):
    """Convert file from 16bit little endian .raw to .tiff
    filename - name of file t be converted
    downscale - if color depth shoud be downscaled to 8 bit"""

    with open(filename, 'rb') as file_:
        file_.seek(15, os.SEEK_SET)
        arr = np.fromfile(file_, dtype=np.dtype('<u2'))
        arr = arr.reshape([960, 1278])
        arr = np.fliplr(arr)
        arr = np.flipud(arr)
        if downscale:
            arr = arr / (arr.max() / (2**8-1))
            # arr[arr>=2**8] = 2**8-1
            arr = arr.astype(dtype=np.dtype('u1'))
            imwrite(filename[0:-4]+'_8b_.tif', arr, arr.shape, dtype=np.dtype('u1'))
            return
        else:
            imwrite(filename[0:-4]+'_16b_.tif', arr, arr.shape, dtype=np.dtype('u2'))

        # plt.imshow(arr)
        # plt.show()


def Create_filelist(full_path):
    """Create list of .raw files in directory or get single filename"""
    #print(full_path)
    #print(os.path.isdir(full_path))
    if not os.path.isdir(full_path):
        #print(1)

        return [full_path]

    else:
        #print(2)
        #print(full_path)
        #print(os.listdir(full_path))
        all_files = [full_path + '\\' + f for f in os.listdir(full_path) if(os.path.splitext(f)[1] == '.raw')]
    #print(all_files)
    return all_files


def conv(path, downscale=False):
    """ convert all files in path directory or
    only file with path = path using raw_to_array() dunction"""
    count = 0
    #print(path)
    for i in Create_filelist(path):
        raw_to_array(i, downscale=downscale)
        count += 1

    print(f'converted {count} files')


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Convert raw to tiff ',
                                     # usage='Any text you want\n',
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     epilog=""" """)

    parser.add_argument('Path', metavar='P', type=str,
                        help='Path to folder or file to  be converted')
    parser.add_argument('D', metavar='D', type=bool, nargs='?', const=False,
                        help="""If image need to be downscaled to 8 bit using mapping from [min_val -  max_val] to [0 - 255]""")
    args = parser.parse_args()

    #print(args.Path)
    if args.D is None:
        conv(args.Path)
    else:
        conv(args.Path, downscale=True)

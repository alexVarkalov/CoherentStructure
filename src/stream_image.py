import os
import arrow
import netCDF4 as nc4
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from utils import *




def main():
    folder = '../StreamImage'
    if not os.path.exists(folder):
        os.makedirs(folder)
    # paths = get_file_paths('nc')
    paths = ['/home/varalex/University/nc/wrfout_d01_2013-05-22_01.nc',]

    horizontal_cut(paths=paths, folder=folder)
    while True and False:
        print '1. Horizontal cut'
        print '2. Vertical cut'
        try:
            choise = input()
        except Exception:
            print('Wrong Input')
            continue
        if choise == 1:
            horizontal_cut(paths=paths, folder=folder)
            break
        elif choise == 2:
            vertical_cut(paths=paths, folder=folder)
            break
        print('Wrong Input')

if __name__ == '__main__':
    main()

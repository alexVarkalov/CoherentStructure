import os
import arrow
import netCDF4 as nc4
import numpy as np
import matplotlib.pyplot as plt
import Tkinter
import tkFileDialog
import ntpath


def cut_nc(path):
    wrf_file = nc4.Dataset(path, mode='r')
    with open('../logs/log{}.txt'.format(arrow.now().timestamp), mode='w', ) as log:
        start_time = arrow.now()
        log.write('***********************\n')
        log.write('Start Time - {}\n'.format(start_time))
        log.write('***********************\n')
        for key, value in wrf_file.variables.items():
            if 'description' in value.ncattrs():
                print("{} -- {}".format(key, getattr(value, 'description')))
                log.write('{} -- {}\n'.format(key, getattr(value, 'description')))
            else:
                print("{} -- {}".format(key, 'no description'))
                log.write('{} -- {}\n'.format(key, 'no description'))
        print wrf_file.variables.keys()
        while True:
            print('Choose Keys')
            # TODO Log
            keys_string = raw_input('Example: "U, V, T"\n').split(', ')
            # print keys_string
            real_keys = []
            for key in keys_string:
                if key in wrf_file.variables.keys():
                    real_keys.append(key)
                else:
                    # todo Log
                    print 'there is no key named {}'. format(key)
            print 'File with this keys will be created\n{}\nAll right?'.format(', '.join(real_keys))
            flag = False
            while True:
                answer = raw_input('Print yes or no\n')
                if 'yes' == answer.strip().lower():
                    flag = True
                    break
                elif 'no' == answer.strip().lower():
                    flag = False
                    break
            if flag:
                break
        end_time = arrow.now()
        work_time = end_time - start_time
        log.write('***********************\n')
        log.write('End Time - {}\n'.format(end_time))
        log.write('Work Time - {}\n'.format(work_time))
        log.write('***********************\n')


def main():
    file_path = None
    file_path = '/home/varalex/University/nc/wrfout_d01_2013-05-22_01.nc'
    print 'Please, select a .nc file'
    while not file_path:
        file_path = tkFileDialog.askopenfilename()
        if not file_path:
            print 'Please, select a .nc file'
            continue
        if file_path.split('.')[1] == 'nc':
            break
        else:
            print ('You choose not .nc file. Repeat again.')
            file_path = None
    cut_nc(file_path)


main()

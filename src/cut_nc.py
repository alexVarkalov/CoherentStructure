import os
import arrow
import netCDF4 as nc4
import numpy as np
import matplotlib.pyplot as plt
import Tkinter
import tkFileDialog
import ntpath
import shutil


def get_file_path(filename_extension):
    # todo use base func param
    file_path = None
    while not file_path:
        print 'Please, select a .{} file'.format(filename_extension)
        file_path = tkFileDialog.askopenfilename()
        if not file_path:
            continue
        if file_path.split('.')[1] == filename_extension:
            return file_path
        else:
            print ('You choose not .{} file. Repeat again.'.format(filename_extension))
            file_path = None


def create_keys_list(keys_string, wrf_file, log_file):
    keys_list = keys_string.split(', ')
    cleaned_keys_list = []
    for key in keys_list:
        if key in wrf_file.variables.keys():
            cleaned_keys_list.append(key)
        else:
            print 'there is no key named {}'.format(key)
    print 'File with this keys will be created\n{}\nAll right?'.format(', '.join(cleaned_keys_list))
    while True:
        answer = raw_input('Print yes or no\n')
        if 'yes' == answer.strip().lower() or 'y' == answer.strip().lower():
            return cleaned_keys_list
        elif 'no' == answer.strip().lower() or 'n' == answer.strip().lower():
            return None


def cut_nc(path, keys_list, log_file):
    new_path = path.split('.')[0] + '_cp.' + path.split('.')[1]
    # input file
    dsin = nc4.Dataset(path, mode='r')
    # output file
    dsout = nc4.Dataset(new_path, "w", format=dsin.data_model)

    # Copy dimensions
    start_dimensions_time = arrow.now()
    log_file.write('--------------------------\n')
    log_file.write('Start Copy Dimensions Time - {}\n'.format(start_dimensions_time))
    log_file.write('--------------------------\n')
    for dname, the_dim in dsin.dimensions.iteritems():
        print dname, len(the_dim)
        dsout.createDimension(dname, len(the_dim) if not the_dim.isunlimited() else None)
    end_dimensions_time = arrow.now()
    delta_dimensions_time = end_dimensions_time - start_dimensions_time

    log_file.write('--------------------------\n')
    log_file.write('End Copy Dimensions Time - {}\n'.format(end_dimensions_time))
    log_file.write('Delta Copy Dimensions Time - {}\n'.format(delta_dimensions_time))
    log_file.write('--------------------------\n')
    # Copy variables
    start_variables_time = arrow.now()
    log_file.write('@@@@@@@@@@@@@@@@@@@@@@@@@@\n')
    log_file.write('Start Copy Variables Time - {}\n'.format(start_dimensions_time))
    log_file.write('@@@@@@@@@@@@@@@@@@@@@@@@@@\n')
    for v_name, varin in dsin.variables.iteritems():
        start_variable_time = arrow.now()
        if v_name not in keys_list:
            continue
        outVar = dsout.createVariable(v_name, varin.datatype, varin.dimensions)
        # Copy variable attributes
        outVar.setncatts({k: varin.getncattr(k) for k in varin.ncattrs()})

        outVar[:] = varin[:]
        end_variable_time = arrow.now()
        delta_variable_time = end_variable_time - start_variable_time
        print 'Copy {}. Delta - {}'.format(v_name, delta_variable_time)
        log_file.write('Copy {}. Delta - {}'.format(v_name, delta_variable_time))
    end_variables_time = arrow.now()
    delta_variables_time = end_variables_time - start_variables_time

    log_file.write('@@@@@@@@@@@@@@@@@@@@@@@@@@\n')
    log_file.write('End Copy Variables Time - {}\n'.format(end_variables_time))
    log_file.write('Delta Copy Variables Time - {}\n'.format(delta_variables_time))
    log_file.write('@@@@@@@@@@@@@@@@@@@@@@@@@@\n')

    # todo create sorting if necessary
    test_dict = {}
    for name in dsin.ncattrs():
        test_dict[name] = getattr(dsin, name)
    dsout.setncatts(test_dict)
    dsin.close()
    dsout.close()


def main():
    path = get_file_path(filename_extension='nc')
    nc_file = nc4.Dataset(path, mode='r')
    start_time = arrow.now()
    with open('../logs/log{}.txt'.format(start_time.timestamp), mode='w', ) as log_file:

        log_file.write('***********************\n')
        log_file.write('Start Time - {}\n'.format(start_time))
        log_file.write('File path - {}\n'.format(path))
        log_file.write('***********************\n')

        with open('../logs/log{}kv.txt'.format(start_time.timestamp), mode='w') as log_kv_file:
            for key, value in nc_file.variables.items():
                if 'description' in value.ncattrs():
                    print("{} -- {}".format(key, getattr(value, 'description')))
                    log_kv_file.write('{} -- {}\n'.format(key, getattr(value, 'description')))
                else:
                    print("{} -- {}".format(key, 'no description'))
                    log_kv_file.write('{} -- {}\n'.format(key, 'no description'))

        while True:
            print ('1. Take keys from file')
            print ('2. Take keys from keyboard')
            choise = input()
            if choise == 1:
                keys_file = get_file_path('txt')
                with open(keys_file, mode='r') as keys_file:
                    keys_string = keys_file.readline().strip('\n')
                    print keys_string
                    keys_list = create_keys_list(keys_string=keys_string, wrf_file=nc_file, log_file=log_file)
                    if not keys_list:
                        continue
                    break
            elif choise == 2:
                print('Choose Keys')
                keys_string = raw_input('Example: "U, V, T"\n')
                keys_list = create_keys_list(keys_string=keys_string, wrf_file=nc_file)
                if not keys_list:
                    continue
                break
            else:
                continue
        print keys_list
        nc_file.close()
        cut_nc(path=path, keys_list=keys_list, log_file=log_file)
        end_time = arrow.now()
        work_time = end_time - start_time
        log_file.write('***********************\n')
        log_file.write('End Time - {}\n'.format(end_time))
        log_file.write('Work Time - {}\n'.format(work_time))
        log_file.write('***********************\n')


main()

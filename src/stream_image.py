import os
import arrow
import netCDF4 as nc4
import numpy as np
import matplotlib.pyplot as plt
import Tkinter
import tkFileDialog
from matplotlib import cm
from utils import get_file_paths, path_leaf


def create_module_matrix(X, Y):
    """ Create Matrix of polar radius """
    sq_X = np.zeros(X.shape)
    sq_Y = np.zeros(Y.shape)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            sq_X[i][j] = X[i][j] ** 2
    for i in range(Y.shape[0]):
        for j in range(Y.shape[1]):
            sq_Y[i][j] = Y[i][j] ** 2
    Z = np.zeros((249, 249))
    for i in range(Z.shape[0]):
        for j in range(Z.shape[1]):
            Z[i][j] = np.sqrt(sq_X[i][j] + sq_Y[i][j])
    return Z


def horizontal_cut(paths, folder, log_file):

    step = 2

    log_file.writelines('step = {} \n'.format(step))

    log_file.writelines('+++++++++++++++++++++++\n')
    log_file.writelines('Horizontal cut\n')
    log_file.writelines('+++++++++++++++++++++++\n')
    for path in paths:
        file_start_time = arrow.now()
        file_name = path_leaf(path)

        log_file.writelines('-----------------------\n')
        log_file.writelines('File {} Start Time - {}\n\n'.format(file_name, file_start_time))
        log_file.writelines('-----------------------\n')

        print 'File {} Start Time - {}'.format(file_name, file_start_time)
        file_folder = file_name.split('.')[0]
        os.makedirs('{}/{}'.format(folder, file_folder))
        # print path
        nc_file = nc4.Dataset(path, mode='r')

        highs = nc_file.variables['U'].shape[1]

        highs = 3

        for h in range(highs):
            high_start_time = arrow.now()
            log_file.writelines('High #{} Start Time - {}\n'.format(h, high_start_time))
            # print 'High #{} Start Time - {}'.format(h, high_start_time)
            x_wind = nc_file.variables['U']
            y_wind = nc_file.variables['V']
            x_wind0 = x_wind[0][h]
            y_wind0 = y_wind[0][h]
            # todo figure out with shape
            X, Y = np.meshgrid(np.arange(0, 249, 1), np.arange(0, 249, 1))
            U = x_wind0
            V = y_wind0
            Z = create_module_matrix(U, V)
            plt.figure(figsize=(10, 10), facecolor='w', edgecolor='r')
            plt.streamplot(
                X[::step, ::step],
                Y[::step, ::step],
                U[::step, ::step],
                V[::step, ::step],
                color=Z[::step, ::step],
                cmap=cm.cool,
                linewidth=1.0,
                arrowstyle='->',
                arrowsize=1.5,
            )
            plt.colorbar()
            plt.axis([-10, 260, -10, 260])
            plt.title('{}/high{}.png'.format(folder, h))
            plt.savefig('{}/{}/high{}.png'.format(folder, file_folder, h))
            plt.close()
            # print ('{}/{}/high{}.png is created'.format(folder, file_folder, h))
            high_end_time = arrow.now()
            high_delta = high_end_time - high_start_time
            print 'High #{} Delta - {}'.format(h, high_delta)
            log_file.writelines('High End Time - {}\n'.format(high_end_time))
            log_file.writelines('High Delta - {}\n\n'.format(high_delta))
        file_end_time = arrow.now()
        log_file.writelines('-----------------------\n')
        log_file.writelines('File {} End Time - {}\n\n'.format(file_name, file_end_time))
        print 'File {} End Time - {}\n'.format(file_name, file_end_time)
        file_delta = file_end_time - file_start_time
        log_file.writelines('File {} Delta - {}\n'.format(file_name, file_delta))
        log_file.writelines('-----------------------\n')
        print 'High {} Delta - {}\n'.format(file_name, file_delta)


def vertical_cut(paths, folder, log_file):
    step = 2

    log_file.writelines('step = {} \n'.format(step))

    log_file.writelines('+++++++++++++++++++++++\n')
    log_file.writelines('Vertical cut\n')
    log_file.writelines('+++++++++++++++++++++++\n')
    for path in paths:
        file_start_time = arrow.now()
        file_name = path_leaf(path)

        log_file.writelines('-----------------------\n')
        log_file.writelines('File {} Start Time - {}\n\n'.format(file_name, file_start_time))
        log_file.writelines('-----------------------\n')
        print 'File {} Start Time - {}'.format(file_name, file_start_time)
        file_folder = file_name.split('.')[0]
        os.makedirs('{}/{}'.format(folder, file_folder))
        # print path
        nc_file = nc4.Dataset(path, mode='r')

        A = (50, 50)
        B = (100, 100)
        sin_alpha = (B[1] - A[1])/np.sqrt((B[0] - A[0])**2 + (B[1] - A[1])**2)
        cos_alpha = np.sqrt(1 - sin_alpha**2)
        print sin_alpha
        print cos_alpha
        return 0
        highs = nc_file.variables['U'].shape[1]

        highs = 3

        for h in range(highs):
            high_start_time = arrow.now()
            log_file.writelines('High #{} Start Time - {}\n'.format(h, high_start_time))
            # print 'High #{} Start Time - {}'.format(h, high_start_time)
            x_wind = nc_file.variables['U']
            z_wind = nc_file.variables['W']
            x_wind0 = x_wind[0][h]
            y_wind0 = y_wind[0][h]
            # todo figure out with shape
            X, Y = np.meshgrid(np.arange(0, 249, 1), np.arange(0, 249, 1))
            U = x_wind0
            V = y_wind0
            Z = create_module_matrix(U, V)
            plt.figure(figsize=(10, 10), facecolor='w', edgecolor='r')
            plt.streamplot(
                X[::step, ::step],
                Y[::step, ::step],
                U[::step, ::step],
                V[::step, ::step],
                color=Z[::step, ::step],
                cmap=cm.cool,
                linewidth=1.0,
                arrowstyle='->',
                arrowsize=1.5,
            )
            plt.colorbar()
            plt.axis([-10, 260, -10, 260])
            plt.title('{}/high{}.png'.format(folder, h))
            plt.savefig('{}/{}/high{}.png'.format(folder, file_folder, h))
            plt.close()
            # print ('{}/{}/high{}.png is created'.format(folder, file_folder, h))
            high_end_time = arrow.now()
            high_delta = high_end_time - high_start_time
            print 'High #{} Delta - {}'.format(h, high_delta)
            log_file.writelines('High End Time - {}\n'.format(high_end_time))
            log_file.writelines('High Delta - {}\n\n'.format(high_delta))
        file_end_time = arrow.now()
        log_file.writelines('-----------------------\n')
        log_file.writelines('File {} End Time - {}\n\n'.format(file_name, file_end_time))
        print 'File {} End Time - {}\n'.format(file_name, file_end_time)
        file_delta = file_end_time - file_start_time
        log_file.writelines('File {} Delta - {}\n'.format(file_name, file_delta))
        log_file.writelines('-----------------------\n')
        print 'High {} Delta - {}\n'.format(file_name, file_delta)

def main():
    directory = '../StreamImage'
    if not os.path.exists(directory):
        os.makedirs(directory)
    start_time = arrow.now()
    folder = '{}/StreamImages#{}'.format(directory, start_time.timestamp)
    os.makedirs(folder)
    with open('{}/log.txt'.format(folder), mode='w', ) as log_file:
        log_file.write('***********************\n')
        log_file.write('Start Time - {}\n'.format(start_time))
        log_file.write('***********************\n')

        # paths = get_file_paths('nc')
        paths = ['/home/varalex/University/nc/wrfout_d01_2013-05-22_01.nc', ]
        while True:
            print '1. Horizontal cut'
            print '2. Vertical cut'
            choise = input()
            if choise == 1:
                horizontal_cut(paths=paths, folder=folder, log_file=log_file)
                break
            elif choise == 2:
                vertical_cut(paths=paths, folder=folder, log_file=log_file)
                break
            else:
                continue

        end_time = arrow.now()
        work_time = end_time - start_time
        log_file.write('***********************\n')
        log_file.write('End Time - {}\n'.format(end_time))
        log_file.write('Work Time - {}\n'.format(work_time))
        log_file.write('***********************\n')


main()

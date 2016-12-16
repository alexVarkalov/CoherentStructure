import os
import arrow
import netCDF4 as nc4
import numpy as np
import matplotlib.pyplot as plt
import Tkinter
import tkFileDialog
from matplotlib import cm
from utils import *


def horizontal_cut(paths, folder, log_file):
    step = 1

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
        max_level = nc_file.variables['U'].shape[1] - 1
        while True:
            try:
                highs = input('Enter High levels. Min is 0. Max is {}. Write -1 for all: '.format(max_level))
            except Exception:
                print('Wrong Input')
                continue
            if highs == -1:
                start_high = 0
                end_high = max_level
                break
            elif isinstance(highs, int) and 0 <= highs <= max_level:
                start_high = highs
                end_high = highs + 1
                break
            elif isinstance(highs, tuple) and len(highs) == 2 and highs[1] > highs[0] >= 0:
                start_high = highs[0]
                end_high = highs[1]
                break
            else:
                print('Wrong Input')
                continue

        for h in range(start_high, end_high):
            high_start_time = arrow.now()
            log_file.writelines('High #{} Start Time - {}\n'.format(h, high_start_time))
            x_wind = nc_file.variables['U']
            y_wind = nc_file.variables['V']
            x_wind0 = x_wind[0][h]
            y_wind0 = y_wind[0][h]
            min_shape = min(x_wind0.shape[0], x_wind0.shape[1], y_wind0.shape[0], y_wind0.shape[1])
            x_wind0 = x_wind0[:min_shape, :min_shape]
            y_wind0 = y_wind0[:min_shape, :min_shape]
            X, Y = np.meshgrid(np.arange(0, x_wind0.shape[0], 1), np.arange(0, x_wind0.shape[1], 1))
            U = x_wind0
            V = y_wind0
            Z = create_module_matrix(U, V)
            plt.figure(figsize=(12.5, 10), facecolor='w', edgecolor='r')
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
            plt.axis([-X.shape[1] * 0.1, X.shape[1] * 1.1, -Y.shape[0] * 0.1, Y.shape[0] * 1.1])
            plt.title('{}/high{}.png'.format(folder, h))
            plt.savefig('{}/{}/high{}.png'.format(folder, file_folder, h))
            plt.close()

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
    step = 1

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
        nc_file = nc4.Dataset(path, mode='r')
        while True:
            print('Enter Points coordinates')
            max_value = min(nc_file.variables['U'][0][0].shape[0], nc_file.variables['U'][0][0].shape[1])
            pointA = raw_input('point A. Min - (0,0). Max({},{}): '.format(max_value - 1, max_value - 1)).split(', ')
            if len(pointA) > 2:
                print('Wrong Input')
                continue
            else:
                pointA[0] = int(pointA[0])
                pointA[1] = int(pointA[1])
                if pointA[0] >= max_value or pointA[1] >= max_value:
                    print('Wrong Input')
                    continue
            pointB = raw_input('point B. Min - (0,0). Max({},{}): '.format(max_value - 1, max_value - 1)).split(', ')
            if len(pointB) > 2:
                print('Wrong Input')
                continue
            else:
                pointB[0] = int(pointB[0])
                pointB[1] = int(pointB[1])
                if pointB[0] >= max_value or pointB[1] >= max_value:
                    print('Wrong Input')
                    continue
            break
        if pointB[0] < pointA[0]:
            pointA, pointB = pointB, pointA
        if pointA[0] - pointB[0] == 0:
            sin_alpha = 1
            cos_alpha = 10 ** 13
        elif pointA[1] - pointB[1] == 0:
            sin_alpha = 10 ** 13
            cos_alpha = 1
        else:
            sin_alpha = (pointB[1] - pointA[1]) / np.sqrt((pointB[0] - pointA[0]) ** 2 + (pointB[1] - pointA[1]) ** 2)
            cos_alpha = np.sqrt(1 - sin_alpha ** 2)

        coords = bresenham_line(pointA, pointB)
        matrixXY = []
        matrixZ = []
        for i in range(27):
            U = nc_file.variables['U'][0][i]
            V = nc_file.variables['V'][0][i]
            W = nc_file.variables['W'][0][i]
            vectorXY = []
            vectorZ = []
            for x, y in coords:
                vectorXY.append(U[x][y] / cos_alpha + V[x][y] / sin_alpha)
                vectorZ.append(W[x][y])
            matrixXY.append(vectorXY)
            matrixZ.append(vectorZ)

        matrixXY = np.array(matrixXY)
        matrixZ = np.array(matrixZ)
        X, Y = np.meshgrid(np.arange(0, matrixXY.shape[1], 1), np.arange(0, matrixXY.shape[0], 1))
        Z = create_module_matrix(matrixXY, matrixZ)
        plt.figure(figsize=(20, 10), facecolor='w', edgecolor='r')
        plt.streamplot(
            X[::step, ::step],
            Y[::step, ::step],
            matrixXY[::step, ::step],
            matrixZ[::step, ::step],
            color=Z[::step, ::step],
            cmap=cm.cool,
            linewidth=1.0,
            arrowstyle='->',
            arrowsize=1.5,
        )
        plt.colorbar()
        plt.axis([-matrixXY.shape[1] * 0.1, matrixXY.shape[1] * 1.1, -matrixXY.shape[0] * 0.1, matrixXY.shape[0]])
        plt.title('{}/A({},{});B({},{}).png'.format(folder, pointA[0], pointA[1], pointB[0], pointB[1]))
        plt.savefig(
            '{}/{}/A({},{});B({},{}).png'.format(folder, file_folder, pointA[0], pointA[1], pointB[0], pointB[1]))
        plt.close()

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

import os
import arrow
import netCDF4 as nc4
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from utils import *


def horizontal_cut(paths, folder):
    step = 1
    start_height, end_height = None, None
    work_folder = '{}/{}'.format(folder, arrow.now().now().strftime("%Y-%m-%d_%H:%M:%S"))
    os.makedirs(work_folder)
    divide_method = get_divide_method()
    for path in paths:
        nc_file = nc4.Dataset(path, mode='r')
        hour = str(arrow.get(''.join(nc_file.variables['Times'][0]), 'YYYY-M-D_HH:mm:ss').time().hour).zfill(2)
        max_level = nc_file.variables['U'].shape[1] - 1
        if not start_height and not end_height:
            start_height, end_height = get_heights(max_level=max_level)

        for height in range(start_height, end_height):
            U = nc_file.variables['U'][0][height]
            V = nc_file.variables['V'][0][height]
            min_shape = min(U.shape[0], U.shape[1], V.shape[0], V.shape[1])
            U = U[:min_shape, :min_shape]
            V = V[:min_shape, :min_shape]
            X = nc_file.variables['XLONG'][0]
            Y = nc_file.variables['XLAT'][0]
            color = create_module_matrix(U, V)
            plt.figure(figsize=(12.5, 10), facecolor='w', edgecolor='r')
            plt.streamplot(
                X[::step, ::step],
                Y[::step, ::step],
                U[::step, ::step],
                V[::step, ::step],
                color=color[::step, ::step],
                cmap=cm.cool,
                linewidth=1.0,
                arrowstyle='->',
                arrowsize=1.5,
            )
            plt.colorbar()
            if divide_method == 'hours':
                if not os.path.exists('{}/hours'.format(work_folder)):
                    os.makedirs('{}/hours'.format(work_folder))
                if not os.path.exists('{}/hours/{}'.format(work_folder, hour)):
                    os.makedirs('{}/hours/{}'.format(work_folder, hour))
                plt.title('{}/hours/{}/height#{}'.format(work_folder, hour, str(height).zfill(2)))
                plt.savefig('{}/hours/{}/{}.png'.format(work_folder, hour, str(height).zfill(2)))
            elif divide_method == 'heights':
                if not os.path.exists('{}/heights'.format(work_folder)):
                    os.makedirs('{}/heights'.format(work_folder))
                if not os.path.exists('{}/heights/{}'.format(work_folder, str(height).zfill(2))):
                    os.makedirs('{}/heights/{}'.format(work_folder, str(height).zfill(2)))
                plt.title('{}/heights/{}/hour-{}'.format(work_folder, str(height).zfill(2), hour))
                plt.savefig('{}/heights/{}/{}.png'.format(work_folder, str(height).zfill(2), hour))
            plt.close()


def vertical_cut(paths, folder):
    step = 1
    pointA, pointB = None, None,
    sin_alpha, cos_alpha = None, None
    start_height, end_height = None, None
    coords = []
    work_folder = '{}/{}'.format(folder, arrow.now().now().strftime("%Y-%m-%d_%H:%M:%S"))
    os.makedirs(work_folder)
    for path in paths:
        nc_file = nc4.Dataset(path, mode='r')
        hour = str(arrow.get(''.join(nc_file.variables['Times'][0]), 'YYYY-M-D_HH:mm:ss').time().hour).zfill(2)
        max_value = min(nc_file.variables['U'][0][0].shape[0], nc_file.variables['U'][0][0].shape[1])
        if not pointA or not pointB or not sin_alpha or not cos_alpha or not coords:
            pointA, pointB = set_points(max_value=max_value)
            sin_alpha, cos_alpha = get_sin_cos_by_points(pointA=pointA, pointB=pointB)
            coords = bresenham_line(pointA, pointB)
        max_level = nc_file.variables['U'].shape[1] - 1
        if not start_height and not end_height:
            start_height, end_height = get_heights(max_level=max_level)
        UVp = []
        Wp = []
        for height in range(start_height, end_height):
            U = nc_file.variables['U'][0][height]
            V = nc_file.variables['V'][0][height]
            W = nc_file.variables['W'][0][height]
            # X = nc_file.variables['XLONG'][0]
            # Y = nc_file.variables['XLAT'][0]
            vectorUVp = []
            vectorWp = []
            for x, y in coords:
                vectorUVp.append(U[x][y] / cos_alpha + V[x][y] / sin_alpha)
                vectorWp.append(W[x][y])
            UVp.append(vectorUVp)
            Wp.append(vectorWp)
        UVp = np.array(UVp)
        Wp = np.array(Wp)
        X, Y = np.meshgrid(np.arange(0, UVp.shape[1], 1), np.arange(start_height, end_height, 1))
        Z = create_module_matrix(UVp, Wp)
        plt.figure(figsize=(20, 10), facecolor='w', edgecolor='r')
        plt.streamplot(
            X[::step, ::step],
            Y[::step, ::step],
            UVp[::step, ::step],
            Wp[::step, ::step],
            color=Z[::step, ::step],
            cmap=cm.cool,
            linewidth=1.0,
            arrowstyle='->',
            arrowsize=1.5,
        )
        plt.colorbar()
        plt.title('{}/{}.png'.format(work_folder, hour))
        plt.savefig('{}/{}.png'.format(work_folder, hour))
        plt.close()


def main():
    folder = '../StreamImage'
    if not os.path.exists(folder):
        os.makedirs(folder)
    start_time = arrow.now()
    paths = get_file_paths('nc')
    while True:
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
        else:
            print('Wrong Input')
            continue
    end_time = arrow.now()
    work_time = end_time - start_time


main()

from utils import *
import os
import arrow
import netCDF4 as nc4
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm


def horizontal_cut():
    folder = '../StreamImage'
    if not os.path.exists(folder):
        os.makedirs(folder)

    step = 1

    paths = get_file_paths('nc')
    start_height, end_height = None, None
    divide_method = None
    coord_system = None

    work_folder = '{}/{}'.format(folder, arrow.now().now().strftime("%Y-%m-%d_%H:%M:%S"))
    os.makedirs(work_folder)

    if divide_method not in ['hours', 'heights']:
        divide_method = choose_divide_method()
    if coord_system not in ['X Y', 'Lat Long']:
        coord_system = choose_coord_system()

    for path in paths:
        nc_file = nc4.Dataset(path, mode='r')
        U_theta, V_theta, W_theta = create_theta_wind_matrix(nc_file)
        hour = str(arrow.get(''.join(nc_file.variables['Times'][0]), 'YYYY-M-D_HH:mm:ss').time().hour).zfill(2)
        max_level = U_theta.shape[0] - 1

        if not start_height and not end_height:
            start_height, end_height = get_heights(max_level=max_level)

        for height in range(start_height, end_height):
            U, V = U_theta[height], V_theta[height]
            shape = U.shape
            if coord_system == 'X Y':
                X, Y = np.meshgrid(np.arange(0, shape[0], 1), np.arange(0, shape[1], 1))
            elif coord_system == 'Lat Long':
                X = nc_file.variables['XLONG'][0]
                Y = nc_file.variables['XLAT'][0]
            vort = wrf_vort(U=U, V=V, dx=1)
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
            if coord_system == 'X Y':
                plt.axis([-shape[0]*0.1, shape[0]*1.1, -shape[1]*0.1, shape[1]*1.1])
            plt.colorbar()
            save_plot(divide_method=divide_method, work_folder=work_folder, hour=hour, height=height)
            plt.close()

if __name__ == '__main__':
    horizontal_cut()

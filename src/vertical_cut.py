from utils import *
import os
import arrow
import netCDF4 as nc4
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm


def vertical_cut():
    folder = '../StreamImage'
    if not os.path.exists(folder):
        os.makedirs(folder)

    step = 1

    paths = get_file_paths('nc')
    pointA, pointB = None, None,
    sin_alpha, cos_alpha = None, None
    start_height, end_height = None, None
    coords = []

    work_folder = '{}/{}'.format(folder, arrow.now().now().strftime("%Y-%m-%d_%H:%M:%S"))
    os.makedirs(work_folder)

    for path in paths:
        nc_file = nc4.Dataset(path, mode='r')
        U_theta, V_theta, W_theta = create_theta_wind_matrix(nc_file)
        hour = str(arrow.get(''.join(nc_file.variables['Times'][0]), 'YYYY-M-D_HH:mm:ss').time().hour).zfill(2)
        max_level = U_theta.shape[0] - 1

        if not pointA or not pointB or not sin_alpha or not cos_alpha or not coords:
            pointA, pointB = set_points(max_value=U_theta.shape[1])
            sin_alpha, cos_alpha = get_sin_cos_by_points(pointA=pointA, pointB=pointB)
            coords = bresenham_line(pointA, pointB)
        if not start_height and not end_height:
            start_height, end_height = get_heights(max_level=max_level)
        UVp = []
        Wp = []
        for height in range(start_height, end_height):
            U = U_theta[height]
            V = V_theta[height]
            W = W_theta[height]
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

if __name__ == '__main__':
    vertical_cut()

import os
import arrow
import sys
import netCDF4 as nc4
import matplotlib.pyplot as plt

from utils import *
from theta_wind_matrix import get_theta_wind_matrix
from demo import demo_values


def horizontal_cut():
    import datetime
    start_time = datetime.datetime.now()
    if 'demo' in sys.argv:
        start_height, end_height, divide_method, paths = demo_values()
    else:
        start_height, end_height = None, None
        divide_method = choose_divide_method()
        paths = get_file_paths('nc')

    folder = '../StreamImage'
    if not os.path.exists(folder):
        os.makedirs(folder)

    step = 1

    work_folder = '{}/{}'.format(folder, arrow.now().now().strftime("%Y-%m-%d_%H:%M:%S"))
    os.makedirs(work_folder)

    for path in paths:
        print path
        nc_file = nc4.Dataset(path, mode='r')
        recreate = True if 'recreate' in sys.argv else False
        u_theta, v_theta, w_theta = get_theta_wind_matrix(path=path, nc_file=nc_file, recreate=recreate)

        hour = str(arrow.get(''.join(nc_file.variables['Times'][0]), 'YYYY-M-D_HH:mm:ss').time().hour).zfill(2)

        max_level = u_theta.shape[0] - 1

        if not start_height and not end_height:
            start_height, end_height = get_heights(max_level=max_level)

        for height in range(start_height, end_height):
            print height
            u, v = u_theta[height], v_theta[height]
            shape = u.shape
            x_axis = nc_file.variables['XLONG'][0]
            y_axis = nc_file.variables['XLAT'][0]

            # vort = wrf_vort(U=u, V=v, dx=1)
            # print('{} - {}'.format(height, vort))
            color = w_theta[height] if 'speed' in sys.argv else create_module_matrix(u, v)

            plt.figure(figsize=(12.5, 10), facecolor='w', edgecolor='r')
            plt.streamplot(
                x_axis[::step, ::step],
                y_axis[::step, ::step],
                u[::step, ::step],
                v[::step, ::step],
                color=color[::step, ::step],
                linewidth=1.5,
                arrowstyle='->',
                arrowsize=1.5,
            )
            length = shape[0]-1
            plt.axis([x_axis[0][0], x_axis[length][length], y_axis[0][0], y_axis[length][length]])
            plt.colorbar()
            save_plot(divide_method=divide_method, work_folder=work_folder, hour=hour, height=height)
            plt.close()
    end_time = datetime.datetime.now()
    print(end_time-start_time)

if __name__ == '__main__':
    horizontal_cut()

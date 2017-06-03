import os
import arrow
import sys
import netCDF4 as nc4
import matplotlib.pyplot as plt


from utils import *
from theta_wind_matrix import get_theta_wind_matrix, theta_wind_matrix
from demo import demo_values


def horizontal_cut():
    start_time = arrow.now()
    speed = 'speed' in sys.argv
    demo = 'demo' in sys.argv
    recreate = 'recreate' in sys.argv
    folder = '../StreamImage'
    if demo:
        start_height, end_height, divide_method, paths = demo_values()
        folder += 'Demo'
    else:
        start_height, end_height = None, None
        divide_method = choose_divide_method()
        paths = get_file_paths('nc')

    if not os.path.exists(folder):
        os.makedirs(folder)

    if recreate:
        theta_wind_matrix(paths=paths)

    step = 1

    work_folder = '{}/{}'.format(folder, arrow.now().now().strftime("%Y-%m-%d_%H:%M:%S"))
    os.makedirs(work_folder)

    for path in paths:
        print path
        nc_file = nc4.Dataset(path, mode='r')
        u_theta, v_theta, w_theta = get_theta_wind_matrix(path=path)

        if u_theta == None or v_theta == None or w_theta == None:
            continue

        hour = str(arrow.get(''.join(nc_file.variables['Times'][0]), 'YYYY-M-D_HH:mm:ss').time().hour).zfill(2)

        max_level = u_theta.shape[0] - 1

        if not start_height and not end_height:
            start_height, end_height = get_heights(max_level=max_level)

        for height in range(start_height, end_height):
            u, v = u_theta[height], v_theta[height]
            length = u.shape[0]-1
            x_axis, y_axis = nc_file.variables['XLONG'][0], nc_file.variables['XLAT'][0]
            background_color = w_theta[height] if speed else np.zeros((249, 249))
            curve_color = 'black' if speed else create_module_matrix(u, v)[::step, ::step]
            plt.figure(figsize=(20, 10), facecolor='w', edgecolor='r')
            plt.streamplot(
                x_axis[::step, ::step],
                y_axis[::step, ::step],
                u[::step, ::step],
                v[::step, ::step],
                color=curve_color,
                linewidth=1.5,
                arrowstyle='->',
                arrowsize=1.5,
            )
            if not speed:
                plt.colorbar()

            frame = (x_axis[0][0], x_axis[length][length], y_axis[0][0], y_axis[length][length])

            plt.imshow(background_color, cmap='Greys' if not speed else None, extent=frame)
            if speed:
                plt.colorbar()

            plt.axis(frame)
            save_plot(divide_method=divide_method, work_folder=work_folder, hour=hour, height=height)
            plt.close()

    end_time = arrow.now()
    print('Working time - {}'.format(end_time-start_time))

if __name__ == '__main__':
    horizontal_cut()

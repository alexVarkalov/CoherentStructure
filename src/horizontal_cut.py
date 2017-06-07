import sys

import arrow
import matplotlib.pyplot as plt
import netCDF4 as nc4
import numpy as np
import os

from theta_wind_matrix import get_theta_wind_matrix, theta_wind_matrix
from ui_utils import get_file_paths, get_heights, choose_divide_method
from utils import save_plot, create_module_matrix, get_hour_from_nc_file, path_leaf
from settings import DEFAULT_HORIZONTAL_CUT_SETTINGS


def plot_horizontal_cut(u, v, w, data):
    v_speed = 'v_speed' in sys.argv
    h_speed = 'h_speed' in sys.argv

    from settings import DEFAULT_STEP
    step = DEFAULT_STEP
    length = u.shape[0] - 1
    x_axis, y_axis = data.get('nc_file').variables['XLONG'][0], data.get('nc_file').variables['XLAT'][0]

    background_color = np.zeros((249, 249))
    curve_color = create_module_matrix(u, v)[::step, ::step]
    color_map = 'Greys'

    if h_speed:
        if 'h_hist' in sys.argv:
            from horizontal_histogram import get_matrix_by_horizontal_histogram
            background_color = get_matrix_by_horizontal_histogram(u=u, v=v)[::step, ::step]
        elif 'a_hist' in sys.argv:
            from angle_histogram import get_matrix_by_angle_histogram
            background_color = get_matrix_by_angle_histogram(u=u, v=v)
        else:
            background_color = create_module_matrix(u, v)[::step, ::step]
        curve_color = 'black'

        color_map = None

    if v_speed:
        if 'h_hist' in sys.argv:
            from horizontal_histogram import get_matrix_by_horizontal_histogram
            background_color = get_matrix_by_horizontal_histogram(u=w, v=np.zeros((w.shape[0], w.shape[1])))[::step, ::step]
        else:
            background_color = w
        curve_color = 'black'
        color_map = None

    fig = plt.figure(figsize=(20, 10), facecolor='w', edgecolor='r')
    plt.streamplot(
        x_axis[::step, ::step],
        y_axis[::step, ::step],
        u[::step, ::step],
        v[::step, ::step],
        color=curve_color,
        linewidth=1.5,
        arrowstyle='->',
        arrowsize=1.5,
        density=1
    )

    if not v_speed and not h_speed:
        plt.colorbar()
        plt.clim(
            vmin=DEFAULT_HORIZONTAL_CUT_SETTINGS.get('horizontal_speed_down', 0),
            vmax=DEFAULT_HORIZONTAL_CUT_SETTINGS.get('horizontal_speed_up', 45),
        )
    frame = (x_axis.min(), x_axis.max(), y_axis.min(), y_axis.max())

    plt.imshow(background_color, cmap=color_map, extent=frame, origin='lower')
    if v_speed or h_speed:
        plt.colorbar()
        if h_speed:
            plt.clim(
                vmin=DEFAULT_HORIZONTAL_CUT_SETTINGS.get('horizontal_speed_down', 0),
                vmax=DEFAULT_HORIZONTAL_CUT_SETTINGS.get('horizontal_speed_up', 45),
            )
        elif v_speed:
            plt.clim(
                vmin=DEFAULT_HORIZONTAL_CUT_SETTINGS.get('vertical_speed_down', -0.5),
                vmax=DEFAULT_HORIZONTAL_CUT_SETTINGS.get('vertical_speed_up', 0.5),
            )

    plt.axis(frame)
    if 'show' in sys.argv:
        plt.show()
        return None

    save_plot(
        data=data,
        img_type='map'
    )
    plt.close(fig)


def create_horizontal_cut(path, data):
    print path
    data['nc_file'] = nc4.Dataset(path, mode='r')

    u_theta, v_theta, w_theta = get_theta_wind_matrix(path=path)

    if u_theta is None or v_theta is None or w_theta is None:
        return None

    data['file_name'] = path_leaf(path)
    data['hour'] = get_hour_from_nc_file(data=data)
    max_level = u_theta.shape[0] - 1
    if 'start_height' not in data.keys() or 'end_height' not in data.keys():
        data['start_height'], data['end_height'] = get_heights(max_level=max_level)

    for height in range(data.get('start_height'), data.get('end_height')):
        data['height'] = height
        plot_horizontal_cut(u=u_theta[height], v=v_theta[height], w=w_theta[height], data=data)


def horizontal_cut(paths=None, data=None):
    start_time = arrow.now()
    if not paths:
        paths = get_file_paths('nc')
        recreate = 'recreate' in sys.argv
        if recreate:
            theta_wind_matrix(paths=paths)

    if not data:
        folder = '../StreamImage'
        if not os.path.exists(folder):
            os.makedirs(folder)
        if 'demo' in sys.argv:
            folder += 'Demo'
        data = dict()
        data['divide_method'] = choose_divide_method()
        data['work_folder'] = '{}/{}'.format(folder, arrow.now().now().strftime("%Y-%m-%d_%H:%M:%S"))
        os.makedirs(data.get('work_folder'))

    for path in paths:
        create_horizontal_cut(path=path, data=data)

    end_time = arrow.now()
    print('Horizontal Cut working time - {}'.format(end_time-start_time))

if __name__ == '__main__':
    horizontal_cut()

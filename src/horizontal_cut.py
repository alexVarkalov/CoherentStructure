import os
import arrow
import sys
import netCDF4 as nc4
import matplotlib.pyplot as plt
import numpy as np

from utils import save_plot, create_module_matrix, get_hour_from_nc_file
from theta_wind_matrix import get_theta_wind_matrix, theta_wind_matrix
from ui_utils import get_file_paths, get_heights, choose_divide_method


def plot_horizontal_cut(u, v, w, data):
    speed = 'speed' in sys.argv

    from settings import DEFAULT_STEP
    step = DEFAULT_STEP
    length = u.shape[0] - 1
    x_axis, y_axis = data.get('nc_file').variables['XLONG'][0], data.get('nc_file').variables['XLAT'][0]
    background_color = w if speed else np.zeros((249, 249))
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
    save_plot(
        divide_method=data.get('divide_method'),
        work_folder=data.get('work_folder'),
        hour=data.get('hour'),
        height=data.get('height'),
        img_type='map'
    )
    plt.close()


def create_horizontal_cut(path, data):
    print path
    data['nc_file'] = nc4.Dataset(path, mode='r')

    u_theta, v_theta, w_theta = get_theta_wind_matrix(path=path)

    if u_theta is None or v_theta is None or w_theta is None:
        return None

    data['hour'] = get_hour_from_nc_file(data=data)
    max_level = u_theta.shape[0] - 1
    if not data.get('start_height') or not data.get('end_height'):
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

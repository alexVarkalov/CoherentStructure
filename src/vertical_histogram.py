import sys

import arrow
import matplotlib.pyplot as plt
import netCDF4 as nc4
import os

from theta_wind_matrix import get_theta_wind_matrix, theta_wind_matrix
from ui_utils import get_file_paths, get_heights, choose_divide_method
from utils import save_plot, get_hour_from_nc_file, path_leaf


def plot_vertical_histogram(u, v, w, data):
    from settings import DEFAULT_STEP, DEFAULT_VERTICAL_HISTOGRAM_SETTINGS
    step = DEFAULT_STEP

    module_vector = w[::step, ::step].ravel()
    fig = plt.figure(figsize=(20, 10), facecolor='w', edgecolor='r')
    plt.hist(
        module_vector,
        bins=DEFAULT_VERTICAL_HISTOGRAM_SETTINGS.get('bins', 100),
        normed=1,
        facecolor='green',
        alpha=0.75
    )

    plt.xlim(
        [
            DEFAULT_VERTICAL_HISTOGRAM_SETTINGS.get('speed_down', -0.5),
            DEFAULT_VERTICAL_HISTOGRAM_SETTINGS.get('speed_up', 0.5)]
    )

    plt.ylim(
        [
            DEFAULT_VERTICAL_HISTOGRAM_SETTINGS.get('probability_down', 0),
            DEFAULT_VERTICAL_HISTOGRAM_SETTINGS.get('probability_up', 30)]
    )

    # plt.xlabel('Smarts')
    plt.ylabel('Probability')
    plt.grid(True)
    save_plot(
        data=data,
        img_type='vertical-histogram'
    )
    plt.close(fig)


def create_vertical_histogram(path, data):
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
        plot_vertical_histogram(u=u_theta[height], v=v_theta[height], w=w_theta[height], data=data)


def vertical_histogram(paths=None, data=None):
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
        create_vertical_histogram(path=path, data=data)

    end_time = arrow.now()
    print('Horizontal Cut working time - {}'.format(end_time-start_time))

if __name__ == '__main__':
    vertical_histogram()

import sys

import arrow
import os

from horizontal_cut import horizontal_cut
from angle_histogram import angle_histogram

from ui_utils import choose_divide_method, get_file_paths


def main():
    start_time = arrow.now()
    paths = get_file_paths('nc')
    folder = '../StreamImage'
    if 'demo' in sys.argv:
        folder += 'Demo'
    data = dict()
    data['divide_method'] = choose_divide_method()
    data['work_folder'] = '{}/{}'.format(folder, arrow.now().now().strftime("%Y-%m-%d_%H:%M:%S"))
    os.makedirs(data.get('work_folder'))
    horizontal_cut(paths=paths, data=data)
    angle_histogram(paths=paths, data=data)
    end_time = arrow.now()
    print('Total working time - {}'.format(end_time-start_time))

if __name__ == '__main__':
    main()

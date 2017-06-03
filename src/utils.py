import Tkinter
import tkFileDialog
import ntpath
import numpy as np
import arrow
import os
import matplotlib.pyplot as plt


def path_leaf(path):
    """ Take file name from path """
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def check_filename_extension(path, filename_extension):
    return True if path.split('.')[1] == filename_extension else False


def get_file_paths(filename_extension):
    # todo use base func param
    while True:
        print 'Please, select a .{} file(s)'.format(filename_extension)
        root = Tkinter.Tk()
        root.withdraw()
        paths = tkFileDialog.askopenfilenames(parent=root, title='Choose a file(s)')
        for path in paths:
            if not check_filename_extension(path=path, filename_extension=filename_extension):
                print ('{} is not .{} file. Choose file(s) again.'.format(path_leaf(path), filename_extension))
                paths = []
                root.destroy()
                break
        if not paths:
            continue
        print 'Your file(s):\n{}\nAll right?'.format('\n'.join(paths))
        while True:
            answer = raw_input('Print yes or no\n')
            if 'yes' == answer.strip().lower() or 'y' == answer.strip().lower():
                return paths
            elif 'no' == answer.strip().lower() or 'n' == answer.strip().lower():
                continue


def bresenham_line((x, y), (x2, y2)):
    """Brensenham line algorithm"""
    steep = 0
    coords = []
    dx = abs(x2 - x)
    if (x2 - x) > 0:
        sx = 1
    else:
        sx = -1
    dy = abs(y2 - y)
    if (y2 - y) > 0:
        sy = 1
    else:
        sy = -1
    if dy > dx:
        steep = 1
        x, y = y, x
        dx, dy = dy, dx
        sx, sy = sy, sx
    d = (2 * dy) - dx
    for i in range(0, dx):
        if steep:
            coords.append((y, x))
        else:
            coords.append((x, y))
        while d >= 0:
            y += sy
            d -= (2 * dx)
        x += sx
        d += (2 * dy)
    coords.append((x2, y2))
    # if switched:
    #     coords.reverse()
    return coords


def create_module_matrix(x, y):
    """ Create Matrix of polar radius """
    sq_x = np.zeros(x.shape)
    sq_y = np.zeros(y.shape)
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            sq_x[i][j] = x[i][j] ** 2
    for i in range(y.shape[0]):
        for j in range(y.shape[1]):
            sq_y[i][j] = y[i][j] ** 2
    z = np.zeros((x.shape[0], x.shape[1]))
    for i in range(z.shape[0]):
        for j in range(z.shape[1]):
            z[i][j] = np.sqrt(sq_x[i][j] + sq_y[i][j])
    return z


def get_heights(max_level):
    while True:
        try:
            heights = input('Enter High levels.\n'
                            'Min is 0. Max is {}. Write -1 for all\n'
                            'Example: 1, 10\n'
                            ': '.format(max_level)
                            )
        except Exception:
            print('Wrong Input')
            continue
        if heights == -1:
            start_high = 0
            end_high = max_level
            break
        elif isinstance(heights, int) and 0 <= heights <= max_level:
            start_high = heights
            end_high = heights + 1
            break
        elif isinstance(heights, tuple) and len(heights) == 2 and heights[1] > heights[0] >= 0:
            start_high = heights[0]
            end_high = heights[1]
            break
        else:
            print('Wrong Input')
            continue
    return start_high, end_high


def choose_divide_method():
    while True:
        print('Divide by heights or hours?')
        print('1. Heights\n2. Hours')
        try:
            choose = input(': ')
        except Exception:
            print('Wrong Input')
            continue
        if choose == 1:
            return 'heights'
        elif choose == 2:
            return 'hours'
        print('Wrong Input')


def choose_coord_system():
    return 'Lat Long'
    while True:
        print('What coordinate system use?')
        print('1. X Y\n2. Lat Long')
        try:
            choose = input(': ')
        except Exception:
            print('Wrong Input')
            continue
        if choose == 1:
            coord_system = 'X Y'
            return coord_system
        elif choose == 2:
            coord_system = 'Lat Long'
            return coord_system
        print('Wrong Input')


def set_points(max_value):
    while True:
        try:
            print('Enter Points coordinates')
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
            if pointB[0] < pointA[0]:
                pointA, pointB = pointB, pointA
            return pointA, pointB
        except Exception:
            print('Wrong Input')
            continue


def get_sin_cos_by_points(point_a, point_b):
    if point_a[0] - point_b[0] == 0:
        sin_alpha = 1
        cos_alpha = 10 ** 13
    elif point_a[1] - point_b[1] == 0:
        sin_alpha = 10 ** 13
        cos_alpha = 1
    else:
        sin_alpha = (point_b[1] - point_a[1]) / np.sqrt((point_b[0] - point_a[0]) ** 2 + (point_b[1] - point_a[1]) ** 2)
        cos_alpha = np.sqrt(1 - sin_alpha ** 2)
    return sin_alpha, cos_alpha


def save_plot(divide_method, work_folder, hour, height):
    plot = ''
    if divide_method == 'hours':
        if not os.path.exists('{}/hours'.format(work_folder)):
            os.makedirs('{}/hours'.format(work_folder))
        if not os.path.exists('{}/hours/{}'.format(work_folder, hour)):
            os.makedirs('{}/hours/{}'.format(work_folder, hour))
        plt.title('{}/hours/{}/height#{}'.format(work_folder, hour, str(height).zfill(2)))
        plot = '{}/hours/{}/{}.png'.format(work_folder, hour, str(height).zfill(2))
        plt.savefig(plot)
    elif divide_method == 'heights':
        if not os.path.exists('{}/heights'.format(work_folder)):
            os.makedirs('{}/heights'.format(work_folder))
        if not os.path.exists('{}/heights/{}'.format(work_folder, str(height).zfill(2))):
            os.makedirs('{}/heights/{}'.format(work_folder, str(height).zfill(2)))
        plt.title('{}/heights/{}/hour-{}'.format(work_folder, str(height).zfill(2), hour))
        plot = '{}/heights/{}/{}.png'.format(work_folder, str(height).zfill(2), hour)
        plt.savefig(plot)
    print('{} is saved'.format(plot))


def wrf_vort( U, V, dx ):
    """Calculate the relative vorticity given the U and V vector components in m/s
    and the grid spacing dx in meters.
    U and V must be the same shape.
    ---------------------
    U (numpy.ndarray): ndarray of U vector values in m/s
    V (numpy.ndarray): ndarray of V vector values in m/s
    dx (float or int): float or integer of U and V grispacing in meters
    ---------------------
    returns:
        numpy.ndarray of vorticity values s^-1 same shape as U and V
    """
    assert U.shape == V.shape, 'Arrays are different shapes. They must be the same shape.'
    dy = dx
    du = np.gradient( U )
    dv = np.gradient( V )
    return ( dv[-1]/dx - du[-2]/dy )


def wrf_absvort(U, V, F, dx):
    """Calculate the absolute vorticity given the U and V vector components in m/s,
    the Coriolis sine latitude term (F) in s^-1, and gridspacing dx in meters. U, V, and F
    must be the same shape.
    ---------------------
    U (numpy.ndarray): ndarray of U vector values in m/s
    V (numpy.ndarray): ndarray of V vector values in m/s
    F (numpy.ndarray): ndarray of Coriolis sine latitude values in s^-1
    dx (float or int): float or integer of U and V grispacing in meters
    ---------------------
    returns:
        numpy.ndarray of absolute vorticity values s^-1 same shape as U and V

    """
    assert U.shape == V.shape, 'Arrays are different shapes. They must be the same shape.'
    return wrf_vort(U, V, dx) + F
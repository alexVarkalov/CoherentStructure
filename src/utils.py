import Tkinter
import tkFileDialog
import ntpath
import numpy as np


def path_leaf(path):
    """ Take file name from path """
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def check_filename_extension(path, filename_extension):
    if path.split('.')[1] == filename_extension:
        return True
    else:
        return False


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


def create_module_matrix(X, Y):
    """ Create Matrix of polar radius """
    sq_X = np.zeros(X.shape)
    sq_Y = np.zeros(Y.shape)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            sq_X[i][j] = X[i][j] ** 2
    for i in range(Y.shape[0]):
        for j in range(Y.shape[1]):
            sq_Y[i][j] = Y[i][j] ** 2
    Z = np.zeros((X.shape[0], X.shape[1]))
    for i in range(Z.shape[0]):
        for j in range(Z.shape[1]):
            Z[i][j] = np.sqrt(sq_X[i][j] + sq_Y[i][j])
    return Z


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


def get_divide_method():
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
        else:
            print('Wrong Input')
            continue


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


def get_sin_cos_by_points(pointA, pointB):
    if pointA[0] - pointB[0] == 0:
        sin_alpha = 1
        cos_alpha = 10 ** 13
    elif pointA[1] - pointB[1] == 0:
        sin_alpha = 10 ** 13
        cos_alpha = 1
    else:
        sin_alpha = (pointB[1] - pointA[1]) / np.sqrt((pointB[0] - pointA[0]) ** 2 + (pointB[1] - pointA[1]) ** 2)
        cos_alpha = np.sqrt(1 - sin_alpha ** 2)
    return sin_alpha, cos_alpha


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
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


def get_hour_from_nc_file(data):
    return str(arrow.get(''.join(data['nc_file'].variables['Times'][0]), 'YYYY-M-D_HH:mm:ss').time().hour).zfill(2)


def bresenham_line((x, y), (x2, y2)):
    """Brensenham line algorithm"""
    steep = 0
    coords = []
    dx = abs(x2 - x)
    sx = 1 if (x2 - x) > 0 else -1
    dy = abs(y2 - y)
    sy = 1 if (y2 - y) > 0 else -1

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


def create_angle_matrix(x, y):
    angle = np.zeros((x.shape[0], x.shape[1]))
    for i in range(angle.shape[0]):
        for j in range(angle.shape[1]):
            degree = np.degrees(np.arctan(y[i][j] / x[i][j]))
            angle[i][j] = degree

    return angle


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


def save_plot(data, img_type):
    divide_method = data.get('divide_method')
    work_folder = data.get('work_folder')
    hour = data.get('hour')
    height = data.get('height')
    file_name = data.get('file_name')
    plot = ''
    if divide_method == 'hours':
        if not os.path.exists('{}/hours'.format(work_folder)):
            os.makedirs('{}/hours'.format(work_folder))
        if not os.path.exists('{}/hours/{}'.format(work_folder, hour)):
            os.makedirs('{}/hours/{}'.format(work_folder, hour))
        # plt.title('{}/hours/{}/height#{}-{}'.format(work_folder, hour, str(height).zfill(2), img_type))
        plt.title('{}/height#{}-{}'.format(file_name, str(height).zfill(2), img_type))
        plot = '{}/hours/{}/{}-{}.png'.format(work_folder, hour, str(height).zfill(2), img_type)
        plt.savefig(plot)
    elif divide_method == 'heights':
        if not os.path.exists('{}/heights'.format(work_folder)):
            os.makedirs('{}/heights'.format(work_folder))
        if not os.path.exists('{}/heights/{}'.format(work_folder, str(height).zfill(2))):
            os.makedirs('{}/heights/{}'.format(work_folder, str(height).zfill(2)))
        plt.title('{}/height#{}-{}'.format(file_name, str(height).zfill(2), img_type))
        # plt.title('{}/heights/{}/hour-{}-{}'.format(work_folder, str(height).zfill(2), hour, img_type))
        plot = '{}/heights/{}/{}-{}.png'.format(work_folder, str(height).zfill(2), hour, img_type)
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
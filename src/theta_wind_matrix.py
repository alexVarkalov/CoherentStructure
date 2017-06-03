import arrow
import numpy as np
import netCDF4 as nc4
import sys

from utils import get_file_paths


def create_theta_wind_matrix(nc_file):
    start_time = arrow.now().timestamp
    u = nc_file.variables['U'][0]
    v = nc_file.variables['V'][0]
    w = nc_file.variables['W'][0]
    # TODO
    u_theta = np.zeros((27, 249, 249))
    v_theta = np.zeros((27, 249, 249))
    w_theta = np.zeros((27, 249, 249))

    start_time_u = arrow.now().timestamp
    for k in range(u.shape[0]):
        for j in range(u.shape[1]):
            for i in range(u.shape[2] - 1):
                u_theta[k][j][i] = 0.5*(u[k][j][i] + u[k][j][i+1])
    end_time_u = arrow.now().timestamp
    delta_time_u = end_time_u - start_time_u
    print('U theta matrix have been created by {} seconds'.format(delta_time_u))

    start_time_v = arrow.now().timestamp
    for k in range(v.shape[0]):
        for j in range(v.shape[1] - 1):
            for i in range(v.shape[2]):
                v_theta[k][j][i] = 0.5 * (v[k][j][i] + v[k][j + 1][i])
    end_time_v = arrow.now().timestamp
    delta_time_v = end_time_v - start_time_v
    print('V theta matrix have been created by {} seconds'.format(delta_time_v))

    start_time_w = arrow.now().timestamp
    for k in range(w.shape[0] - 1):
        for j in range(w.shape[1]):
            for i in range(w.shape[2] - 1):
                w_theta[k][j][i] = 0.5 * (w[k][j][i] + w[k + 1][j][i])
    end_time_w = arrow.now().timestamp
    delta_time_w = end_time_w - start_time_w
    print('W theta matrix have been created by {} seconds'.format(delta_time_w))

    end_time = arrow.now().timestamp
    delta_time = end_time - start_time
    print('All theta matrix have been created by {} seconds'.format(delta_time))
    return u_theta, v_theta, w_theta


def get_theta_wind_matrix(path):
    file_folder = path.split('.')[0]
    try:
        u_theta = np.load('{}/{}'.format(file_folder, 'u_theta.npy'))
        v_theta = np.load('{}/{}'.format(file_folder, 'v_theta.npy'))
        w_theta = np.load('{}/{}'.format(file_folder, 'w_theta.npy'))
    except IOError:
        print('Theta matrix for {} does not exists. Try to use theta_wind_matrix script'.format(file_folder))
        return None, None, None
    return u_theta, v_theta, w_theta


def save_theta_wind_matrix(path, u_theta, v_theta, w_theta):
    file_folder = path.split('.')[0]
    np.save('{}/{}'.format(file_folder, 'u_theta.npy'), u_theta)
    np.save('{}/{}'.format(file_folder, 'v_theta.npy'), v_theta)
    np.save('{}/{}'.format(file_folder, 'w_theta.npy'), w_theta)


def theta_wind_matrix(paths=None):
    if not paths:
        paths = get_file_paths('nc')
    for path in paths:
        print path
        nc_file = nc4.Dataset(path, mode='r')
        u_theta, v_theta, w_theta = create_theta_wind_matrix(nc_file=nc_file)
        save_theta_wind_matrix(path=path, u_theta=u_theta, v_theta=v_theta, w_theta=w_theta)


if __name__ == '__main__':
    theta_wind_matrix()

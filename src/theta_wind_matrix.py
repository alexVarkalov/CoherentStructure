import os
import arrow
import numpy as np


def create_theta_wind_matrix(nc_file):
    start_time = arrow.now().timestamp
    U = nc_file.variables['U'][0]
    V = nc_file.variables['V'][0]
    W = nc_file.variables['W'][0]
    u_theta = np.zeros((27, 249, 249))
    v_theta = np.zeros((27, 249, 249))
    w_theta = np.zeros((27, 249, 249))

    for k in range(U.shape[0]):
        for j in range(U.shape[1]):
            for i in range(U.shape[2] - 1):
                u_theta[k][j][i] = 0.5*(U[k][j][i] + U[k][j][i+1])

    for k in range(V.shape[0]):
        for j in range(V.shape[1] - 1):
            for i in range(V.shape[2]):
                v_theta[k][j][i] = 0.5 * (V[k][j][i] + V[k][j + 1][i])

    for k in range(W.shape[0] - 1):
        for j in range(W.shape[1]):
            for i in range(W.shape[2] - 1):
                w_theta[k][j][i] = 0.5 * (W[k][j][i] + W[k + 1][j][i])
    end_time = arrow.now().timestamp
    delta_time = end_time - start_time
    return u_theta, v_theta, w_theta


def get_theta_wind_matrix(path, nc_file, recreate=False):
    file_folder = path.split('.')[0]
    try:
        if recreate:
            raise IOError
        u_theta = np.load('{}/{}'.format(file_folder, 'u_theta.npy'))
        v_theta = np.load('{}/{}'.format(file_folder, 'v_theta.npy'))
        w_theta = np.load('{}/{}'.format(file_folder, 'w_theta.npy'))
    except IOError:
        if not os.path.exists(file_folder):
            os.makedirs(file_folder)
        u_theta, v_theta, w_theta = create_theta_wind_matrix(nc_file)
        np.save('{}/{}'.format(file_folder, 'u_theta.npy'), u_theta)
        np.save('{}/{}'.format(file_folder, 'v_theta.npy'), v_theta)
        np.save('{}/{}'.format(file_folder, 'w_theta.npy'), w_theta)
    return u_theta, v_theta, w_theta

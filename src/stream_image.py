import os
import arrow
import netCDF4 as nc4
import numpy as np
import matplotlib.pyplot as plt
import Tkinter
import tkFileDialog
import ntpath
from matplotlib import cm


def path_leaf(path):
    """ Take file name from path """
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


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
    Z = np.zeros((249, 249))
    for i in range(Z.shape[0]):
        for j in range(Z.shape[1]):
            Z[i][j] = np.sqrt(sq_X[i][j] + sq_Y[i][j])
    return Z


def func(step, high, paths):
    folder = 'Streams{}'.format(arrow.utcnow().timestamp)
    os.makedirs(folder)
    with open('{}/main_log_{}.txt'.format(folder, arrow.utcnow().timestamp), 'w') as log:
        start_time = arrow.now()
        log.writelines('***********************\n')
        log.writelines('Start Time - {}\n'.format(start_time))
        log.writelines('***********************\n')
        log.writelines('step = {} \n'.format(step))
        log.writelines('high = {} \n'.format(high))

        for path in paths:
            file_start_time = arrow.now()
            file_name = path_leaf(path)
            if file_name.split('.')[1] != 'nc':
                print file_name.split('.')[1]
                print '{} wrong type!!!'.format(file_name)
                continue
            log.writelines('-----------------------\n')
            log.writelines('File {} Start Time - {}\n\n'.format(file_name, file_start_time))
            log.writelines('-----------------------\n')
            print 'File {} Start Time - {}\n'.format(file_name, file_start_time)
            file_folder = file_name.split('.')[0]
            os.makedirs('{}/{}'.format(folder, file_folder))
            file_start_time = arrow.now()
            log.writelines('{} Start Time - {}\n'.format(file_name, file_start_time))
            print '{} Start Time - {}'.format(file_name, file_start_time)
            wrf_file = nc4.Dataset(path, mode='r')
            if high == 0:
                highs = wrf_file.variables['U'].shape[1]
                print '$$$$$$$$$$$$'
                print high
                print '$$$$$$$$$$$$'
            else:
                highs = high
            for h in range(highs):
                high_start_time = arrow.now()
                log.writelines('High #{} Start Time - {}\n'.format(h, high_start_time))
                print 'High #{} Start Time - {}'.format(h, high_start_time)
                x_wind = wrf_file.variables['U']
                y_wind = wrf_file.variables['V']
                x_wind0 = x_wind[0][h]
                y_wind0 = y_wind[0][h]
                X, Y = np.meshgrid(np.arange(0, 249, 1), np.arange(0, 249, 1))
                U = x_wind0
                V = y_wind0
                Z = create_module_matrix(U, V)
                plt.figure(figsize=(10, 10), facecolor='w', edgecolor='r')
                plt.streamplot(
                    X[::step, ::step],
                    Y[::step, ::step],
                    U[::step, ::step],
                    V[::step, ::step],
                    color=Z[::step, ::step],
                    cmap=cm.cool,
                    linewidth=1.0,
                    arrowstyle='->',
                    arrowsize=1.5,
                )
                plt.colorbar()
                # plt.plot(X[::step, ::step], Y[::step, ::step], 'k.')
                plt.axis([-10, 260, -10, 260])
                plt.title('{}/high{}.png'.format(folder, h))
                plt.savefig('{}/{}/high{}.png'.format(folder, file_folder, h))
                plt.close()
                print ('{}/{}/high{}.png is created'.format(folder, file_folder, h))
                high_end_time = arrow.now()
                high_delta = high_end_time - high_start_time
                print 'High #{} Delta - {}\n'.format(h, high_delta)
                log.writelines('High End Time - {}\n'.format(high_end_time))
                log.writelines('High Delta - {}\n\n'.format(high_delta))
            file_end_time = arrow.now()
            log.writelines('-----------------------\n')
            log.writelines('File {} End Time - {}\n\n'.format(file_name, file_end_time))
            print 'File {} End Time - {}\n'.format(file_name, file_end_time)
            file_delta = file_end_time - file_start_time
            log.writelines('File {} Delta - {}\n'.format(file_name, file_delta))
            log.writelines('-----------------------\n')
            print 'High {} Delta - {}\n'.format(file_name, file_delta)
        end_time = arrow.now()
        main_delta = end_time - start_time
        print 'Main Delta - {}'.format(main_delta)
        log.writelines('***********************\n')
        log.writelines('End Time - {}\n'.format(end_time))
        log.writelines('Main Delta - {}\n'.format(main_delta))
        log.writelines('***********************\n')


def main():
    print 'Please, select a file(s) .nc'
    root = Tkinter.Tk()
    paths = tkFileDialog.askopenfilenames(parent=root, title='Choose a file')
    print root.tk.splitlist(paths)
    step = input('Step? ')
    high = input('High? 0 for all highs: ')
    print ""

    func(step=step, high=high, paths=paths)

main()
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

import Tkinter
import tkFileDialog

import ntpath


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




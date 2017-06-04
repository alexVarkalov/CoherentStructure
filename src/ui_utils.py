import Tkinter
import tkFileDialog
import sys
from utils import check_filename_extension, path_leaf


def get_file_paths(filename_extension):
    if 'demo' in sys.argv:
        from settings import DEFAULT_PATHS
        return DEFAULT_PATHS

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


def get_heights(max_level):
    if 'demo' in sys.argv:
        from settings import DEFAULT_START_HEIGHT, DEFAULT_END_HEIGHT
        return DEFAULT_START_HEIGHT, DEFAULT_END_HEIGHT

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
    if 'demo' in sys.argv:
        from settings import DEFAULT_DIVIDE_METHOD
        return DEFAULT_DIVIDE_METHOD

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
    # NOT IN USE
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
            point_a = raw_input('point A. Min - (0,0). Max({},{}): '.format(max_value - 1, max_value - 1)).split(', ')
            if len(point_a) > 2:
                print('Wrong Input')
                continue
            else:
                point_a[0] = int(point_a[0])
                point_a[1] = int(point_a[1])
                if point_a[0] >= max_value or point_a[1] >= max_value:
                    print('Wrong Input')
                    continue
            point_b = raw_input('point B. Min - (0,0). Max({},{}): '.format(max_value - 1, max_value - 1)).split(', ')
            if len(point_b) > 2:
                print('Wrong Input')
                continue
            else:
                point_b[0] = int(point_b[0])
                point_b[1] = int(point_b[1])
                if point_b[0] >= max_value or point_b[1] >= max_value:
                    print('Wrong Input')
                    continue
            if point_b[0] < point_a[0]:
                point_a, point_b = point_b, point_a
            return point_a, point_b
        except Exception:
            print('Wrong Input')
            continue

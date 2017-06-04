DEFAULT_PATHS = (
        '/home/varalex/University/nc/wrfout_d01_2013-05-22_01.nc',
        # '/home/varalex/University/nc/wrfout_d01_2013-05-22_02.nc',
        # '/home/varalex/University/nc/wrfout_d01_2013-05-22_03.nc',
        # '/home/varalex/University/nc/wrfout_d01_2013-05-22_04.nc',
        # '/home/varalex/University/nc/wrfout_d01_2013-05-22_05.nc',
        # '/home/varalex/University/nc/wrfout_d01_2013-05-22_06.nc',
        # '/home/varalex/University/nc/wrfout_d01_2013-05-22_07.nc',
        # '/home/varalex/University/nc/wrfout_d01_2013-05-22_08.nc',
        # '/home/varalex/University/nc/wrfout_d01_2013-05-22_09.nc',
        # '/home/varalex/University/nc/wrfout_d01_2013-05-22_10.nc',
    )

DEFAULT_START_HEIGHT = 6
DEFAULT_END_HEIGHT = 7

DEFAULT_DIVIDE_METHOD = 'heights'
# DEFAULT_DIVIDE_METHOD = 'hours'

DEFAULT_STEP = 1


DEFAULT_HORIZONTAL_HISTOGRAM_SETTINGS = {
        'bins': 30,
        'x_lim_left': 0,
        'x_lim_right': 50,
        'y_lim_down': 0,
        'y_lim_up': 0.3,
}

DEFAULT_VERTICAL_HISTOGRAM_SETTINGS = {
        'bins': 100,
        'x_lim_left': -0.5,
        'x_lim_right': 0.5,
        'y_lim_down': 0,
        'y_lim_up': 30,
}

DEFAULT_ANGLE_HISTOGRAM_SETTINGS = {
        'bins': 60,
        # 'bins': 100,
        'x_lim_left': -90,
        'x_lim_right': 90,
        'y_lim_down': 0,
        'y_lim_up': 0.02,
}

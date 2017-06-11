DEFAULT_PATHS = (
        # '/home/varalex/University/nc/Package1/wrfout_d01_2013-05-22_01.nc',
        # '/home/varalex/University/nc/Package1/wrfout_d01_2013-05-22_02.nc',
        # '/home/varalex/University/nc/Package1/wrfout_d01_2013-05-22_03.nc',
        '/home/varalex/University/nc/Package2/wrfout_d01_2012-08-14_12.nc',
        # '/home/varalex/University/nc/Package2/wrfout_d01_2012-08-14_05.nc',
        # '/home/varalex/University/nc/Package2/wrfout_d01_2012-08-14_06.nc',
        # '/home/varalex/University/nc/Package2/wrfout_d01_2012-08-14_07.nc',
        # '/home/varalex/University/nc/Package2/wrfout_d01_2012-08-14_18.nc',
        # '/home/varalex/University/nc/Package2/wrfout_d01_2012-08-14_02.nc',
        # '/home/varalex/University/nc/Package2/wrfout_d01_2012-08-14_03.nc',
        # '/home/varalex/University/nc/Package2/wrfout_d01_2012-08-14_04.nc',
        # '/home/varalex/University/nc/Package2/wrfout_d01_2012-08-14_05.nc',
        # '/home/varalex/University/nc/Package2/wrfout_d01_2012-08-14_06.nc',
        # '/media/varalex/White/wrfout_d01_2012-08-14_01_00_00.nc',
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

DEFAULT_START_HEIGHT = 15
DEFAULT_END_HEIGHT = 16

DEFAULT_DIVIDE_METHOD = 'heights'
# DEFAULT_DIVIDE_METHOD = 'hours'

DEFAULT_STEP = 1


DEFAULT_HORIZONTAL_HISTOGRAM_SETTINGS = {
        'bins': 30,
        'speed_down': 0,
        'speed_up': 45,
        'probability_down': 0,
        'probability_up': 0.4,
}

DEFAULT_VERTICAL_HISTOGRAM_SETTINGS = {
        'bins': 100,
        'speed_down': -0.5,
        'speed_up': 0.5,
        'probability_down': 0,
        'probability_up': 30,
}

DEFAULT_ANGLE_HISTOGRAM_SETTINGS = {
        'bins': 60,
        # 'bins': 100,
        'min_angle': -90,
        'max_angle': 90,
        'probability_down': 0,
        'probability_up': 0.02,
}


DEFAULT_HORIZONTAL_CUT_SETTINGS = {
        'horizontal_speed_down': 0,
        'horizontal_speed_up': 45,
        'vertical_speed_down': -0.5,
        'vertical_speed_up': 0.5,
}

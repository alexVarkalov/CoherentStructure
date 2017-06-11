import numpy as np
import arrow
import ntpath
import os
import sys

from PIL import Image

from ui_utils import get_file_paths


def save_image(buffer_data, filtered_data, code, start_time):
    if not os.path.exists('{}/{}'.format(buffer_data.get('path'), code)):
        os.makedirs('{}/{}'.format(buffer_data.get('path'), code))
    new_image = Image.fromarray(filtered_data, mode='RGB')
    new_image.save('{}/{}/{}'.format(buffer_data.get('path'), code, buffer_data.get('file_name')))
    end_time = arrow.now()
    print('{} image for {} is ready by {} '.format(code, buffer_data.get('file_name'), end_time - start_time))


def red_impurities(data, buffer_data):
    code = 'red'
    start_time = arrow.now()
    red_color = (250, 100, 10)
    width, height = buffer_data.get('width'), buffer_data.get('height')
    filtered_data = data.copy()
    for i in range(height):
        for j in range(width):
            red, green, blue = data[i][j]
            if red > red_color[0] and green < red_color[1] and blue < red_color[2]:
                pass
            else:
                filtered_data[i][j] = (255, 255, 255)
    save_image(buffer_data=buffer_data, filtered_data=filtered_data, code=code, start_time=start_time)


def cream_impurities(data, buffer_data):
    code = 'cream'
    cream_color = (250, 160, 100)
    start_time = arrow.now()
    width, height = buffer_data.get('width'), buffer_data.get('height')
    filtered_data = data.copy()
    for i in range(height):
        for j in range(width):
            red, green, blue = data[i][j]
            if red > cream_color[0] and green < cream_color[1] and blue < cream_color[2]:
                pass
            else:
                filtered_data[i][j] = (255, 255, 255)
    save_image(buffer_data=buffer_data, filtered_data=filtered_data, code=code, start_time=start_time)


def dark_yellow_impurities(data, buffer_data):
    code = 'dark yellow'
    dark_yellow_color = (250, 210, 10)
    start_time = arrow.now()
    width, height = buffer_data.get('width'), buffer_data.get('height')
    filtered_data = data.copy()
    for i in range(height):
        for j in range(width):
            red, green, blue = data[i][j]
            if red > dark_yellow_color[0] and green < dark_yellow_color[1] and blue < dark_yellow_color[2]:
                pass
            else:
                filtered_data[i][j] = (255, 255, 255)
    save_image(buffer_data=buffer_data, filtered_data=filtered_data, code=code, start_time=start_time)


def yellow_impurities(data, buffer_data):
    code = 'yellow'
    yellow_color = (250, 250, 10)
    start_time = arrow.now()
    width, height = buffer_data.get('width'), buffer_data.get('height')
    filtered_data = data.copy()
    for i in range(height):
        for j in range(width):
            red, green, blue = data[i][j]
            if red > yellow_color[0] and green > yellow_color[1] and blue < yellow_color[2]:
                pass
            else:
                filtered_data[i][j] = (255, 255, 255)
    save_image(buffer_data=buffer_data, filtered_data=filtered_data, code=code, start_time=start_time)


def green_impurities(data, buffer_data):
    code = 'green'
    green_color = (50, 250, 50)
    start_time = arrow.now()
    width, height = buffer_data.get('width'), buffer_data.get('height')
    filtered_data = data.copy()
    for i in range(height):
        for j in range(width):
            red, green, blue = data[i][j]
            if red < green_color[0] and green > green_color[1] and blue < green_color[2]:
                pass
            else:
                filtered_data[i][j] = (255, 255, 255)
    save_image(buffer_data=buffer_data, filtered_data=filtered_data, code=code, start_time=start_time)


def light_blue_impurities(data, buffer_data):
    code = 'light blue'
    light_blue_color = (160, 250, 250)
    start_time = arrow.now()
    width, height = buffer_data.get('width'), buffer_data.get('height')
    filtered_data = data.copy()
    for i in range(height):
        for j in range(width):
            red, green, blue = data[i][j]
            if red < light_blue_color[0] and green > light_blue_color[1] and blue > light_blue_color[2]:
                pass
            else:
                filtered_data[i][j] = (255, 255, 255)
    save_image(buffer_data=buffer_data, filtered_data=filtered_data, code=code, start_time=start_time)


def blue_impurities(data, buffer_data):
    code = 'blue'
    blue_color = (130, 200, 250)
    start_time = arrow.now()
    width, height = buffer_data.get('width'), buffer_data.get('height')
    filtered_data = data.copy()
    for i in range(height):
        for j in range(width):
            red, green, blue = data[i][j]
            if red < blue_color[0] and green > blue_color[1] and blue > blue_color[2]:
                pass
            else:
                filtered_data[i][j] = (255, 255, 255)
    save_image(buffer_data=buffer_data, filtered_data=filtered_data, code=code, start_time=start_time)


def dark_blue_impurities(data, buffer_data):
    code = 'dark blue'
    dark_blue_color = (100, 160, 250)
    start_time = arrow.now()
    width, height = buffer_data.get('width'), buffer_data.get('height')
    filtered_data = data.copy()
    for i in range(height):
        for j in range(width):
            red, green, blue = data[i][j]
            if red < dark_blue_color[0] and green < dark_blue_color[1] and blue < dark_blue_color[2]:
                pass
            else:
                filtered_data[i][j] = (255, 255, 255)
    save_image(buffer_data=buffer_data, filtered_data=filtered_data, code=code, start_time=start_time)


def hot_impurities(data, buffer_data):
    code = 'hot'
    red_color = (250, 100, 10)
    cream_color = (250, 160, 100)
    dark_yellow_color = (250, 210, 10)
    yellow_color = (250, 250, 10)

    start_time = arrow.now()
    width, height = buffer_data.get('width'), buffer_data.get('height')
    filtered_data = data.copy()
    for i in range(height):
        for j in range(width):
            red, green, blue = data[i][j]
            if (red > red_color[0] and green < red_color[1] and blue < red_color[2])\
                    or (red > cream_color[0] and green < cream_color[1] and blue < cream_color[2]) \
                    or (red > dark_yellow_color[0] and green < dark_yellow_color[1] and blue < dark_yellow_color[2]) \
                    or (red > yellow_color[0] and green > yellow_color[1] and blue < yellow_color[2]):
                pass
            else:
                filtered_data[i][j] = (255, 255, 255)
    save_image(buffer_data=buffer_data, filtered_data=filtered_data, code=code, start_time=start_time)


def cold_impurities(data, buffer_data):
    code = 'cold'
    light_blue_color = (160, 250, 250)
    blue_color = (130, 200, 250)
    dark_blue_color = (100, 160, 250)
    start_time = arrow.now()
    width, height = buffer_data.get('width'), buffer_data.get('height')
    filtered_data = data.copy()
    for i in range(height):
        for j in range(width):
            red, green, blue = data[i][j]
            if (red < light_blue_color[0] and green > light_blue_color[1] and blue > light_blue_color[2])\
                    or (red < blue_color[0] and green > blue_color[1] and blue > blue_color[2])\
                    or (red < dark_blue_color[0] and green < dark_blue_color[1] and blue < dark_blue_color[2]):
                pass
            else:
                filtered_data[i][j] = (255, 255, 255)
    save_image(buffer_data=buffer_data, filtered_data=filtered_data, code=code, start_time=start_time)


def impurities_separation(file_path):
    path, file_name = ntpath.split(file_path)
    image = Image.open('{}/{}'.format(path, file_name))
    cropped_image = image.crop((40, 70, 900, 690))
    converted_image = cropped_image.convert('RGB')
    data = np.array(converted_image)
    width, height = converted_image.size
    buffer_data = {
        'width': width,
        'height': height,
        'path': path,
        'file_name': file_name
    }
    if 'detail' in sys.argv:
        red_impurities(data=data, buffer_data=buffer_data)
        cream_impurities(data=data, buffer_data=buffer_data)
        dark_yellow_impurities(data=data, buffer_data=buffer_data)
        yellow_impurities(data=data, buffer_data=buffer_data)
        green_impurities(data=data, buffer_data=buffer_data)
        light_blue_impurities(data=data, buffer_data=buffer_data)
        blue_impurities(data=data, buffer_data=buffer_data)
        dark_blue_impurities(data=data, buffer_data=buffer_data)
    hot_impurities(data=data, buffer_data=buffer_data)
    cold_impurities(data=data, buffer_data=buffer_data)


def anomalies_of_impurities():
    start_time = arrow.now()
    paths = get_file_paths('gif')
    for file_path in paths:
        impurities_separation(file_path=file_path)
    end_time = arrow.now()
    print('Anomalies of impurities working time - {}'.format(end_time - start_time))


if __name__ == '__main__':
    anomalies_of_impurities()

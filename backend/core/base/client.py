# -*- coding: utf-8 -*-
import copy

import cv2
import numpy
from PIL import Image
from PIL.BmpImagePlugin import BmpImageFile
from PIL.PngImagePlugin import PngImageFile

from backend.core.lib import pic


class ClientApi:

    def __init__(self, url):
        self._url = url

    def get_cv2_image(self, image, grey=False):
        if type(image) is str:
            image = cv2.imread(image)
        # elif isinstance(image, BmpImageFile) or isinstance(image, Image):
        elif type(image) is Image.Image or type(image) in [BmpImageFile, PngImageFile]:
            image = cv2.cvtColor(numpy.asarray(image), cv2.COLOR_RGB2BGR)
        if grey:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image

    def find_image(self, image):
        pass

    @classmethod
    def show_image(cls, image, delay=0):
        cv2.imshow('image', image)
        cv2.waitKey(delay)

    @classmethod
    def draw_rect(cls, image, rect, **kwargs):
        """Draw a rectangle on image

        Args:
            image: cv image
            rect: rectangle
            **kwargs:
                color: color of border line
                show: select whether display the image
                delay: the time the image is displayed
        Returns:
            None

        References:
            cv2.rectangle(ip.full_screen, (610, 57),(766, 109), (255, 0, 0))
        """
        color = kwargs.get('color', (255, 0, 0))
        show = kwargs.get('show', True)
        delay = kwargs.get('delay', 0)

        cv2.rectangle(image, (rect.lt_pt.x, rect.lt_pt.y), (rect.rb_pt.x, rect.rb_pt.y), color)
        if show:
            cls.show_image(image, delay)

    @classmethod
    def crop_rect(cls, image, rect, **kwargs):
        show = kwargs.get('show', False)
        delay = kwargs.get('delay', 0)

        crop_img = image[rect.lt_pt.y:rect.rb_pt.y, rect.lt_pt.x:rect.rb_pt.x]
        if show:
            cls.show_image(crop_img, delay)
        return crop_img


class Point:

    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def is_valid(self):
        return self.x >= 0 and self.y >= 0

    def offset(self, point):
        new_point = copy.deepcopy(point)
        print('new_point1:', new_point)
        new_point.x += point.x
        new_point.y += point.y
        print('new_point2:', new_point)
        return new_point


class Rectangle:

    def __init__(self, lt_pt, rb_pt):
        """ Rectangle

        Args:
            lt_pt: left top point
            rb_pt: right bottom point
        """
        self.lt_pt = lt_pt
        self.rb_pt = rb_pt

    def offset(self, point):
        new_rect = copy.deepcopy(self)
        new_rect.left_point = self.lt_pt.offset(point)
        new_rect.right_point = self.rb_pt.offset(point)
        return new_rect


def demo():
    """Demo

    References:
        [Contours](https://docs.opencv.org/4.2.0/d4/d73/tutorial_py_contours_begin.html)

    Returns:

    """
    # 二值化图像
    import cv2 as cv
    api = ClientApi('')
    frame = api.get_cv2_image(pic.TABLE_MODLE_ALLl_APPS_FULLSCREEN)
    print("start to detect lines...\n")
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
    print('ret:', ret)
    print('binary:', binary)
    api.show_image(binary)
    # api.show_image(gray)

    contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # cv.drawContours(img, contours, -1, (0, 255, 0), 1)
    # cnt = contours[4]

def demo2():
    pass


if __name__ == '__main__':
    demo()

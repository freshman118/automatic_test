# -*- coding: utf-8 -*-
import copy

from PIL import Image
from PIL.BmpImagePlugin import BmpImageFile
from PIL.PngImagePlugin import PngImageFile
import cv2
import numpy
from logzero import logger

from backend.core.lib import pic


class ImageProcess:

    def __init__(self, url, full_screen):
        self._url = url
        self._full_screen = self.transfer2cv(full_screen)

    # """ 图片格式转换"""
    def transfer2cv(self, image, grey=False):
        """ 图片转换为OpenCV格式"""
        if type(image) is str:
            image = cv2.imread(image)
        elif type(image) is Image.Image or type(image) in [BmpImageFile, PngImageFile]:
            image = cv2.cvtColor(numpy.asarray(image), cv2.COLOR_RGB2BGR)
        if grey:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        return image

    # """ 模板匹配"""
    def templ_single_match(self, templ, match_rate=0.75, draw=False):
        """ 模板单次匹配

        Args:
            image: 母图片
            templ: 模板图片

        References:
            [模板匹配](https://www.jianshu.com/p/c20adfa72733)

        Returns:
            (Point(lt_pt[0], lt_pt[1]), max_val): a tuple consisted of (left top point, max match rate)
        """
        # 读取模板图
        templ = self.transfer2cv(templ)
        h, w = templ.shape[:2]
        logger.debug('width: {}, height: {}'.format(w, h))

        # 模板匹配，获取匹配度、坐标
        matrix = cv2.matchTemplate(self._full_screen, templ, cv2.TM_CCOEFF_NORMED)
        max_val, max_loc = cv2.minMaxLoc(matrix)[1:4:2]
        logger.debug('max_val: {}, max_loc: {}'.format(max_val, max_loc))
        if max_val > match_rate:
            lt_pt = max_loc  # 左上角坐标点
            rb_pt = (lt_pt[0] + w, lt_pt[1] + h)  # 右下角坐标点
            logger.debug('lt_pt: {}'.format(lt_pt))
            logger.debug('rb_pt: {}'.format(rb_pt))

            # 画出匹配区域
            if draw:
                cv2.rectangle(self._full_screen, lt_pt, rb_pt, (0, 0, 255))
                cv2.imshow('template', templ)
                cv2.imshow('image', self._full_screen)
                cv2.waitKey(0)
        else:
            raise Exception('Template matching failed')

        return (Point(lt_pt[0], lt_pt[1]), max_val)

    def templ_multi_match(self, templ, match_rate=0.75, search_area=None, debug=False):
        """ 模板多次匹配

        Args:
            templ:
            match_rate:
            search_area:
            debug

        Returns:
            (len(ce_pts), ce_pts)
        """
        # 读取模板图
        templ = self.transfer2cv(templ)  # 模板图
        image = self._full_screen  # 母图
        h, w = templ.shape[:2]
        logger.debug('width: {}, height: {}'.format(w, h))
        # 处理匹配区域
        if search_area != None:
            ((lx_search_area, ly_search_are), (rx_search_area, ry_search_area)) = search_area
            image = self._full_screen[ly_search_are:ry_search_area, lx_search_area:rx_search_area]  # 截取指定矩形区域作为匹配区域

        # 标准相关模板匹配
        matrix = cv2.matchTemplate(image, templ, cv2.TM_CCOEFF_NORMED)

        # 匹配度大于0.75得图片
        loc = numpy.where(matrix >= match_rate)
        lf_pts = zip(*loc[::-1])  # 模板左上角坐标
        # （78, 89, 89） （12， 78， 23）
        # （89， 89， 78） （23， 78， 12）
        # (89, 23), （89， 78）， （78， 12）
        ce_pts = []  # 模板中心坐标列表
        for lf_pt in lf_pts:
            # 匹配区域为全屏
            if search_area == None:
                ce_pt = (lf_pt[0] + w / 2, lf_pt[1] + h / 2)  # 模板右下角坐标
                ce_pts.append(ce_pt)
                if debug:
                    rb_pt = (lf_pt[0] + w, lf_pt[1] + h)  # 模板右下角坐标
                    cv2.rectangle(self._full_screen, lf_pt, rb_pt, (0, 0, 255), 2)
                    cv2.imshow('template', templ)
                    cv2.imshow('image', image)
                    cv2.waitKey(0)
                print('Full screen:', len(ce_pts), ce_pts)
            # 指定匹配区域
            else:
                ce_pt = (lf_pt[0] + w / 2 + search_area[0][0], lf_pt[1] + h / 2 + search_area[0][1])  # 模板右下角坐标
                ce_pts.append(ce_pt)
                if debug:
                    rb_pt = (lf_pt[0] + w + search_area[0][0], lf_pt[1] + h + search_area[0][1])  # 模板右下角坐标
                    cv2.rectangle(self._full_screen, lf_pt, rb_pt, (0, 0, 255), 2)
                    cv2.imshow('template', templ)
                    cv2.imshow('image', image)
                    cv2.waitKey(0)
                # print('Search area:', len(ce_pts), ce_pts)
            return (len(ce_pts), ce_pts)

    def offset_image(self, image: str, distance: int, direction: str = 'right', draw=False):
        """ Shift the image a certain distance in a certain direction
        """
        if not isinstance(distance, int):
            raise ValueError("The type of distance must be int.")
        if direction not in ['down', 'right', 'left', 'up']:
            raise ValueError("The distance must be selected from ['down', 'right', 'left', 'up']")

        for scale in [[1, 1]][0]:
            distance = distance * scale
            # Get point by looking for image and size of image
            lt_pt = self.templ_single_match(image)[0]
            if not lt_pt.is_valid():
                continue
            else:
                status = True

            h, w = self.transfer2cv(image).shape[0:2]
            rt_pt = Point(lt_pt.x + w, lt_pt.y)  # Right top point
            rb_pt = Point(lt_pt.x + w, lt_pt.y + h)  # Right bottom point
            lb_pt = Point(lt_pt.x, lt_pt.y + h)  # Left bottom point

            rect_dict = {
                'right': Rectangle(rt_pt, Point(rb_pt.x + distance, rb_pt.y)),
                'down': Rectangle(lb_pt, Point(rb_pt.x, rb_pt.y + distance)),
                'left': Rectangle(Point(lt_pt.x - distance, lt_pt.y), lb_pt),
                'up': Rectangle(lt_pt, Point(rt_pt.x, rt_pt.y - distance)),
            }

            if draw:
                self.draw_rect(self._full_screen, rect_dict[direction], show=True)
            if status:
                break

            return self.crop_rect(self._full_screen, rect_dict[direction])

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
            True
        """
        color = kwargs.get('color', (255, 0, 0))
        show = kwargs.get('show', True)
        delay = kwargs.get('delay', 0)

        cv2.rectangle(image, (rect.lt_pt.x, rect.lt_pt.y), (rect.rb_pt.x, rect.rb_pt.y), color)
        if show:
            cls.show_image(image, delay)

        return True

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
    pass
    # # 二值化图像
    # import cv2 as cv
    # api = ClientApi('')
    # frame = self.get_cv2_image(pic.TABLE_MODLE_ALLl_APPS_FULLSCREEN)
    # print("start to detect lines...\n")
    # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
    # print('ret:', ret)
    # print('binary:', binary)
    # self.show_image(binary)
    # # self.show_image(gray)

    # contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # cv.drawContours(img, contours, -1, (0, 255, 0), 1)
    # cnt = contours[4]

    # session = requests.Session()
    # print(session.post('http://127.0.0.1:8081', json='data.json'))


if __name__ == '__main__':
    pass

# -*- coding: utf-8 -*-
from backend.core.base import client
from backend.core.lib import pic

image_process = client.ImageProcess('http://localhost:8080', pic.pic1)


class Config:

    def get_scale_set(self):
        return [[1, 1]]


config = Config()

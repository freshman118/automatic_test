# -*- coding: utf-8 -*-
from backend.core.base import client

api = client.ClientApi('http://localhost:8080')


class Config:

    def get_scale_set(self):
        return [[1, 1]]


config = Config()

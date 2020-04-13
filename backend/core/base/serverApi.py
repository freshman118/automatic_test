# -*- coding: utf-8 -*-
import asyncio
from aiohttp import web

class ServerApi:

    def __init__(self):
        self._cmd_mapping = {
            'GET_STRING': ''
        }

    async def start(self):
        pass

async def main():
    pass
    app = web.Application()

asyncio.run(main())

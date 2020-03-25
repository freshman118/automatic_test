# -*- coding: utf-8 -*-
import asyncio

from logzero import logger
from aiohttp import web


class ServerApi:
    async def handle(self, request):
        name = request.match_info.get('name', 'Anonymous')
        text = 'Hello, ' + name
        return web.Response(text=text)

    def start(self, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()

        logger.info("Starting web server ...")
        self._app = web.Application(client_max_size=16 * 1024 * 1024)  # transfer size, max to 16M-bytes
        self._app.add_routes([web.get('/', handler=self.handle), web.get('/{name}', handler=self.handle)])
        web.run_app(app=self._app, host='127.0.0.1', port=8081)
        # self._app.router.add_post(r'/api/run')
        # self._svr = await loop.create_server(self._app.make_handler(), host="0.0.0.0", port=port)
        logger.info("Web server is started")


if __name__ == '__main__':
    sever_api = ServerApi()
    sever_api.start()

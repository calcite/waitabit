# -*- coding: utf-8 -*-

"""Main module."""

import asyncio
from aiohttp import web, WSMsgType, WSServerHandshakeError
from collections import deque
import sockjs
import pkg_resources
import time


class WaitABit:

    WEB_ASSETS = pkg_resources.resource_filename('waitabit',
                                                 'frontend/dist/static')
    INDEX = open(pkg_resources.resource_filename(
        'waitabit', 'frontend/dist/index.html')).read()

    def __init__(self, queue_size, loop=None, session_timeout=3600):
        self._queue = deque(maxlen=queue_size)
        self._app = web.Application(loop=loop)
        self._sockjs_manager = None
        self._session_timeout = session_timeout
        self._session_screensaver_status = False
        self._session_last_event = time.time()

        # Initialize routes
        self._app.router.add_get('/', self._index)
        self._app.router.add_static('/static', self.WEB_ASSETS)
        self._app.router.add_get('/api/queue', self._get_queue)
        self._app.router.add_post('/api/queue', self._new_call)
        self._app.router.add_delete('/api/queue', self._delete_call)
        self._app.router.add_post('/api/screensaver',
                                  self._activate_screen_saver)
        self._app.router.add_get('/api/screensaver',
                                 self._get_session_screen_saver)

        # Initialize websockets
        sockjs.add_endpoint(self._app, self._sockjs_handler, name='notifier',
                            prefix='/api/notifications/')

    async def _index(self, request):
        return web.Response(body=self.INDEX, content_type='text/html')

    async def _get_queue(self, request):
        temp = {'queue': list(self._queue), 'length': self._queue.maxlen}
        return web.json_response(temp)

    async def _new_call(self, request):
        try:
            call = (await request.json())['call']
            if call in self._queue:
                return web.HTTPBadRequest(reason="Call already in the queue.")
            self._queue.appendleft(call)
            self._session_last_event = time.time()
            self._set_screen_saver(False)
            self._send_ws_message({'event': 'new_call',
                                   'queue': list(self._queue)})
            return web.json_response({'queue': list(self._queue)})
        except (KeyError):
            return web.HTTPBadRequest(reason="Request in bad format.")

    def _delete_queue(self, to_be_deleted):
        if to_be_deleted == 'all':
            self._queue.clear()
        else:
            self._queue.remove(to_be_deleted)

        self._session_last_event = time.time()
        self._set_screen_saver(False)

        self._send_ws_message({'event': 'delete',
                               'deleted': to_be_deleted,
                               'queue': list(self._queue)})

    async def _delete_call(self, request):
        try:
            to_be_deleted = (await request.json())['del']
            self._delete_queue(to_be_deleted)
            return web.json_response({'queue': list(self._queue)})
        except (KeyError, ValueError):
            return web.HTTPBadRequest()

    def _set_screen_saver(self, status):
        old_status = self._session_screensaver_status
        self._session_screensaver_status = status

        if self._session_screensaver_status != old_status:
            self._send_ws_message(
                {'event': 'screensaver',
                 'status': self._session_screensaver_status})

    async def _activate_screen_saver(self, request):
        self._set_screen_saver(True)
        return web.HTTPOk()

    async def _get_session_screen_saver(self, request):
        temp = {'timeout': self._session_timeout,
                'status': self._session_screensaver_status
                }
        return web.json_response(temp)

    async def _session_timeout_check(self):
        while True:
            await asyncio.sleep(1)
            time_since_last_event = time.time() - self._session_last_event

            if ((time_since_last_event >= self._session_timeout) and
                    self._session_screensaver_status is False):
                print("Shutting down session")
                # Delete the queue and activate screensaver
                self._delete_queue('all')
                self._set_screen_saver(True)

    def _send_ws_message(self, msg):
        if self._sockjs_manager:
            self._sockjs_manager.broadcast(msg)

    def _sockjs_handler(self, msg, session):
        """ SockJS handler is now not doing anything because we onlu use
        SockJS for downstream.
        :param session:
        :return:
        """
        if msg.tp == sockjs.MSG_OPEN:
            self._sockjs_manager = session.manager
            # session.manager.broadcast("Someone joined.")
        elif msg.tp == sockjs.MSG_CLOSED:
            self._sockjs_manager = None
            # session.manager.broadcast("Someone left.")

    def run(self, host='0.0.0.0', port=8000):
        handler = self._app.make_handler()
        # self._app.on_shutdown.append(self._on_shutdown)

        self._app.loop.run_until_complete(asyncio.gather(
            self._app.loop.create_server(handler, host, port),
            self._session_timeout_check())
        )

        # self._app.loop.run_forever()





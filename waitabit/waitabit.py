# -*- coding: utf-8 -*-

"""Main module."""

import asyncio
from aiohttp import web, WSMsgType, WSServerHandshakeError
from collections import deque
import sockjs
import pkg_resources
import time
import logging

from .base import WaitabitException
from .keypad_handler import KeypadHandler

logger = logging.getLogger(__name__)


class WaitABit:

    WEB_ASSETS = pkg_resources.resource_filename('waitabit',
                                                 'frontend/dist/static')
    INDEX = open(pkg_resources.resource_filename(
        'waitabit', 'frontend/dist/index.html')).read()

    def __init__(self, queue_size, loop=None, session_timeout=3600,
                 heart_beat_interval=3, max_digits=3, keypad_port='off',
                 disable_input_page=False):
        self._queue = deque(maxlen=queue_size)
        self._app = web.Application(loop=loop)
        self._sockjs_manager = None
        self._session_timeout = session_timeout
        self._session_screensaver_status = False
        self._session_last_event = time.time()
        self._max_digits = max_digits

        # Custom keypad support
        if keypad_port != 'off':
            self._keypad_handler = KeypadHandler(keypad_port, loop,
                                                 self._on_keypad_input)
        else:
            self._keypad_handler = None

        # Initialize routes
        self._app.router.add_get('/', self._index)
        self._app.router.add_static('/static', self.WEB_ASSETS)
        self._app.router.add_get('/api/queue', self._get_queue)
        if not disable_input_page:
            self._app.router.add_post('/api/queue', self._new_call)
        self._app.router.add_delete('/api/queue', self._delete_call)
        self._app.router.add_post('/api/screensaver',
                                  self._activate_screen_saver)
        self._app.router.add_get('/api/screensaver',
                                 self._get_session_screen_saver)

        # Initialize websockets
        self._last_broadcast = time.time()

        if heart_beat_interval > 0:
            self._heart_beat_interval = heart_beat_interval
        else:
            raise Exception("Heart beat interval 0 or less is not allowed.")

        sockjs.add_endpoint(self._app, self._sockjs_handler, name='notifier',
                            prefix='/api/notifications/')

    async def _on_keypad_input(self, number):
        if number == KeypadHandler.DELETE_CMD:
            self._delete_queue('all')
        else:
            try:
                self._add_call(number)
            except WaitabitException:
                logger.debug("Skipping number already present in-queue.")

    async def _index(self, request):
        return web.Response(body=self.INDEX, content_type='text/html')

    async def _get_queue(self, request):
        temp = {'queue': list(self._queue), 'length': self._queue.maxlen,
                'heartbeat_interval': self._heart_beat_interval,
                'max_digits': self._max_digits}
        return web.json_response(temp)

    def _add_call(self, call_number):
        if call_number in self._queue:
            raise WaitabitException("Call already in the queue.")
        self._queue.appendleft(call_number)
        self._session_last_event = time.time()
        self._set_screen_saver(False)
        self._send_ws_message({'event': 'new_call',
                               'queue': list(self._queue)})

    async def _new_call(self, request):
        try:
            call = (await request.json())['call']
            self._add_call(call)
            return web.json_response({'queue': list(self._queue)})
        except KeyError:
            return web.HTTPBadRequest(reason="Request in bad format.")
        except WaitabitException as wbe:
            return web.HTTPBadRequest(reason=str(wbe))

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
                # Delete the queue and activate screensaver
                self._delete_queue('all')
                self._set_screen_saver(True)

    async def _heart_beat(self):
        """ This is additional high-level heartbeat, which attepts to prevent
            SockJS connection stall on android devices (which somehow happens
            event with SockJS's own heart-beat.
        """
        while True:
            await asyncio.sleep(self._heart_beat_interval)
            time_since_last_broadcast = time.time() - self._last_broadcast

            if time_since_last_broadcast >= self._heart_beat_interval:
                self._send_ws_message({'event': 'heartbeat'})

    def _send_ws_message(self, msg):
        if self._sockjs_manager:
            self._sockjs_manager.broadcast(msg)
            self._last_broadcast = time.time()

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

        if self._session_timeout == 0:
            self._app.loop.run_until_complete(asyncio.gather(
                self._app.loop.create_server(handler, host, port),
                self._heart_beat()))

        elif self._session_timeout > 0:
            self._app.loop.run_until_complete(asyncio.gather(
                self._app.loop.create_server(handler, host, port),
                self._heart_beat(),
                self._session_timeout_check()
            ))
        else:
            raise Exception("Session timeout {0} is not allowed".format(
                self._session_timeout))

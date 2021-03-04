"""
Handler for a Waitabit-custom Keypad device for callout number entering.
Reports the numbers over UART via custom binary protocol.
"""

import asyncio
import serial_asyncio
import serial
import struct
import logging

from .base import WaitabitException

logger = logging.getLogger(__name__)


class KeypadException(WaitabitException):
    pass


class KeypadHandler(asyncio.Protocol):

    EOM = b"\n"
    HEADER = 0xF1
    MSG_LENGTH = 4
    CRC_POLY = 0x18
    BAUDRATE = 19200
    STOPBITS = serial.STOPBITS_TWO
    RECONNECT_INTERVAL = 5.0  # seconds
    DELETE_CMD = 0xFFFF

    def __init__(self, uart_port, loop, data_rcv_clbk):
        super().__init__()
        self._buffer = b""
        self._loop = loop
        self._uart = uart_port
        self._connected = False
        self._transport = None
        self._data_rcv_clbk = data_rcv_clbk
        self._loop.create_task(self._reconnect())

    @property
    def connected(self):
        return self._connected

    def _get_protocol(self):
        return self

    async def _reconnect(self):
        try:
            logger.info("Connecting to Keypad at %s", self._uart)
            self._protocol = await serial_asyncio.create_serial_connection(
                self._loop, self._get_protocol, self._uart, baudrate=self.BAUDRATE,
                stopbits=self.STOPBITS)
        except serial.SerialException:
            self._connected = False
            logger.info(f"Connection failed, will try again in "
                  "%.2f seconds...", self.RECONNECT_INTERVAL)
            await asyncio.sleep(self.RECONNECT_INTERVAL)
            self._loop.create_task(self._reconnect())

    def _crc_check(self, data, crc):
        _crc = 0x00
        for b in data:
            for i in range(8):
                fbck = (_crc ^ b) & 0x01
                if fbck == 0x01:
                    _crc ^= self.CRC_POLY
                _crc = (_crc >> 1) & 0x7F
                if fbck == 0x01:
                    _crc |= 0x80
                b = b >> 1
        if crc != _crc:
            raise KeypadException("CRC fail.")

    def connection_made(self, transport):
        self._transport = transport
        self._connected = True
        logger.debug('UART opened: %s', transport)

    def data_received(self, data):
        self._buffer += data
        try:
            eom_index = self._buffer.index(self.EOM)
            msg = self._buffer[eom_index - self.MSG_LENGTH:eom_index]
            self._buffer = b""
            header, number, crc = struct.unpack('<BHB', msg)
            self._crc_check(msg[:self.MSG_LENGTH-1], crc)
            if header != self.HEADER:
                raise struct.error("Wrong header")
            self._crc_check(msg[:3], crc)
            self._loop.create_task(self._data_rcv_clbk(number))
        except ValueError:
            if len(self._buffer) > 10:
                logger.warning("Flushed buffer")
                self._buffer = b""
        except struct.error:
            logger.error("Unable to parse msg")
        except KeypadException:
            logger.error("Protocol exception")

    def connection_lost(self, exc):
        logger.info('Port closed')
        self._transport = None
        self._connected = False
        self._loop.create_task(self._reconnect())

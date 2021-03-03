# -*- coding: utf-8 -*-

"""Console script for waitabit."""

import click
from .waitabit import WaitABit
import asyncio
import logging

@click.command()
@click.version_option()
@click.option('--host', default='0.0.0.0', help="Host IP address. "
                                                "(Default = 0.0.0.0)")
@click.option('--port', default=8000, help="Server port. (Default = 8000)")
@click.option('--queue_size', default=7,
              help="Number of displayed items in the queue. (Default = 7)")
@click.option('--session_timeout', default=3600,
              help="Number of seconds till the session times out"
                   " (queue is cleared and screensaver is enabled)."
                   " Set 0 for no timeout. (Default = 3600)")
@click.option('--heart_beat', default=3,
              help="Heart beat interval [seconds] "
                   "keeping the server connection alive. "
                   "(Default = 3)")
@click.option('--max_digits', default=3,
              help="Maximum number of digits a called-out number can have "
                   "(Default = 3)")
@click.option('--keypad_port', default='off',
              help="serial port to use for connection with custom number entry"
                   "keypad. 'off' value means keypad is not used."
                   "(default = off)")
@click.option('--disable_input_page', default=False, is_flag=True,
              help="Disable number entry via the input panel page.")
def main(host, port, queue_size, session_timeout,
         heart_beat, max_digits, keypad_port, disable_input_page):
    """Wait-a-Bit server."""
    loop = asyncio.get_event_loop()
    srv = WaitABit(queue_size, loop=loop, session_timeout=session_timeout,
                   heart_beat_interval=heart_beat, max_digits=max_digits,
                   keypad_port=keypad_port,
                   disable_input_page=disable_input_page)

    click.echo("Input screen served at http://{0}:{1}/#/input".format(
        host, port))
    click.echo("Info panel served at http://{0}:{1}/#/panel".format(
        host, port))

    srv.run(host=host, port=port)


if __name__ == "__main__":
    main()

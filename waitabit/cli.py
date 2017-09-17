# -*- coding: utf-8 -*-

"""Console script for waitabit."""

import click
from .waitabit import WaitABit
import asyncio
import logging

@click.command()
@click.version_option()
@click.option('--host', default='0.0.0.0', help="Host IP address")
@click.option('--port', default=8000, help="Server port")
@click.option('--queue_size', default=8,
              help="Number of displayed items in the queue")
@click.option('--session_timeout', default=3600,
              help="Number of seconds till the session times out"
                   " (queue is cleared and screensaver is enabled)."
                   " Set 0 for no timeout.")
def main(host, port, queue_size, session_timeout):
    """Wait-a-Bit server."""
    loop = asyncio.get_event_loop()
    srv = WaitABit(queue_size, loop=loop, session_timeout=session_timeout)

    click.echo("Input screen served at http://{0}:{1}/#/input".format(
        host, port))
    click.echo("Info panel served at http://{0}:{1}/#/panel".format(
        host, port))

    srv.run(host=host, port=port)


if __name__ == "__main__":
    main()

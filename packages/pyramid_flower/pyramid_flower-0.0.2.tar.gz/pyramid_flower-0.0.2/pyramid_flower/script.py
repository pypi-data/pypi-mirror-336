import atexit
import logging
import signal
import sys
from contextlib import suppress
from typing import Any

import click
from celery.bin.base import CeleryCommand
from flower.app import Flower
from flower.command import apply_env_options, extract_settings, print_banner
from flower.urls import settings
from pyramid.paster import bootstrap
from pyramid_celery import setup_app
from tornado.options import options

logger = logging.getLogger(__name__)


def sigterm_handler(signum: Any, _: Any) -> None:
    logger.info("%s detected, shutting down", signum)
    sys.exit(0)


@click.command(cls=CeleryCommand, context_settings={"ignore_unknown_options": True})
@click.argument("ini", default="development.ini")
@click.pass_context
def pflower(ctx: click.Context, ini: str, ini_var: str) -> None:
    """Start flower monitor."""
    click.echo("Starting flower ...")

    apply_env_options()
    # apply_options(sys.argv[0], tornado_argv)

    extract_settings()
    # setup_logging()

    capp = ctx.obj.app
    env = bootstrap(ini, options={})
    registry = env["registry"]
    app = env["app"]
    root = env["root"]
    request = env["request"]
    closer = env["closer"]
    setup_app(app, root, request, registry, closer, ini)

    flower_app = Flower(capp=capp, options=options, **settings)

    atexit.register(flower_app.stop)
    signal.signal(signal.SIGTERM, sigterm_handler)

    if not ctx.obj.quiet:
        print_banner(capp, "ssl_options" in settings)

    with suppress(KeyboardInterrupt, SystemExit):
        flower_app.start()

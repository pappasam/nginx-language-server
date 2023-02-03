"""Cli for nginx language server."""

import argparse
import logging
import sys
from importlib.metadata import version

from nginx_language_server import __version__
from nginx_language_server.server import SERVER


def get_version() -> str:
    """Get the program version."""
    # pylint: disable=import-outside-toplevel
    return version("nginx-language-server")


def cli() -> None:
    """Nginx language server cli entrypoint."""
    parser = argparse.ArgumentParser(
        prog="nginx-language-server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Nginx language server: an LSP server for nginx.conf.",
        epilog="""\
Examples:

    Run from stdio: nginx-language-server
""",
    )
    parser.add_argument(
        "--version",
        help="display version information and exit",
        action="store_true",
    )
    parser.add_argument(
        "--tcp",
        help="use TCP server instead of stdio",
        action="store_true",
    )
    parser.add_argument(
        "--host",
        help="host for TCP server (default 127.0.0.1)",
        type=str,
        default="127.0.0.1",
    )
    parser.add_argument(
        "--port",
        help="port for TCP server (default 2088)",
        type=int,
        default=2088,
    )
    parser.add_argument(
        "--log-file",
        help="redirect logs to the given file instead of writing to stderr",
        type=str,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="increase verbosity of log output",
        action="count",
        default=0,
    )
    args = parser.parse_args()
    if args.version:
        print(__version__)
        sys.exit(0)
    log_level = {0: logging.INFO, 1: logging.DEBUG}.get(
        args.verbose,
        logging.DEBUG,
    )
    if args.log_file:
        logging.basicConfig(
            filename=args.log_file,
            filemode="w",
            level=log_level,
        )
    else:
        logging.basicConfig(stream=sys.stderr, level=log_level)
    if args.tcp:
        SERVER.start_tcp(host=args.host, port=args.port)
    else:
        SERVER.start_io()

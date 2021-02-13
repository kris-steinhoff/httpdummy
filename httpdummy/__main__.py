import argparse
from os import getenv

from werkzeug.serving import run_simple

from httpdummy.server import HttpDummy, NoLogRequestHandler, print_logo

def main():
    parser = argparse.ArgumentParser(
        description='A dummy http server that prints requests and responds')

    show_headers_subgroup = parser.add_mutually_exclusive_group()
    show_headers_subgroup.add_argument(
        '-H',
        # help='print request headers to stdout',
        action='store_const',
        const='on',
        dest='print_headers',
    )
    show_headers_subgroup.add_argument(
        '--print-headers',
        help='print request headers to stdout',
        choices=['on', 'off'],
        default='off',
        dest='print_headers',
    )

    show_body_subgroup = parser.add_mutually_exclusive_group()
    show_body_subgroup.add_argument(
        '-B',
        # help='print request body to stdout',
        action='store_const',
        const='on',
        dest='print_body',
        )
    show_body_subgroup.add_argument(
        '--print-body',
        help='print request body to stdout',
        choices=['on', 'off'],
        default='off',
        dest='print_body',
    )

    parser.add_argument(
        '-a', '--address',
        help='address to bind to (default 127.0.0.1)',
        default='127.0.0.1',
        type=str,
    )

    parser.add_argument(
        '-p', '--port',
        help='port to open on (default 5000)',
        default=5000,
        type=int,
    )

    parser.add_argument(
        '--werkzeug-reloader',
        help='enable server reloader (default on)',
        choices=['on', 'off'],
        default='on',
    )

    parser.add_argument(
        '--werkzeug-reloader-type',
        help='server reloader type (default watchdog)',
        choices=['stat', 'watchdog'],
        default='watchdog',
    )

    parser.add_argument(
        '--werkzeug-debugger',
        help='enable server debugger (default off)',
        choices=['on', 'off'],
        default='off',
    )

    parser.add_argument(
        dest='config_file',
        help='path to configuration file',
        type=argparse.FileType('r'),
        nargs='?',
    )

    args = parser.parse_args()

    extra_files = ['server.py']
    if args.config_file:
        extra_files.append(args.config_file.name)

    app = HttpDummy(**vars(args))

    print_logo()

    run_simple(
        args.address, args.port, app,
        request_handler=NoLogRequestHandler,
        use_debugger=args.werkzeug_debugger == 'on',
        reloader_type=args.werkzeug_reloader_type,
        use_reloader=args.werkzeug_reloader == 'on' and args.config_file,
        extra_files=extra_files,
    )

if __name__ == "__main__":
    main()

import argparse
from os import getenv

from werkzeug.serving import run_simple

from httpdummy.server import HttpDummy, NoLogRequestHandler, print_logo

def main():

    parser = argparse.ArgumentParser(
        prog='httpdummy',
        description='A dummy http server that prints requests and responds')

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

    print_headers_subgroup = parser.add_mutually_exclusive_group()
    print_headers_subgroup.add_argument(
        '-H',
        dest='print_headers',
        action='store_const',
        const='on',
        default='off',
    )
    print_headers_subgroup.add_argument(
        '--print-headers',
        help='print request headers to stdout',
        choices=['on', 'off'],
        default='off',
    )

    print_body_subgroup = parser.add_mutually_exclusive_group()
    print_body_subgroup.add_argument(
        '-B',
        dest='print_body',
        action='store_const',
        const='on',
        default='off',
    )
    print_body_subgroup.add_argument(
        '--print-body',
        help='print request body to stdout',
        choices=['on', 'off'],
        default='off',
    )

    parser.add_argument(
        '--server-reloader',
        help=(
            'enable Werkzeug server reloader (default on if config_file is '
            'specified)'),
        choices=['on', 'off'],
        default='on',
    )

    parser.add_argument(
        '--server-reloader-type',
        help='Werkzeug server reloader type (default watchdog)',
        choices=['stat', 'watchdog'],
        default='watchdog',
    )

    parser.add_argument(
        '--server-debugger',
        help='enable Werkzeug server debugger (default off)',
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

    for a in [
        'print_headers', 'print_body',
        'server_reloader', 'server_debugger',
    ]:
        setattr(args, a, getattr(args, a) == 'on')

    extra_files = ['server.py']
    if args.config_file:
        extra_files.append(args.config_file.name)

    app = HttpDummy(**vars(args))

    print_logo()

    run_simple(
        args.address, args.port, app,
        request_handler=NoLogRequestHandler,
        use_debugger=args.server_debugger,
        reloader_type=args.server_reloader_type,
        use_reloader=args.server_reloader and args.config_file,
        extra_files=extra_files,
    )

if __name__ == "__main__":
    main()

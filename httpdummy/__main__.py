import argparse
from os import getenv

from werkzeug.serving import run_simple

from httpdummy.server import HttpDummy, NoLogRequestHandler, print_logo


def str2bool(val):
    return str(val).lower() in ('true', 'yes', 'y', 'on', '1')


parser = argparse.ArgumentParser(
    description='A dummy http server that prints requests and responds')

parser.add_argument('-H', '--headers', type=str2bool, nargs='?',
                    const=True, default=getenv('HTTPDUMMY_HEADERS'))
parser.add_argument('-B', '--body', type=str2bool, nargs='?',
                    const=True, default=getenv('HTTPDUMMY_BODY'))
parser.add_argument('-a', '--address', type=str,
                    default=getenv('HTTPDUMMY_ADDRESS', '127.0.0.1'))
parser.add_argument('-p', '--port', type=int,
                    default=getenv('HTTPDUMMY_PORT', 5000))
parser.add_argument('-r', '--response-file', type=argparse.FileType('r'),
                    nargs='?',
                    default=getenv('HTTPDUMMY_RESPONSE_FILE', None))
args = parser.parse_args()

use_reloader = (
    str2bool(getenv('HTTPDUMMY_RELOADER', 'on')) and args.response_file)

extra_files = ['server.py']
if args.response_file:
    extra_files.append(args.response_file.name)

app = HttpDummy(vars(args))

print_logo()

run_simple(
    args.address, args.port, app,
    request_handler=NoLogRequestHandler,
    use_debugger=str2bool(getenv('HTTPDUMMY_DEBUGGER', '0')),
    reloader_type=getenv('HTTPDUMMY_RELOADER_TYPE', 'watchdog'),
    use_reloader=use_reloader,
    extra_files=extra_files,
)

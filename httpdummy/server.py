from os import getenv

from colorama import Style
from werkzeug.serving import WSGIRequestHandler
from werkzeug.wrappers import Request, Response


class HttpDummy(object):
    def __init__(self, conf):
        self.conf = conf

    def dispatch_request(self, request):
        print(
            f'{Style.BRIGHT}{request.method}{Style.NORMAL} '
            f'{request.environ.get("RAW_URI")}'
        )

        if self.conf.get('headers'):
            for (k, v) in request.headers:
                print(f'{Style.DIM}{k}: {v}{Style.NORMAL}')
            if self.conf.get('body') and len(request.data) > 0:
                print()

        if self.conf.get('body') and len(request.data) > 0:
            for line in request.data.decode('utf-8').splitlines():
                print(f'{Style.DIM}{line}{Style.NORMAL}')
        resp = Response('Hello World!')
        resp.headers['Server'] = 'HTTPDummy'
        return resp

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


class NoLogRequestHandler(WSGIRequestHandler):
    def log_request(self, *args, **kwargs):
        pass


def main():
    import argparse

    from werkzeug.serving import run_simple

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
    args = parser.parse_args()

    app = HttpDummy(vars(args))
    run_simple(args.address, args.port, app,
               request_handler=NoLogRequestHandler,
               use_debugger=str2bool(getenv('HTTPDUMMY_DEBUGGER', '0')),
               use_reloader=True)

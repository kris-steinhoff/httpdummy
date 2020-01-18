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
            f'{request.path} {request.environ.get("SERVER_PROTOCOL")}'
        )

        if self.conf.get('headers'):
            print(Style.DIM + str(request.headers).strip())
            if self.conf.get('body'):
                print()
            print(Style.NORMAL, end='')

        if self.conf.get('body') and len(request.data) > 0:
            print(Style.DIM + request.data.decode('utf-8').strip()
                  + Style.NORMAL)
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

    parser = argparse.ArgumentParser(
        description='A dummy http server that prints requests and responds')

    parser.add_argument('-H', '--headers', action='store_true',
                        default=getenv('HTTPDUMMY_HEADERS'))
    parser.add_argument('-B', '--body', action='store_true',
                        default=getenv('HTTPDUMMY_BODY'))
    parser.add_argument('-a', '--address', type=str,
                        default=getenv('HTTPDUMMY_ADDRESS', '127.0.0.1'))
    parser.add_argument('-p', '--port', type=int,
                        default=getenv('HTTPDUMMY_PORT', 5000))
    args = parser.parse_args()

    app = HttpDummy(vars(args))
    run_simple(args.address, args.port, app,
               request_handler=NoLogRequestHandler,
               use_debugger=(
                   getenv('HTTPDUMMY_DEBUGGER', '0').lower()
                   in ('1', 'on', 'yes')),
               use_reloader=True)

from base64 import b64decode
from yaml import safe_load as yaml_safe_load

from colorama import Fore, Style
from werkzeug.serving import WSGIRequestHandler, is_running_from_reloader
from werkzeug.wrappers import Request, Response


def print_logo():
    '''Print the HTTPDummy logo. uses is_running_from_reloader to prevent
    double printing on startup and reprinting on reload.'''

    LOGO = '''
                                    __________________
                                   /        ________  \\
                                  /   _____|       |___\\
                                 |   /  __         __   |
                                /|  |  /o \   _   /o \  |  
                               | | /           \        |
                                \|/   __           __   |
                                  \    |\_________/|   /   
                                   \___|___________|__/                  
                                        |         |
                                       /\_________/\\
    _   _ _____ _____ ____  ____     _/     \ /     \_
   | | | |_   _|_   _|  _ \|  _ \ _ | _ _ __ V__  _ __|___  _   _
   | |_| | | |   | | | |_) | | | | | | | '_ ` _ \| '_ ` _ \| | | |
   |  _  | | |   | | |  __/| |_| | |_| | | | | | | | | | | | |_| |
   |_| |_| |_|   |_| |_|   |____/ \__,_|_| |_| |_|_| |_| |_|\__, |
                                                            |___/
'''
    if not is_running_from_reloader():
        for line in LOGO.splitlines():
            print(f'{Fore.CYAN}{line}{Fore.RESET}')


class HttpDummy(object):
    def __init__(self, **kwargs):
        config_file = kwargs.get('config_file')
        config_all = {}
        if config_file:
            try:
                config_all = yaml_safe_load(
                    config_file)
            except Exception as exc:
                # TODO do something here
                raise exc
        self.responses = config_all.get('responses', {})
        self.config = kwargs

    def print_request_info(self, request):
        print(
            f'{Style.BRIGHT}{request.method}{Style.NORMAL} '
            f'{request.environ.get("RAW_URI")}'
        )

        if self.config.get('print_headers'):
            for (k, v) in request.headers:
                print(f'{Style.DIM}{k}: {v}{Style.NORMAL}')
            if self.config.get('print_body') and len(request.data) > 0:
                print()

        if self.config.get('print_body') and len(request.data) > 0:
            for line in request.data.decode('utf-8').splitlines():
                print(f'{Style.DIM}{line}{Style.NORMAL}')

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        self.print_request_info(request)

        response = Response()
        response.status_code = 200
        response.headers.set('Server', 'HTTPDummy')

        configured_resp = (
            self.responses.get(f'{request.method} {request.path}', None)
            or self.responses.get(request.path, None)
        )

        if not configured_resp:
            response.data = 'HTTPDummy'
            return response(environ, start_response)

        # Set status code
        response.status_code = int(
            configured_resp.get('status', response.status_code))

        # Set headers
        for (k, v) in configured_resp.get('headers', {}).items():
            response.headers.set(k, v)

        # Set body
        if 'body_text' in configured_resp.keys():
            response.data = configured_resp['body_text']
        elif 'body_base64' in configured_resp.keys():
            response.data = b64decode(configured_resp['body_base64'])
        # elif 'body_file' in configured_resp.keys():
        #     response.data = open(configured_resp['body_file'])
        elif 'body' in configured_resp.keys():
            # TODO deprecation warning
            response.data = configured_resp['body']
        else:
            response.data = 'HTTPDummy'

        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


class NoLogRequestHandler(WSGIRequestHandler):
    '''This class just supresses the standard werkzeug request logging.'''
    def log_request(self, *args, **kwargs):
        pass

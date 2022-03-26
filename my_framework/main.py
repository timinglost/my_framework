from quopri import decodestring
from my_framework.get_post_requests import GetRequests, PostRequests
import glob
import json


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class Framework:
    def __init__(self, routes_obj, fronts_obj):
        self.routes_lst = routes_obj
        self.fronts_lst = fronts_obj

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']

        if not path.endswith('/'):
            path = f'{path}/'

        request = {}

        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = PostRequests().get_request_params(environ)
            request['data'] = Framework.decode_value(data)
            print(f'Нам пришёл post-запрос: {Framework.decode_value(data)}')
            count_file = len(glob.glob('get_post_json/post_*.json'))
            with open(f'get_post_json/post_{count_file}.json', 'w') as json_file:
                json.dump(Framework.decode_value(data), json_file, indent=4)
        if method == 'GET':
            request_params = GetRequests().get_request_params(environ)
            request['request_params'] = Framework.decode_value(request_params)
            print(f'Нам пришли GET-параметры:'
                  f' {Framework.decode_value(request_params)}')
            if len(Framework.decode_value(request_params)) != 0:
                count_file = len(glob.glob('get_post_json/get_*.json'))
                with open(f'get_post_json/get_{count_file}.json', 'w') as json_file:
                    json.dump(Framework.decode_value(request_params), json_file, indent=4)

        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = PageNotFound404()
        for front in self.fronts_lst:
            front(request)
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data

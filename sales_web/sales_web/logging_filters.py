import logging
from threading import local

thread_local = local()

class RemoveAutoreloadFilter(logging.Filter):
    def filter(self, record):
        return 'autoreload' not in record.name

class AddRequestIPFilter(logging.Filter):
    def filter(self, record):
        record.ip = getattr(thread_local, 'ip', '-')
        return True

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class RequestIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        thread_local.ip = get_client_ip(request)
        response = self.get_response(request)
        return response
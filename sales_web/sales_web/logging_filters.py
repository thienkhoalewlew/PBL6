import logging

class RemoveAutoreloadFilter(logging.Filter):
    def filter(self, record):
        return 'autoreload' not in record.name
from fastcode import InsightPoints
from functools import wraps

def log_codepoint(ip):
    def decorator_main(func):
        def decorator(*args, **kwargs):
            @wraps(func)
            def wrapper(*ipargs, **ipkwargs):
                ip.log_startpoint(*ipargs, **ipkwargs)
                result = func(*args, **kwargs)
                ip.log_endpoint(ipkwargs["id"])
                return result
            return wrapper
        return decorator
    return decorator_main

def log_entrypoint(creds, *ipargs, **ipkwargs):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            ip = InsightPoints(*ipargs, **ipkwargs)
            result = func(ip, *args, **kwargs)
            ip.log_send(creds)
            print(vars(ip))
            return result
        return wrapper
    return decorator
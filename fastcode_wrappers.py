from fastcode import InsightPoints
from functools import wraps

def ioc_startpoint(ip):
    def decorator_main(func):
        def decorator(*args, **kwargs):
            @wraps(func)
            def wrapper(*ipargs, **ipkwargs):
                ip.start_point(*ipargs, **ipkwargs)
                result = func(*args, **kwargs)
                ip.end_point(ipkwargs["id"])
                return result
            return wrapper
        return decorator
    return decorator_main

def ioc_(*ipargs, **ipkwargs):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            ip = InsightPoints(*ipargs, **ipkwargs)
            result = func(ip, *args, **kwargs)
            ip.log()
            print(vars(ip))
            return result
        return wrapper
    return decorator
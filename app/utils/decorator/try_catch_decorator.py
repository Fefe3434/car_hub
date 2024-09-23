from http import HTTPStatus


def try_catch_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            print(args)
            print(kwargs)
            return func(*args, **kwargs)
        except PermissionError as e:
            return {'Error': str(e)}, HTTPStatus.UNAUTHORIZED
        except ValueError as e:
            return {'Error': str(e)}, HTTPStatus.BAD_REQUEST
        except Exception as e:
            return {'Error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
    return wrapper

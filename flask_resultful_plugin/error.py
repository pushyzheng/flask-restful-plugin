# encoding:utf-8

# 401 错误
class UnauthorizedError(Exception):
    pass

# 400 错误
class BadRequestError(Exception):
    pass

class MediaTypeError(Exception):
    pass

# 父异常
class RestfulException(Exception):
    pass
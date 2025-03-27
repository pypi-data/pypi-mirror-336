# @Coding: UTF-8
# @Time: 2024/9/24 12:58
# @Author: xieyang_ls
# @Filename: annotation.py

def Get(path: str):
    if not isinstance(path, str):
        raise ValueError('GET Method: path should be a string')
    if len(path) == 0:
        raise ValueError('GET Method: path should not be empty')

    def decorator_get_func(func):
        func.__decorator__ = "GET"
        func.__decorator_path__ = path
        return func

    return decorator_get_func


def Post(path: str):
    if not isinstance(path, str):
        raise ValueError('POST Method: path should be a string')
    if len(path) == 0:
        raise ValueError('POST Method: path should not be empty')

    def decorator_post_func(func):
        func.__decorator__ = "POST"
        func.__decorator_path__ = path
        return func

    return decorator_post_func


def Put(path: str):
    if not isinstance(path, str):
        raise ValueError('PUT Method: path should be a string')
    if len(path) == 0:
        raise ValueError('PUT Method: path should not be empty')

    def decorator_put_func(func):
        func.__decorator__ = "PUT"
        func.__decorator_path__ = path
        return func

    return decorator_put_func


def Delete(path: str):
    if not isinstance(path, str):
        raise ValueError('DELETE Method: path should be a string')
    if len(path) == 0:
        raise ValueError('DELETE Method: path should be empty')

    def decorator_delete_func(func):
        func.__decorator__ = "DELETE"
        func.__decorator_path__ = path
        return func

    return decorator_delete_func

# @Coding: UTF-8
# @Time: 2024/9/22 17:15
# @Author: xieyang_ls
# @Filename: spirit_application.py
import os

import cgi

import json

import inspect

import importlib.util

from types import FunctionType, MethodType

from pyutils_spirit.style import draw_spirit_banner

from pyutils_spirit.exception import NoneSignatureError

from logging import info, INFO, basicConfig, exception

from http.server import BaseHTTPRequestHandler, HTTPServer

from pyutils_spirit.util import Assemble, HashAssemble, Set, HashSet

from pyutils_spirit.spirit_container.multipart_file import MultipartFile

basicConfig(level=INFO)


class SpiritApplication:
    __unique_modules: Set[object] = None

    __current_file__: str = None

    __current_work_dir__: str = None

    __signatures: tuple[str] = None

    __container: Assemble[str, object] = None

    __auto_wired_list: list[object] = None

    __method_types: tuple[str] = None

    controller_paths_set: set[str] = None

    def __init__(self, __file__):
        self.__unique_modules = HashSet()
        self.__current_file__ = __file__
        SpiritApplication.__signatures = ("Component", "Mapper", "Service", "Controller")
        SpiritApplication.__container = HashAssemble()
        self.__auto_wired_list = list()
        SpiritApplication.__method_types = ("GET", "POST", "PUT", "DELETE")
        SpiritApplication.controller_paths_set = set()

    def start(self, host: str, port: int):
        draw_spirit_banner()
        self.__current_work_dir__ = os.getcwd()
        self.__scan_modules(self.__current_work_dir__)
        self.start_service(host=host, port=port)

    def __scan_modules(self, work_directory: str):
        for dirpath, dirnames, filenames in os.walk(work_directory):
            for file_name in filenames:
                if file_name == "__init__.py":
                    continue
                if file_name.endswith('.py'):
                    file_path = os.path.join(dirpath, file_name)
                    self.__load_module(file_path)
        self.__auto_injected()

    def __load_module(self, file_path):
        current_file_path = os.path.abspath(self.__current_file__)
        if file_path == current_file_path:
            return None
        module_path = file_path[:-3]
        module_name = os.path.basename(module_path)
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.__analyze_module(module)

    def __analyze_module(self, module) -> None:
        for name, obj in inspect.getmembers(module):
            if self.__unique_modules.__contains__(obj) is False:
                self.__unique_modules.add(obj)
                if obj is None:
                    continue
                if isinstance(obj, FunctionType):
                    decorator = getattr(obj, "__decorator__", None)
                    if decorator in SpiritApplication.__signatures:
                        instance = obj()
                        self.__auto_wired_list.append(instance)
                        if decorator == "Controller":
                            params = getattr(obj, "__decorator_params__")
                            SpiritApplication.controller_paths_set.add(params)

    @classmethod
    def get_func_kwargs(cls, path: str, method_type: str) -> [object, callable, dict]:
        for controller_path in cls.controller_paths_set:
            path_list = path.split(controller_path, maxsplit=1)
            if len(path_list) == 1:
                continue
            controller_func_path = path_list[1]
            if len(path_list) > 1 and controller_func_path[0] == "/":
                controller = cls.__container.get(controller_path)
                for method_name, method in inspect.getmembers(controller):
                    decorator = getattr(method, "__decorator__", None)
                    if decorator == method_type:
                        func_path = getattr(method, "__decorator_path__")
                        func_path_list = controller_func_path.split(func_path, maxsplit=1)
                        if len(func_path_list) == 1:
                            continue
                        func_args = func_path_list[1]
                        if len(func_path_list) > 1:
                            if func_args == "":
                                return method, None
                            elif func_args[0] == "?":
                                kwargs = list()
                                for param in func_args.split("?")[1].split("&"):
                                    if "=" in param:
                                        value = param.split("=")[1]
                                        kwargs.append(value)
                                return method, kwargs
        raise ValueError(f"please check the path {path} of {method_type} Method")

    def __auto_injected(self) -> None:
        for instance in self.__auto_wired_list:
            for method_name, method in inspect.getmembers(instance):
                if isinstance(method, MethodType):
                    decorator = getattr(method, "__decorator__", None)
                    if decorator == "Resource":
                        method(self=instance, resources={})

    class RequestHandler(BaseHTTPRequestHandler):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.__data__ = None
            self.__response__ = None

        def do_OPTIONS(self):
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()

        def do_GET(self):
            try:
                func, kwargs = SpiritApplication.get_func_kwargs(self.path, "GET")
                if isinstance(kwargs, list):
                    self.__response__ = func(*kwargs)
                else:
                    self.__response__ = func()
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(json.dumps(self.__response__).encode('utf-8'))
            except Exception as e:
                exception(e)
                self.send_response(500)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))

        def get_post_file(self, post_body_length):
            if self.headers['Content-Type'].startswith('multipart/form-data'):
                # 解析请求体
                form = cgi.FieldStorage(fp=self.rfile,
                                        headers=self.headers,
                                        environ={'REQUEST_METHOD': 'POST'})
                # 处理文件
                if "file" in form:
                    temp_file_handler = form["file"]
                elif "data" in form:
                    temp_file_handler = form["data"]
                else:
                    self.send_response(400)
                    self.end_headers()
                    raise FileNotFoundError("Post Method: Content-Type is multipart/form-data But No file uploaded")
                # 创建临时文件并写入上传的内容
                file = MultipartFile(temp_file_handler=temp_file_handler.file)
                return file
            else:
                data = self.rfile.read(post_body_length)
                return json.loads(data)

        def do_POST(self):
            post_body_length = int(self.headers['Content-Length'])
            try:
                func, kwargs = SpiritApplication.get_func_kwargs(self.path, "POST")
                if post_body_length > 0:
                    self.__data__ = self.get_post_file(post_body_length)
                else:
                    self.send_response(400)
                    self.end_headers()
                    raise ValueError("Post Method: Request Body must be not empty.")
                if isinstance(kwargs, list):
                    self.__response__ = func(*kwargs, self.__data__)
                else:
                    self.__response__ = func(self.__data__)
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(json.dumps(self.__response__).encode('utf-8'))
            except Exception as e:
                exception(e)
                self.send_response(500)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))
            finally:
                if isinstance(self.__data__, MultipartFile):
                    self.__data__.close()

        def do_PUT(self):
            put_body_length = int(self.headers['Content-Length'])
            if put_body_length > 0:
                data = self.rfile.read(put_body_length)
                self.__data__ = json.loads(data)
            else:
                self.__data__ = None
            try:
                func, kwargs = SpiritApplication.get_func_kwargs(self.path, "PUT")
                if isinstance(kwargs, list):
                    self.__response__ = func(*kwargs, self.__data__)
                else:
                    self.__response__ = func(self.__data__)
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(json.dumps(self.__response__).encode('utf-8'))
            except Exception as e:
                exception(e)
                self.send_response(500)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))

        def do_DELETE(self):
            content = self.headers['Content-Length']
            if content is not None:
                delete_body_length = int(content)
                if delete_body_length > 0:
                    data = self.rfile.read(delete_body_length)
                    self.__data__ = json.loads(data)
                else:
                    self.__data__ = None
            else:
                self.__data__ = None
            try:
                func, kwargs = SpiritApplication.get_func_kwargs(self.path, "DELETE")
                if isinstance(kwargs, list):
                    if self.__data__ is None:
                        self.__response__ = func(*kwargs)
                    else:
                        self.__response__ = func(*kwargs, self.__data__)
                else:
                    if self.__data__ is None:
                        self.__response__ = func()
                    else:
                        self.__response__ = func(self.__data__)
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(json.dumps(self.__response__).encode('utf-8'))
            except Exception as e:
                exception(e)
                self.send_response(500)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))

    def start_service(self, host: str, port: int):
        server_address = (host, port)
        service = HTTPServer(server_address, SpiritApplication.RequestHandler)
        info("Spirit Container Service Startup successfully")
        info(f"Listening on Server: {host}:{port}")
        service.serve_forever()

    @classmethod
    def Component(cls, signature: str):
        if not isinstance(signature, str):
            raise NoneSignatureError
        if len(signature) == 0:
            raise ValueError("Component: Signature cannot be empty")

        def get_component_cls(other_cls):

            def get_component_instance(*args, **kwargs) -> object:
                instance = cls.__container.get(signature)
                if instance is None:
                    instance = other_cls(*args, **kwargs)
                    cls.__container.put(signature, instance)
                return instance

            get_component_instance.__decorator__ = "Component"
            get_component_instance.__decorator_params__ = signature
            return get_component_instance

        return get_component_cls

    @classmethod
    def Mapper(cls, signature: str):
        if not isinstance(signature, str):
            raise NoneSignatureError
        if len(signature) == 0:
            raise ValueError("Mapper: Signature cannot be empty")

        def get_mapper_cls(other_cls):

            def get_mapper_instance(*args, **kwargs) -> object:
                instance = cls.__container.get(signature)
                if instance is None:
                    instance = other_cls(*args, **kwargs)
                    cls.__container.put(signature, instance)
                return instance

            get_mapper_instance.__decorator__ = "Mapper"
            get_mapper_instance.__decorator_params__ = signature
            return get_mapper_instance

        return get_mapper_cls

    @classmethod
    def Service(cls, signature: str):
        if not isinstance(signature, str):
            raise NoneSignatureError
        if len(signature) == 0:
            raise ValueError("Service: Signature cannot be empty")

        def get_service_cls(other_cls):

            def get_service_instance(*args, **kwargs) -> object:
                instance = cls.__container.get(signature)
                if instance is None:
                    instance = other_cls(*args, **kwargs)
                    cls.__container.put(signature, instance)
                return instance

            get_service_instance.__decorator__ = "Service"
            get_service_instance.__decorator_params__ = signature
            return get_service_instance

        return get_service_cls

    @classmethod
    def Controller(cls, path: str):
        if not isinstance(path, str):
            raise NoneSignatureError
        if len(path) == 0:
            raise ValueError("Controller: path cannot be empty")

        def get_controller_cls(other_cls):

            def get_controller_instance(*args, **kwargs) -> object:
                instance = cls.__container.get(path)
                if instance is None:
                    instance = other_cls(*args, **kwargs)
                    cls.__container.put(path, instance)
                return instance

            get_controller_instance.__decorator__ = "Controller"
            get_controller_instance.__decorator_params__ = path
            return get_controller_instance

        return get_controller_cls

    @classmethod
    def Resource(cls, names: list[str]):
        if not isinstance(names, list):
            raise ValueError("the names must be a list")
        if not all(isinstance(name, str) for name in names):
            raise ValueError("All elements in the list must be strings")
        if len(names) == 0:
            raise ValueError("the names must not be empty")

        def decorator_func(func):
            def wrapper(*args, **kwargs):
                resources = kwargs["resources"]
                for name in names:
                    resources[name] = cls.__container.get(name)
                func(args[0], resources)

            wrapper.__decorator__ = "Resource"
            return wrapper

        return decorator_func


Component = SpiritApplication.Component
Mapper = SpiritApplication.Mapper
Service = SpiritApplication.Service
Controller = SpiritApplication.Controller
Resource = SpiritApplication.Resource

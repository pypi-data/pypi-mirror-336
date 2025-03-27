# @Coding: UTF-8
# @Time: 2025/3/26 23:42
# @Author: xieyang_ls
# @Filename: __init__.py.py

from pyutils_spirit.annotation import connection, get_instance_signature, singleton

from pyutils_spirit.util import (Assemble,
                                 HashAssemble,
                                 ReentryLock,
                                 Regional,
                                 Queue,
                                 LinkedQueue,
                                 BlockingQueue,
                                 Set,
                                 HashSet,
                                 ThreadExecutor)

from pyutils_spirit.database import Handler, MySQLHandler

from pyutils_spirit.exception import ArgumentException, ConflictSignatureError, NoneSignatureError

from pyutils_spirit.python_spark import PySparkHandler

from pyutils_spirit.style import (BLACK, RED, GREEN, YELLOW,
                                  BLUE, MAGENTA, CYAN, WHITE, RESET,
                                  set_spirit_banner,
                                  set_websocket_banner)

from pyutils_spirit.spirit_container import (Get, Post, Put, Delete,
                                             SpiritApplication,
                                             Component, Mapper,
                                             Service, Controller,
                                             Resource)

from pyutils_spirit.tcp import WebSocketServer, Session, onopen, onmessage, onclose, onerror

__all__ = ['connection',
           'get_instance_signature',
           'singleton',
           'ReentryLock',
           'Regional',
           'ThreadExecutor',
           'Assemble',
           'HashAssemble',
           'Queue',
           'LinkedQueue',
           'BlockingQueue',
           'Set',
           'HashSet',
           'Handler',
           'MySQLHandler',
           'ArgumentException',
           'ConflictSignatureError',
           'NoneSignatureError',
           'PySparkHandler',
           "BLACK",
           "RED",
           "GREEN",
           "YELLOW",
           "BLUE",
           "MAGENTA",
           "CYAN",
           "WHITE",
           "RESET",
           "set_spirit_banner",
           "set_websocket_banner",
           "Get",
           "Post",
           "Put",
           "Delete",
           "SpiritApplication",
           "Component",
           "Mapper",
           "Service",
           "Controller",
           "Resource",
           'WebSocketServer',
           'Session',
           'onopen',
           'onmessage',
           'onclose',
           'onerror']

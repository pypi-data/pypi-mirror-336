# @Coding: UTF-8
# @Time: 2024/9/22 17:13
# @Author: xieyang_ls
# @Filename: __init__.py.py

from pyutils_spirit.spirit_container.annotation import Get, Post, Put, Delete

from pyutils_spirit.spirit_container.spirit_application import (SpiritApplication,
                                                                Component,
                                                                Mapper,
                                                                Service,
                                                                Controller,
                                                                Resource)

__all__ = ["Get",
           "Post",
           "Put",
           "Delete",
           "SpiritApplication",
           "Component",
           "Mapper",
           "Service",
           "Controller",
           "Resource"]

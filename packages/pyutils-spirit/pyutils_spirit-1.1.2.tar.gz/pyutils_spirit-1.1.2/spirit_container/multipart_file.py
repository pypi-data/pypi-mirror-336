# @Coding: UTF-8
# @Time: 2024/9/25 15:58
# @Author: xieyang_ls
# @Filename: multipart_file.py

import os

import shutil

import tempfile

from typing import BinaryIO


class MultipartFile(object):
    __temp_file_handler__: tempfile.TemporaryFile = None

    __temp_file_path__: str | None = None

    __temp_file__: BinaryIO | None = None

    def __init__(self, temp_file_handler: tempfile.TemporaryFile):
        self.__temp_file_handler__ = temp_file_handler
        try:
            self.__temp_file_path__ = tempfile.mktemp()  # 创建临时文件路径
            self.__temp_file__ = open(self.__temp_file_path__, 'wb')
            # 将上传的文件写入临时文件
            shutil.copyfileobj(self.__temp_file_handler__, self.__temp_file__, length=20 * 1024 * 1024)
        except Exception as e:
            raise Exception(e)
        finally:
            if self.__temp_file__ is not None:
                self.__temp_file__.close()  # 确保文件关闭

    def copy(self, file_path: str):
        try:
            shutil.copyfile(self.__temp_file_path__, file_path)
        except Exception as e:
            raise Exception(e)

    def getTempFilePath(self) -> str:
        return self.__temp_file_path__

    def getTempFile(self):
        return self.__temp_file__

    def close(self):
        if self.__temp_file_handler__ is not None:
            self.__temp_file_handler__.close()
            self.__temp_file_handler__ = None
        if self.__temp_file__ is not None:
            self.__temp_file__.close()
            self.__temp_file__ = None
        if self.__temp_file_path__ is not None and os.path.exists(self.__temp_file_path__):
            os.remove(self.__temp_file_path__)  # 确保临时文件删除
            self.__temp_file_path__ = None

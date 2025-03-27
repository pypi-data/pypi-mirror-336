# @Coding: UTF-8
# @Time: 2024/9/10 13:48
# @Author: xieyang_ls
# @Filename: assemble.py

from typing import TypeVar, Generic

from abc import ABC, abstractmethod

K = TypeVar('K')

V = TypeVar('V')


class Assemble(ABC, Generic[K, V]):

    @abstractmethod
    def put(self, key: K, value: V) -> None:
        pass

    @abstractmethod
    def get(self, key: K) -> V:
        pass

    @abstractmethod
    def remove(self, key: K) -> V:
        pass

    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def clean(self) -> None:
        pass


class HashAssemble(Assemble[K, V], Generic[K, V]):
    __LOAD_FACTOR = 0.75

    __initial_capacity: int = None

    __current_capacity: int = None

    __nodes = None

    __expansion_nodes = None

    def __init__(self, initial_capacity: int = 15) -> None:
        if initial_capacity is None or initial_capacity <= 0:
            self.__initial_capacity = 15
        else:
            self.__initial_capacity = initial_capacity
        self.__current_capacity = 0
        self.__nodes: list[HashAssemble.Node[K, V] | None] = [None] * self.__initial_capacity
        self.__expansion_nodes: None = None

    def __handler(self, flag):
        if flag == 'a':
            self.__current_capacity += 1
        else:
            self.__current_capacity -= 1

    def __setattr__(self, key, value):
        if hasattr(self, key):
            super().__setattr__(key, value)
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")

    def __getIdCode(self, key: K) -> int:
        try:
            code = hash(key)
        except TypeError:
            code = id(key)
        return abs(code) % self.__initial_capacity

    def __expansion(self):
        self.__initial_capacity *= 2
        self.__expansion_nodes: list[HashAssemble.Node[K, V] | None] = [None] * self.__initial_capacity
        for node in self.__nodes:
            while node is not None:
                idCode: int = self.__getIdCode(node.key)
                if self.__expansion_nodes[idCode] is None:
                    self.__expansion_nodes[idCode] = node
                else:
                    self.__expansion_nodes[idCode].putNodeToLast(node)
                node = node.getNextDifferenceIdNode(idCode, self.__getIdCode)
        self.__nodes = self.__expansion_nodes
        self.__expansion_nodes = None

    def put(self, key: K, value: V) -> None:
        if self.__current_capacity / self.__initial_capacity >= HashAssemble.__LOAD_FACTOR:
            self.__expansion()
        idCode: int = self.__getIdCode(key)
        if self.__nodes[idCode] is None:
            self.__nodes[idCode] = HashAssemble.Node(key, value)
            self.__current_capacity += 1
        elif self.__nodes[idCode].key == key or self.__nodes[idCode].key is key:
            self.__nodes[idCode].value = value
        else:
            self.__nodes[idCode].putNextNode(key, value, self.__handler)

    def get(self, key: K) -> V:
        idCode: int = self.__getIdCode(key)
        if self.__nodes[idCode] is None:
            return None
        elif self.__nodes[idCode].key == key or self.__nodes[idCode].key is key:
            return self.__nodes[idCode].value
        else:
            return self.__nodes[idCode].getNextNode(key)

    def remove(self, key: K) -> V:
        idCode: int = self.__getIdCode(key)
        if self.__nodes[idCode] is None:
            return None
        elif self.__nodes[idCode].key == key or self.__nodes[idCode].key is key:
            value = self.__nodes[idCode].value
            self.__nodes[idCode] = self.__nodes[idCode].nextNode
            self.__current_capacity -= 1
            return value
        else:
            return self.__nodes[idCode].removeNextNode(key, self.__handler)

    def __len__(self):
        return self.__current_capacity

    def clean(self) -> None:
        self.__current_capacity = 0
        self.__initial_capacity = 15
        self.__nodes = [None] * self.__initial_capacity

    class Node(Generic[K, V]):

        key: K = None

        value: V = None

        def __init__(self, key: K, value: V) -> None:
            self.key = key
            self.value = value
            self.nextNode: [HashAssemble.Node | None] = None

        def putNextNode(self, key: K, value: V, handler: callable(str)) -> None:
            if self.nextNode is None:
                self.nextNode = HashAssemble.Node(key, value)
                handler('a')
            elif self.nextNode.key == key or self.nextNode.key is key:
                self.nextNode.value = value
            else:
                return self.nextNode.putNextNode(key, value, handler)

        def getNextNode(self, key: K) -> V:
            if self.nextNode is None:
                return None
            elif self.nextNode.key == key or self.nextNode.key is key:
                return self.nextNode.value
            else:
                return self.nextNode.getNextNode(key)

        def removeNextNode(self, key: K, handler: callable(str)) -> V:
            if self.nextNode is None:
                return None
            elif self.nextNode.key == key or self.nextNode.key is key:
                value = self.nextNode.value
                self.nextNode = self.nextNode.nextNode
                handler('r')
                return value
            else:
                return self.nextNode.removeNextNode(key, handler)

        def putNodeToLast(self, node: Generic[K, V]) -> None:
            if self.nextNode is None:
                self.nextNode = node
            else:
                self.nextNode.putNodeToLast(node)

        def getNextDifferenceIdNode(self, idCode: int, getIdCode: callable(K)) -> Generic[K, V]:
            if self.nextNode is None:
                return None
            differenceIdCode = getIdCode(self.nextNode.key)
            if differenceIdCode == idCode:
                return self.nextNode.getNextDifferenceIdNode(idCode, getIdCode)
            else:
                eNode: HashAssemble.Node[K, V] = self.nextNode
                self.nextNode = None
                return eNode

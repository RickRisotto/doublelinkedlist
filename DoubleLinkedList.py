from typing import Any, Sequence, Optional
from main import LinkedList
from abc import ABC, abstractmethod
import sqlite3
import os


""" Script takes nums and add two-way-linked list 
    into txt file or db according to strategy chosen"""


class Node:
    def __init__(self, val: Any, next_: Optional['Node'] = None):
        self.val = val
        self.next = next_

    @property
    def next(self):
        return self.__next

    @next.setter
    def next(self, next_: Optional['Node']):
        if not isinstance(self, self.__class__) and next_ is not None:
            msg = f"value passed must be {self.__class__.__name__} instance," \
                  f"not {next_.__class__.__name__} instance"
            print(msg)
            raise TypeError
        self.__next = next_

    def __repr__(self):
        return f"({self.val}, {self.next})"

    def __str__(self):
        return f"{self.val}"


class Context:
    def __init__(self, strategy: ['Strategy'], dll: ['Doublelinkedlist'], name, schema) -> None:
        self._strategy = strategy
        self.dll = dll
        self.name = name
        self.schema = schema

    @property
    def strategy(self) -> 'Strategy':
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: ['Strategy']):
        self._strategy = strategy

    def implement(self):
        result = self.strategy.write(self.dll, self.name, self.schema)
        return result


class Strategy(ABC):

    @abstractmethod
    def write(self, data: list, name, schema):
        pass


class StrategyA(Strategy):
    def write(self, dll: ['Doublelinkedlist'], name, schema=None):
        print(f"writing to txt file...")
        with open(f"{name+'.txt'}", 'w') as f:
            f.write(str(dll))
            print('dll written successfully...')


class StrategyB(Strategy):
    def write(self, dll: ['Doublelinkedlist'], name, schema):
        name = name + '.db'
        db_exists = os.path.exists(name)
        connect = sqlite3.connect(name)
        if not db_exists:
            print('creating schema...')
            filename = os.path.join((os.path.dirname(__file__)), f"venv/{schema}")
            with open(filename, 'r') as file:
                schema = file.read()
                connect.executescript(schema)
                print('Done!')
        else:
            print('db exists')
            connect = sqlite3.connect(name)
            se = str(dll)
            lst = []
            for i in se:
                if i.isdigit():
                    lst.append(i)
            lst = (''.join(lst), )  # create tuple from list
            tuple_list = [lst]
            for row in tuple_list:
                try:
                    with connect:
                        print(f"writing to db...")
                        query1 = '''insert into dll (Forward) values (?)'''
                        connect.execute(query1, row)
                        print('written...')
                except sqlite3.OperationalError as oe:
                        msg = f"Error occured: No such table:{name}"
                        print(msg, oe)
                connect.close()


class Doublelinkedlist(LinkedList):
    class TwoWayLinkedNode(Node):
        def __init__(self, val, prev: Optional['Node'] = None, next_: Optional['Node'] = None):
            super().__init__(val, next_)
            self.prev = prev

        def __repr__(self):
            return f"two_way_linked_node({self.val}, next_={next_}, prev={prev})"

    def __init__(self, data: Sequence = None):
        super().__init__(data)
        if data:
            if self.pointer is None:
                self.append_value(data)

    def append_value(self, data):  # overridden method
        for item in data:
            nod = self.TwoWayLinkedNode(item)
            nod.next = self.pointer
            if self.pointer is not None:
                self.pointer.prev = nod
            self.pointer = nod

    def __str__(self):  # overridden method
        forward = []
        backward = []
        last = None
        n = self.pointer
        while n is not None:
            backward.append(n.val)
            last = n
            n = n.next
        while last is not None:  # regular ll can be returned
            forward.append(last.val)
            last = last.prev
        return f"{backward}"


if __name__=="__main__":
    res = Doublelinkedlist([1, 2, 3, 4, 5])
    context = Context(StrategyA(), res, 'test', 'schema.sql')
    #context = Context(StrategyB(), res, 'test', 'schema.sql')
    output = context.implement()
    print(output)





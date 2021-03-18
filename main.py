from typing import Any, Sequence, Optional


class LinkedList:
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
                raise TypeError
            self.__next = next_

        def __repr__(self):
            return f"({self.val}, {self.next})"

        def __str__(self):
            return f"{self.val}"

    def __init__(self, data: Sequence = None):
        self.__len = 0
        self.pointer = None
        self.data = data

        if data:
            if self.pointer is None:
                self.append_value(data)

    def __str__(self):
        res = []
        while self.pointer is not None:
            res.append(self.pointer.val)
            self.pointer = self.pointer.next
        return f"singly linked list: {res}"

    def __repr__(self):
        return self

    def __len__(self) -> int:
        return self.__len

    def __node_hop(self, index: int) -> 'Node':
        if not isinstance(index, int):
            raise TypeError()
        if not 0 <= index < self.__len:
            raise IndexError
        current_node = self.pointer
        for _ in range(index):
            current_node = current_node.next
        return current_node

    def append_value(self, data):
        if data:
            node = self.Node(data.pop(0))
            self.pointer = node
            for i in data:
                node.next = self.Node(i)
                node = node.next

    def __getitem__(self, item: int) -> Any:
        current_node = self.__node_hop(item)
        return current_node.val

    def __iter__(self):
        return self .get_current_index()

    def get_current_index(self):
        for current_index in range(self.__len):
            yield self[current_index]

    def __next__(self):
        while self.__len < len(self.data):
            value = self.data[self.__len]
            self.__len += 1
            return value
        raise StopIteration


if __name__ == "__main__":
    start = LinkedList([1, 2, 3, 4, 5, 6, 7, 8, 9])
    print(start)





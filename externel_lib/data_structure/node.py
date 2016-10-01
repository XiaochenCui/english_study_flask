class Node(object):
    def __init__(self, key=None, init_data=None, next_node=None):
        self.key = key
        self.data = init_data
        self.next = next_node

    def get_data(self):
        return self.data

    def get_next(self):
        return self.next

    def set_data(self, new_data):
        self.data = new_data

    def set_next(self, new_next):
        self.next = new_next

    def __repr__(self):
        return '{cls}: {key}--{data}'.format(cls=self.__class__.__name__,
                                             key=self.key,
                                             data=self.data)

    __str__ = __repr__


class SimpleNode(object):
    def __init__(self, key=None, data=None):
        self._key = key
        self._data = data

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value


class TreeNode(object):
    def __init__(self, key, init_data, parent=None, left=None, right=None):
        self.key = key
        self.data = init_data
        self.parent = parent
        self.left = left
        self.right = right

    def has_left_child(self):
        return self.left

    def has_right_child(self):
        return self.right

    def is_left_child(self):
        return self.parent and self.parent.left == self

    def is_right_child(self):
        return self.parent and self.parent.right == self

    def is_root(self):
        return not self.parent

    def is_lead(self):
        return not (self.left and self.right)

    def has_any_child(self):
        return self.left or self.right

    def has_both_child(self):
        return self.left and self.right

    def replace_node(self, key, data, left, right):
        self.key = key
        self.data = data
        self.left = left
        self.right = right
        if self.has_left_child():
            self.left.parent = self
        if self.has_right_child():
            self.right.parent = self

    def __repr__(self):
        return '{cls}: (key:{key}, data:{data}, head:{head}, left:{left}, right:{right})' \
            .format(cls=self.__class__.__name__,
                    key=self.key,
                    data=self.data,
                    head=self.parent.key if self.parent else None,
                    left=self.left.key if self.left else None,
                    right=self.right.key if self.right else None,
                    )

    __str__ = __repr__


if __name__ == '__main__':
    temp = Node('he', 93)
    print(temp.get_data())
    print(temp)
    tn1 = TreeNode('tank', 20)
    tn2 = TreeNode('plane', 99)
    tn3 = TreeNode('ship', 1)
    tn1.left = tn2
    tn1.right = tn3
    tn2.parent = tn1
    tn3.parent = tn1
    print(tn1)
    print(tn2)
    print(tn3)

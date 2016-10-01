from cxctools.string import char_at

from externel_lib.data_structure.queue import Queue


class Node(object):
    R = 256

    def __init__(self, value=None, r=R):
        self.value = value
        self.next = [None] * r

    @property
    def children(self):
        return [i for i in self.next if i]


class TrieST(object):
    def __init__(self):
        self.root = Node()

    def __setitem__(self, key, value):
        self.put(key, value)

    def put(self, key: str, value):
        self._put(self.root, key, value, 0)

    def _put(self, node: Node, key: str, value, d: int):
        # node 可能为空
        if not node:
            node = Node()

        # 如果找到了，赋值并返回
        if len(key) == d:
            node.value = value
            return node

        # 计算下一位的索引
        index = char_at(key, d)
        node.next[index] = self._put(node.next[index], key, value, d + 1)

        # 返回node
        return node

    def __getitem__(self, item):
        return self.get(item)

    def get(self, key: str):
        return self._get(self.root, key, 0)

    def _get(self, node: Node, key: str, d: int):
        if not node:
            return None

        if len(key) == d:
            return node.value

        index = char_at(key, d)
        return self._get(node.next[index], key, d + 1)

    def keys(self):
        return self.keys_with_prefix('')

    def keys_with_prefix(self, pre: str):
        q = Queue()
        self.collection(self.root, pre, q)
        return q.items

    def collection(self, node: Node, pre: str, q: Queue):
        if not node:
            return

        if node.value:
            q.en_queue({pre: node.value})

        # 遍历子节点
        for i in range(node.R):
            self.collection(node.next[i], pre + chr(i), q)

    def __repr__(self):
        return str(self.keys())


if __name__ == '__main__':
    t = TrieST()
    t['test']=1
    print(t['test'])
    print(t.keys())

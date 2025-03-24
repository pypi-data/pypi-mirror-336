class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

class Queue:
    def __init__(self):
        self.head = None
        self.curr = None

    def push(self, val):
        if self.head:
            new = Node(val)
            self.curr.next = new
            self.curr = new
        else:
            self.head = Node(val)
            self.curr = self.head

    def pop(self):
        val = None
        if self.head:
            val = self.head.val
            self.head = self.head.next if self.head.next else None
        return val

    def __repr__(self):
        queue = []
        temp = self.head
        while temp:
            queue.append(temp.val)
            temp = temp.next
        return str(queue)

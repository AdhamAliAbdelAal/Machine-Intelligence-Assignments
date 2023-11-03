from queue import PriorityQueue

class CustomClass:
    def __init__(self, name):
        self.name = name

queue: PriorityQueue = PriorityQueue()

# Adding elements to the queue
queue.put((3, 1,CustomClass('bbbbbbbbbbbbb 1')))
queue.put((1,1, CustomClass('zzzzzzzzzzzzz')))
queue.put((1,3, CustomClass('aaaaaaaaa')))

# Removing elements from the queue
while not queue.empty():
    item = queue.get()
    print(item[2].name)

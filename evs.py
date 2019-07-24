import mdb
import ecs

from collections import defaultdict
from collections import deque

class Event:
    @classmethod
    def get_id(cls):
        return cls.__name__
    @classmethod
    def is_instance(cls, inst):
        return isinstance(inst, cls)
        
class EventHandler:
    def recv_event(self, event):
        pass
    
class EventSystem(ecs.System):
    def __init__(self):
        ecs.System.__init__(self)
        self.event_handlers = defaultdict(list)
        self.event_queue = deque()

    def add_event_handler(self, event_cls, event_handler):
        event_id = event_cls.get_id()
        self.event_handlers[event_id].append(event_handler)
   
    def send_event(self, event):
        event_id = event.get_id()
        for event_handler in self.event_handlers[event_id]:
            event_handler.recv_event(event)

    def post_event(self, event):
        self.event_queue.append(event)

    def update(self):
        while self.event_queue:
            event = self.event_queue.pop()
            self.send_event(event)

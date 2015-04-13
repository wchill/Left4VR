__author__ = 'Eric Ahn'

class Event:
    EVENT_KEYBOARD = 0
    EVENT_KEYBOARD_TOGGLE = 1
    EVENT_MOUSE = 2
    EVENT_OTHER = 3

    def __init__(self, event_type=0, data=list()):
        self.event_type = event_type
        self.enabled = False
        if self.event_type == Event.EVENT_KEYBOARD or self.event_type == Event.EVENT_MOUSE:
            self.data = []
            for i in data:
                self.data.append(int(self.data))
        else:
            self.data = data

    def toggle(self):
        self.enabled = not self.enabled
        return self.enabled
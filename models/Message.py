from enum import Enum

class Message:
    level = Enum("MessageLevel", [("info", 1), ("warning", 2), ("error", 3)])
    content = ""

    def __init__(self, level, content):
        self.level = level
        self.content = content

    @staticmethod
    def from_string_list(level, string_list):
        messages = []
        for string in string_list:
            messages.append(Message(level, string))

        return messages

    class Level(Enum):
        info = 1
        warning = 2
        error = 3

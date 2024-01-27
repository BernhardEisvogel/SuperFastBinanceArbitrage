

class BellmanFordError(Exception):
    def __init__(self, message, fatal = False):
        self.message = message
        if fatal:
            quit()


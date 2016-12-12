from lib.basehandler import BaseWebSocket


class Commands(BaseWebSocket):

    def add(self, a, b):

        return a + b

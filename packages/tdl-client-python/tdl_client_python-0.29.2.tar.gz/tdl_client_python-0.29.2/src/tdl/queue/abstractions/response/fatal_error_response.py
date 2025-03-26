
class FatalErrorResponse:

    def __init__(self, message):
        self._message = message
        self.result = message
        self.id = "error"

import json

class Request:

    def __init__(self, method, params, id_):
        self.method = method
        self.params = params
        self.id = id_

    @staticmethod
    def deserialize(message_json, audit):
        try:
            decoded_message = json.loads(message_json)
            return Request(
                decoded_message['method'],
                decoded_message['params'],
                decoded_message['id'])
        except:
            audit.log_line('Invalid message format')
            raise

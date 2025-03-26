import json
from collections.abc import Sequence


class PresentationUtils:

    @staticmethod
    def to_displayable_request(params):
        compressed_params = []
        for param in params:
            representation = PresentationUtils.serialize_and_compress(param)
            compressed_params.append(representation)
            
        return ', '.join(compressed_params)

    @staticmethod
    def to_displayable_response(value):
        return PresentationUtils.serialize_and_compress(value)

    @staticmethod
    def serialize_and_compress(value):
        representation = json.dumps(value, separators=(',', ':'))

            # result is array-like, needs a bit more spacing
        if PresentationUtils.is_list(value):
            representation = representation.replace(',', ', ')
        elif PresentationUtils.is_multiline_string(representation):
            representation = PresentationUtils.suppress_extra_lines(representation)

        return representation


    @staticmethod
    def is_list(value):
        return isinstance(value, Sequence) and not isinstance(value, str)

    @staticmethod
    def is_multiline_string(value):
        return "\\n" in value

    @staticmethod
    def suppress_extra_lines(parameter):
        if not isinstance(parameter, str):
            return str(parameter)
    
        parts = parameter.split("\\n")
        representation = parts[0]
    
        suppressed_parts = len(parts) - 1
        representation += " .. ( "+ str(suppressed_parts) +" more line"
    
        if suppressed_parts > 1:
            representation += "s"
    
        representation += " )\""
        return representation

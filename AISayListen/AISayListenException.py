from typing import Union, Any

class AISayListenException(Exception):
    pass

class AISayListenGttsError(AISayListenException):

    def __init__(self, speech: str):
        self.error = f'Could not use gtts to make the AI talk buf was [{speech}]'

    def __str__(self):
        return self.error

    __repr__ = __str__

class AISayListenAttributeTypeError(AISayListenException):

    def __init__(self, var_name: str, ai: Any):
        self.error = 'Invalid value set of {var_name} -> {ai}'

    def __str__(self):
        return self.error

    __repr__ = __str__

class AISayListenAttributeValueError(AISayListenException):

    def __init__(self, context):
        self.error = context

    def __str__(self):
        return self.error

    __repr__ = __str__

class AISayListenSpeakEnablingError(AISayListenException):

    def __str__(self):
        return "self.can_speak is not True"

    __repr__ = __str__

class AISayListenMicrophoneError(AISayListenException):

    def __init__(self, context):
        self.error = context

    def __str__(self):
        return self.error

    __repr__ = __str__

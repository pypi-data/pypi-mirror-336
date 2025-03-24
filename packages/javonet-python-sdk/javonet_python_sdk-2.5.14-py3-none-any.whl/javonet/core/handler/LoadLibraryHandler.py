from javonet.core.handler.AbstractCommandHandler import *
import sys
import os

class LoadLibraryHandler(AbstractCommandHandler):

    loaded_directories = []

    def __init__(self):
        self._required_parameters_count = 1

    def process(self, command):
        try:
            if len(command.payload) != self._required_parameters_count:
                raise Exception("LoadLibrary payload parameters mismatch")

            if os.path.isdir(command.payload[0]):
                sys.path.append(command.payload[0])
                LoadLibraryHandler.loaded_directories.append(command.payload[0])
            else:
                raise Exception(command.payload[0] + " is not a valid directory")

            return 0
        except Exception as e:
            exc_type, exc_value = type(e), e
            new_exc = exc_type(exc_value).with_traceback(e.__traceback__)
            raise new_exc from None

    @staticmethod
    def get_loaded_directories():
        return LoadLibraryHandler.loaded_directories
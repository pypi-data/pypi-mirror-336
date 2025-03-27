from ..language_object import CoreObjectInterface


class System(CoreObjectInterface):
    def __init__(self):
        self.functions = {
            "EXIT": self._exit,
            "DEBUG": self._debug,
            "OBJ": self._obj,
        }

    def _exit(self, *args):
        result = None
        if len(args) > 0:
            result = self.executor.execute_line(args)
        self.executor.stopped = True
        return result

    def _debug(self, *args):
        if len(args) > 1:
            print(self.executor.execute_line(args))
        elif len(args) == 1:
            print(args[0])
        else:
            print("DEBUG")

    def _obj(self, *args):
        if len(args) == 1:
            return args[0]
        return args

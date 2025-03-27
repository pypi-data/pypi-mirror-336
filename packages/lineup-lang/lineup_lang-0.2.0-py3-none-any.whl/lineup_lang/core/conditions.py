from ..language_object import CoreObjectInterface
from ..line_decoder import LineDecoder
from ..error import LineupError


class Conditions(CoreObjectInterface):
    last_result = None
    version = None

    equal_signs = {
        "EQ": "==",
        "NE": "!=",
        "GT": ">",
        "GE": ">=",
        "LT": "<",
        "LE": "<=",
        "==": "==",
        "!=": "!=",
        ">": ">",
        ">=": ">=",
        "<": "<",
        "<=": "<=",
    }

    def __init__(self):
        self.functions = {
            "IF": self._if,
            "NOTIF": self._notif,
            "ELSE": self._else,
        }

    def _execute_jump(self, jump_size: str):
        if jump_size.startswith("*"):
            self.executor.execute_line(["JUMP", jump_size[1:]])
        else:
            self.executor.execute_line(["GOTO", jump_size])

    def _if(self, jump_size: str, *args):
        result = self._execute_condition(*args)
        if result:
            self.last_result = True
            self._execute_jump(jump_size)
        self.last_result = False
        return result

    def _notif(self, jump_size: str, *args):
        result = self._execute_condition(*args)
        if not result:
            self.last_result = True
            self._execute_jump(jump_size)
        self.last_result = False
        return result

    def _else(self, *args):
        if self.last_result is None:
            raise LineupError("ELSE without IF")
        if not self.last_result:
            self._execute_jump(args[0])
        self.last_result = False

    def _execute_condition(self, *args):
        if len(args) == 3 and args[1] in self.equal_signs.keys():
            return self._equal(args[0], args[1], args[2])
        return self.executor.execute_line(args)

    def _equal(self, arg1: str, sign: str, arg2: str) -> bool:
        sign = self.equal_signs[sign]
        line_decoder = LineDecoder()
        arg1 = line_decoder.decode(arg1)
        arg2 = line_decoder.decode(arg2)
        result_1 = self.executor.execute_line(arg1)
        result_2 = self.executor.execute_line(arg2)
        match sign:
            case "==":
                return result_1 == result_2
            case "!=":
                return result_1 != result_2
            case ">":
                return result_1 > result_2
            case ">=":
                return result_1 >= result_2
            case "<":
                return result_1 < result_2
            case "<=":
                return result_1 <= result_2
        return False

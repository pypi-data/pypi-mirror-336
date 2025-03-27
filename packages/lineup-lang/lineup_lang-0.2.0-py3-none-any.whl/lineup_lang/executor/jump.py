from .default import DefaultExecutor
from ..error import ExecutorFunctionNotExistError, LineupError
from typing import Any, List


class JumperOffsetInvalidError(LineupError):
    pass


class JumperExecutor(DefaultExecutor):
    jump_functions = ["JUMP", "GOTO"]
    line = 0
    # Executor version - it's set on the lineup version
    _version = None

    def jump(self, offset: int):
        if offset == 0:
            raise JumperOffsetInvalidError("The offset can't be 0")
        self.line += offset - 1
        self.logger.debug(f"Jump to line: {self.line + 1}")

    def goto(self, line: int):
        """
        Execute the line passed as argument
        """
        if line <= 0:
            raise JumperOffsetInvalidError("The line can't be 0")
        # -2 because the line is 1-based and the list is 0-based
        # and -1 because the line we want will be the next one
        self.line = line - 2
        self.logger.debug(f"Go to line: {self.line + 1}")

    def execute_jump(self, line: List[str]):
        if len(line) != 2:
            raise ExecutorFunctionNotExistError(
                f"'{line[0]}' need 1 argument, got {len(line) - 1}")
        match line[0]:
            case "JUMP":
                return self.jump(int(line[1]))
            case "GOTO":
                return self.goto(int(line[1]))
        raise ExecutorFunctionNotExistError(
            f"'{line[0]}' not exist in '{self}'")

    def execute_line(self, line: List[str]):
        if line[0] in self.jump_functions:
            self.logger.debug(f"Execute: {line}")
            return self.execute_jump(line)
        return super().execute_line(line)

    def execute(self, script: List[List[str]]) -> Any:
        self.stop = False
        result = None
        self.line = 0
        while self.line < len(script):
            if self.stopped:
                break
            result = self.execute_line(script[self.line])
            self.line += 1
        return result

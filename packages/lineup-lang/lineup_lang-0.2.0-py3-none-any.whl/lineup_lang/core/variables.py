from ..language_object import CoreObjectInterface, LanguageObjectInterface
from ..error import LineupError
from typing import Dict, Any, List, Tuple


class VariableNotExistError(LineupError):
    pass


class VariableNotLanguageObjectError(LineupError):
    pass


class Variables(CoreObjectInterface):
    variables: Dict[str, Any]
    default_variables: List[str]
    version = None

    def __init__(self, variables: Dict[str, Any] | None) -> None:
        if variables is None:
            variables = {}
        self.variables = variables
        self.default_variables = list(variables.keys())
        self.default_values = variables.copy()
        self.functions = {
            "VAR": self._variable,
        }

    def close(self):
        super().close()
        for key in list(self.variables.keys()):
            if isinstance(self.variables[key], LanguageObjectInterface):
                self.variables[key].close()
            self.variables.pop(key)

    def reset(self):
        error = []
        error += self._reset_disregard()
        error += self._reset_default()
        if error:
            for key, e in error:
                self.logger.error(f"Error at close with {key}: {e}")
            raise LineupError(f"Error with {len(error)} variables")

    def _reset_disregard(self) -> List[Tuple[str, Exception]]:
        variables_to_delete = [key for key in self.variables.keys()
                               if key not in self.default_variables]
        error = []
        for key in variables_to_delete:
            if isinstance(self.variables[key], LanguageObjectInterface):
                self.logger.debug(f"{self} close {key}")
                try:
                    self.variables[key].close()
                except Exception as e:
                    error.append((key, e))
            self.variables.pop(key)
        return error

    def _reset_default(self) -> List[Tuple[str, Exception]]:
        error = []
        for key in self.variables.keys():
            if isinstance(self.variables[key], LanguageObjectInterface):
                self.logger.debug(f"{self} reset {key}")
                try:
                    self.variables[key].reset()
                except Exception as e:
                    error.append((key, e))
            else:
                self.variables[key] = self.default_values[key]
        return error

    def _get(self, name: str):
        if name in self.variables:
            return self.variables[name]
        msg = f"'{name}' not exist in '{self}'"
        self.logger.error(msg)
        raise VariableNotExistError(msg)

    def _set(self, name: str, value):
        self.variables[name] = value

    def _delete(self, name: str):
        if name not in self.variables:
            raise VariableNotExistError(f"'{name}' not exist in '{self}'")
        del self.variables[name]

    def _execute_in_variables(self, variables, function_name: str, *args):
        if variables not in self.variables:
            raise VariableNotExistError(f"'{variables}' not exist in '{self}'")
        if not isinstance(self.variables[variables], LanguageObjectInterface):
            raise VariableNotLanguageObjectError(f"'{variables}' is not a LanguageObjectInterface in '{self}'")
        return self.variables[variables].execute(function_name, *args)

    def _execute_from_executor(self, line: List[str]):
        return self.executor.execute_line(line)

    def _exit(self, *args):
        self.executor.stop = True
        return self._execute_from_executor(args)

    def _variable(self, name: str, command: str, *args):
        match command:
            case "GET":
                return self._get(name)
            case "SET":
                self._set(name, args[0])
            case "USE":
                return self._set(name, self._execute_from_executor(args))
            case "UNSET":
                self._delete(name)
            case "EXEC":
                return self._execute_in_variables(name, *args)
            case _:
                return self._execute_in_variables(name, command, *args)
        return None

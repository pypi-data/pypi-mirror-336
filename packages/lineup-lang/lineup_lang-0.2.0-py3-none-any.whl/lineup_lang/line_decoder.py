from .error import DecodeLineStringError
from typing import List
import regex as re
import json


class LineDecoder:
    """
    Decode a line string to an instruction list
    """

    def decode(self, line: str) -> List[str] | None:
        """
        Decode a line string to an instruction list
        """
        line = line.strip()
        if line.startswith("#"):
            return None
        # delete comments on the line
        line = self._delete_comments(line)
        line_splitted = self._split_line(line)
        if not line_splitted:
            return None
        return line_splitted

    def _delete_comments(self, line: str) -> str:
        """
        Delete the comments on the line
        """
        lines = line.split("#")
        result = []
        for i in lines:
            i, _ = self._format_escape(i, False, "#")
            result.append(i)
            if len(i) == 0 or i[-1] != "#":
                break
        return "".join(result)

    def _split_line(self, line: str) -> List[str]:
        lines = self.format_quotes(line)
        result = []
        if len(lines) % 2 == 0:
            raise DecodeLineStringError(f"'{line}' is not valid line string")
        # odd is inside quotes, even is outside
        for i, line in enumerate(lines):
            if i % 2 == 1:
                # inside quotes, the line has to be kept as is
                try:
                    result.append(json.loads(f'"{line}"'))
                except json.JSONDecodeError:
                    raise DecodeLineStringError(f"'{line}' is not valid line string")
            else:
                # outside quotes, split by space for get the instructions
                result.extend([
                    x for x in line.split(" ") if x.strip() != ""
                ])
        return result

    def format_quotes(self, line: str) -> List[str]:
        """
        Format the quotes in the line

        Split the line by quotes, keep the backslahed quotes
        Return a list of odd is inside quotes, even is outside the quotes
        """
        lines = line.split('"')
        result = []
        current_line = ""
        if len(lines) == 1:
            return [line]
        for i in lines:
            # if len(i) % 2 != 1 it means that the line is inside quotes
            # because we don't already write on odd indexes
            i, is_ended = self._format_escape(i, len(result) % 2 == 1)
            current_line += i
            if is_ended:
                result.append(current_line)
                current_line = ""
        if current_line:
            raise DecodeLineStringError(f"'{line}' is not valid line string")
        return result

    def _format_escape(self, line: str, inside_quotes: bool,
                       ended_char: str = '"') -> tuple[str, bool]:
        """
        Format the escape characters in the line"
        """
        if not line:
            return line, True
        nb_backslash_at_end = self.count_backslash_at_end(line)
        if nb_backslash_at_end == 0:
            return line, True
        if not inside_quotes:
            # Outside a quote, we have to remove the backslashes ourselves
            line = line[:-nb_backslash_at_end] + ("\\" * (nb_backslash_at_end // 2))
        # Inside a quote, it's JSON, so we have to keep the backslashes
        if nb_backslash_at_end % 2 == 0:
            return line, True
        line = line + ended_char
        return line, False

    def count_backslash_at_end(self, line: str) -> int:
        """
        Count the number of backslashes at the end of the line
        """
        nb_backslash = 0
        for i in range(len(line) - 1, -1, -1):
            if line[i] == "\\":
                nb_backslash += 1
            else:
                break
        return nb_backslash

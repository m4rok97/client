import re
from typing import List
import argparse


class SmartFormatter(argparse.HelpFormatter):
    """
    from https://gist.github.com/panzi/b4a51b3968f67b9ff4c99459fb9c5b3d
    """

    def _split_lines(self, text: str, width: int) -> List[str]:
        lines: List[str] = []
        for line_str in text.split('\n'):
            line: List[str] = []
            line_len = 0
            for word in line_str.split():
                word_len = len(word)
                next_len = line_len + word_len
                if line: next_len += 1
                if next_len > width:
                    lines.append(' '.join(line))
                    line.clear()
                    line_len = 0
                elif line:
                    line_len += 1

                line.append(word)
                line_len += word_len

            lines.append(' '.join(line))
        return lines

    def _fill_text(self, text: str, width: int, indent: str) -> str:
        return '\n'.join(indent + line for line in self._split_lines(text, width - len(indent)))


def desc(txt):
    return {'help': txt, 'description': txt}


def key_value_t(x):
    if "=" not in x:
        raise argparse.ArgumentTypeError("format must be key=value")
    return x


def time_t(x):
    if not re.match(r"([0-9]+-)?([0-9]+:)?[0-9]+:[0-9]+", x):  # [[dd-]hh:]mm:ss
        raise argparse.ArgumentTypeError("invalid time format")
    return x

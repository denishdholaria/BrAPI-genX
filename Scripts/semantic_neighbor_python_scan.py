#!/usr/bin/env python3
"""Suppress Python comments and syntactic docstrings during lexical field scans.

Only documentation-only spans are masked. Runtime string literals, mapping
keys, attribute access and expressions remain visible to a conservative scan.
"""
from __future__ import annotations

import ast
import io
import tokenize


def executable_python_lines(source: str) -> list[str]:
    """Return source lines with Python comment/docstring spans masked to spaces.

    Keep line numbers and all executable characters unchanged. If Python's
    parser or tokenizer cannot inspect the file, return the original text
    instead of accidentally suppressing a potentially meaningful reference.
    """
    original = source.splitlines()
    try:
        tree = ast.parse(source)
        tokens = list(tokenize.generate_tokens(io.StringIO(source).readline))
    except (SyntaxError, IndentationError, tokenize.TokenError):
        return original

    lines = [list(line) for line in original]

    def mask(start_line: int, start_col: int, end_line: int, end_col: int) -> None:
        for row in range(start_line - 1, end_line):
            if not (0 <= row < len(lines)):
                continue
            lo = start_col if row == start_line - 1 else 0
            hi = end_col if row == end_line - 1 else len(lines[row])
            for col in range(max(0, lo), min(len(lines[row]), hi)):
                lines[row][col] = ' '

    for node in ast.walk(tree):
        if not isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if not node.body:
            continue
        first = node.body[0]
        if (isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
                and first.end_lineno is not None
                and first.end_col_offset is not None):
            mask(first.lineno, first.col_offset,
                 first.end_lineno, first.end_col_offset)
    for token in tokens:
        if token.type == tokenize.COMMENT:
            mask(token.start[0], token.start[1], token.end[0], token.end[1])
    return [''.join(line) for line in lines]


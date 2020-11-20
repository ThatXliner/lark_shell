#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# type: ignore
"""
Initial author: Bryan Hu .

@ThatXliner .

Version: v0.1.3

An implementation of https://lark-parser.github.io/lark/ide/app.html in the terminal.

For playing with Lark.

"""
# TODO: Add command-line arguments and argparse support
import sys

import lark
import urwid
import warnings

__version__ = "0.1.3"
output = urwid.SelectableIcon(("wait", "Output waiting..."))  # Initially wait for input
meta = urwid.SelectableIcon(
    ("success", f"Lark version: {lark.__version__}\nLark_shell version: {__version__}")
)


def _update_grammar(_, new_text: str) -> None:
    """Update the UI when the grammar changes."""
    _parse(new_text, grammar_input.get_edit_text(), output)


def _parse(grammar: str, parse_input: str, output_obj: urwid.Text) -> None:
    """Update the UI with the given grammar and input."""
    try:
        # Create a parser with "earley"
        parser = lark.Lark(grammar, parser="earley", lexer="auto")
        # Generate a tree
        tree = parser.parse(parse_input)

    except (lark.exceptions.GrammarError, TypeError):
        output_obj.set_text(("error", "Incomplete grammar!"))

    except lark.exceptions.UnexpectedEOF as e:
        output_obj.set_text(("error", str(e)))

    except lark.exceptions.UnexpectedInput as e:
        output_obj.set_text(("error", str(e.get_context(parse_input))))

    except FileNotFoundError:  # The relative imported file was not found
        output_obj.set_text(("error", "File not found"))

    except lark.exceptions.LarkError as e:
        output_obj.set_text(("error", repr(e)))

    else:  # Parsing succeeded
        output_obj.set_text(("success", str(tree.pretty())))


def _update_input(_, new_input: str) -> None:
    """Update the UI when the input changes."""
    _parse(lark_grammar.get_edit_text(), new_input, output)


lark_grammar = urwid.Edit(("bold", "Grammar\n"), multiline=True, allow_tab=True)
grammar_input = urwid.Edit(("bold", "Grammar input\n"), multiline=True, allow_tab=True)

urwid.connect_signal(lark_grammar, "change", _update_grammar)
urwid.connect_signal(grammar_input, "change", _update_input)

UI = [
    urwid.LineBox(lark_grammar),
    urwid.LineBox(grammar_input),
    urwid.Divider(div_char="-"),
    output,
    urwid.Divider(div_char="-"),
    meta,
]
PALLETE = [
    ("bold", "bold", ""),
    ("wait", "yellow", ""),
    ("error", "light red", ""),
    ("success", "light green", ""),
]

loop = urwid.MainLoop(urwid.Filler(urwid.Pile(UI)), palette=PALLETE)
# We use urwid.Filler because it needs to be centered. If we left out urwid.Filler
# then urwid would scream at me. I want to replace urwid.Filler, though.
# - ThatXliner


def main() -> None:
    """The main CLI entry point.

    Returns
    -------
    None
        This function does not return anything.

    """
    try:
        loop.run()
    except KeyboardInterrupt:
        sys.exit(0)


class DeprecatedNameWarning(DeprecationWarning):
    pass


def deprecated_main() -> None:
    """The main CLI entry point that issues a deprecation warning

    Returns
    -------
    None
        This function does not return anything.

    """
    warnings.warn(
        "The executable lark_shell is deprecated. Use lark-shell instead.",
        DeprecatedNameWarning,
    )
    try:
        loop.run()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":  # Main entry point
    main()

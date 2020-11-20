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

# Constants
STATE_MAP = {"Earley": "earley", "LALR(1)": "lalr", "CYK": "cyk"}
# REVERSE_MAP = list(STATE_MAP.items())[::-1]
output = urwid.SelectableIcon(("wait", "Output waiting..."))  # Initially wait for input
meta = urwid.SelectableIcon(("success", f"Lark version: {lark.__version__}"))


def set_state(_, state):
    if not state:
        return
    assert state
    global current_selected_parser  # pylint: disable=W0603
    current_selected_parser = STATE_MAP[_.label]

    _parse(
        grammar=lark_grammar.get_edit_text(),
        parse_input=grammar_input.get_edit_text(),
        output_obj=output,
        chosen_parser=current_selected_parser,
    )


parser_list = []
earley = urwid.RadioButton(parser_list, "Earley", on_state_change=set_state)
lalr_1 = urwid.RadioButton(parser_list, "LALR(1)", on_state_change=set_state)
cyk = urwid.RadioButton(parser_list, "CYK", on_state_change=set_state)

assert len(parser_list) == 3

# Set default values
earley.set_state(True)
current_selected_parser = "earley"

assert earley.get_state()
assert (earley.get_state(), lalr_1.get_state(), cyk.get_state()) == (True, False, False)


def _parse(
    grammar: str, parse_input: str, output_obj: urwid.Text, chosen_parser: str
) -> None:
    """Update the UI with the given grammar and input."""
    try:
        # Create a parser with `chosen_parser`
        parser = lark.Lark(grammar, parser=chosen_parser, lexer="auto")

        # Generate a tree
        tree = parser.parse(parse_input)

    # Parsing errors
    except (lark.exceptions.GrammarError, TypeError):
        output_obj.set_text(("error", "Incomplete grammar!"))
    except lark.exceptions.ParseError as e:
        output_obj.set_text(("error", str(e)))
    except lark.exceptions.UnexpectedInput as e:
        output_obj.set_text(("error", str(e.get_context(parse_input))))

    # Importing errors
    except FileNotFoundError:  # The relative imported file was not found
        output_obj.set_text(("error", "File not found, did you spell it correctly?"))
    except KeyError as e:
        _ = e.args[0]  # The token
        # pylint: disable=E1101
        output_obj.set_text(("error", f"Could not import {_.type.lower()} '{_.value}'"))
    except lark.exceptions.LarkError as e:  # Everything else
        output_obj.set_text(("error", repr(e)))

    else:  # Parsing succeeded
        output_obj.set_text(("success", str(tree.pretty())))


def _update_grammar(_, new_text: str) -> None:
    """Update the UI when the grammar changes."""
    _parse(new_text, grammar_input.get_edit_text(), output, current_selected_parser)


def _update_input(_, new_input: str) -> None:
    """Update the UI when the input changes."""
    _parse(lark_grammar.get_edit_text(), new_input, output, current_selected_parser)


lark_grammar = urwid.Edit(("bold", "Grammar\n"), multiline=True, allow_tab=True)
grammar_input = urwid.Edit(("bold", "Grammar input\n"), multiline=True, allow_tab=True)

# When the grammar is updated
urwid.connect_signal(lark_grammar, "change", _update_grammar)
# When the input is updated
urwid.connect_signal(grammar_input, "change", _update_input)


UI = [
    urwid.Columns(parser_list),
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

# We use urwid.Filler because it needs to be centered. If we left out urwid.Filler
# then urwid would scream at me. I want to replace urwid.Filler, though.
# - ThatXliner
loop = urwid.MainLoop(urwid.Filler(urwid.Pile(UI, focus_item=1)), palette=PALLETE)


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

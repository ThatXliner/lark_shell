#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# type: ignore
"""
Initial author: Bryan Hu .

@ThatXliner .

Version: v0.1.0

An implementation of https://lark-parser.github.io/lark/ide/app.html in the terminal.

For playing with Lark.

"""
import urwid
import lark
import sys

output = urwid.SelectableIcon(("wait", "Output waiting..."))
meta = urwid.SelectableIcon(("success", f"Lark-parser, version {lark.__version__}"))
the_input = ""


def handler(_, newtext):  # Lark parse here
    parse(newtext, the_input, output)


def parse(grammar, parse_input, output_obj):
    try:
        _ = lark.Lark(grammar)
        tree = _.parse(parse_input)

    except (lark.exceptions.GrammarError, TypeError):
        output_obj.set_text(("error", "Incomplete grammar!"))
    except (lark.exceptions.UnexpectedToken, lark.exceptions.UnexpectedEOF) as e:
        output_obj.set_text(("error", str(e)))
    except FileNotFoundError:
        output_obj.set_text(("error", "File not found"))

    except Exception as e:  # Everything else...
        output_obj.set_text(("error", repr(e)))
    else:
        output_obj.set_text(("success", str(tree.pretty())))


def new_input(_, newinput):
    parse(lark_grammar.get_edit_text(), newinput, output)


# def vertical_wrapper(ui):
#     return urwid.ListBox(urwid.SimpleFocusListWalker(ui))


lark_grammar = urwid.Edit(("bold", "Grammar\n"), multiline=True, allow_tab=True)
grammar_input = urwid.Edit(("bold", "Grammar input\n"), multiline=True, allow_tab=True)

urwid.connect_signal(lark_grammar, "change", handler)
urwid.connect_signal(grammar_input, "change", new_input)

UI = [
    urwid.LineBox(lark_grammar),
    urwid.LineBox(grammar_input),
    urwid.Divider(div_char="-"),
    output,
    urwid.Divider(div_char="-"),
    meta,
]
main_ui = urwid.Filler(urwid.Pile(UI))
PALLETE = [
    ("bold", "bold", ""),
    ("wait", "yellow", ""),
    ("error", "light red", ""),
    ("success", "light green", ""),
]
loop = urwid.MainLoop(main_ui, palette=PALLETE)
try:
    loop.run()
except KeyboardInterrupt:
    sys.exit(0)

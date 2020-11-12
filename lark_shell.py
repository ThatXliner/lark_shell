#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Initial author: Bryan Hu .

@ThatXliner .

Version: v0.1.0

An implementation of https://lark-parser.github.io/lark/ide/app.html in the terminal.

For playing with Lark.

"""
import urwid
import lark

output = urwid.Text(("wait", "Output waiting..."))

the_input = ""


def handler(_, newtext):  # Lark parse here
    try:
        tree = lark.Lark(newtext).parse(the_input)
    except (lark.exceptions.GrammarError, ValueError):
        output.set_text(("error", "Incomplete grammar"))
    except Exception as e:
        output.set_text(repr(e))
    else:
        output.set_text(repr(tree.pretty()))


def new_input(_, newtext):
    the_input = newtext  # noqa


def vertical_wrapper(ui):
    return urwid.ListBox(urwid.SimpleFocusListWalker(ui))


lark_grammar = urwid.Edit(("bold", "Grammar\n"), multiline=True, allow_tab=True)
grammar_input = urwid.Edit(("bold", "Grammar input\n"), multiline=True, allow_tab=True)

urwid.connect_signal(lark_grammar, "change", handler)
urwid.connect_signal(grammar_input, "change", new_input)

UI = [
    urwid.LineBox(lark_grammar),
    # urwid.Divider(div_char="-"),
    urwid.LineBox(grammar_input),
    urwid.Divider(div_char="-"),
    output,
]
main_ui = urwid.Filler(urwid.Pile(UI))
PALLETE = [("wait", "yellow", ""), ("error", "light red", ""), ("bold", "bold", "")]
loop = urwid.MainLoop(main_ui, palette=PALLETE)
loop.run()

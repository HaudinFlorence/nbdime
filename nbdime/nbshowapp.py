# coding: utf-8

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

from __future__ import unicode_literals
from __future__ import print_function

import os
import sys
import argparse
import nbformat

from nbdime.prettyprint import pretty_print_notebook
from nbdime.args import add_generic_args, IgnorableAction, process_exclusive_ignorables
from nbdime.utils import setup_std_streams


_description = """Show a Jupyter notebook in terminal.
By default shows all notebook fields.
Limit to specific fields by passing options.
"""


def main_show(args):

    if len(args.notebook) == 1 and args.notebook[0] == "-":
        files = [sys.stdin]
    else:
        for fn in args.notebook:
            if not os.path.exists(fn):
                print("Missing file {}".format(fn))
                return 1
        files = args.notebook
        if not files:
            print("Missing filenames.")
            return 1

    for fn in files:
        nb = nbformat.read(fn, as_version=4)

        # This printer is to keep the unit tests passing,
        # some tests capture output with capsys which doesn't
        # pick up on sys.stdout.write()
        class Printer:
            def write(self, text):
                print(text, end="")
        if not any((args.sources, args.outputs, args.attachments, args.metadata, args.details)):
            ppargs = None
        else:
            ppargs = args

        if len(args.notebook) > 1:
            # 'more' prints filenames with colons, should be good enough for us as well
            print(":"*14)
            print(fn)
            print(":"*14)
        pretty_print_notebook(nb, ppargs, Printer())

    return 0


def _build_arg_parser():
    """Creates an argument parser for the nbshow command."""
    parser = argparse.ArgumentParser(
        description=_description,
        add_help=True,
        )
    add_generic_args(parser)
    parser.add_argument("notebook", nargs="*", help="notebook filename(s) or - to read from stdin")

    # Things we can choose to show or not
    parser.add_argument(
        '-s', '--sources',
        action=IgnorableAction,
        help="show sources.")
    parser.add_argument(
        '-o', '--outputs',
        action=IgnorableAction,
        help="show outputs.")
    parser.add_argument(
        '-a', '--attachments',
        action=IgnorableAction,
        help="show attachments.")
    parser.add_argument(
        '-m', '--metadata',
        action=IgnorableAction,
        help="show metadata.")
    parser.add_argument(
        '-d', '--details',
        action=IgnorableAction,
        help="show details not covered by other options.")

    return parser


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    setup_std_streams()
    arguments = _build_arg_parser().parse_args(args)
    process_exclusive_ignorables(
        arguments,
        ('sources', 'outputs', 'attachments', 'metadata', 'details'))
    return main_show(arguments)


if __name__ == "__main__":
    sys.exit(main())

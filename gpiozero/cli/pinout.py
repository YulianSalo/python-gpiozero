#!/usr/bin/env python
"""
pinout - gpiozero command-line pinout tool.

Output Raspberry Pi GPIO pinout information.
"""

from __future__ import unicode_literals, absolute_import, print_function, division

import argparse
import sys

from gpiozero import pi_info


class PinoutTool(object):
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description=__doc__
        )
        self.parser.add_argument(
            '-r', '--revision',
            dest='revision',
            default='',
            help='RPi revision. Default is to autodetect revision of current device'
        )
        self.parser.add_argument(
            '-c', '--color',
            action="store_true",
            default=None,
            help='Force colored output (by default, the output will include ANSI'
            'color codes if run in a color-capable terminal). See also --monochrome'
        )
        self.parser.add_argument(
            '-m', '--monochrome',
            dest='color',
            action='store_false',
            help='Force monochrome output. See also --color'
        )

    def __call__(self, args=None):
        if args is None:
            args = sys.argv[1:]
        try:
            return self.main(self.parser.parse_args(args)) or 0
        except argparse.ArgumentError as e:
            # argparse errors are already nicely formatted, print to stderr and
            # exit with code 2
            raise e
        except Exception as e:
            # Output anything else nicely formatted on stderr and exit code 1
            self.parser.exit(1, '{prog}: error: {message}\n'.format(
                prog=self.parser.prog, message=e))

    def main(self, args):
        if args.revision == '':
            try:
                pi_info().pprint(color=args.color)
            except IOError:
                raise IOError('This device is not a Raspberry Pi')
        else:
            pi_info(args.revision).pprint(color=args.color)
        print('')
        print('For further information, please refer to https://pinout.xyz/')


main = PinoutTool()

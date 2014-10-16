#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
#    <PROG> - <DESCRIPTION>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    Copyright (C) 2014 Kevin Roy <kiniou@gmail.com>

import os
import sys
from pprint import pprint
from subprocess import call
from docopt import docopt
import logging

logging.basicConfig()
logger = logging.getLogger()

__doc__ = \
"""Inoticoming Asciidoc

Usage:
    inoticoming-asciidoc [-v|-d] [-n] [--suffix=<SUFFIX>] [--prefix=<PREFIX>] [--regexp=<REGEXP>] <directory>

Options:
    -s,--suffix=<SUFFIX>        [default: .txt]
    -p,--prefix=<PREFIX>
    -r,--regexp=<REGEXP>
    -v, --verbose
    -d, --debug
    -n, --dry-run
    <directory>     listen for inotify changes on this directory tree
"""

asciidoc_cmd = [
    '-c',
    "'",
    "export PATH={};".format(os.environ['PATH']),
    'asciidoc.sh',
    '--backend=html5',
    '-f ~/.asciidoc/knokorpo.conf',
    '--theme=flask-custom',
    '-a icons',
    '-a data-uri',
]

#inoticoming_cmd = [
#    'inoticoming',
#    '--foreground',
#    '--initialsearch'
#]

inoticoming_cmd = [
    'iwatch',
    '-e modify,create',
    '-r',
]

def main():
    #do your stuff here
    args = docopt(__doc__)
    if args['--verbose'] :
        logger.setLevel(logging.INFO)
        asciidoc_cmd.extend(['--verbose'])
    if args['--debug'] :
        logger.setLevel(logging.DEBUG)
        asciidoc_cmd.extend(['--verbose'])
    logger.debug(args)

    asciidoc_cmd.extend([ '%f', "'"])
    inoticoming_cmd.extend([
        '-t "\{}$"'.format(args['--suffix'])
    ])
    inoticoming_cmd.extend(asciidoc_cmd)
    inoticoming_cmd.extend([
        args['<directory>'],
    #    '--suffix={}'.format(args['--suffix']),
    #    '--prefix={}'.format(args['--prefix']) if args['--prefix'] is not None else '',
    #    '--regexp={}'.format(args['--regexp']) if args['--regexp'] is not None else '',
    ])

    logger.debug(" ".join(inoticoming_cmd))
    if not args['--dry-run']:
        ret = call(" ".join(inoticoming_cmd), shell=True)
    else:
        print(" ".join(inoticoming_cmd))
    return 0

if __name__ == '__main__' :
    sys.exit(main())


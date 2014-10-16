#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    <FILE> - <DESCRIPTION>
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
from pprint import pprint, pformat

import json
from docopt import docopt
__doc__ = """{command} - {description}
Usage: {command} [-v|-d]

Options:
    -v, --verbose   log informative steps
    -d, --debug     log debug steps
""".format(
    command = sys.argv[0],
    description=""
)

import logging
logging.basicConfig()
logger = logging.getLogger()


import android, time

if __name__ == "__main__":
    android.HOST = "localhost"
    android.PORT= 99999

    args = docopt(__doc__)
    if args['--verbose'] :
        logger.setLevel(logging.INFO)
    if args['--debug'] :
        logger.setLevel(logging.DEBUG)
    #do your stuff here
    droid = android.Android()
    droid.startSensingTimed(1, 250)
    time.sleep(1)
    sensors_result = droid.readSensors().result
    droid.stopSensing()
    logger.debug(pformat(sensors_result))
    print("Light: {light}".format(**sensors_result))
    if (sensors_result['light'] > 300) :
        print "light"
    else :
        print "dark"
    sys.exit(0)

#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#    watch_code_change.py - watch code changes and trigger actions
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
#    Copyright (C) 2013 Kevin Roy <kiniou@gmail.com>

import os, sys, re
import pyinotify
import shlex
from subprocess import call
from pprint import pprint

wm = pyinotify.WatchManager()
rootpath = os.path.abspath('.')

excl_lst = [ r'^.*\.py$',
#             r'\.git/',
#             r'^tools'
]
excl_comp = [re.compile(pat) for pat in excl_lst]

class WatchHandler(pyinotify.ProcessEvent):

    def process_IN_MODIFY(self,event):
        self.process_event(event)

    def process_IN_CLOSE_WRITE(self,event):
        self.process_event(event)

    def process_event(self,event) :
        pathname = event.pathname
        relpathname = os.path.relpath(pathname,rootpath)
        matches = [pat.match(relpathname) is not None for pat in excl_comp]

        print matches
        print "%s" % relpathname
        if any(matches):
            print "%s matched" % relpathname
            print "%s" % pathname
            pprint(event)
            call(shlex.split("touch /tmp/knokorpo_wsgi"))

handler = WatchHandler()
notifier = pyinotify.Notifier(wm,default_proc_fun=handler)
# Add watches
res = wm.add_watch([rootpath],
                   pyinotify.IN_CLOSE_WRITE, rec=True, auto_add=True)

notifier.loop()


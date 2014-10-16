#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#    analyse_logs.py - analyse apache access logs and do some stats
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

import re
import sys
import os
import shlex
from subprocess import call, check_output, Popen
from argparse import ArgumentParser

from pprint import pprint

#import httpagentparser
from csv import DictWriter


parser = ArgumentParser()
parser.add_argument("-o", "--output")
parser.add_argument("pattern")

stats = {}


#nombre de code d'erreur par useragent
#"chemin", "useragent", "code-erreur", "count"
#"chemin", ""

parts = [
    r'(?P<host>\S+)',                   # host %h
    r'\S+',                             # indent %l (unused)
    r'(?P<user>\S+)',                   # user %u
    r'\[(?P<time>.+)\]',                # time %t
    r'"(?P<request>.+)"',               # request "%r"
    r'(?P<status>[0-9]+)',              # status %>s
    r'(?P<size>\S+)',                   # size %b (careful, can be '-')
    r'"(?P<referer>.*)"',               # referer "%{Referer}i"
    r'"(?P<agent>.*)"',                 # user agent "%{User-agent}i"
]

access_pattern = re.compile(r'\s+'.join(parts)+r'\s*\Z')

if __name__ == "__main__" :
    args = parser.parse_args()
    pprint(args)
    cmd = "ls -1 %s | sort -V" % (args.pattern)
    s = check_output(cmd, shell=True)
    for fname in s.split() :
        print("processing %s" % fname)
        if (os.path.exists(fname) and os.path.isfile(fname)):
            with open(fname) as fhandle:
                for l in fhandle:
                    m = access_pattern.match(l)
                    matches = m.groupdict()
                    m_request = matches['request']
                    m_agent = matches['agent']
                    m_status = matches['status']
                    if m_request not in stats:
                        stats[m_request] = {}
                    if m_agent not in stats[m_request]:
                        stats[m_request][m_agent] = {}
                    if m_status not in stats[m_request][m_agent]:
                        stats[m_request][m_agent][m_status] = 0

                    stats[m_request][m_agent][m_status] += 1

    with open('analysis.csv','w') as f:
        csv_file = DictWriter(f, ('request','agent','status','count'))
        csv_file.writeheader()
        for k_request,v_request in stats.items():
            for k_agent,v_agent in v_request.items():
                for k_status,v_status in v_agent.items():
                    csv_file.writerow({
                        'request' : k_request,
                        'agent' : k_agent,
                        'status' : k_status,
                        'count' : v_status
                    })

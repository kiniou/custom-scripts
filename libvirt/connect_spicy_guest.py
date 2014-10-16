#!/usr/bin/env python
import sys
from pprint import pprint, pformat

import libvirt

conn = libvirt.openReadOnly("qemu:///system")
if conn == None:
    print "failed to open connection to the hypervisor"
    sys.exit(1)

try:
    running_domains = map(lambda x:conn.lookupByID(x), conn.listDomainsID())
except:
    print "Failed to list domains IDs"
    sys.exit(2)

devices = conn.listAllDevices()

for dev in devices:
    pprint(dir(dev.parent))
    pprint(dev.parent.im_class)

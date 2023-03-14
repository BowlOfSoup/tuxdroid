#!/usr/bin/env python
# -*- coding: latin1 -*-

from distutils.sysconfig import *
from distutils.core import setup
from glob import glob
import os
import sys

os.environ['PYTHONHOME']='/usr'
#
# Check dependencies
#
packageDependencies = [
    'xml.dom.minidom',
    'httplib',
    'zipfile',
    'urllib2',
    'socket',
    'threading',
    'copy',
    're',
    'urllib',
]

for moduleName in packageDependencies:
    try:
        print "check module presence (%s)" % moduleName
        exec("import %s" % moduleName) in globals()
        exec("del %s" % moduleName) in globals()
    except:
        print "ERROR : Module (%s) not found !" % moduleName
        sys.exit(-1)

#
# Packages list
#
mPackages = [
    'tuxisalive',
    'tuxisalive.api',
    'tuxisalive.api.base',
    'tuxisalive.api.base.const',
    'tuxisalive.api.base.lib',
    'tuxisalive.api.tuxdroid',
    'tuxisalive.api.tuxdroid.const',
]

#
# Install the package
#
setup(
    name = 'tuxapi',
    version = '0.5.0',
    description = 'Python API for Tuxdroid',
    author = 'Remi Jocaille',
    author_email = 'remi.jocaille@c2me.be',
    url = 'http://www.tuxisalive.com',
    packages = mPackages,
)

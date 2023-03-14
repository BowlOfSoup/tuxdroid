# -*- coding: utf-8 -*-

import version
__author__ = version.author
__date__ = version.date
__version__ = version.version
__licence__ = version.licence
del version

#    Copyleft (C) 2008 Acness World
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import unittest

import test_DirectoriesAndFilesTools
import test_XMLSerializer
import test_URLTools
import test_FilesCache

# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(
        test_DirectoriesAndFilesTools.suite())
    unittest.TextTestRunner(verbosity=2).run(test_XMLSerializer.suite())
    tSuite = test_URLTools.suite()
    if tSuite != None:
        unittest.TextTestRunner(verbosity=2).run(tSuite)
    unittest.TextTestRunner(verbosity=2).run(test_FilesCache.suite())

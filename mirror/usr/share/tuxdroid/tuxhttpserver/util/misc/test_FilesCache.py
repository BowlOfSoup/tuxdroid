# -*- coding: utf-8 -*-

import version
__author__ = version.author
__date__ = version.date
__version__ = version.version
__licence__ = version.licence
del version

#    Copyleft (C) 2008 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import unittest
import os

import FilesCache

_URL_FILE_TO_TEST = "http://ftp.kysoh.com/apps/installers/win32/" + \
    "software_updater/install.txt"

# ==============================================================================
# Public class
# ==============================================================================

# ------------------------------------------------------------------------------
# A test class for filesCache module.
# ------------------------------------------------------------------------------
class testFilesCache(unittest.TestCase):
    """A test class for filesCache module.
    """

    # --------------------------------------------------------------------------
    # Create objects.
    # --------------------------------------------------------------------------
    def setUp(self):
        """Create objects.
        """
        self.cfContainer = FilesCache.CachedFilesContainer("cache_unittest")

    # --------------------------------------------------------------------------
    # Test the presence of the temp directory of the cache.
    # --------------------------------------------------------------------------
    def test00TempDirCache(self):
        """Test the presence of the temp directory of the cache.
        """
        cacheDir = self.cfContainer.getCacheDir()
        self.assertNotEqual(cacheDir, "")
        self.assertTrue(os.path.isdir(cacheDir))

    # --------------------------------------------------------------------------
    # Test the creation of a cached file from the hard drive.
    # --------------------------------------------------------------------------
    def test01CreateFileCacheFromDisk(self):
        """Test the creation of a cached file from the hard drive.
        """
        # Create cached file with existing file
        fc = self.cfContainer.createFileCache(__file__)
        # fc object must be != than None
        self.assertNotEqual(fc, None)
        # md5Tag must exists
        self.assertNotEqual(fc.getMd5Tag(), "")
        # Output filename must exists
        self.assertTrue(os.path.isfile(fc.getOutputFilePath()))
        # Destroy the cached file
        fc.destroy()
        # Create cached file with unexisting file
        fc = self.cfContainer.createFileCache("c:\\inconnu.bidule")
        # fc object must be == None
        self.assertEqual(fc, None)

    # --------------------------------------------------------------------------
    # Test the creation of a cached file from an url.
    # --------------------------------------------------------------------------
    def test02CreateFileCacheFromURL(self):
        """Test the creation of a cached file from an url.
        """
        # Create cached file with existing url
        fc = self.cfContainer.createFileCache(_URL_FILE_TO_TEST)
        # fc object must be != than None
        self.assertNotEqual(fc, None)
        # md5Tag must exists
        self.assertNotEqual(fc.getMd5Tag(), "")
        # Output filename must exists
        self.assertTrue(os.path.isfile(fc.getOutputFilePath()))

    # --------------------------------------------------------------------------
    # Test the destroying of the cached files container.
    # --------------------------------------------------------------------------
    def test03DestroyContainer(self):
        """Test the destroying of the cached files container.
        """
        cacheDir = self.cfContainer.getCacheDir()
        # Destroy the container
        self.cfContainer.destroy()
        # Temp dir cache must not exists
        self.assertFalse(os.path.isdir(cacheDir))

# ==============================================================================
# Public functions
# ==============================================================================

# ------------------------------------------------------------------------------
# Unitest suite for the module 'FilesCache'
# ------------------------------------------------------------------------------
def suite():
    """Unitest suite for the module 'FilesCache'
    """
    print "\n" + "".join("=" * 70)
    print "Test the 'FilesCache' Module"
    print "".join("=" * 70) + "\n"
    
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testFilesCache))
    return suite

# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

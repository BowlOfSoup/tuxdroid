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

import URLTools
import DirectoriesAndFilesTools

_URL_FILE_TO_TEST = "http://ftp.kysoh.com/apps/installers/win32/" + \
    "software_updater/install.txt"

# ==============================================================================
# Public class
# ==============================================================================

# ------------------------------------------------------------------------------
# A test class for URLTools module.
# ------------------------------------------------------------------------------
class testURLTools(unittest.TestCase):
    """A test class for URLTools module.
    """

    # --------------------------------------------------------------------------
    # Test the header infos retrieving from a valid URL.
    # --------------------------------------------------------------------------
    def test00GetInfos(self):
        """Test the header infos retrieving from a valid URL.
        """
        infos = URLTools.URLGetInfos(_URL_FILE_TO_TEST)
        self.assertNotEqual(infos, None)
        self.assertNotEqual(infos['Last-Modified'], '')
        self.assertNotEqual(infos['Content-Length'], '')

    # --------------------------------------------------------------------------
    # Test the header infos retrieving from a bad URL.
    # --------------------------------------------------------------------------
    def test01GetInfos2(self):
        """Test the header infos retrieving from a bad URL.
        """
        infos = URLTools.URLGetInfos(_URL_FILE_TO_TEST + 'xxx')
        self.assertEqual(infos, None)

    # --------------------------------------------------------------------------
    # Test the downloading of a file from a valid URL to a string.
    # --------------------------------------------------------------------------
    def test02DownloadToString(self):
        """Test the downloading of a file from a valid URL to a string.
        """
        strRes = URLTools.URLDownloadToString(_URL_FILE_TO_TEST)
        self.assertNotEqual(strRes, None)
        self.assertNotEqual(strRes, "")

    # --------------------------------------------------------------------------
    # Test the downloading of a file from a bad URL to a string.
    # --------------------------------------------------------------------------
    def test03DownloadToString2(self):
        """Test the downloading of a file from a bad URL to a string.
        """
        strRes = URLTools.URLDownloadToString(_URL_FILE_TO_TEST + 'xxx')
        self.assertEqual(strRes, None)

    # --------------------------------------------------------------------------
    # Test the downloading of a file from a valid URL to a file.
    # --------------------------------------------------------------------------
    def test04DownloadToFile(self):
        """Test the downloading of a file from a valid URL to a file.
        """
        self.tmpDirectory = DirectoriesAndFilesTools.GetOSTMPDir()
        res = URLTools.URLDownloadToFile(_URL_FILE_TO_TEST, os.path.join(
            self.tmpDirectory, 'temp.tmp'))
        self.assertTrue(res)
        self.assertTrue(os.path.isfile(os.path.join(self.tmpDirectory,
            'temp.tmp')))
        os.remove(os.path.join(self.tmpDirectory, 'temp.tmp'))

    # --------------------------------------------------------------------------
    # Test the downloading of a file from a bad URL to a file.
    # --------------------------------------------------------------------------
    def test05DownloadToFile2(self):
        """Test the downloading of a file from a bad URL to a file.
        """
        self.tmpDirectory = DirectoriesAndFilesTools.GetOSTMPDir()
        res = URLTools.URLDownloadToFile(_URL_FILE_TO_TEST + 'xxx',
            os.path.join(self.tmpDirectory, 'temp.tmp'))
        self.assertFalse(res)
        self.assertFalse(os.path.isfile(os.path.join(self.tmpDirectory,
            'temp.tmp')))

# ==============================================================================
# Public functions
# ==============================================================================

# ------------------------------------------------------------------------------
# Unitest suite for the module 'URLTools'
# ------------------------------------------------------------------------------
def suite():
    """Unitest suite for the module 'URLTools'
    """
    print "\n" + "".join("=" * 70)
    print "Test the 'URLTools' Module"
    print "".join("=" * 70) + "\n"

    # Check the internet connection
    if not URLTools.URLCheckConnection():
        print "ERROR ! You need an Internet connection to test this module.\n"
        return None

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testURLTools))
    return suite

# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    tSuite = suite()
    if tSuite != None:
        unittest.TextTestRunner(verbosity=2).run(tSuite)

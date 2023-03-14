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

import DirectoriesAndFilesTools

# ==============================================================================
# Public class
# ==============================================================================

# ------------------------------------------------------------------------------
# A test class for DirectoriesAndFilesTools module.
# ------------------------------------------------------------------------------
class testDirectoriesAndFilesTools(unittest.TestCase):
    """A test class for DirectoriesAndFilesTools module.
    """

    # --------------------------------------------------------------------------
    # Initialization.
    # --------------------------------------------------------------------------
    def setUp(self):
        """Initialization.
        """
        self.tmpDirectory = ""

    # --------------------------------------------------------------------------
    # Test the retrieving of the temporary directory.
    # --------------------------------------------------------------------------
    def test00GetOSTMPDir(self):
        """Test the retrieving of the temporary directory.
        """
        # Retrieve the temporary directory of the OS.
        self.tmpDirectory = DirectoriesAndFilesTools.GetOSTMPDir()
        self.assertNotEqual(self.tmpDirectory, "")
        # Check the creation of a file in the retrieved directory
        work = True
        try:
            f = open(os.path.join(self.tmpDirectory, "test.tmp"), 'wb')
            f.write("\n")
            f.close()
            os.remove(os.path.join(self.tmpDirectory, "test.tmp"))
        except:
            work = False
        self.assertEqual(work, True)

    # --------------------------------------------------------------------------
    # Test the creation of a new directories tree.
    # --------------------------------------------------------------------------
    def test01CreateDirectoriesTree(self):
        """Test the creation of a new directories tree.
        """
        # Create a directories tree
        self.tmpDirectory = DirectoriesAndFilesTools.GetOSTMPDir()
        extTree = os.path.join(self.tmpDirectory, 'test', 'test2', 'test3')
        DirectoriesAndFilesTools.MKDirs(extTree)
        # Check if the last directory exists
        self.assertTrue(os.path.isdir(extTree))
        # Create a file
        try:
            f = open(os.path.join(extTree, 'myfile.tmp'), 'wb')
            f.close()
        except:
            pass
        self.assertTrue(os.path.isfile(os.path.join(extTree, 'myfile.tmp')))

    # --------------------------------------------------------------------------
    # Test the creation of a clean directories tree (Erase the old one).
    # --------------------------------------------------------------------------
    def test02CreateDirectoriesTreeFFS(self):
        """Test the creation of a clean directories tree (Erase the old one).
        """
        # Create a directories tree
        self.tmpDirectory = DirectoriesAndFilesTools.GetOSTMPDir()
        extTree = os.path.join(self.tmpDirectory, 'test', 'test2', 'test3')
        DirectoriesAndFilesTools.MKDirsF(extTree)
        # Check if the last directory exists
        self.assertTrue(os.path.isdir(extTree))
        # Check if the previously created file still exists
        self.assertFalse(os.path.isfile(os.path.join(extTree, 'myfile.tmp')))

    # --------------------------------------------------------------------------
    # Test the removing of directories and files with a name filter.
    # --------------------------------------------------------------------------
    def test03RemoveDAFRecWF(self):
        """Test the removing of directories and files with a name filter.
        """
        self.tmpDirectory = DirectoriesAndFilesTools.GetOSTMPDir()
        extTree = os.path.join(self.tmpDirectory, 'test', 'test2', 'test3')
        # Create some files
        try:
            f = open(os.path.join(extTree, 'myfile.tmp'), 'wb')
            f.close()
            f = open(os.path.join(extTree, 'myfile2.tmp'), 'wb')
            f.close()
            f = open(os.path.join(extTree, 'myfile.ttt'), 'wb')
            f.close()
            f = open(os.path.join(extTree, 'myfile.h'), 'wb')
            f.close()
        except:
            pass
        self.assertTrue(os.path.isfile(os.path.join(extTree, 'myfile.tmp')))
        # Create a directory called '.tmp'
        DirectoriesAndFilesTools.MKDirs(os.path.join(extTree, 'truc.tmp'))
        self.assertTrue(os.path.isdir(os.path.join(extTree, 'truc.tmp')))
        # Remove files and directories with 'tmp' extention
        DirectoriesAndFilesTools.RMWithFilters(extTree, filters = ['.tmp', ])
        self.assertFalse(os.path.isfile(os.path.join(extTree, 'myfile.tmp')))
        self.assertFalse(os.path.isfile(os.path.join(extTree, 'myfile2.tmp')))
        self.assertFalse(os.path.isdir(os.path.join(extTree, 'truc.tmp')))
        self.assertTrue(os.path.isdir(extTree))

    # --------------------------------------------------------------------------
    # Test the copying of directories tree.
    # --------------------------------------------------------------------------
    def test04CopyTree(self):
        """Test the copying of directories tree.
        """
        self.tmpDirectory = DirectoriesAndFilesTools.GetOSTMPDir()
        extTree = os.path.join(self.tmpDirectory, 'test2', 'test2', 'test3')
        DirectoriesAndFilesTools.CPDir(os.path.join(self.tmpDirectory, 'test'),
            os.path.join(self.tmpDirectory, 'test2'))
        self.assertTrue(os.path.isfile(os.path.join(extTree, 'myfile.ttt')))

    # --------------------------------------------------------------------------
    # Test the removing of directories tree with files.
    # --------------------------------------------------------------------------
    def test05RemoveDAFRec(self):
        """Test the removing of directories tree with files.
        """
        self.tmpDirectory = DirectoriesAndFilesTools.GetOSTMPDir()
        baseTree = os.path.join(self.tmpDirectory, 'test')
        DirectoriesAndFilesTools.RMDirs(baseTree)
        self.assertFalse(os.path.isdir(baseTree))
        baseTree = os.path.join(self.tmpDirectory, 'test2')
        DirectoriesAndFilesTools.RMDirs(baseTree)
        self.assertFalse(os.path.isdir(baseTree))

# ==============================================================================
# Public functions
# ==============================================================================

# ------------------------------------------------------------------------------
# Unitest suite for the module 'DirectoriesAndFilesTools'
# ------------------------------------------------------------------------------
def suite():
    """Unitest suite for the module 'DirectoriesAndFilesTools'
    """
    print "\n" + "".join("=" * 70)
    print "Test the 'DirectoriesAndFilesTools' Module"
    print "".join("=" * 70) + "\n"

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testDirectoriesAndFilesTools))
    return suite

# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

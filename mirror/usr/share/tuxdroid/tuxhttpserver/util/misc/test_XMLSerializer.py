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
import os

from DirectoriesAndFilesTools import GetOSTMPDir
import XMLSerializer

_OS_TMP_DIR = GetOSTMPDir()

_EXAMPLE_STRUCT = {
    'root': {
        'header': {
            'name': 'Test',
            'author': 'Remi Jocaille',
            'version': '0.0.0',
            'a_list': ['Hello', 0, 'Coucou', 'Remi'],
            'a_float': 0.0,
        },
        'body1': {
            'an_integer': 0
        },
        'body2': {
            'sub_body': {
                'language': 'python',
                'about': 'Empty'
            }
        }
    }
}

# ==============================================================================
# Public class
# ==============================================================================

# ------------------------------------------------------------------------------
# A test class for XMLSerializer module.
# ------------------------------------------------------------------------------
class testXMLSerializer(unittest.TestCase):
    """A test class for XMLSerializer module.
    """

    # --------------------------------------------------------------------------
    # Test the first writing of the reference structure to a XML file.
    # --------------------------------------------------------------------------
    def test00WriteToXmlFirst(self):
        """Test the first writing of the reference structure to a XML file.
        """
        # Get the xml file string of the structure
        xmlStr = XMLSerializer.toXML(_EXAMPLE_STRUCT)
        self.assertNotEqual(xmlStr, "")
        self.assertNotEqual(xmlStr, None)
        # Write the string into a XML file
        f = open(os.path.join(_OS_TMP_DIR, "test1.xml"), 'wb')
        f.write(xmlStr)
        f.close()
        # Check the file presence in the hard drive
        self.assertTrue(os.path.isfile(os.path.join(_OS_TMP_DIR, "test1.xml")))

    # --------------------------------------------------------------------------
    # Test the reading/rewriting of the created XML file.
    # --------------------------------------------------------------------------
    def test01ReadRewriteTheXMLFile(self):
        """Test the reading/rewriting of the created XML file.
        """
        # Read the XML file
        struct = XMLSerializer.fromXML(os.path.join(_OS_TMP_DIR, "test1.xml"))
        # Check the structure integrity
        self.assertEqual(struct['root']['header']['a_list'][3].decode('utf-8'),
            'Remi')
        self.assertEqual(struct['root']['header']['author'].decode('utf-8'),
            'Remi Jocaille')
        self.assertEqual(struct['root']['header']['a_float'], 0.0)
        self.assertEqual(struct['root']['body1']['an_integer'], 0)
        # Get the xml file string of the structure
        xmlStr = XMLSerializer.toXML(struct)
        self.assertNotEqual(xmlStr, "")
        self.assertNotEqual(xmlStr, None)
        # Rewrite the string into another XML file
        f = open(os.path.join(_OS_TMP_DIR, "test2.xml"), 'wb')
        f.write(xmlStr)
        f.close()
        # Check the file presence in the hard drive
        self.assertTrue(os.path.isfile(os.path.join(_OS_TMP_DIR, "test2.xml")))

    # --------------------------------------------------------------------------
    # Test the re-reading of the created XML file.
    # --------------------------------------------------------------------------
    def test02ReReadTheXMLFile(self):
        """Test the re-reading of the created XML file.
        """
        # Read the XML file
        struct = XMLSerializer.fromXML(os.path.join(_OS_TMP_DIR, "test2.xml"))
        # Check the structure integrity
        self.assertEqual(struct['root']['header']['a_list'][3].decode('utf-8'),
            'Remi')
        self.assertEqual(struct['root']['header']['author'].decode('utf-8'),
            'Remi Jocaille')
        self.assertEqual(struct['root']['header']['a_float'], 0.0)
        self.assertEqual(struct['root']['body1']['an_integer'], 0)
        # Delete XML files
        os.remove(os.path.join(_OS_TMP_DIR, "test1.xml"))
        os.remove(os.path.join(_OS_TMP_DIR, "test2.xml"))

# ==============================================================================
# Public functions
# ==============================================================================

# ------------------------------------------------------------------------------
# Unitest suite for the module 'XMLSerializer'
# ------------------------------------------------------------------------------
def suite():
    """Unitest suite for the module 'XMLSerializer'
    """
    print "\n" + "".join("=" * 70)
    print "Test the 'XMLSerializer' Module"
    print "".join("=" * 70) + "\n"

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testXMLSerializer))
    return suite

# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

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

import os
import shutil

if os.name == 'nt':
    import win32con
    import win32file

# ==============================================================================
# Public functions
# ==============================================================================

# ------------------------------------------------------------------------------
# Force to create a directories tree if not exists.
# ------------------------------------------------------------------------------
def MKDirs(path):
    """Force to create a directories tree if not exists.
    @param path: Directory path.
    """
    if not os.path.isdir(path):
        try:
            os.makedirs(path)
        except:
            pass

# ------------------------------------------------------------------------------
# Force to create a directories tree after having deleted the old one.
# ------------------------------------------------------------------------------
def MKDirsF(path):
    """Force to create a directories tree after having deleted the old one.
    @param path: Directory path.
    """
    if os.path.isdir(path):
        RMDirs(path)
    os.makedirs(path)

# ------------------------------------------------------------------------------
# Remove directories and files recursively.
# ------------------------------------------------------------------------------
def RMDirs(path):
    """Remove directories and files recursively.
    @param path: Path of the base directory.
    """
    if not os.path.isdir(path):
        return
    for root, dirs, files in os.walk(path, topdown = False):
        for d in dirs:
            try:
                os.removedirs(os.path.join(root, d))
            except:
                pass
        for f in files:
            try:
                if os.name == 'nt':
                    win32file.SetFileAttributesW(os.path.join(root, f),
                        win32con.FILE_ATTRIBUTE_NORMAL)
                os.remove(os.path.join(root, f))
            except:
                pass
    if os.path.isdir(path):
        try:
            os.removedirs(path)
        except:
            pass

# ------------------------------------------------------------------------------
# Remove directories and files recursively with filters.
# ------------------------------------------------------------------------------
def RMWithFilters(path, filters = ['.pyc', '.pyo']):
    """Remove directories and files recursively with filters.
    @param path: Path of the base directory.
    @param filters: Filters as list.
    """
    def checkFilter(name):
        for filter in filters:
            if name.lower().find(filter.lower()) == (len(name) - len(filter)):
                return True
        return False

    if not os.path.isdir(path):
        return

    for root, dirs, files in os.walk(path, topdown = False):
        for d in dirs:
            if checkFilter(os.path.join(root, d)):
                RMDirs(os.path.join(root, d))
        for f in files:
            if checkFilter(os.path.join(root, f)):
                try:
                    if os.name == 'nt':
                        win32file.SetFileAttributesW(os.path.join(root, f),
                            win32con.FILE_ATTRIBUTE_NORMAL)
                    os.remove(os.path.join(root, f))
                except:
                    pass

# ------------------------------------------------------------------------------
# Remove a file.
# ------------------------------------------------------------------------------
def RMFile(path):
    """Remove a file.
    @param path: File path.
    """
    if os.path.isfile(path):
        try:
            if os.name == 'nt':
                win32file.SetFileAttributesW(path,
                    win32con.FILE_ATTRIBUTE_NORMAL)
            os.remove(path)
        except:
            pass

# ------------------------------------------------------------------------------
# Copy a directories tree to another directory.
# ------------------------------------------------------------------------------
def CPDir(src, dest):
    """Copy a directories tree to another directory.
    @param src: Source path.
    @param dest: Destination path.
    """
    if not os.path.isdir(src):
        return
    if os.path.isdir(dest):
        RMDirs(dest)
    shutil.copytree(src, dest)

# ------------------------------------------------------------------------------
# Copy a file.
# ------------------------------------------------------------------------------
def CPFile(src, dest):
    """Copy a file.
    @param src: Source file path.
    @param dest: Destination file path.
    @return: True or False.
    """
    if not os.path.isfile(src):
        return False
    try:
        shutil.copy(src, dest)
    except:
        return False
    return True

# ------------------------------------------------------------------------------
# Retrieve the OS temporary directory.
# ------------------------------------------------------------------------------
def GetOSTMPDir():
    """Retrieve the OS temporary directory.
    @return: The OS temporary directory.
    """
    result = None
    # On Windows
    if os.name == 'nt':
        result = os.environ.get('tmp')
        if result == None:
            result = os.environ.get('temp')
            if result == None:
                result = "c:\\windows\\temp"
    # On linux
    else:
        result = "/tmp"
    return result

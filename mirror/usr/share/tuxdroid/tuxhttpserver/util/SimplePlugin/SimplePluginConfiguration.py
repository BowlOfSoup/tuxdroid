# -*- coding: latin1 -*-

import version
__author__ = version.author
__date__ = version.date
__version__ = version.version
__licence__ = version.licence
del version

#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html
#
#    This module is a portage of the java package write by "Yoran Brault"
#    "com.kysoh.tuxdroid.gadget.framework.gadget"

# ------------------------------------------------------------------------------
# Class of the default plugin configuration.
# ------------------------------------------------------------------------------
class SimplePluginConfiguration(object):
    """Class of the default plugin configuration.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self):
        """Constructor of the class.
        """
        self.__traces = True
        self.__pitch = 100
        self.__language = "en"
        self.__country = "US"
        self.__locutor = "Ryan"
        self.__daemon = False

    # --------------------------------------------------------------------------
    # Get the pitch value.
    # --------------------------------------------------------------------------
    def getPitch(self):
        """Get the pitch value.
        @return: An integer.
        """
        return self.__pitch

    # --------------------------------------------------------------------------
    # Set the pitch value.
    # --------------------------------------------------------------------------
    def setPitch(self, pitch):
        """Set the pitch value.
        @param pitch: The pitch.
        """
        self.__pitch = pitch

    # --------------------------------------------------------------------------
    # Get the language.
    # --------------------------------------------------------------------------
    def getLanguage(self):
        """Get the language.
        @return: A string.
        """
        return self.__language

    # --------------------------------------------------------------------------
    # Set the language.
    # --------------------------------------------------------------------------
    def setLanguage(self, language):
        """Set the language.
        @param language: The language.
        """
        self.__language = language

    # --------------------------------------------------------------------------
    # Get the country.
    # --------------------------------------------------------------------------
    def getCountry(self):
        """Get the country.
        @return: A string.
        """
        return self.__country

    # --------------------------------------------------------------------------
    # Set the country.
    # --------------------------------------------------------------------------
    def setCountry(self, country):
        """Set the country.
        @param country: The country.
        """
        self.__country = country

    # --------------------------------------------------------------------------
    # Get the locutor.
    # --------------------------------------------------------------------------
    def getLocutor(self):
        """Get the locutor.
        @return: A string.
        """
        return self.__locutor

    # --------------------------------------------------------------------------
    # Set the locutor.
    # --------------------------------------------------------------------------
    def setLocutor(self, locutor):
        """Set the locutor.
        @param locutor: The locutor.
        """
        self.__locutor = locutor

    # --------------------------------------------------------------------------
    # Get if the plugin is traced or not.
    # --------------------------------------------------------------------------
    def isTraces(self):
        """Get if the plugin is traced or not.
        @return: A boolean.
        """
        return self.__traces

    # --------------------------------------------------------------------------
    # Set if the plugin is traced or not.
    # --------------------------------------------------------------------------
    def setTraces(self, traces):
        """Set if the plugin is traced or not.
        @param traces: Is traced or not.
        """
        self.__traces = traces

    # --------------------------------------------------------------------------
    # Get if the plugin is a daemon or not.
    # --------------------------------------------------------------------------
    def isDaemon(self):
        """Get if the plugin is a daemon or not.
        @return: A boolean.
        """
        return self.__daemon

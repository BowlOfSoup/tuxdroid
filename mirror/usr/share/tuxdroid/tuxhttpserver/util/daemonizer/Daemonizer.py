# -*- coding: utf-8 -*-

import version
__date__ = version.date
__version__ = version.version
__licence__ = version.licence
del version

#    Copyleft (C) 2008 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import os
import sys
import errno
from util.misc.systemPaths import systemPaths

# ==============================================================================
# Public class
# ==============================================================================

# ------------------------------------------------------------------------------
# Class to deal with the pidfile.
# ------------------------------------------------------------------------------
class PIDFile(object):
    """Class to deal with the pidfile.
    The original version come from the sysklogd package,
    under GPL Copyright (c) 1995  Martin Schulze <Martin.Schulze@Linux.DE>
    """

    # --------------------------------------------------------------------------
    # Constructor.
    # --------------------------------------------------------------------------
    def __init__(self, name, path = "/var/run"):
        """Constructor of the class.

        @param name: name of the daemon.
        @param path: path of the pid file.
        """
        # Search where the PID file must be placed
        path = systemPaths.getPidPath()
        if not os.path.isdir(path):
            os.makedirs(path, mode=0755)

        self.__PIDFILE = "%s/%s.pid" % (path, name)

    # --------------------------------------------------------------------------
    # Read the pid value from the pid file.
    # --------------------------------------------------------------------------
    def read(self):
        """Read the pid value from the pid file.
        @return: pid if exists or 0.
        """
        pid = 0
        try:
            f = open(self.__PIDFILE, "r")
            try:
                pid = int(f.readline())
            finally:
                f.close()
        except:
            pass
        return pid

    # --------------------------------------------------------------------------
    # Write the pid value in the pid file.
    # --------------------------------------------------------------------------
    def write(self):
        """Write the pid value in the pid file.
        @return: the success of the operation.
        """
        pid = os.getpid()
        result = False
        try:
            f = open(self.__PIDFILE, "w")
            try:
                f.write("%d\n" % pid)
            finally:
                f.close()
                result = True
        except:
            print 'can not write file'
        return result

    # --------------------------------------------------------------------------
    # Check that an instance of the same program is started.
    # --------------------------------------------------------------------------
    def check(self):
        """Check that an instance of the same program is started.
        If the program is already started, the function kill it.
        @return: False in all cases except for that a program is already started.
        """
        pid = os.getpid()
        oldPid = self.read()
        # Program not runned or its pid is the same
        if (oldPid == pid) or (oldPid == 0):
            # RETURN only one instance.
            return False
        # Program is already started
        # Try to kill it.
        try:
            os.kill(oldPid, 0)
        # Can't kill it.
        except OSError, why:
            if why[0] == errno.ESRCH:
                # RETURN only one instance (old pid reference is broken)
                return False
            else:
                # RETURN not the only one instance (Can't kill the program)
                return True
        # RETURN only one instance (old pid instance has been killed)
        return False

    # --------------------------------------------------------------------------
    # Remove the pid file.
    # --------------------------------------------------------------------------
    def remove(self):
        """Remove the pid file.
        """
        try:
            os.remove(self.__PIDFILE)
        except:
            pass

# ------------------------------------------------------------------------------
# Class to daemonizing a program. (Unix)
# ------------------------------------------------------------------------------
class Daemonizer(object):
    """Class to daemonizing a program. (Unix)
    """

    # --------------------------------------------------------------------------
    # Constructor.
    # --------------------------------------------------------------------------
    def __init__(self, name, logPath, serviceFunct, redirectIO = True):
        """Constructor of the class.

        @param name: name of the program.
        @param logPath: path of the log file.
        @param serviceFunct: pointer to the service to run.
        @param redirectIO: indicate if the stdout and stdin must be redirected
        in the log file.
        """
        if not os.path.isdir(logPath):
            os.makedirs(logPath, mode=0755)
        logFilename = '%s/%s.log' % (logPath, name)
        self.__daemonize(redirectIO, '/dev/null', logFilename, logFilename)
        self.__pidfile = PIDFile(name)
        self.__serviceFunct = serviceFunct

    # --------------------------------------------------------------------------
    # Start the service as daemon.
    # --------------------------------------------------------------------------
    def start(self):
        """Start the service as daemon.
        @return: the success of the operation.
        """
        result = True
        if not self.__pidfile.check():
            if not self.__pidfile.write():
                result = False
        else:
            result = False
        if result:
            try:
                self.__serviceFunct()
            except:
                result = False
        return result

    # --------------------------------------------------------------------------
    # Destructor of the class.
    # --------------------------------------------------------------------------
    def destroy(self):
        """Destructor of the class.
        """
        pass
        #self.__pidfile.remove()

    # --------------------------------------------------------------------------
    # Daemonize the application.
    # --------------------------------------------------------------------------
    #References: UNIX Programming FAQ
    #1.7 How do I get my program to act like a daemon?
    #http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
    #
    #Advanced Programming in the Unix Environment
    #W. Richard Stevens, 1992, Addison-Wesley, ISBN 0-201-56317-7.
    def __daemonize(self, redirectIO, stdin, stdout, stderr):
        """Daemonize the application.
        """
        # Do first fork.
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0) # Exit first parent.
        except OSError, e:
            sys.stderr.write ("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
            sys.exit(1)

        # Decouple from parent environment.
        os.chdir("/")
        os.umask(0)
        os.setsid()

        # Do second fork.
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0) # Exit second parent.
        except OSError, e:
            sys.stderr.write ("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
            sys.exit(1)

        # Now I am a daemon!

        # Redirect standard file descriptors.
        if redirectIO:
            si = file(stdin, 'r')
            so = file(stdout, 'w')
            se = file(stderr, 'w', 0)
            os.dup2(si.fileno(), sys.stdin.fileno())
            os.dup2(so.fileno(), sys.stdout.fileno())
            os.dup2(se.fileno(), sys.stderr.fileno())

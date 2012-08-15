#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
fileasobj.py - Manage a local file as an object. Store contents in a 
                uniq list and ignore commented lines.

nullpass, 2012

"""
__version__ = '1.b.0'

import sys
import os
import fileinput
import platform
import time

class FileAsObj:
    """
    Manage a file as an object. Each line of a file is added to the list
    'self.contents'. Lines that start with a # are ignored. Lines that
    already exist in the .contents lists are ignored- this uniqs the 
    data, however no sorting is done.
    Elements can be added or removed with .add and .rm. 
    The object's contents can be written back to the file, overwritting
    the file, with .write. 
    
    """
    def __init__(self,file):
        """
        read file into list varaible, uniq and without line breaks
        Ignore lines that start with #
        """
        self.Birthday = (float(time.time()),str(time.strftime("%a %b %d %H:%M:%S %Z %Y", time.localtime())))
        #
        # Name of file this is running as
        self.thisExec = str(os.path.basename(sys.argv[0]))
        if len(self.thisExec) < 3 or len(self.thisExec) > 255:
            #
            # If there's no name in argv[0], like if you call this from 
            # the Python shell, call this python_$$
            # Also catches names too short or long.
            self.thisExec = 'python_'+str(os.getpid())
        #
        # Hostname
        self.thisHost = node()
        #
        # Current executable and PID, like myapp[12345]
        self.thisProc = self.thisExec.rstrip('.py')+"["+str(os.getpid())+"]"
        #
        # List of any exceptions caught
        self.Errors = []
        #
        # String containing information about steps taken. Used for debugging
        self.Trace = ''
        #
        #
        self.contents = []
        #
        #
        try:
            self.__log('Read-only opening '+file)
            for line in fileinput.input(file):
                if line[0] is not "#":
                    #
                    #uniq the contents of the file when reading.
                    line = line.strip("\n")
                    if len(line) > 1 and line not in self.contents:
                        self.contents.append(line)
            fileinput.close()
        except Exception as e:
            self.Errors.append(e)
            return False
        #
        #declare current state is original data from file.
        self.virgin = True
        #
        #set filename inside object, used during .write()
        self.filename = file
    def __log(self,thisEvent):
        """
        Private method to update self.Trace with str(thisEvent) given
        as argument.
        """
        if not self.Enabled:
            return True
        self.Trace += str(time.strftime("%a %b %d %H:%M:%S %Z %Y", time.localtime()))+' '+self.thisHost+' '+self.thisProc+' '+str(thisEvent)+'\n'
        return
    def check(self,needle):
        """
        check existing contents of file for a string
        
        if myfile.check('foo'):
            -or-
        if 'foo' in myfile.contents:
        """
        if needle in self.contents:
            return True
        return False
    def add(self,item):
        """
        add item to end of list unless it already exists.
        """
        #
        #Check for the item.
        if item not in self.contents:
            #
            # not present, adding.
            self.contents.append(item)
            #
            #declare something in this object has changed since __init__
            self.virgin = False
            return True
        #
        # Already present, no changes made.
        return False
    def rm(self,item):
        """
        remove item from contents.
        """
        #
        #Check for item
        self.__log("Call to remove '"+item+"' from "+self.filename)
        if item in self.contents:
            #
            #item found, removed.
            self.contents.remove(item)
            #
            #declare something in this object has changed since __init__
            self.virgin = False
            return True
        #
        # wasn't there, nothing changed.
        return False
    def inventory(self):
        """
        return contents of self.contents
        
        Useful for printing contents, but hilariously redundant.
        """
        return self.contents
    def write(self):
        """
        write self.contents to self.filename
        self.filename was defined during __init__
        """
        self.__log("Writing "+self.filename)
        f = open(self.filename, "w")
        for line in self.contents:
            f.write(line+"\n")
        f.close()
        return True

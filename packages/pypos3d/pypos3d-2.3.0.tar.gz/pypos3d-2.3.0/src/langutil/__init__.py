# -*- coding: utf-8 -*-
__version__ = '1.8.2'
__author__  = 'Olivier DUFAILLY'
__license__ = 'BSD'


import os
import os.path
import gzip
import logging

# Usual and common return codes
C_CANCEL  = 0x100
C_WARNING = 0x010
C_OK      = 0
C_FAIL    = -3
C_FILE_NOT_FOUND = -4
C_UNKNOWN        = -5
C_ERROR   = -1000 # Should be a very wrong case

def GetLowExt(fn):
  ''' Return the file extension in lower char '''
  lfn = fn.lower()
  p = lfn.rfind('.')
  return lfn[p+1:] if p>0 else ''

def cmp(a, b):
  return (a > b) - (a < b) 

#-----------------------------------------------------------------------#
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False

# def getDirectory(path): --> use os.path.dirname

def RemoveExt(filename):
  posext = -1 if (filename == None) else filename.rfind('.')
  return filename[0:posext] if posext>0 else filename

def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K:
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K


class UsageError(Exception):
  ''' Exception used to manage 'usage' errors:
  - Syntax Errors
  - User Input Errors
  - Missing actors, groups, ...
  '''
  def __init__(self, msg, ret=C_OK, *args):
    super().__init__(msg)
    self.ret = ret
    
def RaiseCond(condition, msg, ret=C_OK, statusCell=None):
  '''
  Raise an UsageError Exception when 'condition' is True
  Useful for non (really) structured coding.
  '''
  if condition:
    raise UsageError(msg, statusCell, ret)

class LogStatus:
  ''' Simple Logging class used to return statuses of complex algorithms '''
  def __init__(self, usedLogging = True):
    self.ret = C_OK
    self.msg = ''
    self.uselog = usedLogging
    
  def info(self, msg='', *args):
    '''
    To be Overloaded for MMI purpose.
    Called by status(), worstStatus and logCond() methods
    '''
    sm = self.__class__.__name__  + ':' + msg.format(*args)
    self.msg = self.msg+' '+sm if self.msg else sm
    if self.uselog:
      logging.info(self.msg)
    return self.msg

  def status(self, ret=C_OK, msg='', *args):
    self.ret = ret
    if msg:
      self.info(msg, *args)
    return self.ret

  def worstStatus(self, ret=C_OK, msg='', *args):
    self.ret = min(ret, self.ret)
    if msg:
      self.info(msg, *args)
    return self.ret

  def logCond(self, cond, msg, *args):
    if cond:
      self.info(msg, *args)
    return cond
  
  def raiseCode(self, ret=C_OK, msg='', *args):
    if ret!=C_OK:
      self.status(ret=ret, msg=msg, *args)
      raise UsageError(msg, self)
    
# This code was written by Krzysztof Kowalczyk (http://blog.kowalczyk.info)
# and is placed in public domain.
# Convert a Mozilla-style version string into a floating-point number
#   1.2.3.4, 1.2a5, 2.3.4b1pre, 3.0rc2, etc
def version2float(v):

  def v2fhelper(v, suff, version, weight):
    parts = v.split(suff)
    if 2 != len(parts):
        return v
    version[4] = weight
    version[5] = parts[1]
    return parts[0]
  
  version = [
      0, 0, 0, 0, # 4-part numerical revision
      4, # Alpha, beta, RC or (default) final
      0, # Alpha, beta, or RC version revision
      1  # Pre or (default) final
  ]
  parts = v.split("pre")
  if 2 == len(parts):
      version[6] = 0
      v = parts[0]

  v = v2fhelper(v, "a",  version, 1)
  v = v2fhelper(v, "b",  version, 2)
  v = v2fhelper(v, "rc", version, 3)

  parts = v.split(".")[:4]
  for (p, i) in zip(parts, range(len(parts))):
      version[i] = p
  ver = float(version[0])
  ver += float(version[1]) / 100.
  ver += float(version[2]) / 10000.
  ver += float(version[3]) / 1000000.
  ver += float(version[4]) / 100000000.
  ver += float(version[5]) / 10000000000.
  ver += float(version[6]) / 1000000000000.
  return ver



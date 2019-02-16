#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

#_______________________________________________________________________________
class pycolor():
  end       = '\033[0m'
  bold      = '\033[1m'
  underline = '\033[4m'
  reverse   = '\033[07m'
  invisible = '\033[08m'
  black     = '\033[30m'
  red       = '\033[31m'
  green     = '\033[32m'
  yellow    = '\033[33m'
  blue      = '\033[34m'
  magenta   = '\033[35m'
  cyan      = '\033[36m'
  white     = '\033[37m'
  clear     = '\033[2'
  cut       = '\033[K'
  up        = '\033[A'
  down      = '\033[B'

  #_____________________________________________________________________________
  @classmethod
  def Form(cls, arg, opt=''):
    return opt + arg + cls.end

  #_____________________________________________________________________________
  @classmethod
  def Print(cls, arg, opt):
    print(opt + arg + cls.end)

#_______________________________________________________________________________
def ExitFailure(message):
  sys.stderr.write(pycolor.yellow + pycolor.bold
                   + '#E ' + message + '\n' + pycolor.end)
  sys.exit(-1)

#_____________________________________________________________________________
def Print(arg, color):
  print(color + arg + pycolor.end)

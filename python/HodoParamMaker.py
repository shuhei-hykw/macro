#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import sys

import EnvManager as env
import utility

myname = os.path.basename(__file__).replace('.py', '')

#_______________________________________________________________________________
def MakeParameter(parray, overwrite=False, verbose=False):
  func_name = myname + '.MakeParameter()'
  if not os.path.isfile(env.param_file):
    utility.ExitFailure(func_name + ' cannot find parameter')
  for elem in parray:
    if len(elem) != 7:
      parray.remove(elem)
  with open(env.output_file, 'w') as out:
    #print(func_name + ' open ' + env.param_file)
    with open(env.param_file, 'r') as param:
      for line in param:
        buf = line
        columns = line.split()
        if not '#' in line and len(columns) == 7:
          for elem in parray:
            check = True
            for i in range(5):
              check = (True if check and int(elem[i]) == int(columns[i])
                       else False)
            if check:
              buf = ('{0}\t{1}\t{2}\t{3}\t{4}\t{5:.3f}\t{6:.3f}\n'
                     .format(elem[0], elem[1], elem[2], elem[3],
                             elem[4], elem[5], elem[6]))
        out.write(buf)
  if overwrite:
    if verbose:
      print(func_name + ' copy ' + env.output_file
            + ' -> ' + env.param_file)
    shutil.copy2(env.output_file, env.param_file)

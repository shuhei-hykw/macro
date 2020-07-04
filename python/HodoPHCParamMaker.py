#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import sys

import EnvManager as env
import utility

myname = os.path.basename(__file__).replace('.py', '')

#_______________________________________________________________________________
#	Type=1 ct=t-p[0]/sqrt(a-p[1])+p[2]
''' Type=2 ct=p[0]*a*a + p[1]*a + p[2] '''
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
        if not '#' in line and len(columns) == 9:
          for elem in parray:
            check = True
            for i in range(6):
              check = (True if check and int(elem[i]) == int(columns[i])
                       else False)
            if check:
              buf = ('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6:.3f}\t{7:.3f}\t{8:.3f}\n'
                     .format(elem[0], elem[1], elem[2], elem[3], elem[4],
                             elem[5], elem[6], elem[7], elem[8]))
        out.write(buf)
  if overwrite:
    if verbose:
      print(func_name + ' copy ' + env.output_file
            + ' -> ' + env.param_file)
    shutil.copy2(env.output_file, env.param_file)

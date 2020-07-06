#!/usr/bin/env python3

import argparse
import os
import shutil
import sys
import subprocess

import settings

#______________________________________________________________________________
class RunMacro():

  #____________________________________________________________________________
  def __init__(self, macro_path, run_number,
               compile=True, batch=True, interactive=False, quiet=False,
               sync=True):
    output_path = '{}_{:05d}'.format(macro_path.replace('.C', ''), run_number)
    macro_path = os.path.join(settings.macro_dir, os.path.basename(macro_path))
    macro_path = macro_path.replace('.C', '')+'.C'
    self.__status = os.path.isfile(macro_path)
    macro_path += '+O' if compile else ''
    command = 'root -l {} {} "{}({})"'.format('-b' if batch else '',
                                              '-q' if not interactive else '',
                                              macro_path, run_number)
    self.__macro_path = macro_path
    self.__run_number = run_number
    self.__compile = compile
    self.__batch = batch
    self.__interactive = interactive
    self.__quiet = quiet
    self.__sync = sync
    self.__command = command
    self.__process = None
    self.__devnull = open(os.devnull, 'w')
    self.__stdout = self.__devnull if quiet else sys.stdout
    self.__stderr = self.__devnull if quiet else sys.stderr
    self.__output = os.path.join(settings.tune_dir, output_path)
    if 'TFitBH1' in self.__output:
      self.__param = os.path.join(settings.param_dir, 'HDPRM',
                                  'HodoParam_{:05d}'.format(run_number))
    else:
      self.__param = None
      self.__status = False

  #____________________________________________________________________________
  def __del__(self):
    if self.__process is not None:
      self.wait()
    self.__devnull.close()

  #____________________________________________________________________________
  def isrunning(self):
    if self.__process is None:
      return False
    else:
      return (self.__process.poll() is None)

  #____________________________________________________________________________
  def run(self):
    if not self.__status or self.__process is not None:
      print('RunMacro.run() failed, status = {}, process = {}'
            .format(self.__status, self.__process))
      print(self.__macro_path)
      return
    print('RunMacro.run()',
          os.path.basename(self.__macro_path), self.__run_number)
    try:
      self.__process = subprocess.Popen(self.__command, shell=True,
                                        stdout=self.__stdout,
                                        stderr=self.__stderr)
    except subprocess.CalledProcessError as e:
      print('\n#E "{}" returned error code {}\n'
            .format(e.cmd, e.returncode))
    if self.__sync:
      self.wait()

  #____________________________________________________________________________
  def update(self):
    if (not self.__status or self.__param is None or
        not os.path.isfile(self.__param) or
        not os.path.isfile(self.__output)):
      print('RunMacro.update() failed, status = {}'
            .format(self.__status))
      return
    print('RunMacro.update() copy {} -> {}'
          .format(os.path.basename(self.__output),
                  os.path.basename(self.__param)))
    shutil.copy2(self.__output, self.__param)

  #____________________________________________________________________________
  def wait(self):
    while True:
      if self.__process is None or self.__process.poll() is not None:
        break

#______________________________________________________________________________
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('macro_path',
                      help='target macro path')
  parser.add_argument('run_number', type=int,
                      help='run number')
  parser.add_argument('-c', '--compile', action='store_true',
                      help='flag to compile macro')
  args = parser.parse_args()
  RunMacro(args.macro_path, args.run_number, args.compile).run()

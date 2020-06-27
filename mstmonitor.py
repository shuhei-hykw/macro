#!/usr/bin/env python3

import os
import subprocess
import sys
import time

#______________________________________________________________________________
def make_root_file(run_number, root_file):
  base_yml = 'runmanager/runlist/mstmonitor.yml'
  base_head, base_ext = os.path.splitext(base_yml)
  new_yml = '{}_{:05d}{}'.format(base_head, run_number, base_ext)
  if os.path.isfile(new_yml):
    return
  res = subprocess.Popen('bjobs 2>/dev/null|wc -l',
                         stdout=subprocess.PIPE,
                         shell=True).communicate()[0]
  # if int(res) > 600:
  #   return
  print('make {}'.format(root_file))
  with open(base_yml, 'r') as base:
    with open(new_yml.format(run_number), 'w') as newlist:
      for line in base:
        newlist.write(line)
      newlist.write('  {}:\n'.format(run_number))
  cmd = 'runmanager/run.py {}'.format(new_yml)
  subprocess.Popen(cmd.split())
  time.sleep(10)

#______________________________________________________________________________
def monitor():
  data_dir = 'e40_2020feb'
  root_dir = 'MsTMonitor/rootfile'
  while True:
    for dat in sorted(os.listdir(data_dir)):
      if '.dat.gz' not in dat or '.run' in dat:
        continue
      run_head = dat.replace('.dat.gz', '')
      run_number = int(run_head.replace('run', ''))
      if run_number < 7100:
        continue
      root_file = '{}/{}_MsTMonitor.root'.format(root_dir, run_head)
      tmp_file = '{}/tmp/{}_tmp'.format(root_dir, run_head)
      if not os.path.isfile(root_file):
        if not os.path.isfile(tmp_file):
          print('touch ', tmp_file)
          with open(tmp_file, 'w') as f:
            pass
        make_root_file(run_number, root_file)
      else:
        if os.path.isfile(tmp_file):
          print('remove ', tmp_file)
          os.remove(tmp_file)
    time.sleep(1)

#______________________________________________________________________________
if __name__ == '__main__':
  monitor()

#!/usr/bin/env python3

import glob
import os

#______________________________________________________________________________
def check_scaler_evnum():
  work_dir = os.path.dirname(os.path.dirname(__file__))
  scaler_dir = os.path.join(work_dir, 'scaler')
  print('scaler_dir = {}'.format(scaler_dir))
  for file_path in sorted(glob.glob(os.path.join(scaler_dir, '*.txt'))):
    event_recorder = 0
    event_unpacker = 0
    with open(file_path, 'r') as f:
      lines = f.readlines()
      if len(lines) == 116:
        recorder = lines[0].split()
        if len(recorder) == 20:
          event_recorder = int(recorder[15])
        event = lines[3].split()
        if len(event) == 2:
          event_unpacker = int(event[1])
    if event_recorder != event_unpacker:
      print('{} : R={:8d}, U={:8d}'
            .format(file_path, event_recorder, event_unpacker))

#______________________________________________________________________________
if __name__ == '__main__':
  check_scaler_evnum()

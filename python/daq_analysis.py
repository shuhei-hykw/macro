#!/usr/bin/env python2

import glob
import os
import EnvManager
import helper
import ROOT

#______________________________________________________________________________
def analyze():
  ROOT.gROOT.SetBatch()
  # EnvManager.Print()
  scaler_dir = os.path.join(EnvManager.ana_dir, 'scaler')
  fig_file = os.path.join(EnvManager.fig_dir, 'daq_analysis.pdf')
  print('scaler_dir = {}'.format(scaler_dir))
  helper.HB1(1, 'NWords', 1000, 0, 10000, 'Words', 'Counts')
  helper.HB1(2, 'DAQ Eff.', 310, 0.70, 1.01, '', 'Counts')
  # helper.HB1(3, 'L2 Eff.', 1010, 0, 1.01, '%', 'Counts')
  helper.HB2(3, 'DAQ Eff. % NWords', 100, 4800, 6000, 100, 0.70, 0.90, 'Words', '')
  helper.HB2(4, 'DAQ Eff. % L2 Eff', 30*2, 0.30, 0.60, 31*2, 0.70, 1.01, '', '')
  for file_path in sorted(glob.glob(os.path.join(scaler_dir, '*.txt'))):
    scaler = dict()
    with open(file_path, 'r') as f:
      for line in f.readlines():
        column = line.split()
        if len(column) == 20:
          recorder_event_number = int(column[15])
          recorder_data_size = float(column[18]) / 4.
        if len(column) == 2:
          scaler[column[0]] = float(column[1])
    if 'DAQ-Eff' not in scaler or 'L2-Eff' not in scaler:
      continue
    one_event_data_size = recorder_data_size / recorder_event_number
    print(one_event_data_size)
    helper.HF1(1, one_event_data_size)
    helper.HF1(2, scaler['DAQ-Eff'])
    # helper.HF1(3, scaler['L2-Eff'])
    helper.HF2(3, one_event_data_size, scaler['DAQ-Eff'])
    helper.HF2(4, scaler['L2-Eff'], scaler['DAQ-Eff'])
  c1 = ROOT.TCanvas()
  c1.Divide(2, 2)
  for i in range(4):
    c1.cd(i + 1)
    h = helper.HGet(i + 1)
    if h is not None:
      h.Draw('colz')
  c1.Print(fig_file)

#______________________________________________________________________________
if __name__ == '__main__':
  analyze()

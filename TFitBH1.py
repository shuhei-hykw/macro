#!/usr/bin/env python2

import argparse
import os
import sys
import ROOT

import EnvManager
from DetectorID import MaxDepth, DetIdBH1, NumOfSegBH1, AorT, UorD

#______________________________________________________________________________
def Run(root_file):
  ROOT.gROOT.SetBatch()
  print(('TFitBH1.Run() ' + '_'*80)[:80])
  f = ROOT.TFile.Open(root_file)
  t = f.Get('tree')
  harray = []
  for ud in UorD:
    for i in range(NumOfSegBH1):
      n = 'h{}_{}'.format(i, ud)
      harray.append(ROOT.TH1D(n, '{};TDC;Counts'.format(n),
                              100000, 300000., 400000.))
  nevent = t.GetEntries()
  t.SetBranchStatus('*', False)
  t.SetBranchStatus('bh1nhits', True)
  t.SetBranchStatus('bh1ut', True)
  t.SetBranchStatus('bh1dt', True)
  t.Print()
  for iev in range(nevent):
    if (iev % 1000) == 0:
      print('event number = {}/{}'.format(iev, nevent))
    t.GetEntry(iev)
    for i in range(NumOfSegBH1):
      for m in range(MaxDepth):
        if t.bh1ut[i*16+m] > 0:
          harray[i].Fill(t.bh1ut[i*16+m])
        # if t.bh1dt[i][m] > 0:
        #   harray[i + NumOfSegBH1].Fill(t.bh1dt[i][m])
  print('Start fitting BH1 TDC')
  c1 = ROOT.TCanvas('c1', 'c1', 1200, 800)
  c1.Divide(6, 4)
  for ud in UorD:
    print(type(ud))
    #    for i in range(NumOfSegBH1):
    #      c1.cd(i + ud*(NumOfSegBH1+1) + 1)
    #      h = TH1D('')
  c1.Print(EnvManager.fig_file)

#______________________________________________________________________________
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('run_number', type=int, help='run_number')
  parsed, unpased = parser.parse_known_args()
  EnvManager.SetFigFile('tune', 'TFitBH1.pdf')
  EnvManager.SetParamFile('HDPRM',
                          'HodoParam_{:05d}'.format(parsed.run_number))
  EnvManager.SetRootFile('Hodoscope', parsed.run_number)
  EnvManager.Print()
  try:
    Run(EnvManager.root_file)
  except KeyboardInterrupt:
    print()

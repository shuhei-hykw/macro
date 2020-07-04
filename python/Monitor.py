#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import os
import sys

interval = 10 # [sec]
target_jobs = ['s', 'l', 'h']

#_______________________________________________________________________________
def monitor(batch=False):
  ROOT.gROOT.SetBatch(batch)
  c1 = ROOT.TCanvas('c1', '{} -- {}@{}'.format(os.path.basename(__file__),
                                               ROOT.gSystem.Getenv('USER'),
                                               ROOT.gSystem.Getenv('HOSTNAME')),
                    500, 500)
  c1.SetTopMargin(0.050)
  name = []
  command = []
  for j in target_jobs:
    name.append('Run  ({})'.format(j))
    name.append('Pend ({})'.format(j))
    command.append('bjobs 2>/dev/null | grep RUN  | grep " {} " | wc -l'.format(j))
    command.append('bjobs 2>/dev/null | grep PEND | grep " {} " | wc -l'.format(j))
  NumOfGraph = len(name)
  NumOfPlot  = 100
  njobs = [[0 for i in range(NumOfPlot)] for j in range(NumOfGraph)]
  color = [ROOT.kMagenta, ROOT.kCyan, ROOT.kRed,
           ROOT.kBlue, ROOT.kGreen, ROOT.kOrange]
  unix_time = []
  now = ROOT.TTimeStamp()
  now.Add(ROOT.TTimeStamp(-now.GetZoneOffset()))
  for ip in range(NumOfPlot):
    unix_time.append(now.GetSec() + interval * (ip - NumOfPlot))
  graphs = [ROOT.TGraph() for i in range(NumOfGraph)]
  leg = ROOT.TLegend(0.150, 0.150, 0.340, 0.500)
  leg.SetTextAlign(12)
  leg.SetTextSize(0.040)
  for ig, g in enumerate(graphs):
    g.SetPoint(0, 0, 0)
    g.SetLineColor(color[ig])
    g.SetLineWidth(3)
    leg.AddEntry(g, name[ig], 'L')
    g.Draw('AL') if ig==0 else g.Draw('L')
  leg.Draw()
  text = ROOT.TText(0.150, 0.850, '')
  text.SetNDC(1)
  text.SetTextFont(42)
  text.Draw()
  try:
    while True:
      print(now.AsString('s'))
      now.Set()
      now.Add(ROOT.TTimeStamp(-now.GetZoneOffset()))
      unix_time.pop(0)
      unix_time.append(now.GetSec())
      max_jobs = 0
      for ig in xrange(NumOfGraph):
        val = process_command(command[ig])
        graphs[ig].Set(0)
        njobs[ig].pop(0)
        njobs[ig].append(val)
        for ip, u in enumerate(unix_time):
          graphs[ig].SetPoint(ip, u, njobs[ig][ip])
          max_jobs = ROOT.TMath.Max(max_jobs, njobs[ig][ip])
        graphs[ig].GetXaxis().SetTimeDisplay(1)
        graphs[ig].GetXaxis().SetLabelOffset(0.04)
        graphs[ig].GetXaxis().SetTimeFormat('#splitline{%Y/%m/%d}{  %H:%M:%S}')
        graphs[ig].GetXaxis().SetTimeOffset(now.GetZoneOffset(), 'jpn')
        graphs[ig].GetXaxis().SetNdivisions(-503)
        print(' {0} : {1:5d} '.format(name[ig], val), end='')
        if (ig % 2) == 1 and ig != NumOfGraph - 1: print('')
      graphs[0].GetYaxis().SetRangeUser(0., max_jobs*1.1)
      text.SetText( 0.140, 0.880, now.AsString('s') )
      c1.Modified()
      c1.Update()
      print('')
      sleep(interval)
  except KeyboardInterrupt:
    print('Ctrl-C interrupted')
  ROOT.gApplication.Terminate()

#_______________________________________________________________________________
def process_command(command):
  pipe = ROOT.gSystem.OpenPipe(command, 'r')
  line = ROOT.TString()
  if line.Gets(pipe):
    ROOT.gSystem.ClosePipe(pipe)
    return int(line.Data())
  else:
    return 0

#_______________________________________________________________________________
def sleep(sec):
  now = ROOT.TTimeStamp()
  while not ROOT.gSystem.ProcessEvents():
    if ROOT.TTimeStamp().GetSec() - now.GetSec() > sec:
      return

#_______________________________________________________________________________
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-b', '--batch', action='store_true', help='batch mode')
  parsed, unparsed = parser.parse_known_args()
  try:
    import ROOT
    monitor(parsed.batch)
  except:
    print(sys.exc_info())

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import os
import sys

from ROOT import (
  TCanvas, TGraph, TLegend, TMath, TString, TSystem, TText, TTimeStamp,
  gApplication, gROOT, gSystem,
  kMagenta, kCyan, kRed, kBlue, kGreen, kOrange, kBlack
)

interval = 10 # [sec]
target_jobs = ['s', 'l', 'h']

#_______________________________________________________________________________
def sleep(sec=interval):
  now = TTimeStamp()
  while not gSystem.ProcessEvents():
    if TTimeStamp().GetSec() - now.GetSec() > sec:
      return

#_______________________________________________________________________________
def process_command(command):
  pipe = gSystem.OpenPipe(command, 'r')
  line = TString()
  if line.Gets(pipe):
    gSystem.ClosePipe(pipe)
    return int(line.Data())
  else:
    return 0

#_______________________________________________________________________________
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--batch', '-b', action='store_true',
                      default=False, help='batch mode option')
  parsed, unparsed = parser.parse_known_args()
  gROOT.Reset()
  if parsed.batch:
    gROOT.SetBatch(True)
  c1 = TCanvas('c1', '{0}@{1}'.format(gSystem.Getenv('USER'),
                                      gSystem.Getenv('HOSTNAME')),
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
  color = [kMagenta, kCyan, kRed, kBlue, kGreen, kOrange]
  unix_time = []
  now = TTimeStamp()
  now.Add(TTimeStamp(-now.GetZoneOffset()))
  for ip in range(NumOfPlot):
    unix_time.append(now.GetSec() + interval * (ip - NumOfPlot))
  graphs = [TGraph() for i in range(NumOfGraph)]
  leg = TLegend(0.150, 0.150, 0.340, 0.500)
  leg.SetTextAlign(12)
  leg.SetTextSize(0.040)
  for ig, g in enumerate(graphs):
    g.SetPoint(0, 0, 0)
    g.SetLineColor(color[ig])
    g.SetLineWidth(3)
    leg.AddEntry(g, name[ig], 'L')
    g.Draw('AL') if ig==0 else g.Draw('L')
  leg.Draw()
  text = TText(0.150, 0.850, '')
  text.SetNDC(1)
  text.SetTextFont(42)
  text.Draw()
  try:
    while True:
      print(now.AsString('s'))
      now.Set()
      now.Add(TTimeStamp(-now.GetZoneOffset()))
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
          max_jobs = TMath.Max(max_jobs, njobs[ig][ip])
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
      sleep()
  except KeyboardInterrupt:
    print('Ctrl-C interrupted')
  gApplication.Terminate()

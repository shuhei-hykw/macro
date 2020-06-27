#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import sys

from ROOT import (
  TCanvas, TGraph, TLegend, TMath, TString, TSystem, TText, TTimeStamp,
  gApplication, gROOT, gSystem,
  kMagenta, kCyan, kRed, kBlue, kGreen, kOrange, kBlack
  )

"""
global
"""
interval = 10 # [sec]


#_______________________________________________________________________________
def sleep(sec=interval):
  now = TTimeStamp()
  while not gSystem.ProcessEvents():
    if TTimeStamp().GetSec() - now.GetSec() > sec:
      return

#_______________________________________________________________________________
def process_command(command):
  pipe = gSystem.OpenPipe(command, "r")
  line = TString()
  if line.Gets(pipe):
    gSystem.ClosePipe(pipe)
    return line.Data()
  else:
    return "0"

#_______________________________________________________________________________
if __name__ == "__main__":
  gROOT.Reset()
  # gROOT.SetBatch(True)
  c1 = TCanvas("c1", "{0}@{1}".format(
    gSystem.Getenv("USER"), gSystem.Getenv("HOSTNAME")), 500, 500)
  c1.SetTopMargin(0.050)
  name = ["Run  (s)", "Pend (s)",
          "Run  (l)", "Pend (l)",
          "Run  (h)", "Pend (h)"]
  NumOfGraph = len(name)
  NumOfPlot  = 100
  njobs = [[0 for i in range(NumOfPlot)] for j in range(NumOfGraph)]
  color = [kMagenta, kCyan, kRed, kBlue, kGreen, kOrange]
  cmd = [
    "bjobs 2>/dev/null | grep RUN  | grep ' s ' | wc -l",
    "bjobs 2>/dev/null | grep PEND | grep ' s ' | wc -l",
    "bjobs 2>/dev/null | grep RUN  | grep ' l ' | wc -l",
    "bjobs 2>/dev/null | grep PEND | grep ' l ' | wc -l",
    "bjobs 2>/dev/null | grep RUN  | grep ' h ' | wc -l",
    "bjobs 2>/dev/null | grep PEND | grep ' h ' | wc -l"
  ]
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
    leg.AddEntry(g, name[ig], "L")
    if ig==0:
      g.Draw("AL")
    else:
      g.Draw("L")
  leg.Draw()
  text = TText(0.150, 0.850, "")
  text.SetNDC(1)
  text.SetTextFont(42)
  text.Draw()
  try:
    while True:
      buf = now.AsString("s") + '\n'
      now.Set()
      now.Add(TTimeStamp(-now.GetZoneOffset()))
      unix_time.pop(0)
      unix_time.append(now.GetSec())
      max = 0
      for ig in xrange(NumOfGraph):
        val = int(process_command(cmd[ig]))
        graphs[ig].Set(0)
        njobs[ig].pop(0)
        njobs[ig].append(val)
        for ip, u in enumerate(unix_time):
          graphs[ig].SetPoint(ip, u, njobs[ig][ip])
          max = TMath.Max(max, njobs[ig][ip])
        graphs[ig].GetXaxis().SetTimeDisplay(1)
        graphs[ig].GetXaxis().SetLabelOffset(0.04)
        graphs[ig].GetXaxis().SetTimeFormat("#splitline{%Y/%m/%d}{  %H:%M:%S}")
        graphs[ig].GetXaxis().SetTimeOffset(now.GetZoneOffset(), "jpb")
        graphs[ig].GetXaxis().SetNdivisions(-503)
        buf += ' {0} : {1}'.format(name[ig], val)
        if (ig % 2) == 1 and ig != NumOfGraph - 1: buf += '\n'
      graphs[0].GetYaxis().SetRangeUser(0., max*1.1)
      text.SetText( 0.140, 0.880, now.AsString("s") )
      c1.Modified()
      c1.Update()
      print(buf)
      sleep()
  except KeyboardInterrupt:
    print("Ctrl-C interrupted")
  gApplication.Terminate()

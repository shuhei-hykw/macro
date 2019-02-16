#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os

import EnvManager
import fwhm
import run_number
import ROOT
from ROOT import (gROOT, gStyle, kRed, kBlue, TArrow,
                  TCanvas, TCut, TF1, TFile, TGraph,
                  TH1F, TLatex, TLine, TPad)

#_______________________________________________________________________________
if __name__ == '__main__':
  gROOT.Reset()
  gROOT.SetBatch()
  gStyle.SetPalette(52) # grayscale
  ROOT.TColor.InvertPalette()
  rarray = (run_number.emulsion_2016
            + run_number.emulsion_2017)
  g1 = TGraph()
  for m in rarray:
    for r in m:
      message = ('{}/Messages/msglog_run{:05d}.txt'
                 .format('e07_2016' if r < 2000 else
                         'e07_2017', r))
      th1 = [-1 for x in range(24)]
      th2 = [-1 for x in range(24)]
      it1 = 0
      it2 = 0
      with open(message, 'r') as f:
        for l in f:
          columns = l.split()
          if 'Threshold:' in columns:
            for i in range(6):
              th1[it1] = float(columns[i+8])
              it1 += 1
          elif 'Threshold2:' in columns:
            for i in range(6):
              th2[it2] = float(columns[i+1])
              it2 += 1
      print(r, th1)
      print(r, th2)
      if th1[0] > 0:
        g1.SetPoint(g1.GetN(), r, th1[0])
  c1 = TCanvas()
  g1.SetMarkerStyle(8)
  g1.SetMarkerSize(0.4)
  g1.Draw('AP')
  c1.Print('ssd_threshold.ps')

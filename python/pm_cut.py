#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os

import EnvManager
import fwhm
import hstyle
import ROOT
from ROOT import (gROOT, gStyle, kRed, kBlue, TArrow,
                  TCanvas, TCut, TF1, TFile, TGraph,
                  TH1F, TH2F,
                  TLatex, TLine,
                  TMath, TPad)

#_______________________________________________________________________________
if __name__ == '__main__':
  gROOT.Reset()
  gROOT.SetBatch()
  gStyle.SetPalette(52) # grayscale
  ROOT.TColor.InvertPalette()
  #EnvManager.Load()
  parser = argparse.ArgumentParser()
  parser.add_argument('run_number', type=int, help='run_number')
  parsed, unpased = parser.parse_known_args()
  root_file = os.path.join('root/dc/run{:05d}_KuramaTracking.root'.format(parsed.run_number))
  print('run{0:05d} '.format(parsed.run_number) + '_' * 60)
  f1 = TFile.Open(root_file)
  tex = TLatex()
  tex.SetTextFont(132)
  tex.SetTextSize(0.08)
  fig_file = EnvManager.fig_dir + '/dc/pm_cut.ps'
  t1 = f1.Get('kurama')
  h1 = TH1F('h1', 'h1', 300, -0.8, 2.2)
  h2 = TH2F('h2', 'h2', 300, -0.8, 2.2, 250, 0, 2.5)
  h1.SetXTitle('Mass #times Charge [GeV/#font[12]{c}^{2}]')
  h1.SetYTitle('Counts [/0.01 GeV/#font[12]{c}^{2}]')
  h2.SetXTitle('Mass #times Charge [GeV/#font[12]{c}^{2}]')
  h2.SetYTitle('Momentum [GeV/#font[12]{c}]')
  t1.SetBranchStatus('*', 0)
  t1.SetBranchStatus('trigflag', 1)
  t1.SetBranchStatus('ntKurama', 1)
  t1.SetBranchStatus('pKurama', 1)
  t1.SetBranchStatus('qKurama', 1)
  t1.SetBranchStatus('chisqrKurama', 1)
  t1.SetBranchStatus('m2', 1)
  for i in range(t1.GetEntries()):
    t1.GetEntry(i)
    if t1.trigflag[7] > 0:
      for j in range(t1.ntKurama):
        if t1.chisqrKurama[j] < 30:
        #if t1.chisqrKurama[j] < 200:
          # if 0.9 < t1.pKurama[j] and t1.pKurama[j] < 1.5:
          h1.Fill(t1.qKurama[j] * TMath.Sqrt(t1.m2[j]))
          h2.Fill(t1.qKurama[j] * TMath.Sqrt(t1.m2[j]),
                  t1.pKurama[j])
  c1 = TCanvas()
  c1.Divide(2,2)
  c1.cd(1).SetLogz()
  h2.GetXaxis().SetRangeUser(0.35, 0.55)
  h2.GetYaxis().SetRangeUser(0.9, 1.5)
  h2.Draw('col')
  c1.cd(2)
  hp = h2.ProfileY()
  hp.Draw()
  gp = TGraph()
  for i in range(hp.GetNbinsX()):
    if i == 0 or i == hp.GetNbinsX() - 1:
      continue
    gp.SetPoint(gp.GetN(), 0.9+0.05*i, hp.GetBinError(i))
  c1.cd(3)
  gp.SetMarkerStyle(8)
  gp.Draw('AP')
  fp = TF1('fp', 'pol1')
  gp.Fit('fp', '', '')
  c1.Print(fig_file)
  print(fig_file)
  print('done')

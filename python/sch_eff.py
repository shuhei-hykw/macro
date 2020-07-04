#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

import EnvManager
import ROOT
from ROOT import (gROOT, gStyle, kRed, TGraphErrors, TMath,
                  TCanvas, TCut, TFile, TH1F, TH2F, TLatex, TLine)

#_______________________________________________________________________________
if __name__ == '__main__':
  gROOT.Reset()
  gROOT.SetBatch()
  gStyle.SetPalette(52)
  #EnvManager.Load()
  parser = argparse.ArgumentParser()
  parser.add_argument('run_number', type=int, help='root_file')
  parsed, unpased = parser.parse_known_args()
  print('run{0:05d} '.format(parsed.run_number) + '_' * 60)
  fig_file = EnvManager.fig_dir + '/dc/sch_eff.pdf'
  kk_files = ['DstKKAna_{0:05d}.root'.format(parsed.run_number),
              'DstKKAna_02378.root', 'DstKKAna_02907.root', 'DstKKAna_03076.root']
  # ea0c_file = 'Easiroc_{0:05d}.root'.format(parsed.run_number)
  c1 = TCanvas('c1', 'c1')
  h1 = TH1F('h', 'h', 20, 0, 20)
  h2 = TH2F('h2', 'h2', 80, -500, 300, 20, 0, 20)
  tex = TLatex()
  tex.SetTextSize(0.08)
  for k in kk_files:
    f1 = TFile.Open(EnvManager.root_dir + '/' + k)
    # f2 = TFile.Open(EnvManager.root_dir + '/' + ea0c_file)
    t1 = f1.Get('kk')
    # t2 = f2.Get('ea0c')
    # t1.AddFriend( t2 )
    for i in range(t1.GetEntries()):
      # if i == 2000: break
      if i%10000 == 0:
        print(i, t1.GetEntries())
      t1.GetEntry(i)
      if t1.trigflag[5] <= 0: continue
      if t1.ntSdcIn <= 0: continue
      h1.Fill(t1.nhSch)
      for it in range(t1.ntSdcIn):
        h2.Fill(t1.x0SdcIn[it]-t1.u0SdcIn[it]*387.15-150, t1.nhSch)
  g1 = TGraphErrors()
  g1.SetMarkerStyle(8)
  ip = 0
  for i in range(82):
    n0 = h2.GetBinContent(i, 1)
    nall = 0
    for j in range(22):
      nall = nall + h2.GetBinContent(i, j)
    if nall == 0: continue
    eff = 1. - n0/nall
    print(nall-n0, nall, eff)
    g1.SetPoint(ip, -500+10*i, eff)
    g1.SetPointError(ip, 5, TMath.Sqrt(eff*(1-eff)/nall))
    ip = ip + 1
  h1.GetXaxis().SetTitle('SCH NHits')
  h1.Draw()
  c1.Print(fig_file + '(')
  c1.Clear()
  tex.DrawLatexNDC(0.6, 0.6, 'eff. {:.3f}'
                   .format(1. - h1.GetBinContent(1)/h1.GetEntries()))
  print('eff. =', 1. - h1.GetBinContent(1)/h1.GetEntries())
  g1.GetXaxis().SetTitle('Hit position on SCH using SdcIn [mm]')
  g1.GetYaxis().SetTitle('Efficiency')
  g1.GetYaxis().SetRangeUser(0.8, 1.01)
  g1.Draw('AP')
  c1.Print(fig_file + ')')
  print('done')

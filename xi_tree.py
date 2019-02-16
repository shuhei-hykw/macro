#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os

import EnvManager
import fwhm
import hstyle
import ROOT
from ROOT import (gPad, gROOT, gStyle, kRed, kBlue, kGray, TArrow,
                  TCanvas, TCut, TEllipse,
                  TF1, TFile, TGraph, TH1F, TH2F,
                  TLatex, TLine,
                  TMath, TPad, TTree)

#ext = '.ps'
ext = '.pdf'

draw_line = True

target_line = [None, None]

cut_line = []

#_______________________________________________________________________________
def draw_cut_line(h, cut):
  ymax = -1e10
  for i, c in enumerate(cut):
    ymax = max(ymax, h.GetBinContent(h.FindBin(c)) +
               h.GetMaximum()*0.00)
  # if len(cut) == 2:
  #   ymax = 0
  for i, c in enumerate(cut):
    cut_line.append(TArrow(c, h.GetMaximum()*(0.05 if gPad.GetLogy() else 0.5),
                           c, ymax, 0.04, '>'))
    cut_line[-1].Draw()

#_______________________________________________________________________________
def draw_target_size(h, size):
  global target_line
  target_line[0] = TArrow(size[0], h.GetMaximum(),
                          size[0], 0, 0.02, '')
  target_line[1] = TArrow(size[1], h.GetMaximum(),
                          size[1], 0, 0.02, '')
  target_line[0].SetLineStyle(2)
  target_line[1].SetLineStyle(2)
  target_line[0].Draw()
  target_line[1].Draw()

#_______________________________________________________________________________
if __name__ == '__main__':
  gROOT.SetBatch()
  root_file = 'root/v13/DstXiAna_All.root'
  # root_file = 'root/dc/DstXiAna_All.root'
  f1 = TFile.Open(root_file)
  t1 = f1.Get('xi')
  t1.SetBranchStatus('*', 0)
  t1.SetBranchStatus('nCombi', 1)
  t1.SetBranchStatus('chi2Kp', 1)
  t1.SetBranchStatus('pKp', 1)
  t1.SetBranchStatus('m2Kp', 1)
  t1.SetBranchStatus('resAngle', 1)
  t1.SetBranchStatus('MissMass', 1)
  t1.SetBranchStatus('MissP', 1)
  t1.SetBranchStatus('thetaXi', 1)
  t1.SetBranchStatus('MeanDeXi', 1)
  t1.SetBranchStatus('Ssd2Flag', 1)
  tex = TLatex()
  tex.SetTextFont(132)
  tex.SetTextSize(0.08)
  harray = []
  harray.append(TH1F('h1', 'h1;Missing mass [GeV/#font[12]{c}^{2}];Counts [/5 MeV/#font[12]{c}^{2}]', 160, 1., 1.8))
  harray.append(TH1F('h2', 'h2;Incident angle [deg];Counts [/0.5 deg]', 180, 0., 90.))
  #harray.append(TH1F('h3', 'h3;Squared mass [(GeV/#font[12]{c}^{2})^{2}];Counts [/0.002 (GeV/#font[12]{c}^{2})^{2}]', 250, 0., 0.5))
  harray.append(TH1F('h3', 'h3;Squared mass [(GeV/#font[12]{c}^{2})^{2}];Counts', 250, 0., 0.5))
  harray.append(TH1F('h4', 'h4;Mass [GeV/#font[12]{c}^{2}];Counts [/2 GeV/#font[12]{c}^{2}]', 1000, 0., 1))
  harray.append(TH2F('h5', 'h5;Squared mass [(GeV/#font[12]{c}^{2})^{2}];Momentum [GeV/#font[12]{c}]', 200, 0.02, 0.42, 120, 0.9, 1.5))
  harray.append(TH2F('h6', 'h6;Squared mass [(GeV/#font[12]{c}^{2})^{2}];Momentum [GeV/#font[12]{c}]', 200, 0.02, 0.42, 120, 0.9, 1.5))
  harray.append(TH1F('h7', 'h7;#chi^{2}', 1000, 0., 100))
  harray.append(TH2F('h8', 'h8;Mean #DeltaE SSD1 [arb. unit];Missing momentum [GeV/#font[12]{c}]', 150, 0., 150000., 160, 0., 1.6))
  harray_stop = []
  for h in harray:
    hstop = h.Clone()
    # hstop.SetLineColor(kRed+1)
    harray_stop.append(hstop)
  good_event = 0
  for ievent in range(t1.GetEntries()):
    # if ievent == 10000: break
    t1.GetEntry(ievent)
    is_good_event = False
    for iCombi in range(t1.nCombi):
      if t1.resAngle[iCombi] > 3.: continue
      if t1.pKp[iCombi] < 0.9: continue
      if t1.pKp[iCombi] > 1.5: continue
      # if abs(t1.m2Kp[iCombi]-0.22) > 0.12: continue
      harray[6].Fill(t1.chi2Kp[iCombi])
      if t1.chi2Kp[iCombi] > 30.: continue
      cm2 = t1.m2Kp[iCombi] + 0.020
      harray[0].Fill(t1.MissMass[iCombi])
      harray[1].Fill(t1.thetaXi[iCombi])
      harray[2].Fill(cm2)
      harray[3].Fill(TMath.Sqrt(cm2))
      harray[4].Fill(cm2, t1.pKp[iCombi])
      harray[7].Fill(t1.MeanDeXi[iCombi], t1.MissP[iCombi])
      if t1.Ssd2Flag[iCombi] != 2:
        is_good_event = True
        harray_stop[0].Fill(t1.MissMass[iCombi])
        harray_stop[1].Fill(t1.thetaXi[iCombi])
        harray_stop[2].Fill(cm2)
        harray_stop[3].Fill(TMath.Sqrt(cm2))
        harray_stop[4].Fill(cm2, t1.pKp[iCombi])
        harray_stop[7].Fill(t1.MeanDeXi[iCombi], t1.MissP[iCombi])
    if is_good_event:
      good_event += 1
  print('evnet = {}'.format(good_event))
  c1 = TCanvas()
  # harray[0].Draw()
  harray_stop[0].Draw()
  print('xi track        = {}'.format(harray[0].GetEntries()))
  print('xi track (stop) = {}'.format(harray_stop[0].GetEntries()))
  tex.DrawLatexNDC(0.23, 0.83, '(a)')
  c1.Print('fig/dc/xi_missmass' + ext)
  #harray[1].Draw()
  harray_stop[1].Draw()
  c1.Print('fig/dc/xi_theta' + ext)
  harray[2].Draw()
  # harray_stop[2].Draw('same')
  func1 = TF1('func1', 'gaus+pol1(3)')
  func1.SetLineColor(1)
  func1.SetLineWidth(1)
  func1.SetParameter(0, 1000)
  func1.SetParameter(1, 0.24)
  func1.SetParameter(2, 0.03)
  func1.SetParameter(3, 100)
  func1.SetParameter(4, 0)
  #harray[2].Clone().Fit('func1', '', '', 0.04, 0.40)
  harray[2].Fit('func1', '', '', 0.06, 0.42)
  harray[2].GetXaxis().SetRangeUser(0.06, 0.42)
  #harray[2].GetXaxis().SetRangeUser(0.12, 0.36)
  #harray[2].Draw()
  func2 = TF1('func2', 'gaus', 0.06, 0.42, 'VEC')
  func2.SetLineColor(1)
  func2.SetLineWidth(1)
  func2.SetFillColor(kGray)
  func2.SetFillStyle(1001)
  #func2.SetFillStyle(3003)
  for i in range(3):
    func2.SetParameter(i, func1.GetParameter(i))
  func3 = TF1('func3', 'pol1', 0.06, 0.42, 'VEC')
  func3.SetLineColor(1)
  func3.SetLineWidth(1)
  func3.SetFillColor(kGray)
  func3.SetFillStyle(1001)
  #func3.SetFillStyle(3003)
  for i in range(2):
    func3.SetParameter(i, func1.GetParameter(i+3))
  print(func1.Integral(0.14, 0.34),
        func2.Integral(0.14, 0.34),
        func2.Integral(0.14, 0.34)/func1.Integral(0.14, 0.34))
  # func2.Draw('same')
  func3.Draw('same')
  draw_cut_line(harray[2], [0.241-0.038*3, 0.241+0.038*3])
  c1.RedrawAxis()
  c1.Print('fig/dc/xi_m2kp' + ext)
  harray[4].Draw('col')
  c1.Print('fig/dc/xi_m2p' + ext)
  harray[6].Draw()
  c1.Print('fig/dc/xi_chi2' + ext)
  harray_stop[7].GetXaxis().SetRangeUser(0,1.0e5)
  # harray_stop[7].GetXaxis().SetMaxDigits(3);
  # harray_stop[7].GetXaxis().SetNdivisions(505);
  # harray_stop[7].GetXaxis().SetNoExponent()
  harray_stop[7].Draw('col')
  c1.Print('fig/dc/xi_momde' + ext)
  hpy = harray_stop[7].ProjectionY()
  hpy.SetYTitle('Counts [/10 MeV/#font[12]{c}]')
  hpy.Draw()
  tex.DrawLatexNDC(0.23, 0.83, '(b)')
  c1.Print('fig/dc/xi_missmom' + ext)
  print('done')

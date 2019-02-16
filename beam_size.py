#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import ROOT

import fwhm

draw_fwhm = False

#_______________________________________________________________________________
if __name__ == '__main__':
  ROOT.gROOT.SetBatch()
  ROOT.gStyle.SetPadGridX(0)
  ROOT.gStyle.SetPadGridY(0)
  #fig_name = 'tmp.pdf'
  fig_dir = 'fig/dc'
  f1 = ROOT.TFile.Open(sys.argv[1])
  t1 = f1.Get('k18track')
  c1 = ROOT.TCanvas()
  hp = ROOT.TH1F('hp', 'pK18', 400, 1.6, 2.0)
  hx = ROOT.TH1F('hx', 'X@Target', 500, -100., 100.)
  hy = ROOT.TH1F('hy', 'Y@Target', 1000, -100., 100.)
  hu = ROOT.TH1F('hu', 'U@Target', 500, -0.1, 0.1)
  hv = ROOT.TH1F('hv', 'V@Target', 500, -0.02, 0.02)
  cut = 'chisqrK18[0]<10 && trigflag[16]>0'
  '''p'''
  t1.Project('hp', 'p_3rd[0]', cut)
  if draw_fwhm:
    line = fwhm.FWHM(hp, 0.2, 'Momentum [GeV/#font[12]{c}]')
    line.Draw()
  else:
    hp.SetXTitle('Momentum [GeV/#font[12]{c}]')
    hp.SetYTitle('Counts [/0.1 GeV/#font[12]{c}]')
    hp.Draw()
  c1.Print(os.path.join(fig_dir, 'pk18.ps'))
  c1.Clear()
  c1.Divide(2, 2)
  '''X'''
  c1.cd(1)
  t1.Project('hx', 'xtgtK18[0]', cut)
  if draw_fwhm:
    line = fwhm.FWHM(hx, unit='Horizontal position [mm]')
    line.Draw()
  '''Y'''
  c1.cd(2)
  t1.Project('hy', 'ytgtK18[0]', cut)
  if draw_fwhm:
    line = fwhm.FWHM(hy, unit='Vertical position [mm]')
    line.Draw()
  '''U'''
  c1.cd(3)
  t1.Project('hu', 'TMath::ATan( utgtK18[0] )', cut)
  if draw_fwhm:
    line = fwhm.FWHM(hu, unit='Horizontal angle [rad]')
    line.Draw()
  '''V'''
  c1.cd(4)
  t1.Project('hv', 'TMath::ATan( vtgtK18[0] )', cut)
  if draw_fwhm:
    line = fwhm.FWHM(hv, unit='Vertical angle [rad]')
    line.Draw()
  c1.Print(os.path.join(fig_dir, 'xyuvk18.ps'))

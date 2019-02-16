#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os

import EnvManager
import fwhm
import hstyle
import ROOT
from ROOT import (gROOT, gStyle, kRed, kBlue, TArrow,
                  TCanvas, TCut, TEllipse,
                  TF1, TFile, TGraph, TH1F, TH2F,
                  TLatex, TLine,
                  TMath, TPad)

draw_line = True

target_line = [None, None]
cut_line = [None, None]

#_______________________________________________________________________________
def draw_cut_line(h, cut):
  global cut_line
  for i, c in enumerate(cut):
    cut_line[i] = TArrow(c, h.GetMaximum()*0.5,
                         c, h.GetBinContent(h.FindBin(c)), 0.02, '>')
    cut_line[i].SetLineWidth(2)
    cut_line[i].Draw()

#_______________________________________________________________________________
def draw_target_size(h, size):
  global target_line
  target_line[0] = TArrow(size[0], h.GetMaximum(),
                          size[0], 0, 0.02, '')
  target_line[1] = TArrow(size[1], h.GetMaximum(),
                          size[1], 0, 0.02, '')
  target_line[0].SetLineStyle(7)
  target_line[1].SetLineStyle(7)
  target_line[0].Draw()
  target_line[1].Draw()

#_______________________________________________________________________________
if __name__ == '__main__':
  gROOT.Reset()
  gROOT.SetBatch()
  gStyle.SetPalette(52) # grayscale
  root_file = 'uv.root'
  f1 = TFile.Open(root_file)
  tex = TLatex()
  tex.SetTextFont(132)
  tex.SetTextSize(0.08)
  '''resuv'''
  h1 = f1.Get('MissMassCorr')
  c1 = TCanvas()
  hstyle.set_style(h1)
  h1.Draw()
  c1.Print('fig/dc/xi_resuv.ps')
  '''vtx'''
  h1 = f1.Get('h6301')
  hstyle.set_style(h1)
  h1.SetXTitle('x-vertex [mm]')
  h1.SetYTitle('Counts [/mm]')
  h1.Draw()
  cut = [-30, 30]
  line1 = TArrow(cut[0], h1.GetMaximum()*0.5,
                 cut[0], 0, 0.02, '>')
  line2 = TArrow(cut[1], h1.GetMaximum()*0.5,
                 cut[1], 0, 0.02, '>')
  line1.SetLineWidth(2)
  line2.SetLineWidth(2)
  line1.Draw()
  line2.Draw()
  draw_target_size(h1, [-25, 25])
  tex.DrawLatexNDC(0.23, 0.83, '(a)')
  c1.Print('fig/dc/xi_vtx.ps')
  '''vty'''
  h1 = f1.Get('h6202')
  hstyle.set_style(h1)
  h1.SetXTitle('y-vertex [mm]')
  h1.SetYTitle('Counts [/mm]')
  h1.Draw()
  cut = [-20, 20]
  line1 = TArrow(cut[0], h1.GetMaximum()*0.5,
                 cut[0], 0, 0.02, '>')
  line2 = TArrow(cut[1], h1.GetMaximum()*0.5,
                 cut[1], 0, 0.02, '>')
  line1.SetLineWidth(2)
  line2.SetLineWidth(2)
  line1.Draw()
  line2.Draw()
  draw_target_size(h1, [-15, 15])
  tex.DrawLatexNDC(0.23, 0.83, '(b)')
  c1.Print('fig/dc/xi_vty.ps')
  '''vtz'''
  h1 = f1.Get('h6203')
  hstyle.set_style(h1)
  h1.SetXTitle('z-vertex [mm]')
  h1.SetYTitle('Counts [/2 mm]')
  h1.GetXaxis().SetRangeUser(-80, 80)
  h1.Draw()
  draw_cut_line(h1, [-40, 40])
  draw_target_size(h1, [-15, 15])
  tex.DrawLatexNDC(0.23, 0.83, '(c)')
  c1.Print('fig/dc/xi_vtz.ps')
  '''close'''
  h1 = f1.Get('h6204')
  hstyle.set_style(h1)
  h1.SetXTitle('Closest distance [mm]')
  h1.SetYTitle('Counts [/0.1 mm]')
  h1.Draw()
  draw_cut_line(h1, [10])
  tex.DrawLatexNDC(0.23, 0.83, '(d)')
  c1.Print('fig/dc/xi_close.ps')
  '''resvtx'''
  h1 = f1.Get('h6344')
  hstyle.set_style(h1)
  h1.SetXTitle('Residual x-vertex [mm]')
  h1.SetYTitle('Counts [/0.1 mm]')
  h1.Draw()
  cut = [-1.12*5, 1.12*5]
  line1 = TArrow(cut[0], h1.GetMaximum()*0.5,
                 cut[0], 0, 0.02, '>')
  line2 = TArrow(cut[1], h1.GetMaximum()*0.5,
                 cut[1], 0, 0.02, '>')
  line1.SetLineWidth(2)
  line2.SetLineWidth(2)
  line1.Draw()
  line2.Draw()
  tex.DrawLatexNDC(0.23, 0.83, '(a)')
  c1.Print('fig/dc/xi_resvtx.ps')
  '''resvty'''
  h1 = f1.Get('h6345')
  hstyle.set_style(h1)
  h1.SetXTitle('Residual y-vertex [mm]')
  h1.SetYTitle('Counts [/0.1 mm]')
  h1.Draw()
  cut = [-1.50*5, 1.50*5]
  line1 = TArrow(cut[0], h1.GetMaximum()*0.5,
                 cut[0], 0, 0.02, '>')
  line2 = TArrow(cut[1], h1.GetMaximum()*0.5,
                 cut[1], 0, 0.02, '>')
  line1.SetLineWidth(2)
  line2.SetLineWidth(2)
  line1.Draw()
  line2.Draw()
  tex.DrawLatexNDC(0.23, 0.83, '(b)')
  c1.Print('fig/dc/xi_resvty.ps')
  '''resvtz'''
  h1 = f1.Get('h6346')
  hstyle.set_style(h1)
  h1.SetXTitle('Residual z-vertex [mm]')
  h1.SetYTitle('Counts [/0.1 mm]')
  h1.Draw()
  cut = [-7.41*5, 7.41*5]
  line1 = TArrow(cut[0], h1.GetMaximum()*0.5,
                 cut[0], 0, 0.02, '>')
  line2 = TArrow(cut[1], h1.GetMaximum()*0.5,
                 cut[1], 0, 0.02, '>')
  line1.SetLineWidth(2)
  line2.SetLineWidth(2)
  line1.Draw()
  line2.Draw()
  tex.DrawLatexNDC(0.23, 0.83, '(c)')
  c1.Print('fig/dc/xi_resvtz.ps')
  '''ssd2'''
  h1 = f1.Get('h7033')
  hstyle.set_style(h1)
  h1.SetXTitle('Residual SSD2 [mm]')
  h1.SetYTitle('#DeltaE SSD2 [arb. unit]')
  h1.RebinX(2)
  h1.RebinY(2)
  #h1.GetYaxis().SetRangeUser(0, 9e4)
  #h1.GetYaxis().SetNoExponent()
  h1.Draw('col')
  cut = [-0.871319*3, 0.871319*3]
  line1 = TArrow(cut[0], 1e5, cut[0], 0, 0.02, '')
  line2 = TArrow(cut[1], 1e5, cut[1], 0, 0.02, '')
  line3 = TArrow(-20, 2e4, 20, 2e4, 0.02, '')
  line1.SetLineWidth(2)
  line2.SetLineWidth(2)
  line3.SetLineWidth(2)
  line1.Draw()
  line2.Draw()
  line3.Draw()
  #tex.DrawLatexNDC(0.23, 0.83, '(c)')
  c1.Print('fig/dc/xi_ssd2.ps')
  '''ssd2flag'''
  h1 = f1.Get('h7043')
  hstyle.set_style(h1)
  h1.SetXTitle('Number of Hits SSD2')
  h1.SetYTitle('Counts')
  h1.GetXaxis().SetRangeUser(0, 8)
  h1.Draw()
  c1.Print('fig/dc/xi_ssd2flag.ps')
  '''missmass'''
  h1 = f1.Get('h6505')
  hstyle.set_style(h1)
  h1.Rebin(4)
  h1.SetXTitle('Missing mass [GeV/#font[12]{c}^{2}]')
  h1.SetYTitle('Counts [/4 MeV/#font[12]{c}^{2}]')
  h1.Draw()
  c1.Print('fig/dc/xi_missmass.ps')
  '''theta'''
  h1 = f1.Get('h6536')
  hstyle.set_style(h1)
  h1.SetXTitle('Scattering angle [deg]')
  h1.SetYTitle('Counts [/0.5 deg]')
  h1.Draw()
  c1.Print('fig/dc/xi_theta.ps')
  '''de'''
  h1 = f1.Get('h6506')
  hstyle.set_style(h1)
  h1.SetXTitle('Mean #DeltaE SSD1 [arb. unit]')
  h1.SetYTitle('Counts [/750 arb. unit]')
  h1.Draw()
  c1.Print('fig/dc/xi_de.ps')
  '''mom/de'''
  h1 = f1.Get('h6508')
  hstyle.set_style(h1)
  h1.SetXTitle('Mean #DeltaE SSD1 [arb. unit]')
  h1.SetYTitle('Missing momentum [GeV/#font[12]{c}]')
  h1.Draw('col')
  c1.Print('fig/dc/xi_momde.ps')
  '''emxy'''
  h1 = f1.Get('h7207')
  hstyle.set_style(h1)
  h1.SetXTitle('Horizontal position [mm]')
  h1.SetYTitle('Vertical position [mm]')
  h1.Draw('col')
  l = TLine()
  s = [345., 350.]
  l.DrawLine(-s[0]/2, -s[1]/2, s[0]/2, -s[1]/2)
  l.DrawLine(-s[0]/2,  s[1]/2, s[0]/2,  s[1]/2)
  l.DrawLine(-s[0]/2, -s[1]/2, -s[0]/2, s[1]/2)
  l.DrawLine( s[0]/2, -s[1]/2,  s[0]/2, s[1]/2)
  c1.Print('fig/dc/xi_emxy.ps')

  print('done')

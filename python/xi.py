#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os

import EnvManager
import fwhm
import hstyle
import ROOT
from ROOT import (gPad, gROOT, gStyle, kRed, kBlue, TArrow,
                  TCanvas, TCut, TEllipse,
                  TF1, TFile, TGraph, TH1F, TH2F,
                  TLatex, TLine,
                  TMath, TPad)

draw_line = True

target_line = [None, None]

ext = '.ps'
#ext = '.pdf'

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
  target_line[0].SetLineStyle(7)
  target_line[1].SetLineStyle(7)
  target_line[0].Draw()
  target_line[1].Draw()

#_______________________________________________________________________________
if __name__ == '__main__':
  # gROOT.Reset()
  gROOT.SetBatch()
  # gStyle.SetPalette(52) # grayscale
  # ROOT.TColor.InvertPalette()
  #root_file = 'root/v13/DstXiAna_All.root'
  root_file = 'root/dc/DstXiAna_All.root'
  f1 = TFile.Open(root_file)
  tex = TLatex()
  tex.SetTextFont(132)
  tex.SetTextSize(0.08)
  '''resuv'''
  h1 = f1.Get('h6125')
  c1 = TCanvas()
  hstyle.set_style(h1)
  h1.SetXTitle('Residual dx/dz')
  h1.SetYTitle('Residual dy/dz')
  # h1.RebinX(2)
  # h1.RebinY(2)
  h1.Draw('colz')
  gPad.SetRightMargin(0.14)
  # h1.SetZTitle('Counts')
  h1.GetZaxis().SetLabelSize(0.04)
  h1.GetZaxis().SetTitleOffset(0.8)
  h1.GetZaxis().SetTitleSize(0.05)
  ell = TGraph()
  np = 100
  for i in range(np):
    t = i*TMath.Pi()*2/np
    ell.SetPoint(ell.GetN(),
                 0.60*TMath.Cos(t),
                 0.57*TMath.Sin(t))
  ell.SetPoint(ell.GetN(), 0.60, 0)
  ell.SetLineColor(ROOT.kRed)
  ell.SetLineWidth(4)
  ell.Draw('L')
  c1.Print('fig/dc/xi_resuv' + ext)
  '''vtx'''
  h1 = f1.Get('h6301')
  hstyle.set_style(h1)
  h1.SetXTitle('x-vertex [mm]')
  h1.SetYTitle('Counts [/mm]')
  h1.GetXaxis().SetRangeUser(-60, 60)
  h1.Draw()
  draw_cut_line(h1, [-30, 30])
  draw_target_size(h1, [-25, 25])
  tex.DrawLatexNDC(0.23, 0.83, '(a)')
  c1.Print('fig/dc/xi_vtx' + ext)
  '''vty'''
  h1 = f1.Get('h6202')
  hstyle.set_style(h1)
  h1.SetXTitle('y-vertex [mm]')
  h1.SetYTitle('Counts [/mm]')
  h1.GetXaxis().SetRangeUser(-60, 60)
  h1.Draw()
  draw_cut_line(h1, [-20, 20])
  draw_target_size(h1, [-15, 15])
  tex.DrawLatexNDC(0.23, 0.83, '(b)')
  c1.Print('fig/dc/xi_vty' + ext)
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
  c1.Print('fig/dc/xi_vtz' + ext)
  '''close'''
  h1 = f1.Get('h6204')
  hstyle.set_style(h1)
  h1.SetXTitle('Closest distance [mm]')
  h1.SetYTitle('Counts [/0.1 mm]')
  h1.Draw()
  draw_cut_line(h1, [10])
  tex.DrawLatexNDC(0.23, 0.83, '(d)')
  c1.Print('fig/dc/xi_close' + ext)
  '''resvtx'''
  h1 = f1.Get('h6344')
  hstyle.set_style(h1)
  h1.SetXTitle('Residual x-vertex [mm]')
  h1.SetYTitle('Counts [/0.1 mm]')
  h1.Draw()
  draw_cut_line(h1, [-1.12*5, 1.12*5])
  tex.DrawLatexNDC(0.23, 0.83, '(a)')
  c1.Print('fig/dc/xi_resvtx' + ext)
  '''resvty'''
  h1 = f1.Get('h6345')
  hstyle.set_style(h1)
  h1.SetXTitle('Residual y-vertex [mm]')
  h1.SetYTitle('Counts [/0.1 mm]')
  h1.Draw()
  draw_cut_line(h1, [-1.50*5, 1.50*5])
  tex.DrawLatexNDC(0.23, 0.83, '(b)')
  c1.Print('fig/dc/xi_resvty' + ext)
  '''resvtz'''
  h1 = f1.Get('h6346')
  hstyle.set_style(h1)
  h1.SetXTitle('Residual z-vertex [mm]')
  h1.SetYTitle('Counts [/0.1 mm]')
  h1.Draw()
  draw_cut_line(h1, [-7.41*5, 7.41*5])
  tex.DrawLatexNDC(0.23, 0.83, '(c)')
  c1.Print('fig/dc/xi_resvtz' + ext)
  '''ssd2'''
  h1 = f1.Get('h7033')
  hstyle.set_style(h1)
  h1.SetXTitle('Residual SSD2 [mm]')
  h1.SetYTitle('#DeltaE SSD2 [arb. unit]')
  h1.RebinX(2)
  h1.RebinY(2)
  #h1.GetYaxis().SetRangeUser(0, 9e4)
  #h1.GetYaxis().SetNoExponent()
  h1.Draw('colz')
  gPad.SetRightMargin(0.14)
  h1.SetZTitle('Counts')
  h1.GetZaxis().SetLabelSize(0.04)
  h1.GetZaxis().SetTitleOffset(0.8)
  h1.GetZaxis().SetTitleSize(0.05)
  cut = [-0.871319*3, 0.871319*3]
  line1 = TArrow(cut[0], 1e5, cut[0], 0, 0.02, '')
  line2 = TArrow(cut[1], 1e5, cut[1], 0, 0.02, '')
  line3 = TArrow(-20, 2e4, 20, 2e4, 0.02, '')
  # line1.SetLineWidth(2)
  # line2.SetLineWidth(2)
  # line3.SetLineWidth(2)
  line1.Draw()
  line2.Draw()
  line3.Draw()
  #tex.DrawLatexNDC(0.23, 0.83, '(c)')
  c1.Print('fig/dc/xi_ssd2' + ext)
  '''ssd2flag'''
  h1 = f1.Get('h7043')
  hstyle.set_style(h1)
  h1.SetXTitle('Number of Hits SSD2')
  h1.SetYTitle('Counts')
  h1.GetXaxis().SetRangeUser(0, 8)
  h1.Draw()
  c1.Print('fig/dc/xi_ssd2flag' + ext)
  '''missmass'''
  h1 = f1.Get('h6505')
  hstyle.set_style(h1)
  h1.Rebin(4)
  h1.SetXTitle('Missing mass [GeV/#font[12]{c}^{2}]')
  h1.SetYTitle('Counts [/4 MeV/#font[12]{c}^{2}]')
  h1.Draw()
  c1.Print('fig/dc/xi_missmass' + ext)
  '''theta'''
  h1 = f1.Get('h6536')
  hstyle.set_style(h1)
  h1.SetXTitle('Scattering angle [deg]')
  h1.SetYTitle('Counts [/0.5 deg]')
  h1.Draw()
  c1.Print('fig/dc/xi_theta' + ext)
  '''de'''
  h1 = f1.Get('h6506')
  hstyle.set_style(h1)
  h1.SetXTitle('Mean #DeltaE SSD1 [arb. unit]')
  h1.SetYTitle('Counts [/750 arb. unit]')
  h1.GetXaxis().SetRangeUser(0, 100000)
  h1.Draw()
  h2 = f1.Get('h3416')
  hstyle.set_style(h2)
  h2.SetBinContent(1,0)
  h2.Scale(h1.GetMaximum()/h2.GetMaximum())
  h2.Draw('hist same')
  tex.SetTextSize(0.07)
  tex.DrawLatexNDC(0.27, 0.83, '#font[12]{K}^{#plus}')
  tex.DrawLatexNDC(0.47, 0.83, '#Xi^{#minus}')
  c1.Print('fig/dc/xi_de' + ext)
  '''mom/de'''
  h1 = f1.Get('h6508')
  hstyle.set_style(h1)
  h1.SetXTitle('Mean #DeltaE SSD1 [arb. unit]')
  h1.SetYTitle('Missing momentum [GeV/#font[12]{c}]')
  h1.Draw('col')
  c1.Print('fig/dc/xi_momde' + ext)
  '''emxy'''
  h1 = f1.Get('h7207')
  hstyle.set_style(h1)
  h1.SetXTitle('Horizontal position [mm]')
  h1.SetYTitle('Vertical position [mm]')
  h1.Draw('colz')
  gPad.SetRightMargin(0.12)
  # h1.SetZTitle('Counts')
  h1.GetZaxis().SetLabelSize(0.04)
  h1.GetZaxis().SetTitleOffset(0.7)
  h1.GetZaxis().SetTitleSize(0.05)
  l = TLine()
  l.SetLineColor(ROOT.kRed)
  l.SetLineWidth(4)
  s = [345., 350.]
  l.DrawLine(-s[0]/2, -s[1]/2, s[0]/2, -s[1]/2)
  l.DrawLine(-s[0]/2,  s[1]/2, s[0]/2,  s[1]/2)
  l.DrawLine(-s[0]/2, -s[1]/2, -s[0]/2, s[1]/2)
  l.DrawLine( s[0]/2, -s[1]/2,  s[0]/2, s[1]/2)
  c1.Print('fig/dc/xi_emxy' + ext)

  print('done')

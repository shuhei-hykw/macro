#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import math
import os

import EnvManager
import ROOT
from ROOT import (gROOT, gStyle, kRed, kBlue, TArrow,
                  TCanvas, TCut, TFile, TH1F, TLatex, TLine)

#_______________________________________________________________________________
def FWHM(h, factor=1, unit='', verbose=False):
  label = None
  if 'Horizontal position' in unit:
    label = '(a)'
  if 'Vertical position' in unit:
    label = '(b)'
  if 'Horizontal angle' in unit:
    label = '(c)'
  if 'Vertical angle' in unit:
    label = '(d)'
  tex = ROOT.TLatex()
  tex.SetNDC()
  tex.SetTextFont(132)
  tex.SetTextSize(0.05)
  h.GetXaxis().SetTitle(unit)
  h.GetYaxis().SetTitle('Counts')
  h.Draw()
  if label is not None:
    tex.DrawLatex(0.25, 0.75, label)
  line = None
  peak = [h.GetBinCenter(h.GetMaximumBin()),
          h.GetMaximum()]
  initial = [None, None]
  for i in xrange(h.GetNbinsX()+2):
    if (initial[0] is None and h.GetBinContent(i) > peak[1] / 2.):
      initial[0] = h.GetBinCenter(i)
    if (initial[0] is not None and initial[1] is None and
        h.GetBinContent(i) < peak[1] / 2.):
      initial[1] = h.GetBinCenter(i)
  width = abs(peak[0] - initial[0]) * factor
  if verbose:
    print('peak = ', peak)
    print('initial = ', initial)
    print('width = ', width)
  f1 = ROOT.TF1('f1', '[0] + x*[1]',
                initial[0] - width, initial[0] + width)
  f1.SetParameter(0, peak[1])
  f1.SetParameter(1, peak[1] / width)
  width = abs(peak[0] - initial[1]) * factor
  f2 = ROOT.TF1('f2', '[0] + x*[1]',
                initial[1] - width, initial[1] + width)
  f2.SetParameter(0, peak[1])
  f2.SetParameter(1, peak[1] / width)
  h.Fit(f1, 'RQ')
  h.Fit(f2, 'RQ')
  f1.Draw('same')
  f2.Draw('same')
  p1 = f1.GetParameters()
  p2 = f2.GetParameters()
  x1 = (peak[1] / 2. - p1[0]) / p1[1]
  x2 = (peak[1] / 2. - p2[0]) / p2[1]
  # line = ROOT.TArrow(x1, peak[1] / 2., x2, peak[1] / 2., 0.02, '<|>')
  fwhm_str = 'FWHM={:6.3e} {} '.format(abs(x1 - x2), unit)
  peak_str = 'peak={:6.3e} {}'.format((x1 + x2)/2., unit)
  tex.DrawLatex(0.23, 0.80, fwhm_str)
  tex.DrawLatex(0.23, 0.70, peak_str)
  print(fwhm_str + ' (sigma={})'.format(math.sqrt(2)*abs(x1 - x2)/2.35482))
  if verbose:
    print(peak_str)
  #return line

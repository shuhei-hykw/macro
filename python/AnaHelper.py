#!/usr/bin/env python
# -*- coding: utf-8 -*-

from array import array
from ROOT import (gROOT, gStyle, gPad,
                  TCanvas, TF1, TFile,
                  TGraph, TGraphErrors, TH1, TMath,
                  kMagenta)

#_______________________________________________________________________________
def FitGaus(h, width=None, xmin=None, xmax=None, niter=3):
  if h is None or h.GetEntries() == 0:
    return None
  f = TF1('f', 'gaus')
  center = h.GetBinCenter(h.GetMaximumBin())
  width = h.GetStdDev() if width is None else width
  bmin = h.GetXaxis().GetXmin()
  bmax = h.GetXaxis().GetXmax()
  xmin = center - width if xmin is None else xmin
  xmax = center + width if xmax is None else xmax
  xmin = TMath.Max(xmin, bmin)
  xmax = TMath.Min(xmax, bmax)
  imin = h.GetXaxis().FindBin(xmin)
  imax = h.GetXaxis().FindBin(xmax)
  if h.Integral(imin, imax) == 0:
    return None
  h.Fit('f', 'Q', '', xmin, xmax)
  for i in range(niter):
    center = f.GetParameter(1)
    width = f.GetParameter(2)
    xmin = center - 3 * width
    xmax = center + 3 * width
    imin = h.GetXaxis().FindBin(xmin)
    imax = h.GetXaxis().FindBin(xmax)
    xmin = TMath.Max(xmin, bmin)
    xmax = TMath.Min(xmax, bmax)
    if h.Integral(imin, imax) == 0:
      break
    h.Fit('f', 'Q', '', xmin, xmax)
  return f

#_______________________________________________________________________________
def FitPHC(h, width=None, f=TF1('f', '[0]*x*x + [1]*x + [2]')):
  if h is None or h.GetEntries() < 10:
    return None
  de = array('f')
  time = array('f')
  de_error = array('f')
  time_error = array('f')
  amin = h.GetXaxis().GetXmin()
  amax = h.GetXaxis().GetXmax()
  nbin = h.GetXaxis().GetNbins()
  width = (amax - amin) / nbin if width is None else width
  nslice = int((amax - amin) / width)
  ctmp = TCanvas('ctmp', 'ctmp', 800, 800)
  for s in xrange(nslice):
    xmin = amin + s * width
    xmax = amin + s * width + width
    min_bin = h.GetXaxis().FindBin(xmin)
    max_bin = h.GetXaxis().FindBin(xmax)
    # print('{} {}'.format(min_bin, max_bin))
    h_slice = h.ProjectionY('', min_bin, max_bin)
    if h_slice is None or h_slice.GetEntries() < 10:
      continue
    ftmp = FitGaus(h_slice, 10)
    if ftmp is None:
      continue
    mean = ftmp.GetParameter(1)
    mean_error = ftmp.GetParError(1)
    if abs(mean) > 10:
      continue
    de.append(amin + (s + 0.5)*width)
    de_error.append(width/2.)
    time.append(mean)
    time_error.append(mean_error)
  if len(de) < 10:
    return None
  #print('{} {}'.format(de, time))
  #g = TGraph(len(de), de, time)
  g = TGraphErrors(len(de), de, time, de_error, time_error)
  g.SetMarkerStyle(4)
  g.SetMarkerSize(1.2)
  g.SetMarkerColor(kMagenta)
  g.Fit(f, 'Q')
  return g

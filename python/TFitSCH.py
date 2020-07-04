#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os

from ROOT import (gROOT, gStyle,
                  TCanvas, TF1, TFile, TLatex,
                  kBlue, kRed)

import AnaHelper as ana
import EnvManager as env
import HodoParamMaker as hpm
from utility import pycolor as pc

myname = os.path.basename(__file__).replace('.py', '')
DetIdSCH = 7
NumOfSegSCH = 64

#_______________________________________________________________________________
if __name__ == '__main__':
  gROOT.Reset()
  env.Load()
  gStyle.SetStatW(0.2)
  parser = argparse.ArgumentParser()
  parser.add_argument('run_number', type=int, help='run number')
  parser.add_argument('overwrite', type=int, nargs='?',
                      default=0,
                      help='run number')
  parser.add_argument('verbose', type=int, nargs='?',
                      default=0,
                      help='verbose')
  parsed, unparsed = parser.parse_known_args()
  env.ana_type = 'Easiroc'
  env.param_file = ('{0}/HDPRM/HodoParam_{1:05d}'
                    .format(env.param_dir, parsed.run_number))
  env.root_file = ('{0}/run{1:05d}_{2}.root'
                   .format(env.root_dir, parsed.run_number, env.ana_type))
  env.fig_file = ('{0}/{1}_{2:05d}.pdf'
                  .format(env.fig_dir, myname, parsed.run_number))
  env.output_file = ('{0}/{1}_{2:05d}'
                     .format(env.output_dir, myname, parsed.run_number))
  if parsed.verbose:
    env.Print()

  f1 = TFile.Open(env.root_file)
  if f1 is None:
    quit()
  c1 = TCanvas('c1', 'c1', 1000, 800)
  c1.Print(env.fig_file + '[');
  h = gROOT.FindObject('h{}'.format(20003))
  f = ana.FitGaus(h, 10)
  c = f.GetParameter(1)
  w = f.GetParameter(2)
  ref_mean = c
  h.GetXaxis().SetRangeUser(c - 10. * w, c + 20. * w)
  c1.Print(env.fig_file)
  c1.Clear()
  parray = [] # did plane seg at ud p0 p1
  if parsed.verbose:
    print('\nSeg    mean         sigma')
  for i in range(NumOfSegSCH):
    good_fit = False
    cparam = ref_mean
    mean = -99999
    sigma = 99999
    h = gROOT.FindObject('h{}'.format(21001 + i))
    if h is not None:
      h.Draw()
      if h.GetEntries() > 10:
        f = ana.FitGaus(h, 10)
        mean  = f.GetParameter(1)
        sigma = f.GetParameter(2)
      if abs(mean - ref_mean) < 10 and sigma < 10:
        good_fit = True
        cparam = mean
      h.GetXaxis().SetRangeUser(600, 750)
    parray.append([DetIdSCH, 0, i, 1, 0, cparam, 1])
    sig = (('OK' if good_fit else 'NG')
           + ' -> {:10.3f}'.format(cparam))
    col = pc.blue if good_fit else pc.red
    if parsed.verbose:
      print('{0:3d} {1} {2:>10.3f} {3:>10.3f}  {4}'
            .format(i, 0, mean, sigma,
                    pc.Form(sig[:2], col + pc.bold) + sig[2:]))
    tex = TLatex()
    tex.SetNDC()
    tex.SetTextSize(0.07)
    sig = ('#color[{0}]{1}{2}'.format(kBlue if good_fit else kRed,
                                      '{' + sig[:2] + '}',
                                      sig[2:]))
    tex.DrawLatex(0.140, 0.800, sig)
    c1.Print(env.fig_file)
  hpm.MakeParameter(parray, parsed.overwrite, parsed.verbose)
  c1.Print(env.fig_file + ']')

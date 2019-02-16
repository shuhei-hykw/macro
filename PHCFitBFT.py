#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os

from ROOT import (gROOT, gStyle,
                  TCanvas, TF1, TFile, TLatex,
                  kBlue, kRed)

import AnaHelper as ana
import EnvManager as env
import HodoPHCParamMaker as hpm
from utility import pycolor as pc

myname = os.path.basename(__file__).replace('.py', '')
DetIdBFT = 110
NumOfSegBFT = 160

#_______________________________________________________________________________
if __name__ == '__main__':
  env.Load()
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
  env.param_file = ('{0}/HDPHC/HodoPHCParam_{1:05d}'
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
  c1.Divide(1, 2)
  ref_param = []
  g = []
  for i in range(2):
    h = gROOT.FindObject('h{}'.format(10023 + i))
    f = TF1('f', '[0]*x*x + [1]*x + [2]')
    f.SetParameter( 0,  -0.01 )
    f.SetParameter( 1,   0.6  )
    f.SetParameter( 2, -19.0  )
    f.SetParLimits( 0,  -0.1,  -0.0 )
    f.SetParLimits( 1,   0.4,   0.8 )
    f.SetParLimits( 2, -22.0, -16.0 )
    g.append(ana.FitPHC(h, 1, f))
    c1.cd(i + 1)
    if g[i] is None:
      h.Draw('colz')
      continue
    h.SetStats(False)
    h.GetXaxis().SetRangeUser(-10, 100)
    h.GetYaxis().SetRangeUser(-30,  40)
    h.Draw('colz')
    g[i].Draw('P')
    ref_param.append(f.GetParameters())
  c1.Print(env.fig_file)
  c1.Clear()
  parray = [] # did plane seg at ud p0 p1
  if parsed.verbose:
    print('\nSeg UD   mean         sigma')
  for ud in range(2):
    for i in range(NumOfSegBFT):
      good_fit = False
      cparam = ref_param[ud]
      p = [-999, -999, -999]
      h = gROOT.FindObject('h{}'.format(15001 + i + ud * 1000))
      if h is not None:
        h.RebinY(4)
        f = TF1('f', '[0]*x*x + [1]*x + [2]')
        f.SetParameter( 0,  -0.01 )
        f.SetParameter( 1,   0.6  )
        f.SetParameter( 2, -19.0  )
        f.SetParLimits( 0,  -0.1,  -0.0 )
        f.SetParLimits( 1,   0.4,   0.8 )
        f.SetParLimits( 2, -20.0, -14.0 )
        g = ana.FitPHC(h, 2, f)
        h.Draw('colz')
        if g is not None:
          p = f.GetParameters()
          h.SetStats(False)
          h.Draw('colz')
          g.Draw('P')
          if (g.GetN() > 5 and
              f.GetChisquare()/f.GetNDF() < 20):
            good_fit = True
            cparam = f.GetParameters()
      parray.append([DetIdBFT, ud, i, 1, 2, 3,
                     cparam[0], cparam[1], cparam[2]])
      sig = (('OK' if good_fit else 'NG')
             + ' -> {0:8.3f} {1:8.3f} {2:8.3f}'.format(
               cparam[0], cparam[1], cparam[2]))
      col = pc.blue if good_fit else pc.red
      if parsed.verbose:
        print('{0:3d} {1} {2:8.3f} {3:8.3f} {4:8.3f}  {5}'
              .format(i, ud, p[0], p[1], p[2],
                      pc.Form(sig[:2], col + pc.bold) + sig[2:]))
      tex = TLatex()
      tex.SetNDC()
      tex.SetTextSize(0.07)
      sig = ('#color[{0}]{1}{2}'.format(kBlue if good_fit else kRed,
                                        '{' + sig[:2] + '}',
                                        sig[2:]))
      tex.DrawLatex(0.140, 0.150, sig)
      c1.Print(env.fig_file)
  hpm.MakeParameter(parray, parsed.overwrite, parsed.verbose)
  c1.Print(env.fig_file + ']')

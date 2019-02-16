#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import array
import numpy
import os
import ROOT

import fwhm

tex = ROOT.TLatex()
tex.SetTextFont(132)
tex.SetTextSize(0.08)

#_______________________________________________________________________________
def process(track_file):
  track_list = []
  for file_name in track_file:
    tracks = []
    with open(file_name, 'r') as f:
      print('Open file : {}'.format(file_name))
      for line in f:
        ''' columns : ph phv u v x y z0 z1 '''
        columns = line.split()
        for i, e in enumerate(columns):
          columns[i] = float(e)
        tracks.append(columns)
    track_list.append(tracks)

  c1 = ROOT.TCanvas('c1', 'c1', 1100, 1000)
  nbin = 200
  xmin = -50
  xmax =  50
  ymin = -50
  ymax =  50
  xcut = [-1, 2]
  ycut = [24, 26]
  # xcut = [15, 20]
  # ycut = [33, 38]
  title = 'residual'
  h1 = ROOT.TH2F('h1', 'h1;x-{} [#mum];y-{} [#mum]'.format(title, title),
                 nbin, xmin, xmax, nbin, ymin, ymax)
  hx = ROOT.TH1F('hx', 'hx', nbin, xmin, xmax)
  hy = ROOT.TH1F('hy', 'hy', nbin, ymin, ymax)
  ht = ROOT.TH1F('ht', 'ht', 100, 0, 0.2)
  hx.GetYaxis().SetNdivisions(100, 0)
  hy.GetYaxis().SetNdivisions(100, 0)
  for l1 in track_list[0]:
    for l2 in track_list[1]:
      du = l2[2] - l1[2]
      dv = l2[3] - l1[3]
      dx = (l2[4] - l1[4])*1e3
      dy = (l2[5] - l1[5])*1e3
      theta = ROOT.TMath.Sqrt( du*du + dv*dv )
      if (xmin < dx and dx < xmax and
          ymin < dy and dy < ymax):
        h1.Fill(dx, dy)
        if ycut[0] < dy and dy < ycut[1]:
          hx.Fill(dx)
        if xcut[0] < dx and dx < xcut[1]:
          hy.Fill(dy)
      ht.Fill(theta)
  psize = 1
  if psize < 1.0:
    c1 = ROOT.TCanvas('c1', 'c1', 1100, 1000)
    p1 = ROOT.TPad('p1', 'p1', 0, 0, psize, psize)
    p1.Draw()
    pt = ROOT.TPad('pt', 'pt', 0, psize, psize, 1.0)
    pr = ROOT.TPad('pr', 'pr', psize, 0, 1.0, psize)
    margin = 0
    p1.SetTopMargin(margin)
    p1.SetRightMargin(margin)
    pt.SetBottomMargin(margin)
    pt.SetRightMargin(margin)
    pr.SetLeftMargin(margin)
    pr.SetTopMargin(margin)
    pt.Draw()
    pr.Draw()
    p1.cd()
  else:
    c1 = ROOT.TCanvas()
  h1.Draw('col')
  bx = array.array('i', [0])
  by = array.array('i', [0])
  bz = array.array('i', [0])
  h1.GetMaximumBin(bx, by, bz)
  mx = h1.GetXaxis().GetBinCenter(bx[0])
  my = h1.GetYaxis().GetBinCenter(by[0])
  mw = 21
  h1.GetXaxis().SetRangeUser(mx-mw, mx+mw)
  h1.GetYaxis().SetRangeUser(my-mw, my+mw)
  hx.GetXaxis().SetRangeUser(mx-mw, mx+mw)
  hy.GetXaxis().SetRangeUser(my-mw, my+mw)
  hpx = h1.ProjectionX('hpx', by[0]-1, by[0]+1)
  hpy = h1.ProjectionY('hpy', bx[0]-1, bx[0]+1)
  # hpx.GetYaxis().SetNdivisions(500)
  # hpy.GetYaxis().SetNdivisions(500)
  if psize < 1.0:
    pt.cd()
    hpx.Draw('bar')
    pr.cd()
    hpy.Draw('hbar')
  c1.Print('fig/dc/empattern.ps')
  c1 = ROOT.TCanvas()
  hpx.GetYaxis().SetNdivisions(510, 1)
  f1 = ROOT.TF1('f1', 'gaus+pol0(3)')
  f1.SetParameter(0, 1000)
  f1.SetParameter(1, mx)
  f1.SetParameter(2, 0.7)
  f1.SetParameter(3, 0)
  f1.SetParLimits(1, mx-2, mx+2)
  f1.SetParLimits(0, 0, 1000)
  f1.SetParLimits(2, 0, 1)
  hpx.SetYTitle('Counts [/0.5 #mum]')
  hpx.Clone().Fit('f1', '', '', mx-15, mx+15)
  hpx.Draw()
  tex.DrawLatexNDC(0.23, 0.83, '(a)')
  c1.Print('fig/dc/empatternx.ps')
  hpy.GetYaxis().SetNdivisions(510, 1)
  f1.SetParLimits(1, my-2, my+2)
  f1.SetParameter(1, my)
  hpy.SetYTitle('Counts [/0.5 #mum]')
  hpy.Clone().Fit('f1', '', '', my-15, my+15)
  hpy.Draw()
  tex.DrawLatexNDC(0.23, 0.83, '(b)')
  c1.Print('fig/dc/empatterny.ps')

#_______________________________________________________________________________
if __name__ == '__main__':
  ROOT.gROOT.SetBatch()
  parser = argparse.ArgumentParser()
  first = '0020864935457184'
  best = '0020864888768760'
  parser.add_argument('track_id', nargs='?',
                      default=best,
                      help='track_id')
  parsed, unpased = parser.parse_known_args()
  module_dir = '/hsm/had/sks/E07/Microscope/trackfollow/mod047'
  track_file = [os.path.join(module_dir,
                             'pl09/v11.manual/ID{}_vmt1_detector-0.txt'
                             .format(parsed.track_id)),
                os.path.join(module_dir,
                             'pl10/v11.manual/ID{}_vmt0_detector-0.txt'
                             .format(parsed.track_id))]
  process(track_file)

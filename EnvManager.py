#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import ROOT

#_______________________________________________________________________________
myname = os.path.basename(__file__).replace('.py', '')
macro_dir = os.path.dirname(os.path.realpath(__file__))
ana_type = None
ana_dir = os.path.dirname(macro_dir)
param_dir = os.path.join(ana_dir, 'param')
conf_dir = os.path.join(param_dir, 'conf')
root_dir = os.path.join(ana_dir, 'root/all')
fig_dir = os.path.join(ana_dir, 'fig')
output_dir = os.path.join(macro_dir, 'output')
param_file = None
root_file = None
fig_file = None
output_file = None

#_______________________________________________________________________________
def Print():
  print(myname + '.Print()' + '_'*68)
  print(' ana_type    : {}'.format(ana_type))
  print(' ana_dir     : {}'.format(ana_dir))
  print(' param_dir   : {}'.format(param_dir))
  print(' macro_dir   : {}'.format(macro_dir))
  print(' root_dir    : {}'.format(root_dir))
  print(' fig_dir     : {}'.format(fig_dir))
  print(' output_dir  : {}'.format(output_dir))
  print(' param_file  : {}'.format(os.path.basename(param_file)))
  print(' root_file   : {}'.format(os.path.basename(root_file)))
  print(' fig_file    : {}'.format(os.path.basename(fig_file)))
  print(' output_file : {}'.format(os.path.basename(output_file)))

#_______________________________________________________________________________
def Load():
  # ROOT.gROOT.Reset()
  ROOT.gROOT.SetBatch()
  ROOT.gStyle.SetOptStat(1111110)
  ROOT.gStyle.SetOptFit(1)
  # ROOT.gStyle.SetStatX(.90);
  # ROOT.gStyle.SetStatY(.90);
  # ROOT.gStyle.SetStatW(.30);
  # ROOT.gStyle.SetStatH(.20);

#_______________________________________________________________________________
if __name__ == '__main__':
  Print()

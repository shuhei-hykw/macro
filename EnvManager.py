#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import ROOT

#_______________________________________________________________________________
macro_dir = os.path.dirname(os.path.realpath(__file__))
ana_dir = os.path.dirname(macro_dir)
param_dir = ana_dir + '/param'
conf_dir = param_dir + '/conf'
root_dir = ana_dir + '/root/all'
fig_dir = ana_dir + '/fig'

#_______________________________________________________________________________
def PrintEnv():
  print('print_env() ' + '_'*68)
  print(' ana_dir   : {}'.format(ana_dir))
  print(' macro_dir : {}'.format(macro_dir))
  print(' root_dir  : {}'.format(root_dir))
  print(' fig_dir   : {}'.format(fig_dir))

#_______________________________________________________________________________
def Load():
  ROOT.gROOT.SetBatch()
  ROOT.gStyle.SetOptStat(1111110)
  ROOT.gStyle.SetStatX(.90);
  ROOT.gStyle.SetStatY(.90);
  ROOT.gStyle.SetStatW(.30);
  ROOT.gStyle.SetStatH(.20);

#_______________________________________________________________________________
if __name__ == '__main__':
  print_env()

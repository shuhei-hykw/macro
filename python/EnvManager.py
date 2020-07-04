#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import ROOT

#_______________________________________________________________________________
myname = os.path.basename(__file__).replace('.pyc', '').replace('.py', '')
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
  print((myname + '.Print() ' + '_'*80)[:80])
  print(' ana_type    : {}'.format(ana_type))
  print(' ana_dir     : {}'.format(ana_dir))
  print(' param_dir   : {}'.format(param_dir))
  print(' macro_dir   : {}'.format(macro_dir))
  print(' root_dir    : {}'.format(root_dir))
  print(' fig_dir     : {}'.format(fig_dir))
  print(' output_dir  : {}'.format(output_dir))
  if param_file is not None:
    print(' param_file  : {}'.format(os.path.basename(param_file)))
  if root_file is not None:
    print(' root_file   : {}'.format(os.path.basename(root_file)))
  if fig_file is not None:
    print(' fig_file    : {}'.format(os.path.basename(fig_file)))
  if output_file is not None:
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
def SetFigDir(dir_name):
  global fig_dir
  fig_dir = os.path.join(fig_dir, dir_name)

#_______________________________________________________________________________
def SetFigFile(key, fig_name):
  global fig_dir
  global fig_file
  fig_dir = os.path.join(fig_dir, key)
  fig_file = os.path.join(fig_dir, fig_name)

#_______________________________________________________________________________
def SetParamFile(key, param_name):
  global param_dir
  global param_file
  param_dir = os.path.join(param_dir, key)
  param_file = os.path.join(param_dir, param_name)

#_______________________________________________________________________________
def SetRootFile(bin_name, run_number):
  global ana_type
  global root_file
  ana_type = bin_name
  root_file = os.path.join(root_dir,
                           'run{:05d}_{}.root'.format(run_number, bin_name))

#_______________________________________________________________________________
if __name__ == '__main__':
  Print()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys

import EnvManager
import run_number

#_______________________________________________________________________________
def read(scaler_txt, run_number):
  with open(scaler_txt, 'r') as f:
    scaler = {}
    for line in f:
      columns = line.split()
      if len(columns) < 2:
        continue
      scaler[columns[0]] = columns[1]
  return scaler

#_______________________________________________________________________________
def show(array):
  data_top_dir = '/group/had/sks/E07/'
  total_k_beam = 0
  total_pi_beam = 0
  total_p_beam = 0
  total_beam = 0
  total_l1_req = 0
  total_l1_acc = 0
  for i, m in enumerate(array):
    k_beam = 0
    pi_beam = 0
    p_beam = 0
    beam = 0
    l1_req = 0
    l1_acc = 0
    for j, r in enumerate(m):
      data_dir = (os.path.join(data_top_dir, 'KURAMA2016Jun') if r < 2000 else
                  os.path.join(data_top_dir, 'KURAMA2017Apr'))
      scaler_txt = os.path.join(data_dir, 'scaler/scaler_{:05d}.txt'.format(r))
      if not os.path.isfile(scaler_txt):
        raise Exception
      scaler = read(scaler_txt, r)
      k_beam += int(scaler['K_beam'])
      pi_beam += int(scaler['Pi_beam'])
      p_beam += int(scaler['/p_beam'])
      beam += int(scaler['BH1xBH2'])
      l1_req += int(scaler['L1_Req'])
      l1_acc += int(scaler['L1_Acc'])
    total_k_beam += k_beam
    total_pi_beam += pi_beam
    total_p_beam += p_beam
    total_beam += beam
    total_l1_req += l1_req
    total_l1_acc += l1_acc
    # print(k_beam, pi_beam, beam)
  print('K={}, Pi={}, P={}, All={}, L1Req={}, L1Acc={}, DAQEff={}'
        .format(total_k_beam, total_pi_beam, total_p_beam, total_beam,
                total_l1_req, total_l1_acc, float(total_l1_acc)/total_l1_req))

#_______________________________________________________________________________
if __name__ == '__main__':
  EnvManager.Load()
  parser = argparse.ArgumentParser()
  try:
    show(run_number.emulsion_2016)
    show(run_number.emulsion_2017)
    show(run_number.emulsion_2016 + run_number.emulsion_2017)
    # show(run_number.ch2_2016)
    # show(run_number.ch2_2017)
    # show(run_number.beam_2017)
    show(run_number.pbar_2016)
    show(run_number.pbar_2017)
    show(run_number.pbar_2016 + run_number.pbar_2017)
  except:
    print(sys.exc_info())
  # parser.add_argument('scaler_path', help='data path of scaler text')
  # parsed, unpased = parser.parse_known_args()
  # for s in sorted(os.listdir(parsed.scaler_path)):
  #   s = parsed.scaler_path + '/' + s
  #   print(s)
  #   with open(s, 'r') as f:
  #     f.read()

#!/usr/bin/env python2

import enum

MaxDepth = 16

DetIdBH1 = 1
NumOfSegBH1 = 11

class AorT(enum.Enum):
  ADC = 0
  TDC = 1

class UorD(enum.Enum):
  UP = 0
  DOWN = 1

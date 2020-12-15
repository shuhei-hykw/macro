#!/usr/bin/env python3

import logging
import os

script_dir = os.path.dirname(__file__)
ana_dir = os.path.dirname(os.path.dirname(script_dir))
macro_dir = os.path.join(os.path.dirname(script_dir), 'cpp')
tune_dir = os.path.join(os.path.dirname(script_dir), 'output', 'tune')
param_dir = os.path.join(ana_dir, 'param')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(module)s.%(funcName)s() %(message)s')

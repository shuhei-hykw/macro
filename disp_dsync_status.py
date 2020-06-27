#!/usr/bin/env python

import cv2

image_path = '/group/had/sks/E40/JPARC2019Feb/E40SubData2019Feb/data_sync/dsync_status.png'

while True:
  try:
    img = cv2.imread(image_path)
    cv2.imshow('image', img)
    cv2.waitKey(2000)
  except KeyboardInterrupt:
    break
  except:
    pass

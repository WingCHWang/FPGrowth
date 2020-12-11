#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import time

from fpgrowth import mine_fp

if __name__ == "__main__":
   db = [
      ['I1','I2','I5'],
      ['I2','I4'],
      ['I2','I3'],
      ['I1','I2','I4'],
      ['I1','I3'],
      ['I2','I3'],
      ['I1','I3'],
      ['I1','I2','I3','I5'],
      ['I1','I2','I3']
   ]
   start = time.time()
   
   for itemset, support in mine_fp(db, 2):
      print(itemset, support)
   print(time.time() - start, 'sec')
#!/usr/bin/env python

'''
Script for a rough estimate of quantity of the translated text.
An error of measurement - about 10%

Usage:
    statusof.py book/ch01.xml
'''

import sys, re

f = file(sys.argv[1])
ru = en = 0.0
in_tr = in_para = False

for line in f:
  if re.search('^( *|\t*)\<\!-- @ENGLISH \{\{\{', line):
    in_tr = True

  if re.search('^ *\<para>', line):
    in_para = True

  if in_para or re.search('^ *\<para>.*\</para>$', line):
    if in_tr:
      ru += 1
    else:
      en += 1

  if re.search('\</para>$', line):
    in_para = False

  if re.search('@ *ENGLISH \}\}\} -->$', line):
    in_tr = False

print "Translated %3.2f%%" % ((ru / en) * 100)

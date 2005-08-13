#!/usr/bin/env python

import sys, os, string, getopt, re

bfiles = ['appa.xml', 'appb.xml', 'appc.xml', 'book.xml', 'ch00.xml', \
          'ch01.xml', 'ch02.xml', 'ch03.xml', 'ch04.xml', 'ch05.xml', \
          'ch06.xml', 'ch07.xml', 'ch08.xml', 'ch09.xml', 'copyright.xml', \
          'foreword.xml', 'styles.css']

def usage(err_msg):
  stream = err_msg and sys.stderr or sys.stdout
  if err_msg:
    stream.write("ERROR: %s\n\n" % (err_msg))
  stream.write("""Usage: %s [-f <filename>] [-l]

Options:
    -f:    File which needs to be synchronized
    -l:    List all files and revisions with which they are sinchronized
""" % (os.path.basename(sys.argv[0])))
  sys.exit(err_msg and 1 or 0)

def get_last(fname):
  return int(os.popen('svn propget last-sync '+fname).readline())

def set_last(fname, last):
  os.system('svn propset last-sync '+last+' '+fname)

def get_base(fname = ''):
  global bfiles
  if fname != '':
    for line in os.popen('svn info '+fname):
      if re.match('Revision: ', line):
        return int(re.sub('Revision: ', '', line))
  else:
    rmin = 0xffffffff
    rlist = []
    for file in bfiles:
      for line in os.popen('svn info '+file):
        if re.match('Revision: ', line):
          rev = int(re.sub('Revision: ', '', line))
      if rev < rmin:
        rmin = rev
      rlist.append(rev)
    return max(rlist)

def get_status(fname):
  f = file(fname)
  ru = 0.0
  en = 0.001
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
  return "(%3.2f%%)" % ((ru / en) * 100)

def get_list():
  import platform
  global bfiles
  frlist = ()
  rmin = 0xffffffff
  rbase = get_base() + 1
  for file in bfiles:
    rev = get_last(file)
    if rev < rmin:
      rmin = rev
    frlist += (file, rev),
  rdelta1 = rmin + ((rbase - rmin) / 3)
  rdelta2 = rbase - ((rbase - rmin) / 3)
  for f, r in frlist:
    if platform.system() == 'Windows':
      print f, '\t', r, '\t', get_status(f)
    else:
      if r in range(rdelta2, rbase):
        print '\x1b[32m', f, '\t', r, '\t', get_status(f), '\x1b[0m'
      elif r in range(rdelta1, rdelta2):
        print '\x1b[33m', f, '\t', r, '\t', get_status(f), '\x1b[0m'
      elif r in range(rmin, rdelta1):
        print '\x1b[31m', f, '\t', r, '\t', get_status(f), '\x1b[0m'

def main():
  global bfiles
  if len(sys.argv) < 2:
    usage(None)
  os.chdir('book')
  try:
    opts, args = getopt.getopt(sys.argv[1:], "f:l")
  except:
    usage('Invalid syntax')
  fname = ''
  for o, a in opts:
    if o == '-f':
      a = os.path.basename(a)
      if a in bfiles:
        fname = a
      else:
        usage('Invalid syntax')
    elif o == '-l':
      return get_list()
  cmd = string.Template('svn $a -r $r1:$r2 https://svn.red-bean.com/svnbook/trunk/src/en/book/$t')
  last = get_last(fname)
  base = get_base(fname)
  print ('########################################################################')
  print 'Sync r%(r1)s:r%(r2)s' % { 'r1' :  last, 'r2' : base }
  diff = os.popen(cmd.substitute(a='diff', r1=last, r2=base, t=fname)).read()
  if len(diff) != 0:
    os.system(cmd.substitute(a='log', r1=last, r2=base, t=fname))
    raw_input('Above is log message, to see diff press ENTER')
    print diff
    os.system(cmd.substitute(a='merge', r1=last, r2=base, t=fname))
  set_last(fname, str(base))

if __name__ == "__main__":
  main()

#!/usr/bin/env python

import sys, os, string, getopt, re, glob

def usage(err_msg):
  stream = err_msg and sys.stderr or sys.stdout
  if err_msg:
    stream.write("ERROR: %s\n\n" % (err_msg))
  stream.write("""Usage: %s [-r <revision>] [-u] [--dry-run]

Options:
    -r: Revision to sync
    -u: Update TRANSLATION-STATUS file

    --dry-run:  Execute a command, but don't make actual changes
""" % (os.path.basename(sys.argv[0])))
  sys.exit(err_msg and 1 or 0)

def get_last():
  return int(os.popen('svn propget last-sync book').readline())

def set_last(last):
  c = 'svn propset last-sync '+last+' book'
  print c
  os.system(c)

def get_percent(fname):
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
  return '%i%%' % ((ru / en) * 100)

def get_status(fname):
  return os.popen('svn propget status '+fname).readline()

def update_status_file():
  bfiles = glob.glob('book/*.xml')
  st_f = file('TRANSLATION-STATUS')
  tmp_st_f = file('TRANSLATION-STATUS.tmp', 'w')
  curr_sta = ''
  in_sta = False
  indention = '        '
  for line in st_f:
    if in_sta:
      if re.match(' {8}\*', line):
        fcount = 0
        for f in bfiles:
          if re.match(curr_sta, get_status(f)):
            if curr_sta == 'Transl':
              tmp_st_f.write(indention+'* '+os.path.basename(f)+', '+get_percent(f)+'\n')
            else:
              tmp_st_f.write(indention+'* '+os.path.basename(f)+'\n')
            fcount += 1
        if fcount == 0:
          tmp_st_f.write(indention+'* [none]\n')
        in_sta = False
      else:
        tmp_st_f.write(line)
    else:
      if re.match(' {2}\w', line):
        in_sta = True
        curr_sta = line[2:8]
      if not re.match(' {8}\*', line):
        tmp_st_f.write(line)
  tmp_st_f.close()
  st_f.close()
  os.remove('TRANSLATION-STATUS')
  os.rename('TRANSLATION-STATUS.tmp', 'TRANSLATION-STATUS')

def main():
  if len(sys.argv) < 2:
    usage(None)
  try:
    opts, args = getopt.getopt(sys.argv[1:], 'r:u', ['dry-run'])
  except:
    usage('Invalid syntax')
  dry_run = False
  last = base = get_last()
  for o, a in opts:
    if o == '-r':
      base = int(a)
    elif o == '--dry-run':
      dry_run = True
    elif o == '-u':
      return update_status_file()
  cmd = string.Template(
      'svn $a -r $r1:$r2 http://svn.red-bean.com/svnbook/trunk/src/en/book/$t')
  print ('########################################################################')
  print 'Sync r%s:r%s' % (last, base)
  diff = os.popen(cmd.substitute(a='diff', r1=last, r2=base, t='')).read()
  if len(diff) != 0:
    os.system(cmd.substitute(a='log', r1=last+1, r2=base, t=''))
    c = cmd.substitute(a='merge', r1=last, r2=base, t=' book/')
    if dry_run:
      c += ' --dry-run'
    print c
    os.system(c)
  if not dry_run:
    set_last(str(base))

if __name__ == "__main__":
  main()

# vim: tabstop=2 shiftwidth=2 expandtab smarttab


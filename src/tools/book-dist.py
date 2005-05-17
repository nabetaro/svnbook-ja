#!/usr/bin/env python2

import sys
import os
import shutil

def die(msg):
  sys.stderr.write('ERROR: ' + msg)
  sys.exit(1)

if len(sys.argv) < 2:
  die("Usage: %s LOCALE [TARGET...]\n" % (os.path.basename(sys.argv[0])))
  
elif len(sys.argv) == 2:
  locale = sys.argv[1]
  targets = ['install-book-html',
             'install-book-html-chunk',
             'install-book-pdf']
else:
  locale = sys.argv[1]
  targets = sys.argv[2:]

cwd = os.getcwd()
if not os.path.exists('book') \
   or not os.path.exists('Makefile'):
  die('Please run this from the Subversion book source directory\n')
  
if not os.getenv('JAVA_HOME'):
  die('JAVA_HOME is not set.\n')

tarball_base = os.path.join(cwd, 'svnbook-%s' % (locale))
os.putenv('FOP_OPTS', '-Xms100m -Xmx200m')

try:
  os.mkdir('svnbook-tmp')
  os.system('DESTDIR=svnbook-tmp make book-clean %s' % (' '.join(targets)))
  os.rename('svnbook-tmp/usr/share/doc/subversion/book', tarball_base)
  os.system('tar cvfz ' + tarball_base + '.tar.gz ' + tarball_base)
finally:
  shutil.rmtree(tarball_base)
  shutil.rmtree('svnbook-tmp')
  
if not os.path.exists(tarball_base + '.tar.gz'):
  die('Hrm.  It appears the tarball was not created.\n')

print 'Your tarball sits in %s.tar.gz.  Enjoy!' % (tarball_base)

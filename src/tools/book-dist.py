#!/usr/bin/env python2

import sys
import os
import shutil
import getopt



def die(msg):
    sys.stderr.write('ERROR: ' + msg)
    sys.exit(1)


def usage(errorcode):
    stream = errorcode and sys.stderr or sys.stdout
    stream.write("""Usage: %s OPTIONS

Options:
   --html:         Make the single-page HTML book
   --html-chunk:   Make the chunked HTML book
   --pdf:          Make the PDF book
   --name:         The base name of the tarball, and top-level tar directory
""" % (os.path.basename(sys.argv[0])))
    sys.exit(errorcode)
    

def main():
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "h",
                                      ['help', 'html', 'html-chunk',
                                       'pdf', 'name='])
    except:
        usage(1)
    html = html_chunk = pdf = 0
    name = 'svnbook'
    targets = []
    for opt, arg in optlist:
        if opt == '--help' or opt == '-h':
            usage(0)
        if opt == '--html':
            html = 1
        if opt == '--html-chunk':
            html_chunk = 1
        if opt == '--pdf':
            pdf = 1
        if opt == '--name':
            name = arg

    if pdf and not os.getenv('JAVA_HOME'):
        die('JAVA_HOME is not set.\n')

    if os.path.basename(name) != name:
        die('Name "%s" is not a single path component\n' % (name))
        
    if html: targets.append('install-book-html')
    if html_chunk: targets.append('install-book-html-chunk')
    if pdf: targets.append('install-book-pdf')

    if len(targets) < 1:
        die('No targets specified.\n')
        
    if not os.path.exists('book') or not os.path.exists('Makefile'):
        die('Please run this from the Subversion book source directory.\n')
    os.putenv('FOP_OPTS', '-Xms100m -Xmx200m')

    def _cleanup_tmp_dirs():
        if os.path.exists(name): shutil.rmtree(name)
        if os.path.exists('__SVNBOOK_TMP__'): shutil.rmtree('__SVNBOOK_TMP__')
      
    try:
        _cleanup_tmp_dirs()
        os.mkdir('__SVNBOOK_TMP__')
        os.system('DESTDIR=__SVNBOOK_TMP__ make book-clean %s' \
                  % (' '.join(targets)))
        os.rename('__SVNBOOK_TMP__/usr/share/doc/subversion/book', name)
        os.system('tar cvfz %s.tar.gz %s' % (name, name))
    finally:
        _cleanup_tmp_dirs()
  
    if not os.path.exists(name + '.tar.gz'):
        die('Hrm.  It appears the tarball was not created.\n')

    print 'Tarball %s.tar.gz created.  Enjoy!' % (name)

if __name__ == "__main__":
    main()

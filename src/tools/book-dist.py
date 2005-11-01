#!/usr/bin/env python2

import sys
import os
import shutil
import getopt



def die(msg):
    sys.stderr.write('ERROR: ' + msg)
    sys.exit(1)


def usage(err_msg):
    stream = err_msg and sys.stderr or sys.stdout
    if err_msg:
        stream.write("ERROR: %s\n\n" % (err_msg))
    stream.write("""Usage: %s OPTIONS

Options:
   --html:         Make the single-page HTML book
   --html-chunk:   Make the chunked HTML book
   --pdf:          Make the PDF book (requires JAVA_HOME environment variable)
   --name:         The base name of the tarball, and top-level tar directory
""" % (os.path.basename(sys.argv[0])))
    sys.exit(err_msg and 1 or 0)
    

def main():
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "h",
                                      ['help', 'html', 'html-chunk',
                                       'pdf', 'name='])
    except:
        usage("Invalid syntax")
    html = html_chunk = pdf = 0
    name = 'svnbook'
    targets = []
    for opt, arg in optlist:
        if opt == '--help' or opt == '-h':
            usage(None)
        if opt == '--html':
            html = 1
        if opt == '--html-chunk':
            html_chunk = 1
        if opt == '--pdf':
            pdf = 1
        if opt == '--name':
            name = arg

    if pdf and not os.getenv('JAVA_HOME'):
        usage('JAVA_HOME is not set.')

    if os.path.basename(name) != name:
        usage('Name "%s" is not a single path component' % (name))
        
    if html: targets.append('install-html')
    if html_chunk: targets.append('install-html-chunk')
    if pdf: targets.append('install-pdf')

    if len(targets) < 1:
        usage('No targets specified.')
        
    if not os.path.exists('book') or not os.path.exists('Makefile'):
        die('Please run this from the Subversion book source directory.\n')
    os.putenv('FOP_OPTS', '-Xms100m -Xmx200m')

    def _cleanup_tmp_dirs():
        if os.path.exists(name): shutil.rmtree(name)
        if os.path.exists('__SVNBOOK_TMP__'): shutil.rmtree('__SVNBOOK_TMP__')
      
    try:
        _cleanup_tmp_dirs()
        os.mkdir('__SVNBOOK_TMP__')
        os.system('DESTDIR=__SVNBOOK_TMP__ make clean %s' \
                  % (' '.join(targets)))
        if os.path.isdir('__SVNBOOK_TMP__/usr/share/doc/subversion/book'):
            os.rename('__SVNBOOK_TMP__/usr/share/doc/subversion/book', name)
            os.system('tar cvfz %s.tar.gz %s' % (name, name))
    finally:
        _cleanup_tmp_dirs()
  
    if not os.path.exists(name + '.tar.gz'):
        die('Hrm.  It appears the tarball was not created.\n')

    print 'Tarball %s.tar.gz created.  Enjoy!' % (name)

if __name__ == "__main__":
    main()

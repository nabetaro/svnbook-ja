#!/usr/bin/env python

import sys, os, string

subcmd = ("diff", "di", "log", "merge")

def usage(err_msg):
  stream = err_msg and sys.stderr or sys.stdout
  if err_msg:
    stream.write("ERROR: %s\n\n" % (err_msg))
  stream.write("""Usage: %(name)s <subcommand> [filename]

Valid subcommands: %(valid_subcmd)s

Examples:
   %(name)s log book/foreword.xml
   %(name)s diff
""" % { 'name' : os.path.basename(sys.argv[0]), 'valid_subcmd' : subcmd })
  sys.exit(err_msg and 1 or 0)

def main():

  if len(sys.argv) < 2:
    usage(None)

  if not sys.argv[1] in subcmd:
    usage("Invalid syntax")

  book_src_url = "https://svn.red-bean.com/svnbook/trunk/src/en/book/"
  fd = open("LAST_UPDATED", "r")
  last_up_rev = fd.readline()
  fd.close()

  print "svn update"
  os.system("svn update")
  os.chdir("book")

  if len(sys.argv) > 2:
    cmd = "svn " + sys.argv[1] + " -r " + last_up_rev + ":HEAD " + book_src_url + \
          os.path.basename(sys.argv[2])
    print cmd
    os.system(cmd)
  else:
    cmd = "svn " + sys.argv[1] + " -r " + last_up_rev + ":HEAD " + book_src_url
    print cmd
    os.system(cmd)
    if sys.argv[1] == 'merge':
      if string.lower(raw_input("Whether to udate 'LAST_UPDATED'? [y/N] ")) == 'y':
        os.chdir("..")
        cmd = "svnversion . --no-newline > LAST_UPDATED"
        print cmd
        os.system(cmd)

if __name__ == "__main__":
    main()
#!/usr/bin/env python2

import sys, os, getopt, string

def usage(err_msg):
    stream = err_msg and sys.stderr or sys.stdout
    if err_msg:
        stream.write("ERROR: %s\n\n" % (err_msg))
    stream.write("""Usage: %(name)s OPTIONS

Options:
   -f:     <filename.xml>
   -a:     <action>, can be [log | diff | merge]
   -b:     Merging ru/ with en/

Examples:
   %(name)s -f book/ch01.xml -a diff   <- view diff for ch01.xml
   %(name)s -b                         <- merging ru/ with en/
""" % { 'name' : os.path.basename(sys.argv[0]) })
    sys.exit(err_msg and 1 or 0)

def main():

    if len(sys.argv) < 2:
      usage(None)

    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:a:b")
    except:
        usage("Invalid syntax")

    fname = action = ''
    bmerge = False

    book_src = os.listdir("book")
    file_actions = ("log", "diff", "merge")
    book_src_url = "https://svn.red-bean.com/svnbook/trunk/src/en/"

    for o, a in opts:
        if o == "-f":
            if os.path.basename(a) in book_src:
                fname = a
        elif o == "-a":
            if a in file_actions:
                action = a
        elif o == "-b":
            bmerge = True

    fd = open("LAST_UPDATED", "r")
    last_up_rev = fd.readline()
    fd.close()

    attention = """ATTENTION! First it is necessary to make synchronization
for separate files and commit performed changes!
Continue? [y/N] """

    if bmerge:
        if string.lower(raw_input(attention)) == 'y':
            print "svn update"
            os.system("svn update")
            os.chdir("book")
            cmd = "svn merge" + " -r " + last_up_rev + ":" + "HEAD" + " " + \
                  book_src_url + "book/"
            print cmd
            os.system(cmd)
            os.chdir("..")
            os.system("svnversion . --no-newline > LAST_UPDATED")
        sys.exit()

    if fname == '' or action == '':
        usage("Invalid syntax")

    print "svn update"
    os.system("svn update")

    os.chdir("book")
    cmd = "svn " + action + " -r " + last_up_rev + ":" + "HEAD" + " " + \
          book_src_url + fname
    print cmd
    os.system(cmd)

if __name__ == "__main__":
    main()

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
   -l:     View log for en/book/

Examples:
   %(name)s -f book/ch01.xml -a diff   <- view diff for ch01.xml
   %(name)s -b                         <- merging ru/ with en/
   %(name)s -l                         <- view log for en/book/
""" % { 'name' : os.path.basename(sys.argv[0]) })
    sys.exit(err_msg and 1 or 0)

def main():

    if len(sys.argv) < 2:
      usage(None)

    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:a:bl")
    except:
        usage("Invalid syntax")

    fname = action = ''
    bmerge = blog = False

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
        elif o == "-l":
            blog = True

    fd = open("LAST_UPDATED", "r")
    last_up_rev = fd.readline()
    fd.close()

    attention = """ATTENTION! First it is necessary to make synchronization
for separate files (and commit performed changes if during
synchronization you had conflicts)!
Continue? [y/N] """

    merge_error = """During merge there were some errors. Solve a problem
and start merge once again."""

    if bmerge:
        if string.lower(raw_input(attention)) == 'y':
            print "svn update"
            os.system("svn update")
            os.chdir("book")
            cmd = "svn merge -r " + last_up_rev + ":HEAD " + \
                  book_src_url + "book/"
            print cmd
            os.system(cmd)
            os.chdir("..")
            os.system("svnversion . --no-newline > LAST_UPDATED")
            fd = open("LAST_UPDATED", "r")
            s = fd.readline()
            fd.close()
            if s != last_up_rev:
                print merge_error
                os.system("svn revert LAST_UPDATED")
        sys.exit()

    if blog:
        cmd = "svn log -r " + last_up_rev + ":HEAD " + book_src_url + "book/"
        print cmd
        os.system(cmd)
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

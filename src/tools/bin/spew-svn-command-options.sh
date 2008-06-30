#!/bin/bash

### Print 'svn' subcommands and their non-global, non-deprecated options. ###

for subcommand in `svn help | grep '^   [a-z]' | cut -f 4 -d ' '`; do 
    echo "*** ${subcommand} ***"
    svn help ${subcommand} | cut -c3- | grep '^\-' | sort | grep -v '^-\(-username\|-password\|-non-interactive\|-no-auth-cache\|-config-dir\|N \)' | sed 's,^,   ,'
done
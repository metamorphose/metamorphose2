#!/bin/bash

#
# Update or create all translation files.
#

msgfmt='/usr/bin/msgfmt'
msgs_dir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

cd $msgs_dir
for dir in `ls -1`; do
    if [ -d $dir ]; then
        if [ ! -d $dir/LC_MESSAGES ]; then
            mkdir $dir/LC_MESSAGES
        fi
        echo "$msgs_dir/$dir/LC_MESSAGES/metamorphose2.mo"
        $msgfmt -o $dir/LC_MESSAGES/metamorphose2.mo $dir/$dir.po
        rm -f $dir/*.mo
    fi
done


#!/bin/bash

msgfmt='/usr/bin/msgfmt';

for dir in `ls -1`; do
    if [ -d $dir ]; then
        if [ ! -d $dir/LC_MESSAGES ]; then
            mkdir $dir/LC_MESSAGES
        fi
        $msgfmt -o $dir/LC_MESSAGES/metamorphose2.mo $dir/$dir.po;
        rm -f $dir/*.mo;
    fi
done


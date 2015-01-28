#!/bin/sh
#
# Update or create all translation files.
#

# XXX TODO Verify compatibility on non-Bourne shells such as zsh

unamestr=`uname`

if [ "$unamestr" == 'Linux' ]; then
	msgfmt='/usr/bin/msgfmt'
elif [ "$unamestr" == 'FreeBSD' ]; then
	msgfmt='/usr/local/bin/msgfmt'
fi

msgs_dir=$( cd "$( dirname "${0}" )" && pwd )

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


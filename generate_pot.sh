#!/bin/bash

# Grabs all translatable strings in python files

FILES=''

cd src

for file in `find . -name "*.py"`; do
    FILES="$FILES ${file:2}";
done

pygettext -a $FILES

mv messages.pot ../messages/

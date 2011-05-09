#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2007, Ianaré Sévi <ianare@gmail.com>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

"""
Convert integers to Greek numerals. In the case of a negative integer,
its absolute value will be used.
Input can be an integer or a string, output will be in unicode.

Based on http://search.cpan.org/perldoc?Convert::Number::Greek

Example usage in python:
    import greek_numb as greek
    greek_number = greek.int2greek(1984)


Variables (default values shown):
    numbersign = True
    Append the Greek numerical symbol 'ʹ' to number

    upper = False
    Return capital letters

    stigma = True
    Use stigma 'ϛ' rather than sigma-tau 'στ' for 6

    arch_qoppa = False
    Use archaic qoppa 'ϙ' rather than modern 'ϟ' for 90


Usage from command line:
    greek_numb.py --help


Testing in bash:
    for ((i=0; i<=100; i=i+1)); do ./greek_numb.py $i; done;


TODO
* Values greater than 9999 cause problems.
* Function to convert Greek numerals to integers.

"""

from __future__ import print_function
import math

class Error(EnvironmentError):
    pass

# Create the numeral list
greek_digits = [u',α,β,γ,δ,ε,ϛ,ζ,η,θ',
	u',ι,κ,λ,μ,ν,ξ,ο,π,ϟ',
	u',ρ,σ,τ,υ,φ,χ,ψ,ω,ϡ']

greek_digits = map(lambda x: x.split(','), greek_digits)


def int2greek(number, numbersign=True, upper=False, stigma=True, arch_qoppa=False):
    """Convert integer to Greek numeral."""
    number = str(number).lstrip('-')
    if not number.isdigit():
        raise Error, 'Input must be an integer'

    if not stigma:
        greek_digits[0][6] = u'στ'
    if arch_qoppa:
        greek_digits[1][9] = u'ϙ'

    length = len(number)
    greek = u''

    for place in reversed(range(length)):
        digit = int(number[length - place - 1])
        greek += u'ͺ' * int(math.floor(place / 3)) + \
			greek_digits[place % 3][digit]

    if upper:
        greek = greek.upper()
    if greek != '' and numbersign:
        greek += u'ʹ'

    return greek


# XXX TODO Convert Greek numeral to integer
def greek2int(greek):
    pass


''' Command line stuff '''

# show command line usage
def usage(exit_status):
    msg = 'Usage: greek_numb.py [OPTIONS] INTEGER\n'
    msg += 'Converts integers to Greek numerals.\n\nSetting options inverses their defaults.\n'
    msg += '(Defaults shown in parentheses)\n\n'
    msg += "-n --numbersign (True)\tAppend the Greek numerical symbol 'ͺ' to number\n"
    msg += "-u --upper (False) \tReturn capital letters\n"
    msg += "-s --stigma (True)\tUse stigma 'ϛ' rather than sigma-tau 'στ' for 6\n"
    msg += "-q --arch_qoppa (False)\tUse archaic qoppa 'ϙ' rather than modern 'ϟ' for 90\n"
    print(msg)
    sys.exit(exit_status)


# run from command line
if __name__ == '__main__':
    import sys
    import getopt

    # parse command line options/arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hnusq",
								   ["help", "numbersign", "upper", "stigma", "arch_qoppa"])
    except getopt.GetoptError:
        usage(2)
    if len(args) == 0 or len(args) > 1:
        usage(2)

    numbersign = True
    upper = False
    stigma = True
    arch_qoppa = False

    for o, a in opts:
        if o in ("-h", "--help"):
            usage(0)
        if o in ("-n", "--numbersign"):
            numbersign = False
        if o in ("-u", "--upper"):
            upper = True
        if o in ("-s", "--stigma"):
            stigma = False
        if o in ("-q", "arch_qoppa"):
            arch_qoppa = True

    number = args[0]

    print(int2greek(number, numbersign, upper, stigma, arch_qoppa))



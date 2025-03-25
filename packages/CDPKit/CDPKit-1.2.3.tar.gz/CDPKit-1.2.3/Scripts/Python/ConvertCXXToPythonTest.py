## 
# ConvertCXXToPythonTest.py 
#
# This file is part of the Chemical Data Processing Toolkit
#
# Copyright (C) 2003 Thomas Seidel <thomas.seidel@univie.ac.at>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; see the file COPYING. If not, write to
# the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
##


import sys
import re
import math


def cxxToPythonCode():
    if len(sys.argv) < 3:
        print('Usage:', sys.argv[0], '[input file] [output file]', file=sys.stderr)
        sys.exit(2)

    output = list()

    for line in open(sys.argv[1], 'r'):
        if re.match('#include "CDPL/Base/Exceptions\.hpp"', line):
            continue

        match = re.match('#include "CDPL/(\w+)/(\w+).hpp"', line)

        if match:
            output.append('from CDPL.' + match.group(1) + ' import ' + match.group(2) + '\n')
            continue

        if re.match('#include <boost/test/auto_unit_test\.hpp', line):
            output.append('import unittest\n')
            continue

        if re.match('#include <boost', line):
            continue

        if re.match('\s*private:\s*$', line):
            continue

        if re.match('\s*public:\s*$', line):
            continue

        if re.match('\s*protected:\s*$', line):
            continue

        if re.search('namespace', line):
            continue

        if re.match('\s*\{\s*$', line):
            continue

        if re.match('\s*\}\s*;*\s*$', line):
            continue

        match = re.match('BOOST_AUTO_TEST_CASE\((\w+)Test\)', line)

        if match:
            output.append('class TestCase(unittest.TestCase):\n')
            output.append('\n')
            output.append('    def runTest(self):\n')
            output.append('        """Testing ' + match.group(1) + '"""\n')
            continue

        line = re.sub('^/\*', '##', line)
        line = re.sub('^\s\*/', '##', line)
        line = re.sub('^\s\*', '#', line)
        line = re.sub('Test\.cpp', 'Test.py', line)
        line = re.sub(';', '', line)
        line = re.sub('BOOST_CHECK\(', 'self.assert_(', line)
        line = re.sub('^//', '    #', line)
        line = re.sub('::', '.', line)
        line = re.sub('&&', 'and', line)
        line = re.sub('\|\|', 'or', line)
        line = re.sub('&', '', line)
        line = re.sub('const ', '', line)
        line = re.sub('!', 'not ', line)
        line = re.sub('not =', '!=', line)
        line = re.sub('\.getProperty<[\w\.]+>', '.getProperty', line)
        line = re.sub('Base\.IndexOutOfBounds', 'IndexError', line)
        line = re.sub('IndexOutOfBounds', 'IndexError', line)
        line = re.sub('Base\.InvalidArgument', 'RuntimeError', line)
        line = re.sub('InvalidArgument', 'RuntimeError', line)
        line = re.sub('Base\.IOError', 'IOError', line)
        line = re.sub('Base\.CalculationFailed', 'RuntimeError', line)
        line = re.sub('CalculationFailed', 'RuntimeError', line)
        line = re.sub('Base\.Exception', 'RuntimeError', line)
        line = re.sub('Exception', 'RuntimeError', line)
        line = re.sub('Base\.OperationFailed', 'RuntimeError', line)
        line = re.sub('OperationFailed', 'RuntimeError', line)
        line = re.sub('Base\.ItemNotFound', 'RuntimeError', line)
        line = re.sub('ItemNotFound', 'RuntimeError', line)
        line = re.sub('const_cast<[\s\w<>&]+>\(([\w]+)\)', r'\1', line)
        line = re.sub('false', 'False', line)
        line = re.sub('true', 'True', line)
        line = re.sub('"', "'", line)

        match = re.search('BOOST_CHECK_THROW\((.+),\s+(.+)\)\s*$', line)

        if match:
            line = '    ' + 'self.assertRaises(' + match.group(2) + ', ' + match.group(1) + ')\n'

        def percent_to_places(percent):
            return str(round(-math.log(float(percent) / 100.0, 10)))
   
        match = re.search('BOOST_CHECK_SMALL\((.+),\s+([0-9\.]+)\)\s*$', line)

        if match:
            line = '    ' + 'self.assertAlmostEqual(' + match.group(1) + ', 0.0, ' +\
            percent_to_places(match.group(2)) + ')\n'

        match = re.search('BOOST_CHECK_CLOSE\((.+),\s+(.+),\s+([0-9\.]+)\)\s*$', line)

        if match:
            line = '    ' + 'self.assertAlmostEqual(' + match.group(1) + ', ' + match.group(2) +\
            ', ' + percent_to_places(match.group(3)) + ')\n'

        
        match = re.search('^\s+(\w+)\s+=\s+(.+)\s*$', line)

        if match:
            line = '    ' + match.group(1) + '.assign(' + match.group(2) + ')\n'

        match = re.search('^\s+([\w\.<>]+)\s+(\w+)\((.*)\)\s*$', line)

        if match:
            line = '    ' + match.group(2) + ' = ' + match.group(1) + '(' + match.group(3) + ')\n'

        match = re.search('^\s+([\w\.<>]+)\s+(\w+)\s*$', line)

        if match:
            line = '    ' + match.group(2) + ' = ' + match.group(1) + '()\n'

        match = re.search('^\s+([\w\.<>]+)\s+(\w+)\s+=\s+(.+)\s*$', line)

        if match:
            line = '    ' + match.group(2) + ' = ' + match.group(3) + '\n'

        line = re.sub('BOOST_CHECK_SMALL\(', 'self.assertAlmostEqual(', line)
        line = re.sub('BOOST_CHECK_CLOSE\(', 'self.assertAlmostEqual(', line)
        line = re.sub('BOOST_CHECK_THROW\(', 'self.assertRaises(', line)

        if line[0] != '#':
            line = '    ' + line

        output.append(line)

    open(sys.argv[2], 'w+').writelines(output)


if __name__ == '__main__':
    cxxToPythonCode()

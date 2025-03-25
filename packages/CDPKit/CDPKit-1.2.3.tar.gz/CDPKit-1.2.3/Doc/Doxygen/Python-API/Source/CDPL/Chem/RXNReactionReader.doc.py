#
# This file is part of the Chemical Data Processing Toolkit
#
# Copyright (C) Thomas Seidel <thomas.seidel@univie.ac.at>
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
#

##
# \brief A reader for reaction data in the <em>MDL Rxn-File</em> [\ref CTFILE] format.
# 
# <tt>RXNReactionReader</tt> supports the following control-parameters:
# 
# <table>
#  <tr><th>Control-Parameter</th><th>Default Value (see Chem.ControlParameterDefault)</th><th>Description</th></tr>
#  <tr><td>Chem.ControlParameter.STRICT_ERROR_CHECKING</td><td><tt>False</tt></td><td>Specifies whether non-fatal recoverable errors should be ignored or cause a read operation to fail</td></tr>
#  <tr><td>Chem.ControlParameter.MDL_IGNORE_PARITY</td><td><tt>False</tt></td><td>Specifies whether the stereo parity of atoms shall be ignored</td></tr>
#  <tr><td>Chem.ControlParameter.MDL_TRIM_STRINGS</td><td><tt>True</tt></td><td>Specifies whether to remove leading and trailing whitespace from string values</td></tr>
#  <tr><td>Chem.ControlParameter.MDL_TRIM_LINES</td><td><tt>False</tt></td><td>Specifies whether to remove leading and trailing whitespace from data lines</td></tr>
#  <tr><td>Chem.ControlParameter.MDL_IGNORE_LINE_LENGTH_LIMIT</td><td><tt>True</tt></td><td>Specifies whether to check if data lines exceed the maximum allowed line length</td></tr>
# </table>
# 
class RXNReactionReader(ReactionReaderBase):

    ##
    # \brief Constructs a <tt>RXNReactionReader</tt> instance that will read the reaction data from the input stream <em>is</em>.
    # 
    # \param is The input stream to read from.
    # 
    def __init__(is: Base.IStream) -> None: pass

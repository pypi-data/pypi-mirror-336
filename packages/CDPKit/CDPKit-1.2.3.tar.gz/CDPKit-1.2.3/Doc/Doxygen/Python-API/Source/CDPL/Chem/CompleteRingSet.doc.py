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
# \brief Implements the exhaustive perception of rings in a molecular graph.
# 
# \see [\ref HANSER]
# 
class CompleteRingSet(FragmentList):

    ##
    # \brief Constructs an empty <tt>CompleteRingSet</tt> instance.
    # 
    def __init__() -> None: pass

    ##
    # \brief Constructs a <tt>CompleteRingSet</tt> instance that contains the rings in the molecular graph <em>molgraph</em>.
    # 
    # \param molgraph The molecular graph for which to perceive the complete set of rings.
    # 
    def __init__(molgraph: MolecularGraph) -> None: pass

    ##
    # \brief Replaces the current set of rings by the rings in the molecular graph <em>molgraph</em>.
    # 
    # \param molgraph The molecular graph for which to perceive the complete set of rings.
    # 
    def perceive(molgraph: MolecularGraph) -> None: pass

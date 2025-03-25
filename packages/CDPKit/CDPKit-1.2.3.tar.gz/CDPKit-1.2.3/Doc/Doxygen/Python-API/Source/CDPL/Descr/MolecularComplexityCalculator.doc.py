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
# \brief MolecularComplexityCalculator.
# 
# \see [\ref MCPLX]
# 
class MolecularComplexityCalculator(Boost.Python.instance):

    ##
    # \brief Constructs the <tt>MolecularComplexityCalculator</tt> instance.
    # 
    def __init__() -> None: pass

    ##
    # \brief Constructs the <tt>MolecularComplexityCalculator</tt> instance and calculates the complexity of the molecular graph <em>molgraph</em>.
    # 
    # The calculated complexity can be retrieved by a call to getResult().
    # 
    # \param molgraph The molecular graph for which to calculate the complexity.
    # 
    def __init__(molgraph: Chem.MolecularGraph) -> None: pass

    ##
    # \brief Returns the numeric identifier (ID) of the wrapped C++ class instance.
    # 
    # Different Python \c %MolecularComplexityCalculator instances may reference the same underlying C++ class instance. The commonly used Python expression
    # <tt>a is not b</tt> thus cannot tell reliably whether the two \c %MolecularComplexityCalculator instances \e a and \e b reference different C++ objects. 
    # The numeric identifier returned by this method allows to correctly implement such an identity test via the simple expression
    # <tt>a.getObjectID() != b.getObjectID()</tt>.
    # 
    # \return The numeric ID of the internally referenced C++ class instance.
    # 
    def getObjectID() -> int: pass

    ##
    # \brief Calculates the complexity of the molecular graph <em>molgraph</em>.
    # 
    # \param molgraph The molecular graph for which to calculate the complexity.
    # 
    # \return The calculated complexity of the molecular graph <em>molgraph</em>.
    # 
    def calculate(molgraph: Chem.MolecularGraph) -> float: pass

    ##
    # \brief Returns the result of the last molecular graph complexity calculation.
    # 
    # \return The result of the last molecular graph complexity calculation, or zero if a calculation has not yet been performed.
    # 
    def getResult() -> float: pass

    objectID = property(getObjectID)

    result = property(getResult)

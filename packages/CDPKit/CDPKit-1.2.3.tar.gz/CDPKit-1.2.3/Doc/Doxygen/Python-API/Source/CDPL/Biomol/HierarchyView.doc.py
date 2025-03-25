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
# \brief A data structure allowing a hierarchical view on biological macromolecules.
# 
class HierarchyView(Boost.Python.instance):

    ##
    # \brief Constructs an empty <tt>HierarchyView</tt> instance.
    # 
    def __init__() -> None: pass

    ##
    # \brief Constructs a <tt>HierarchyView</tt> instance for the molecular graph <em>molgraph</em>.
    # 
    # \param molgraph The molecular graph for which to build the hierarchy view.
    # 
    def __init__(molgraph: Chem.MolecularGraph) -> None: pass

    ##
    # \brief Returns the numeric identifier (ID) of the wrapped C++ class instance.
    # 
    # Different Python \c %HierarchyView instances may reference the same underlying C++ class instance. The commonly used Python expression
    # <tt>a is not b</tt> thus cannot tell reliably whether the two \c %HierarchyView instances \e a and \e b reference different C++ objects. 
    # The numeric identifier returned by this method allows to correctly implement such an identity test via the simple expression
    # <tt>a.getObjectID() != b.getObjectID()</tt>.
    # 
    # \return The numeric ID of the internally referenced C++ class instance.
    # 
    def getObjectID() -> int: pass

    ##
    # \brief Build the hierarchy view for the molecular graph <em>molgraph</em>.
    # 
    # \param molgraph The molecular graph for which to build the hierarchy view.
    # 
    def build(molgraph: Chem.MolecularGraph) -> None: pass

    ##
    # \brief 
    # \return 
    #
    def getResidues() -> ResidueList: pass

    ##
    # \brief 
    # \return 
    #
    def getNumModels() -> int: pass

    ##
    # \brief 
    # \param idx 
    # \return 
    #
    def getModel(idx: int) -> HierarchyViewModel: pass

    ##
    # \brief 
    # \param num 
    # \return 
    #
    def hasModelWithNumber(num: int) -> bool: pass

    ##
    # \brief 
    # \param num 
    # \return 
    #
    def getModelByNumber(num: int) -> HierarchyViewModel: pass

    ##
    # \brief 
    # \return 
    #
    def __len__() -> int: pass

    ##
    # \brief 
    # \param idx 
    # \return 
    #
    def __getitem__(idx: int) -> HierarchyViewModel: pass

    objectID = property(getObjectID)

    numModels = property(getNumModels)

    residues = property(getResidues)

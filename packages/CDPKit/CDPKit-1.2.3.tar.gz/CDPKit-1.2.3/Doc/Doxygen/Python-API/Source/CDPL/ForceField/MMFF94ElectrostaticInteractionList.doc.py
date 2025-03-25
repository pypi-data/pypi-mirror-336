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
# \brief 
#
class MMFF94ElectrostaticInteractionList(Boost.Python.instance):

    ##
    # \brief Initializes the \e %MMFF94ElectrostaticInteractionList instance.
    # 
    def __init__() -> None: pass

    ##
    # \brief Initializes a copy of the \e %MMFF94ElectrostaticInteractionList instance \a ia_list.
    # \param ia_list The \e %MMFF94ElectrostaticInteractionList instance to copy.
    # 
    def __init__(ia_list: MMFF94ElectrostaticInteractionList) -> None: pass

    ##
    # \brief Returns the numeric identifier (ID) of the wrapped C++ class instance.
    # 
    # Different Python \c %MMFF94ElectrostaticInteractionList instances may reference the same underlying C++ class instance. The commonly used Python expression
    # <tt>a is not b</tt> thus cannot tell reliably whether the two \c %MMFF94ElectrostaticInteractionList instances \e a and \e b reference different C++ objects. 
    # The numeric identifier returned by this method allows to correctly implement such an identity test via the simple expression
    # <tt>a.getObjectID() != b.getObjectID()</tt>.
    # 
    # \return The numeric ID of the internally referenced C++ class instance.
    # 
    def getObjectID() -> int: pass

    ##
    # \brief 
    # \return 
    #
    def getSize() -> int: pass

    ##
    # \brief 
    # \return 
    #
    def isEmpty() -> bool: pass

    ##
    # \brief 
    # \param num_elem 
    # \param value 
    #
    def resize(num_elem: int, value: MMFF94ElectrostaticInteraction) -> None: pass

    ##
    # \brief 
    # \param num_elem 
    #
    def reserve(num_elem: int) -> None: pass

    ##
    # \brief 
    # \return 
    #
    def getCapacity() -> int: pass

    ##
    # \brief 
    #
    def clear() -> None: pass

    ##
    # \brief Replaces the current state of \a self with a copy of the state of the \c %MMFF94ElectrostaticInteractionList instance \a array.
    # \param array The \c %MMFF94ElectrostaticInteractionList instance to copy.
    # \return \a self
    # 
    def assign(array: MMFF94ElectrostaticInteractionList) -> MMFF94ElectrostaticInteractionList: pass

    ##
    # \brief 
    # \param num_elem 
    # \param value 
    #
    def assign(num_elem: int, value: MMFF94ElectrostaticInteraction) -> None: pass

    ##
    # \brief 
    # \param value 
    #
    def addElement(value: MMFF94ElectrostaticInteraction) -> None: pass

    ##
    # \brief 
    # \param values 
    #
    def addElements(values: MMFF94ElectrostaticInteractionList) -> None: pass

    ##
    # \brief 
    # \param idx 
    # \param value 
    #
    def insertElement(idx: int, value: MMFF94ElectrostaticInteraction) -> None: pass

    ##
    # \brief 
    # \param idx 
    # \param num_elem 
    # \param value 
    #
    def insertElements(idx: int, num_elem: int, value: MMFF94ElectrostaticInteraction) -> None: pass

    ##
    # \brief 
    # \param index 
    # \param values 
    #
    def insertElements(index: int, values: MMFF94ElectrostaticInteractionList) -> None: pass

    ##
    # \brief 
    #
    def popLastElement() -> None: pass

    ##
    # \brief 
    # \param idx 
    #
    def removeElement(idx: int) -> None: pass

    ##
    # \brief 
    # \param begin_idx 
    # \param end_idx 
    #
    def removeElements(begin_idx: int, end_idx: int) -> None: pass

    ##
    # \brief 
    # \return 
    #
    def getFirstElement() -> MMFF94ElectrostaticInteraction: pass

    ##
    # \brief 
    # \return 
    #
    def getLastElement() -> MMFF94ElectrostaticInteraction: pass

    ##
    # \brief 
    # \param idx 
    # \return 
    #
    def getElement(idx: int) -> MMFF94ElectrostaticInteraction: pass

    ##
    # \brief 
    # \param idx 
    # \param value 
    #
    def setElement(idx: int, value: MMFF94ElectrostaticInteraction) -> None: pass

    ##
    # \brief 
    # \param idx 
    #
    def __delitem__(idx: int) -> None: pass

    ##
    # \brief 
    # \param idx 
    # \return 
    #
    def __getitem__(idx: int) -> MMFF94ElectrostaticInteraction: pass

    ##
    # \brief 
    # \return 
    #
    def __len__() -> int: pass

    ##
    # \brief 
    # \param index 
    # \param value 
    #
    def __setitem__(index: int, value: MMFF94ElectrostaticInteraction) -> None: pass

    objectID = property(getObjectID)

    size = property(getSize)

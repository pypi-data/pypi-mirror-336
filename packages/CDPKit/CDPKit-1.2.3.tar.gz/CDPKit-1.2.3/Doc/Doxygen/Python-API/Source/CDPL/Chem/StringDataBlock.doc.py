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
# \brief An array of Chem.StringDataBlockEntry objects used to store the structure or reaction data block of a <em>STRING SD-</em> or <em>RD-File</em> data record (see [\ref CTFILE]).
# 
class StringDataBlock(Boost.Python.instance):

    ##
    # \brief Initializes the \e %StringDataBlock instance.
    # 
    def __init__() -> None: pass

    ##
    # \brief Initializes a copy of the \e %StringDataBlock instance \a data_block.
    # \param data_block The \e %StringDataBlock instance to copy.
    # 
    def __init__(data_block: StringDataBlock) -> None: pass

    ##
    # \brief Returns the numeric identifier (ID) of the wrapped C++ class instance.
    # 
    # Different Python \c %StringDataBlock instances may reference the same underlying C++ class instance. The commonly used Python expression
    # <tt>a is not b</tt> thus cannot tell reliably whether the two \c %StringDataBlock instances \e a and \e b reference different C++ objects. 
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
    def resize(num_elem: int, value: StringDataBlockEntry) -> None: pass

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
    # \brief Replaces the current state of \a self with a copy of the state of the \c %StringDataBlock instance \a array.
    # \param array The \c %StringDataBlock instance to copy.
    # \return \a self
    # 
    def assign(array: StringDataBlock) -> StringDataBlock: pass

    ##
    # \brief 
    # \param num_elem 
    # \param value 
    #
    def assign(num_elem: int, value: StringDataBlockEntry) -> None: pass

    ##
    # \brief 
    # \param value 
    #
    def addElement(value: StringDataBlockEntry) -> None: pass

    ##
    # \brief 
    # \param values 
    #
    def addElements(values: StringDataBlock) -> None: pass

    ##
    # \brief 
    # \param idx 
    # \param value 
    #
    def insertElement(idx: int, value: StringDataBlockEntry) -> None: pass

    ##
    # \brief 
    # \param idx 
    # \param num_elem 
    # \param value 
    #
    def insertElements(idx: int, num_elem: int, value: StringDataBlockEntry) -> None: pass

    ##
    # \brief 
    # \param index 
    # \param values 
    #
    def insertElements(index: int, values: StringDataBlock) -> None: pass

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
    def getFirstElement() -> StringDataBlockEntry: pass

    ##
    # \brief 
    # \return 
    #
    def getLastElement() -> StringDataBlockEntry: pass

    ##
    # \brief 
    # \param idx 
    # \return 
    #
    def getElement(idx: int) -> StringDataBlockEntry: pass

    ##
    # \brief 
    # \param idx 
    # \param value 
    #
    def setElement(idx: int, value: StringDataBlockEntry) -> None: pass

    ##
    # \brief 
    # \param header 
    # \param data 
    #
    def addEntry(header: str, data: str) -> None: pass

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
    def __getitem__(idx: int) -> StringDataBlockEntry: pass

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
    def __setitem__(index: int, value: StringDataBlockEntry) -> None: pass

    ##
    # \brief Returns the result of the comparison operation <tt>self == data_block</tt>.
    # \param data_block The \c %object instance to be compared with.
    # \return The result of the comparison operation.
    # 
    def __eq__(data_block: object) -> bool: pass

    ##
    # \brief Returns the result of the comparison operation <tt>self != data_block</tt>.
    # \param data_block The \c %object instance to be compared with.
    # \return The result of the comparison operation.
    # 
    def __ne__(data_block: object) -> bool: pass

    objectID = property(getObjectID)

    size = property(getSize)

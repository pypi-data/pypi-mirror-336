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
# \brief A data type for the storage and lookup of arbitrary entity to entity mappings.
# 
# Entity3Ds mappings are stored as pairs of references to the mapped Chem.Entity3D objects. Mappings do not have to be unique and multiple mappings of a given entity to other entities are possible. If a mapping entry for a particular entity does not exist, the methods Entity3DMapping.getValue() and Entity3DMapping.operator[]() return a <em>None</em> reference to indicate that the lookup of the mapped entity has failed.
# 
class Entity3DMapping(Boost.Python.instance):

    ##
    # \brief Initializes the \e %Entity3DMapping instance.
    # 
    def __init__() -> None: pass

    ##
    # \brief Initializes a copy of the \e %Entity3DMapping instance \a mapping.
    # \param mapping The \e %Entity3DMapping instance to copy.
    # 
    def __init__(mapping: Entity3DMapping) -> None: pass

    ##
    # \brief Returns the numeric identifier (ID) of the wrapped C++ class instance.
    # 
    # Different Python \c %Entity3DMapping instances may reference the same underlying C++ class instance. The commonly used Python expression
    # <tt>a is not b</tt> thus cannot tell reliably whether the two \c %Entity3DMapping instances \e a and \e b reference different C++ objects. 
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
    #
    def clear() -> None: pass

    ##
    # \brief Replaces the current state of \a self with a copy of the state of the \c %Entity3DMapping instance \a map.
    # \param map The \c %Entity3DMapping instance to copy.
    # \return \a self
    # 
    def assign(map: Entity3DMapping) -> Entity3DMapping: pass

    ##
    # \brief 
    # \param key 
    # \return 
    #
    def getValue(key: Entity3D) -> Entity3D: pass

    ##
    # \brief 
    # \param key 
    # \param def_value 
    # \return 
    #
    def getValue(key: Entity3D, def_value: Entity3D) -> Entity3D: pass

    ##
    # \brief 
    # \param key 
    # \return 
    #
    def removeEntry(key: Entity3D) -> bool: pass

    ##
    # \brief 
    # \param key 
    # \param value 
    #
    def setEntry(key: Entity3D, value: Entity3D) -> None: pass

    ##
    # \brief 
    # \return 
    #
    def getKeys() -> object: pass

    ##
    # \brief 
    # \return 
    #
    def keys() -> object: pass

    ##
    # \brief 
    # \return 
    #
    def getValues() -> object: pass

    ##
    # \brief 
    # \param key 
    # \return 
    #
    def getValues(key: Entity3D) -> object: pass

    ##
    # \brief 
    # \return 
    #
    def values() -> object: pass

    ##
    # \brief 
    # \return 
    #
    def getEntries() -> object: pass

    ##
    # \brief 
    # \return 
    #
    def items() -> object: pass

    ##
    # \brief 
    # \param key 
    # \return 
    #
    def getNumEntries(key: Entity3D) -> int: pass

    ##
    # \brief 
    # \param key 
    # \return 
    #
    def removeEntries(key: Entity3D) -> int: pass

    ##
    # \brief 
    # \param key 
    # \param value 
    #
    def insertEntry(key: Entity3D, value: Entity3D) -> None: pass

    ##
    # \brief 
    # \return 
    #
    def __len__() -> int: pass

    ##
    # \brief 
    # \param key 
    # \return 
    #
    def __getitem__(key: Entity3D) -> Entity3D: pass

    ##
    # \brief 
    # \param key 
    # \param value 
    #
    def __setitem__(key: Entity3D, value: Entity3D) -> None: pass

    ##
    # \brief 
    # \param key 
    # \return 
    #
    def __delitem__(key: Entity3D) -> bool: pass

    ##
    # \brief Returns the result of the membership test operation <tt>key in self</tt>.
    # \param key The value to test for membership.
    # \return The result of the membership test operation.
    # 
    def __contains__(key: Entity3D) -> int: pass

    objectID = property(getObjectID)

    size = property(getSize)

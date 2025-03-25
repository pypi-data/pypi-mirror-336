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
class MMFF94AromaticAtomTypeDefinitionTable(Boost.Python.instance):

    ##
    # \brief 
    #
    class Entry(Boost.Python.instance):

        ##
        # \brief Initializes a copy of the \e %Entry instance \a entry.
        # \param entry The \e %Entry instance to copy.
        # 
        def __init__(entry: Entry) -> None: pass

        ##
        # \brief Initializes the \e %Entry instance.
        # \param old_type 
        # \param aro_type 
        # \param atomic_no 
        # \param ring_size 
        # \param het_atom_dist 
        # \param im_cation 
        # \param n5_anion 
        # 
        def __init__(old_type: str, aro_type: str, atomic_no: int, ring_size: int, het_atom_dist: int, im_cation: bool, n5_anion: bool) -> None: pass

        ##
        # \brief Returns the numeric identifier (ID) of the wrapped C++ class instance.
        # 
        # Different Python \c %Entry instances may reference the same underlying C++ class instance. The commonly used Python expression
        # <tt>a is not b</tt> thus cannot tell reliably whether the two \c %Entry instances \e a and \e b reference different C++ objects. 
        # The numeric identifier returned by this method allows to correctly implement such an identity test via the simple expression
        # <tt>a.getObjectID() != b.getObjectID()</tt>.
        # 
        # \return The numeric ID of the internally referenced C++ class instance.
        # 
        def getObjectID() -> int: pass

        ##
        # \brief Replaces the current state of \a self with a copy of the state of the \c %Entry instance \a entry.
        # \param entry The \c %Entry instance to copy.
        # \return \a self
        # 
        def assign(entry: Entry) -> Entry: pass

        ##
        # \brief 
        # \return 
        #
        def getOldAtomType() -> str: pass

        ##
        # \brief 
        # \return 
        #
        def getAromAtomType() -> str: pass

        ##
        # \brief 
        # \return 
        #
        def getAtomicNumber() -> int: pass

        ##
        # \brief 
        # \return 
        #
        def getRingSize() -> int: pass

        ##
        # \brief 
        # \return 
        #
        def getHeteroAtomDistance() -> int: pass

        ##
        # \brief 
        # \return 
        #
        def isImidazoliumCation() -> bool: pass

        ##
        # \brief 
        # \return 
        #
        def isN5RingAnion() -> bool: pass

        objectID = property(getObjectID)

        oldAtomType = property(getOldAtomType)

        aromAtomType = property(getAromAtomType)

        atomicNumber = property(getAtomicNumber)

        ringSize = property(getRingSize)

        heteroAtomDistance = property(getHeteroAtomDistance)

        imidazoliumCation = property(isImidazoliumCation)

        n5RingAnion = property(isN5RingAnion)

    ##
    # \brief Initializes the \e %MMFF94AromaticAtomTypeDefinitionTable instance.
    # 
    def __init__() -> None: pass

    ##
    # \brief Initializes a copy of the \e %MMFF94AromaticAtomTypeDefinitionTable instance \a table.
    # \param table The \e %MMFF94AromaticAtomTypeDefinitionTable instance to copy.
    # 
    def __init__(table: MMFF94AromaticAtomTypeDefinitionTable) -> None: pass

    ##
    # \brief Returns the numeric identifier (ID) of the wrapped C++ class instance.
    # 
    # Different Python \c %MMFF94AromaticAtomTypeDefinitionTable instances may reference the same underlying C++ class instance. The commonly used Python expression
    # <tt>a is not b</tt> thus cannot tell reliably whether the two \c %MMFF94AromaticAtomTypeDefinitionTable instances \e a and \e b reference different C++ objects. 
    # The numeric identifier returned by this method allows to correctly implement such an identity test via the simple expression
    # <tt>a.getObjectID() != b.getObjectID()</tt>.
    # 
    # \return The numeric ID of the internally referenced C++ class instance.
    # 
    def getObjectID() -> int: pass

    ##
    # \brief 
    # \param old_type 
    # \param aro_type 
    # \param atomic_no 
    # \param ring_size 
    # \param het_atom_dist 
    # \param im_cation 
    # \param n5_anion 
    #
    def addEntry(old_type: str, aro_type: str, atomic_no: int, ring_size: int, het_atom_dist: int, im_cation: bool, n5_anion: bool) -> None: pass

    ##
    # \brief 
    # \param idx 
    #
    def removeEntry(idx: int) -> None: pass

    ##
    # \brief 
    # \param idx 
    # \return 
    #
    def getEntry(idx: int) -> Entry: pass

    ##
    # \brief 
    #
    def clear() -> None: pass

    ##
    # \brief 
    # \return 
    #
    def getNumEntries() -> int: pass

    ##
    # \brief 
    # \return 
    #
    def getEntries() -> list: pass

    ##
    # \brief 
    # \param is 
    #
    def load(is: Base.IStream) -> None: pass

    ##
    # \brief 
    #
    def loadDefaults() -> None: pass

    ##
    # \brief Replaces the current state of \a self with a copy of the state of the \c %MMFF94AromaticAtomTypeDefinitionTable instance \a table.
    # \param table The \c %MMFF94AromaticAtomTypeDefinitionTable instance to copy.
    # \return \a self
    # 
    def assign(table: MMFF94AromaticAtomTypeDefinitionTable) -> MMFF94AromaticAtomTypeDefinitionTable: pass

    ##
    # \brief 
    # \param table 
    #
    @staticmethod
    def set(table: MMFF94AromaticAtomTypeDefinitionTable) -> None: pass

    ##
    # \brief 
    # \param  
    # \return 
    #
    @staticmethod
    def get(: ) -> MMFF94AromaticAtomTypeDefinitionTable: pass

    objectID = property(getObjectID)

    numEntries = property(getNumEntries)

    entries = property(getEntries)

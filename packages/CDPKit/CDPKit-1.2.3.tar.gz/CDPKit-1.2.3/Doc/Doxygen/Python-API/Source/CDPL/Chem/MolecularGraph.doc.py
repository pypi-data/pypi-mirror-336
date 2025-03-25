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
# \brief MolecularGraph.
# 
class MolecularGraph(AtomContainer, BondContainer, Base.PropertyContainer):

    ##
    # \brief 
    #
    class AtomSequence(Boost.Python.instance):

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
        def __getitem__(idx: int) -> Atom: pass

        ##
        # \brief Returns the result of the membership test operation <tt>atom in self</tt>.
        # \param atom The value to test for membership.
        # \return The result of the membership test operation.
        # 
        def __contains__(atom: Atom) -> bool: pass

    ##
    # \brief 
    #
    class BondSequence(Boost.Python.instance):

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
        def __getitem__(idx: int) -> Bond: pass

        ##
        # \brief Returns the result of the membership test operation <tt>bond in self</tt>.
        # \param bond The value to test for membership.
        # \return The result of the membership test operation.
        # 
        def __contains__(bond: Bond) -> bool: pass

    ##
    # \brief Initializes the \e %MolecularGraph instance.
    # 
    def __init__() -> None: pass

    ##
    # \brief 
    # \return 
    #
    def getAtoms() -> AtomSequence: pass

    ##
    # \brief 
    # \return 
    #
    def getBonds() -> BondSequence: pass

    ##
    # \brief Creates a copy of the molecular graph.
    # 
    # \return A smart reference to the copy of the molecular graph.
    # 
    def clone() -> MolecularGraph: pass

    ##
    # \brief 
    # \param idx 
    # \return 
    #
    def getAtom(idx: int) -> Atom: pass

    ##
    # \brief 
    # \param atom 
    # \return 
    #
    def containsAtom(atom: Atom) -> bool: pass

    ##
    # \brief 
    # \param atom 
    # \return 
    #
    def getAtomIndex(atom: Atom) -> int: pass

    ##
    # \brief 
    # \return 
    #
    def getNumAtoms() -> int: pass

    ##
    # \brief 
    # \param func 
    #
    def orderAtoms(func: ForceField.InteractionFilterFunction2) -> None: pass

    ##
    # \brief 
    # \param idx 
    # \return 
    #
    def getEntity(idx: int) -> Entity3D: pass

    ##
    # \brief 
    # \return 
    #
    def getNumEntities() -> int: pass

    ##
    # \brief 
    # \param idx 
    # \return 
    #
    def getBond(idx: int) -> Bond: pass

    ##
    # \brief 
    # \param bond 
    # \return 
    #
    def containsBond(bond: Bond) -> bool: pass

    ##
    # \brief 
    # \param func 
    #
    def orderBonds(func: BoolBond2Functor) -> None: pass

    ##
    # \brief 
    # \param bond 
    # \return 
    #
    def getBondIndex(bond: Bond) -> int: pass

    ##
    # \brief 
    # \return 
    #
    def getNumBonds() -> int: pass

    ##
    # \brief Returns the result of the membership test operation <tt>atom in self</tt>.
    # \param atom The value to test for membership.
    # \return The result of the membership test operation.
    # 
    def __contains__(atom: Atom) -> bool: pass

    ##
    # \brief Returns the result of the membership test operation <tt>bond in self</tt>.
    # \param bond The value to test for membership.
    # \return The result of the membership test operation.
    # 
    def __contains__(bond: Bond) -> bool: pass

    ##
    # \brief Returns the result of the membership test operation <tt>key in self</tt>.
    # \param key The value to test for membership.
    # \return The result of the membership test operation.
    # 
    def __contains__(key: Base.LookupKey) -> bool: pass

    ##
    # \brief 
    # \param key 
    # \return 
    #
    def __getitem__(key: Base.LookupKey) -> Base.Any: pass

    ##
    # \brief 
    # \param key 
    # \param value 
    #
    def __setitem__(key: Base.LookupKey, value: Base.Any) -> None: pass

    ##
    # \brief 
    # \param key 
    # \return 
    #
    def __delitem__(key: Base.LookupKey) -> bool: pass

    ##
    # \brief 
    # \return 
    #
    def __len__() -> int: pass

    atoms = property(getAtoms)

    bonds = property(getBonds)

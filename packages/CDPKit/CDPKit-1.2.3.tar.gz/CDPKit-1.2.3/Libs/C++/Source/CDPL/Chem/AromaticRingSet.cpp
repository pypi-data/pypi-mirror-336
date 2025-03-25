/* 
 * AromaticRingSet.cpp 
 *
 * This file is part of the Chemical Data Processing Toolkit
 *
 * Copyright (C) 2003 Thomas Seidel <thomas.seidel@univie.ac.at>
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this library; see the file COPYING. If not, write to
 * the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 */


#include "StaticInit.hpp"

#include <algorithm>
#include <functional>

#include "CDPL/Chem/AromaticRingSet.hpp"
#include "CDPL/Chem/MolecularGraph.hpp"
#include "CDPL/Chem/Bond.hpp"
#include "CDPL/Chem/MolecularGraphFunctions.hpp"
#include "CDPL/Chem/UtilityFunctions.hpp"


using namespace CDPL;


Chem::AromaticRingSet::AromaticRingSet(const MolecularGraph& molgraph)
{
    perceive(molgraph);
}

void Chem::AromaticRingSet::perceive(const MolecularGraph& molgraph)
{
    clear();

    if (molgraph.getNumAtoms() == 0 || molgraph.getNumBonds() == 0)
        return;

    init(molgraph);
    findAromaticRings();
}

void Chem::AromaticRingSet::init(const MolecularGraph& molgraph)
{
    molGraph = &molgraph;

    const FragmentList::BaseType& rings = *getRings(molgraph);

    FragmentList::BaseType::ConstElementIterator rings_end = rings.getElementsEnd();

    for (FragmentList::BaseType::ConstElementIterator it = rings.getElementsBegin(); it != rings_end; ++it) {
        const Fragment::SharedPointer& ring_ptr = *it;

        std::size_t num_ring_bonds = ring_ptr->getNumBonds();

        if (num_ring_bonds == 0 || num_ring_bonds != ring_ptr->getNumAtoms()) // sanity check
            continue;
    
        if (isNotAromatic(*ring_ptr, molgraph))
            continue;

        addElement(ring_ptr);
    }

    std::size_t num_bonds = molgraph.getNumBonds();

    if (!aromBondMask.empty())
        aromBondMask.clear();

    aromBondMask.resize(num_bonds);
}

void Chem::AromaticRingSet::findAromaticRings()
{
    BaseType::ElementIterator rings_end = getBase().getElementsEnd();
    BaseType::ElementIterator arom_rings_end = getBase().getElementsBegin();

    while (true) {
        BaseType::ElementIterator next_arom_rings_end =
            std::partition(arom_rings_end, rings_end, 
                           std::bind(&AromaticRingSet::isAromatic, this, std::placeholders::_1));

        if (next_arom_rings_end == arom_rings_end)
            break;

        arom_rings_end = next_arom_rings_end;
    }

    removeElements(arom_rings_end, rings_end);
}

bool Chem::AromaticRingSet::isAromatic(const Fragment::SharedPointer& ring_ptr)
{
    const Fragment& ring = *ring_ptr;

    if (!Chem::isAromatic(ring, *molGraph, aromBondMask))
        return false;

    std::for_each(ring.getBondsBegin(), ring.getBondsEnd(), 
                  std::bind(static_cast<Util::BitSet& (Util::BitSet::*)(Util::BitSet::size_type, bool)>(&Util::BitSet::set), std::ref(aromBondMask), 
                            std::bind(&BondContainer::getBondIndex, molGraph, std::placeholders::_1), true));

    return true;
}

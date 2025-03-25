/* 
 * MMFF94BondLengthTable.cpp
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

#include <functional>

#include "CDPL/ForceField/MolecularGraphFunctions.hpp"

#include "MMFF94BondLengthTable.hpp"


using namespace CDPL;


ConfGen::MMFF94BondLengthTable::MMFF94BondLengthTable()
{
    using namespace std::placeholders;
    
    atomTyper.setAromaticRingSetFunction(std::bind(&MMFF94BondLengthTable::getAromaticRings, this, _1));

    bondTyper.setAtomTypeFunction(std::bind(&MMFF94BondLengthTable::getNumericAtomType, this, _1));
    bondTyper.setAromaticRingSetFunction(std::bind(&MMFF94BondLengthTable::getAromaticRings, this, _1));

    bondStretchingParameterizer.setAtomTypeFunction(std::bind(&MMFF94BondLengthTable::getNumericAtomType, this, _1));
    bondStretchingParameterizer.setBondTypeIndexFunction(std::bind(&MMFF94BondLengthTable::getBondTypeIndex, this, _1));
    bondStretchingParameterizer.setAromaticRingSetFunction(std::bind(&MMFF94BondLengthTable::getAromaticRings, this, _1));
}

void ConfGen::MMFF94BondLengthTable::setup(const Chem::MolecularGraph& molgraph, bool strict_param)
{
    using namespace ForceField;

    molGraph = &molgraph;

    if (hasMMFF94AromaticRings(molgraph))
        usedAromRings = getMMFF94AromaticRings(molgraph);

    else {
        if (!aromRings)
            aromRings.reset(new MMFF94AromaticSSSRSubset());

        aromRings->extract(molgraph);
        usedAromRings = aromRings;
    }

    std::size_t num_atoms = molgraph.getNumAtoms();

    numAtomTypes.resize(num_atoms);
    symAtomTypes.resize(num_atoms);

    atomTyper.perceiveTypes(molgraph, symAtomTypes, numAtomTypes, strict_param);

    std::size_t num_bonds = molgraph.getNumBonds();

    bondTypeIndices.resize(num_bonds);
    bondTyper.perceiveTypes(molgraph, bondTypeIndices, strict_param);

    bondStretchingParameterizer.parameterize(molgraph, bondStretchingParams, strict_param);
}

double ConfGen::MMFF94BondLengthTable::get(std::size_t atom1_idx, std::size_t atom2_idx) const
{
    using namespace ForceField;

    for (MMFF94BondStretchingInteractionList::ConstElementIterator it = bondStretchingParams.getElementsBegin(), 
             end = bondStretchingParams.getElementsEnd(); it != end; ++it) { 

        const MMFF94BondStretchingInteraction& params = *it;

        if ((params.getAtom1Index() == atom1_idx && params.getAtom2Index() == atom2_idx) ||
            (params.getAtom1Index() == atom2_idx && params.getAtom2Index() == atom1_idx))
            return params.getReferenceLength();
    }

    return 0.0;
}

unsigned int ConfGen::MMFF94BondLengthTable::getBondTypeIndex(const Chem::Bond& bond) const
{
    return bondTypeIndices[molGraph->getBondIndex(bond)];
}

unsigned int ConfGen::MMFF94BondLengthTable::getNumericAtomType(const Chem::Atom& atom) const
{
    return numAtomTypes[molGraph->getAtomIndex(atom)];
}

const Chem::FragmentList::SharedPointer& 
ConfGen::MMFF94BondLengthTable::getAromaticRings(const Chem::MolecularGraph& molgraph) const
{
    return usedAromRings;
}

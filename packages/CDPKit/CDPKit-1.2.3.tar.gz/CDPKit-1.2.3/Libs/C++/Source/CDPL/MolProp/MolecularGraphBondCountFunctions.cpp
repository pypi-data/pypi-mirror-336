/* 
 * MolecularGraphBondCountFunctions.cpp 
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

#include "CDPL/MolProp/MolecularGraphFunctions.hpp"
#include "CDPL/MolProp/BondContainerFunctions.hpp"
#include "CDPL/MolProp/BondFunctions.hpp"
#include "CDPL/Chem/MolecularGraph.hpp"
#include "CDPL/Chem/Bond.hpp"


using namespace CDPL; 


std::size_t MolProp::getBondCount(const Chem::MolecularGraph& molgraph)
{
    return (molgraph.getNumBonds() + getImplicitHydrogenCount(molgraph));
}

std::size_t MolProp::getBondCount(const Chem::MolecularGraph& molgraph, std::size_t order, bool inc_aro)
{
    std::size_t count = getExplicitBondCount(molgraph, order, inc_aro);

    if (order == 1)
        count += getImplicitHydrogenCount(molgraph);

    return count;
}

std::size_t MolProp::getHydrogenBondCount(const Chem::MolecularGraph& molgraph)
{
    return (getExplicitHydrogenBondCount(molgraph) + getImplicitHydrogenCount(molgraph));
}

std::size_t MolProp::getChainBondCount(const Chem::MolecularGraph& molgraph)
{
    return (getExplicitChainBondCount(molgraph) + getImplicitHydrogenCount(molgraph));
}

std::size_t MolProp::getRotatableBondCount(const Chem::MolecularGraph& molgraph, bool h_rotors, bool ring_bonds, bool amide_bonds)
{
    std::size_t count = 0;

    for (Chem::MolecularGraph::ConstBondIterator it = molgraph.getBondsBegin(), end = molgraph.getBondsEnd(); it != end; ++it)
        if (isRotatable(*it, molgraph, h_rotors, ring_bonds, amide_bonds))
            count++;

    return count;
}

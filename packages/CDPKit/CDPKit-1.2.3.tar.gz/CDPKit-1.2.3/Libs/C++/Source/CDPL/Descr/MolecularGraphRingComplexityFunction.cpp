/* 
 * MolecularGraphRingComplexityFunction.cpp 
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

#include <numeric>
#include <functional>

#include "CDPL/Descr/MolecularGraphFunctions.hpp"
#include "CDPL/Chem/MolecularGraphFunctions.hpp"
#include "CDPL/MolProp/AtomContainerFunctions.hpp"


using namespace CDPL; 


double Descr::calcRingComplexity(const Chem::MolecularGraph& molgraph)
{
    using namespace Chem;
    using namespace std::placeholders;
    
    const FragmentList& sssr = *getSSSR(molgraph);

    std::size_t sum_ring_sizes = std::accumulate(sssr.getElementsBegin(), sssr.getElementsEnd(), std::size_t(0), 
                                                 std::bind(std::plus<std::size_t>(), _1, 
                                                           std::bind(&Fragment::getNumBonds, _2)));

    std::size_t num_ring_atoms = MolProp::getRingAtomCount(molgraph);
    double complexity = (num_ring_atoms == 0 ? 0.0 : double(sum_ring_sizes) / num_ring_atoms);

    return complexity;
}

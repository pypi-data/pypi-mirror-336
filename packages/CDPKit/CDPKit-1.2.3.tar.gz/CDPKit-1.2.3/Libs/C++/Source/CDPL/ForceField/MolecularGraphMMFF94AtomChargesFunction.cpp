/* 
 * MolecularGraphMMFF94AtomChargesFunction.cpp 
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

#include "CDPL/ForceField/MolecularGraphFunctions.hpp"
#include "CDPL/ForceField/AtomFunctions.hpp"
#include "CDPL/ForceField/MMFF94ChargeCalculator.hpp"
#include "CDPL/Chem/MolecularGraph.hpp"
#include "CDPL/Chem/Atom.hpp"
#include "CDPL/Util/Array.hpp"
#include "CDPL/Util/SequenceFunctions.hpp"


using namespace CDPL; 


void ForceField::calcMMFF94AtomCharges(Chem::MolecularGraph& molgraph, bool strict, bool overwrite)
{
    if (!overwrite && std::find_if(molgraph.getAtomsBegin(), molgraph.getAtomsEnd(),
                                   std::bind(std::equal_to<bool>(), false,
                                             std::bind(&hasMMFF94Charge, std::placeholders::_1))) == molgraph.getAtomsEnd())
        return;

    Util::DArray charges;
    MMFF94ChargeCalculator charge_calc(molgraph, charges, strict);

    Util::forEachPair(molgraph.getAtomsBegin(), molgraph.getAtomsEnd(), charges.getElementsBegin(), &setMMFF94Charge);
}

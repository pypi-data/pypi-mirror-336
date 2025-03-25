/* 
 * HBondDonorFeatureGenerator.cpp 
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

#include "CDPL/Pharm/HBondDonorFeatureGenerator.hpp"
#include "CDPL/Pharm/FeatureType.hpp"
#include "CDPL/Pharm/FeatureGeometry.hpp"
#include "CDPL/Chem/UtilityFunctions.hpp"


using namespace CDPL; 


Pharm::HBondDonorFeatureGenerator::HBondDonorFeatureGenerator(bool static_h_bonds)
{
    init(static_h_bonds);
}

Pharm::HBondDonorFeatureGenerator::HBondDonorFeatureGenerator(const Chem::MolecularGraph& molgraph, Pharmacophore& pharm, bool static_h_bonds) 
{
    init(static_h_bonds);
    generate(molgraph, pharm);
}

void Pharm::HBondDonorFeatureGenerator::init(bool static_h_bonds)
{
    using namespace Chem;

    addIncludePattern(parseSMARTS("[CX2:7][#1:8]"), FeatureType::H_BOND_DONOR, 1.5, FeatureGeometry::VECTOR, -1.0);

    if (!static_h_bonds) {
        addIncludePattern(parseSMARTS("[#7:11](~[*:4])(~[*:4])(~[*:4])[#1]"), FeatureType::H_BOND_DONOR, 1.5, FeatureGeometry::VECTOR, 2.5);
        addIncludePattern(parseSMARTS("[#7:11](~[*:4])(~[*:4])[#1]"), FeatureType::H_BOND_DONOR, 1.5, FeatureGeometry::VECTOR, 2.5);
        addIncludePattern(parseSMARTS("[*:4]-,=[#7,O,S:11][#1]"), FeatureType::H_BOND_DONOR, 1.5, FeatureGeometry::SPHERE);
        addIncludePattern(parseSMARTS("[#7,O,S:3][#1]"), FeatureType::H_BOND_DONOR, 1.5, FeatureGeometry::SPHERE);
    
    } else {
        addIncludePattern(parseSMARTS("[#7,O,S:7][#1:9]"), FeatureType::H_BOND_DONOR, 1.5, FeatureGeometry::VECTOR, 2.5);
    }

    addExcludePattern(parseSMARTS("[O:1]-[C,P,S]=O"));
    addExcludePattern(parseSMARTS("c1[n:1][n:1][n:1][n:1]1"));
    addExcludePattern(parseSMARTS("[N:1]-[SX4](=O)(=O)[CX4](F)(F)F"));
}

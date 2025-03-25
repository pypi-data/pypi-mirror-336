/* 
 * MoleculeAutoCorr2DDescriptorCalculator.cpp 
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

#include "CDPL/Descr/MoleculeAutoCorr2DDescriptorCalculator.hpp"
#include "CDPL/Chem/AtomType.hpp"
#include "CDPL/Chem/AtomFunctions.hpp"
#include "CDPL/Math/VectorProxy.hpp"


using namespace CDPL;


namespace
{

    struct AtomPairWeightFuncFS
    {

        double operator()(const Chem::Atom& atom1, const Chem::Atom& atom2, unsigned int slot_type1, unsigned int slot_type2) const {
            unsigned int atom_type1 = getType(atom1);
            unsigned int atom_type2 = getType(atom2);

            if ((atom_type1 == slot_type1 && atom_type2 == slot_type2) ||
                (atom_type2 == slot_type1 && atom_type1 == slot_type2))
                return 1;

            return 0;
        }
    };

    struct AtomPairWeightFuncSS
    {

        double operator()(const Chem::Atom& atom1, const Chem::Atom& atom2, unsigned int slot_type, unsigned int) const {
            unsigned int atom_type1 = getType(atom1);
            unsigned int atom_type2 = getType(atom2);
    
            if (atom_type1 == slot_type && atom_type2 == slot_type)
                return 2;

            if (atom_type1 == slot_type || atom_type2 == slot_type)
                return 1;

            return 0;
        }
    };

    unsigned int ATOM_TYPES[] = {
        Chem::AtomType::H,
        Chem::AtomType::C,
        Chem::AtomType::N,
        Chem::AtomType::O,
        Chem::AtomType::S,
        Chem::AtomType::P,
        Chem::AtomType::F,
        Chem::AtomType::Cl,
        Chem::AtomType::Br,
        Chem::AtomType::I
    };
}


CDPL::Descr::MoleculeAutoCorr2DDescriptorCalculator::MoleculeAutoCorr2DDescriptorCalculator(): 
    weightFunc(), mode(FULL_SPLIT)
{
    setMaxDistance(15);
} 

CDPL::Descr::MoleculeAutoCorr2DDescriptorCalculator::MoleculeAutoCorr2DDescriptorCalculator(const Chem::MolecularGraph& molgraph, Math::DVector& descr): 
    weightFunc(), mode(FULL_SPLIT)
{
    setMaxDistance(15);
    calculate(molgraph, descr);
}

void CDPL::Descr::MoleculeAutoCorr2DDescriptorCalculator::setMaxDistance(std::size_t max_dist)
{
    autoCorrCalculator.setMaxDistance(max_dist);
}

std::size_t CDPL::Descr::MoleculeAutoCorr2DDescriptorCalculator::getMaxDistance() const
{
    return autoCorrCalculator.getMaxDistance();
}

void CDPL::Descr::MoleculeAutoCorr2DDescriptorCalculator::setMode(Mode mode)
{
    this->mode = mode;
}

CDPL::Descr::MoleculeAutoCorr2DDescriptorCalculator::Mode CDPL::Descr::MoleculeAutoCorr2DDescriptorCalculator::getMode() const
{
    return mode;
}

void CDPL::Descr::MoleculeAutoCorr2DDescriptorCalculator::setAtomPairWeightFunction(const AtomPairWeightFunction& func)
{
    weightFunc = func;
}

void CDPL::Descr::MoleculeAutoCorr2DDescriptorCalculator::calculate(const Chem::MolecularGraph& molgraph, Math::DVector& descr)
{
    using namespace std::placeholders;
    
    std::size_t sub_descr_size = autoCorrCalculator.getMaxDistance() + 1;
    std::size_t num_atom_types = sizeof(ATOM_TYPES) / sizeof(unsigned int);
    Math::DVector sub_descr(sub_descr_size);

    if (mode == FULL_SPLIT) {
        descr.resize((sub_descr_size * (num_atom_types + 1) * num_atom_types) / 2, false);

        for (std::size_t i = 0, offs = 0; i < num_atom_types; i++) {
            for (std::size_t j = i; j < num_atom_types; j++, offs += sub_descr_size) {
                if (weightFunc)
                    autoCorrCalculator.setAtomPairWeightFunction(std::bind<double>(weightFunc, _1, _2, ATOM_TYPES[i], ATOM_TYPES[j]));
                else
                    autoCorrCalculator.setAtomPairWeightFunction(std::bind<double>(AtomPairWeightFuncFS(), _1, _2, ATOM_TYPES[i], ATOM_TYPES[j]));

                autoCorrCalculator.calculate(molgraph, sub_descr);
        
                Math::VectorRange<Math::DVector>(descr, Math::range(offs, offs + sub_descr_size)).assign(sub_descr);
            }
        }

        return;
    }

    descr.resize(sub_descr_size * num_atom_types, false);

    for (std::size_t i = 0, offs = 0; i < num_atom_types; i++, offs += sub_descr_size) {
        if (weightFunc)
            autoCorrCalculator.setAtomPairWeightFunction(std::bind<double>(weightFunc, _1, _2, ATOM_TYPES[i], ATOM_TYPES[i]));
        else
            autoCorrCalculator.setAtomPairWeightFunction(std::bind<double>(AtomPairWeightFuncSS(), _1, _2, ATOM_TYPES[i], ATOM_TYPES[i]));

        autoCorrCalculator.calculate(molgraph, sub_descr);

        Math::VectorRange<Math::DVector>(descr, Math::range(offs, offs + sub_descr_size)).assign(sub_descr);
    }
}

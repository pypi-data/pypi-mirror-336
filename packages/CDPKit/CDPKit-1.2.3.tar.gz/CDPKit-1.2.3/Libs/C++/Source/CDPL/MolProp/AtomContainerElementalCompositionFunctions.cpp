/* 
 * AtomContainerElementalCompositionFunctions.cpp 
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

#include <map>
#include <sstream>

#include "CDPL/MolProp/AtomContainerFunctions.hpp"
#include "CDPL/Chem/AtomFunctions.hpp"
#include "CDPL/Chem/AtomContainer.hpp"
#include "CDPL/Chem/Atom.hpp"
#include "CDPL/Chem/AtomType.hpp"
#include "CDPL/Chem/AtomDictionary.hpp"


using namespace CDPL; 


void MolProp::generateExplicitMolecularFormula(const Chem::AtomContainer& cntnr, std::string& formula)
{
    using namespace Chem;

    typedef std::map<std::string, std::size_t> ElemCountMap;

    ElemCountMap elem_counts;
    std::size_t unknown_count = 0;

    for (AtomContainer::ConstAtomIterator it = cntnr.getAtomsBegin(), atoms_end = cntnr.getAtomsEnd(); it != atoms_end; ++it) {
        unsigned int atom_type = getType(*it);

        if (atom_type == AtomType::UNKNOWN || atom_type > AtomType::MAX_ATOMIC_NO)
            unknown_count++;
        else
            elem_counts[AtomDictionary::getSymbol(atom_type)]++;
    }

    std::ostringstream formula_os;

    ElemCountMap::iterator it = elem_counts.find("C");

    if (it != elem_counts.end()) {
        formula_os << 'C';

        if (it->second > 1)
            formula_os << it->second;

        elem_counts.erase(it);

        it = elem_counts.find("H");

        if (it != elem_counts.end()) {
            formula_os << 'H';
            
            if (it->second > 1)
                formula_os << it->second;

            elem_counts.erase(it);
        }
    }

    for (ElemCountMap::const_iterator it = elem_counts.begin(), end = elem_counts.end(); it != end; ++it) {
        formula_os << it->first;

        if (it->second > 1)
            formula_os << std::to_string(it->second);
    }

    if (unknown_count > 0)
        formula_os << '?';
    if (unknown_count > 1)
        formula_os << std::to_string(unknown_count);
    
    formula = formula_os.str();
}

void MolProp::generateExplicitElementHistogram(const Chem::AtomContainer& cntnr, ElementHistogram& hist, bool append)
{
    using namespace Chem;
    
    if (!append)
        hist.clear();

    for (AtomContainer::ConstAtomIterator it = cntnr.getAtomsBegin(), atoms_end = cntnr.getAtomsEnd(); it != atoms_end; ++it) {
        unsigned int atom_type = getType(*it);

        if (atom_type > AtomType::MAX_ATOMIC_NO)
            atom_type = AtomType::UNKNOWN;

        hist[atom_type]++;
    }
}

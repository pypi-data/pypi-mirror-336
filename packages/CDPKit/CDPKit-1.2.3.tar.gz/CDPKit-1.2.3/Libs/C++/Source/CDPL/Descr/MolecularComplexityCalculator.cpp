/* 
 * MolecularComplexityCalculator.cpp 
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
#include <numeric>
#include <cmath>

#include "CDPL/Descr/MolecularComplexityCalculator.hpp"
#include "CDPL/Chem/Atom.hpp"
#include "CDPL/Chem/Bond.hpp"
#include "CDPL/Chem/AtomFunctions.hpp"
#include "CDPL/Chem/BondFunctions.hpp"
#include "CDPL/Chem/AtomPropertyFlag.hpp"
#include "CDPL/MolProp/AtomFunctions.hpp"


using namespace CDPL;


Descr::MolecularComplexityCalculator::MolecularComplexityCalculator(const Chem::MolecularGraph& molgraph) 
{
    calculate(molgraph);
}

double Descr::MolecularComplexityCalculator::calculate(const Chem::MolecularGraph& molgraph)
{
    using namespace std::placeholders;
    
    molGraph = &molgraph;

    numHeavyAtoms = 0;
    numDoubleBonds = 0;
    numTripleBonds = 0;
    etaTotal = 0;

    symmetryTerms.clear();
    atomTypeCounts.clear();
    piBondTerms.clear();

    std::for_each(molgraph.getAtomsBegin(), molgraph.getAtomsEnd(),
                  std::bind(&MolecularComplexityCalculator::processAtom, this, _1));

    std::for_each(molgraph.getBondsBegin(), molgraph.getBondsEnd(),
                  std::bind(&MolecularComplexityCalculator::processBond, this, _1));

    calcAtomTypeComplexity();
    calcStructuralComplexity();

    complexity = atmTypeComplexity + structComplexity;

    return complexity;
}

double Descr::MolecularComplexityCalculator::getResult() const
{
    return complexity;
}

void Descr::MolecularComplexityCalculator::processAtom(const Chem::Atom& atom)
{
    using namespace Chem;
    
    if (MolProp::isOrdinaryHydrogen(atom, *molGraph, 
                                    AtomPropertyFlag::ISOTOPE | AtomPropertyFlag::FORMAL_CHARGE | AtomPropertyFlag::H_COUNT))
        return;

    unsigned int atom_type = getType(atom);

    atomTypeCounts[atom_type]++;
    numHeavyAtoms++;

    std::size_t sym_class_id = getSymmetryClass(atom);

    SymmetryTermMap::iterator lb = symmetryTerms.lower_bound(sym_class_id);

    if (lb != symmetryTerms.end() && !symmetryTerms.key_comp()(sym_class_id, lb->first)) 
        lb->second.incNumEquivAtoms();
    else 
        lb = symmetryTerms.insert(lb, SymmetryTermMap::value_type(sym_class_id, SymmetryTerm(*molGraph, atom)));

    etaTotal += lb->second.getEtaContribution();
}

void Descr::MolecularComplexityCalculator::processBond(const Chem::Bond& bond)
{
    if (!molGraph->containsAtom(bond.getBegin()) || !molGraph->containsAtom(bond.getEnd()))
        return;

    std::size_t order = getOrder(bond);

    if (order == 2)
        numDoubleBonds++;

    else if (order == 3)
        numTripleBonds++;

    else
        return;

    PiBondTerm pi_term(getSymmetryClass(bond.getBegin()), 
                       getSymmetryClass(bond.getEnd()), order);

    if (!pi_term.isRelevant(symmetryTerms))
        return;

    piBondTerms.insert(pi_term);
}

void Descr::MolecularComplexityCalculator::calcAtomTypeComplexity()
{
    atmTypeComplexity = numHeavyAtoms * std::log(double(numHeavyAtoms)) * M_LOG2E;

    AtomTypeCountMap::const_iterator type_counts_end = atomTypeCounts.end();

    for (AtomTypeCountMap::const_iterator it = atomTypeCounts.begin(); it != type_counts_end; ++it) {
        double count = it->second;

        atmTypeComplexity -= count * std::log(count) * M_LOG2E;
    }
}

void Descr::MolecularComplexityCalculator::calcStructuralComplexity()
{
    using namespace std::placeholders;
    
    etaTotal -= numDoubleBonds + 3 * numTripleBonds;

    structComplexity = 2.0 * etaTotal * std::log(etaTotal) * M_LOG2E;

    structComplexity = std::accumulate(symmetryTerms.begin(), symmetryTerms.end(), structComplexity, 
                                       std::bind(std::minus<double>(), _1,
                                                 std::bind(&SymmetryTerm::getValue,
                                                           std::bind(&SymmetryTermMap::value_type::second, _2))));

    structComplexity = std::accumulate(piBondTerms.begin(), piBondTerms.end(), structComplexity, 
                                       std::bind(std::plus<double>(), _1,
                                                 std::bind(&PiBondTerm::getCorrection, _2, std::ref(symmetryTerms))));
}


Descr::MolecularComplexityCalculator::SymmetryTerm::SymmetryTerm(const Chem::MolecularGraph& molgraph, const Chem::Atom& atom): 
    numEquivAtoms(1)
{
    using namespace Chem;
    
    typedef std::map<std::size_t, std::size_t> NbrSymClassIDCounts;

    NbrSymClassIDCounts nbr_class_ids;

    std::size_t hvy_valence = 0;
    std::size_t num_hvy_nbrs = 0;

    Atom::ConstAtomIterator nbrs_end = atom.getAtomsEnd();
    Atom::ConstBondIterator b_it = atom.getBondsBegin();

    for (Atom::ConstAtomIterator a_it = atom.getAtomsBegin(); a_it != nbrs_end; ++a_it, ++b_it) {
        if (!molgraph.containsBond(*b_it))
            continue;

        const Atom& nbr_atom = *a_it;

        if (!molgraph.containsAtom(nbr_atom))
            continue;

        if (MolProp::isOrdinaryHydrogen(nbr_atom, molgraph, 
                                        AtomPropertyFlag::ISOTOPE | AtomPropertyFlag::FORMAL_CHARGE | AtomPropertyFlag::H_COUNT))
            continue;

        std::size_t order = std::max(getOrder(*b_it), std::size_t(1));

        nbr_class_ids[getSymmetryClass(nbr_atom)] += order;
        hvy_valence += order;
        num_hvy_nbrs++;
    }

    hCount = (hvy_valence > 4 ? 0 : 4 - hvy_valence); 

    std::size_t r = 0;

    NbrSymClassIDCounts::const_iterator nbr_class_ids_end = nbr_class_ids.end();

    for (NbrSymClassIDCounts::const_iterator it = nbr_class_ids.begin(); it != nbr_class_ids_end; ++it)
        r += (it->second > 2 ? it->second : it->second - 1);

    if (num_hvy_nbrs == 1)
        id = 0;

    else if (num_hvy_nbrs == 2 && hvy_valence == 2)
        id = 1;

    else if (num_hvy_nbrs == 2 && hvy_valence == 4 && nbr_class_ids.size() == 1)
        id = 11;

    else 
        id = (3 - hCount) * (2 - hCount) + r;
}

void Descr::MolecularComplexityCalculator::SymmetryTerm::incNumEquivAtoms()
{
    numEquivAtoms++;
}

double Descr::MolecularComplexityCalculator::SymmetryTerm::getValue() const
{
    switch (id) {

        case 1:
            return (numEquivAtoms * std::log(numEquivAtoms) * M_LOG2E);

        case 2:
            return (3.0 * numEquivAtoms * std::log(numEquivAtoms) * M_LOG2E);

        case 3:
            return ((2.0 * numEquivAtoms * std::log(2.0 * numEquivAtoms) 
                     + numEquivAtoms * std::log(numEquivAtoms)) * M_LOG2E);
        case 5:
            return (3.0 * numEquivAtoms * std::log(3.0 * numEquivAtoms) * M_LOG2E);

        case 6:
            return (6.0 * numEquivAtoms * std::log(numEquivAtoms) * M_LOG2E);

        case 7:
            return ((4.0 * numEquivAtoms * std::log(2.0 * numEquivAtoms) 
                     + 2.0 * numEquivAtoms * std::log(numEquivAtoms)) * M_LOG2E);
        case 8:
            return ((4.0 * numEquivAtoms * std::log(4.0 * numEquivAtoms) 
                     + 2.0 * numEquivAtoms * std::log(numEquivAtoms)) * M_LOG2E);
        case 9:
            return (6.0 * numEquivAtoms * std::log(3.0 * numEquivAtoms) * M_LOG2E);

        case 10:
            return (6.0 * numEquivAtoms * std::log(6.0 * numEquivAtoms) * M_LOG2E);

        case 11:
            return ((4.0 * numEquivAtoms * std::log(4.0 * numEquivAtoms) 
                     + 2.0 * numEquivAtoms * std::log(2.0 * numEquivAtoms)) * M_LOG2E);
        default:
            return 0.0;
    }
}

double Descr::MolecularComplexityCalculator::SymmetryTerm::getEtaContribution() const
{
    return (0.5 * (4 - hCount) * (3 - hCount));
}

double Descr::MolecularComplexityCalculator::SymmetryTerm::getNumEquivAtoms() const
{
    return numEquivAtoms;
}

std::size_t Descr::MolecularComplexityCalculator::SymmetryTerm::getID() const
{
    return id;
}


Descr::MolecularComplexityCalculator::PiBondTerm::PiBondTerm(std::size_t class_id1, std::size_t class_id2, std::size_t order):
    symClassID1(std::min(class_id1, class_id2)), symClassID2(std::max(class_id1, class_id2)), order(order)
{}

double Descr::MolecularComplexityCalculator::PiBondTerm::getCorrection(const SymmetryTermMap& sym_terms) const
{
    const SymmetryTerm& sym_term1 = sym_terms.find(symClassID1)->second;

    if (symClassID1 == symClassID2) {
        if (order == 2)
            return ((sym_term1.getNumEquivAtoms() * std::log(sym_term1.getNumEquivAtoms())
                     - 0.5 * sym_term1.getNumEquivAtoms() * std::log(0.5 * sym_term1.getNumEquivAtoms())) * M_LOG2E);

        return ((3.0 * sym_term1.getNumEquivAtoms() * std::log(3.0 * sym_term1.getNumEquivAtoms())
                 - 1.5 * sym_term1.getNumEquivAtoms() * std::log(1.5 * sym_term1.getNumEquivAtoms())) * M_LOG2E);
    }

    const SymmetryTerm& sym_term2 = sym_terms.find(symClassID2)->second;

    if (order == 2) {
        if (sym_term1.getID() != 11 && sym_term2.getID() != 11)
            return ((0.5 * sym_term1.getNumEquivAtoms() * std::log(sym_term1.getNumEquivAtoms())
                     + 0.5 * sym_term2.getNumEquivAtoms() * std::log(sym_term2.getNumEquivAtoms())) * M_LOG2E);

        if (sym_term1.getID() == 11)
            return ((sym_term1.getNumEquivAtoms() * std::log(2.0 * sym_term1.getNumEquivAtoms())
                     + 0.5 * sym_term2.getNumEquivAtoms() * std::log(sym_term2.getNumEquivAtoms())) * M_LOG2E);

        return ((0.5 * sym_term1.getNumEquivAtoms() * std::log(sym_term1.getNumEquivAtoms())
                 + sym_term2.getNumEquivAtoms() * std::log(2.0 * sym_term2.getNumEquivAtoms())) * M_LOG2E);
    }

    return ((1.5 * sym_term1.getNumEquivAtoms() * std::log(3.0 * sym_term1.getNumEquivAtoms())
             + 1.5 * sym_term2.getNumEquivAtoms() * std::log(3.0 * sym_term2.getNumEquivAtoms())) * M_LOG2E);
}

bool Descr::MolecularComplexityCalculator::PiBondTerm::isRelevant(const SymmetryTermMap& sym_terms) const
{
    if (symClassID1 == symClassID2)
        return true;

    SymmetryTermMap::const_iterator it = sym_terms.find(symClassID1);

    if (it == sym_terms.end() || it->second.getID() == 0)
        return false;
    
    it = sym_terms.find(symClassID2);

    if (it == sym_terms.end() || it->second.getID() == 0)
        return false;

    return true;
}

bool Descr::MolecularComplexityCalculator::PiBondTerm::operator<(const PiBondTerm& term) const
{
    if (symClassID1 == term.symClassID1) {
        if (symClassID2 == term.symClassID2)
            return (order < term.order);

        return (symClassID2 < term.symClassID2);
    }

    return (symClassID1 < term.symClassID1);
}

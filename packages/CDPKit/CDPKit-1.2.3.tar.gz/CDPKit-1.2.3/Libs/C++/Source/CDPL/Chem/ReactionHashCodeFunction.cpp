/* 
 * ReactionHashCodeFunction.cpp 
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

#include <vector>
#include <algorithm>

#include "CDPL/Chem/ReactionFunctions.hpp"
#include "CDPL/Chem/MolecularGraphFunctions.hpp"
#include "CDPL/Chem/FragmentFunctions.hpp"
#include "CDPL/Chem/Reaction.hpp"
#include "CDPL/Chem/HashCodeCalculator.hpp"
#include "CDPL/Internal/SHA1.hpp"


using namespace CDPL; 


std::uint64_t Chem::calcHashCode(const Reaction& rxn, unsigned int role_mask, 
                                 unsigned int atom_flags, unsigned int bond_flags, 
                                 bool ord_h_deplete)
{
    HashCodeCalculator hash_calc;

    if (atom_flags == AtomPropertyFlag::DEFAULT)
        atom_flags = HashCodeCalculator::DEF_ATOM_PROPERTY_FLAGS;

    if (bond_flags == BondPropertyFlag::DEFAULT)
        bond_flags = HashCodeCalculator::DEF_BOND_PROPERTY_FLAGS;

    hash_calc.setAtomHashSeedFunction(HashCodeCalculator::DefAtomHashSeedFunctor(hash_calc, atom_flags));
    hash_calc.setBondHashSeedFunction(HashCodeCalculator::DefBondHashSeedFunctor(bond_flags));

    Fragment tmp_frag;
    std::vector<std::uint64_t> comp_hashes;
    std::size_t hash_offs = 0;

    unsigned int roles[3] = { ReactionRole::REACTANT, ReactionRole::AGENT, ReactionRole::PRODUCT };

    for (std::size_t i = 0; i < 3; i++) {
        unsigned int role = roles[i];

        if ((role & role_mask) == 0)
            continue;

        Reaction::ConstComponentIterator comps_end = rxn.getComponentsEnd(role);

        for (Reaction::ConstComponentIterator c_it = rxn.getComponentsBegin(role); c_it != comps_end; ++c_it) {
            const Molecule& mol = *c_it;
            const FragmentList& mol_comps = *getComponents(mol);

            FragmentList::ConstElementIterator mol_comps_end = mol_comps.getElementsEnd(); 

            for (FragmentList::ConstElementIterator mc_it = mol_comps.getElementsBegin(); mc_it != mol_comps_end; ++mc_it) {
                const Fragment& mol_comp = *mc_it;

                if (ord_h_deplete) {
                    tmp_frag = mol_comp;

                    makeOrdinaryHydrogenDeplete(tmp_frag, AtomPropertyFlag::ISOTOPE | AtomPropertyFlag::H_COUNT |
                                                AtomPropertyFlag::FORMAL_CHARGE);

                    comp_hashes.push_back(hash_calc.calculate(tmp_frag));

                } else
                    comp_hashes.push_back(hash_calc.calculate(mol_comp));
            } 
        }

        std::sort(comp_hashes.begin() + hash_offs, comp_hashes.end());

        comp_hashes.push_back(0);
        
        hash_offs = comp_hashes.size();
    }

    Internal::SHA1 sha;

    sha.input(comp_hashes.begin(), comp_hashes.end());

    unsigned char sha_hash[Internal::SHA1::HASH_SIZE];

    sha.getResult(sha_hash);

    return (std::uint64_t(sha_hash[0]) | (std::uint64_t(sha_hash[1]) << 8)
            | (std::uint64_t(sha_hash[2]) << 16) | (std::uint64_t(sha_hash[3]) << 24)
            | (std::uint64_t(sha_hash[4]) << 32) | (std::uint64_t(sha_hash[5]) << 40)
            | (std::uint64_t(sha_hash[6]) << 48) | (std::uint64_t(sha_hash[7]) << 56));
}

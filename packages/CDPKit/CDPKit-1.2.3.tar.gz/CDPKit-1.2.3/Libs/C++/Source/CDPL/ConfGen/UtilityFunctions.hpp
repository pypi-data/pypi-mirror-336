/* 
 * UtilityFunctions.hpp 
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

/**
 * \file
 * \brief Declaration of internal utility functions.
 */

#ifndef CDPL_CONFGEN_UTILITYFUNCTIONS_HPP
#define CDPL_CONFGEN_UTILITYFUNCTIONS_HPP

#include <string>
#include <cstddef>

#include "CDPL/ForceField/ElasticPotentialList.hpp"


namespace CDPL
{

    namespace Chem
    {

        class MolecularGraph;
        class BondContainer;
        class AtomContainer;
        class FragmentList;
    } // namespace Chem

    namespace ConfGen
    {

        std::string fragmentTypeToString(unsigned int frag_type, bool human);

        std::string returnCodeToString(unsigned int ret_code);

        std::string getSMILES(Chem::MolecularGraph& molgraph);

        std::string getSMILES(const Chem::MolecularGraph& molgraph);

        bool isFixed(const Chem::Bond& bond, const Chem::MolecularGraph* fixed_substr);
        
        std::size_t getNonAromaticSingleBondCount(const Chem::BondContainer& cntnr, const Chem::MolecularGraph* fixed_substr);

        std::size_t getMaxNonAromaticSingleBondCount(const Chem::FragmentList& frags, const Chem::MolecularGraph* fixed_substr);

        double normalizeAngle(double angle);

        double getAbsoluteAngleDistance(double angle1, double angle2);

        void generatePairwiseElasticPotentials(const Chem::AtomContainer& atoms, const Chem::MolecularGraph& molgraph,
                                               const Math::Vector3DArray& coords, ForceField::ElasticPotentialList& potentials,
                                               double k);
        
        template <typename InteractionList>
        void extractFragmentMMFF94InteractionParams2(const InteractionList& src_ia_list, InteractionList& tgt_ia_list,
                                                     const Util::BitSet& tgt_atom_mask)
        {
            for (typename InteractionList::ConstElementIterator it = src_ia_list.getElementsBegin(), end = src_ia_list.getElementsEnd(); it != end; ++it) {
                const typename InteractionList::ElementType& params = *it;

                if (tgt_atom_mask.test(params.getAtom1Index()) &&
                    tgt_atom_mask.test(params.getAtom2Index())) {

                    tgt_ia_list.addElement(params);
                }
            }
        }

        template <typename InteractionList>
        void extractFragmentMMFF94InteractionParams2(const InteractionList& src_ia_list, InteractionList& tgt_ia_list,
                                                     Util::BitSet& free_ia_mask, const Util::BitSet& tgt_atom_mask)
        {
            for (Util::BitSet::size_type i = free_ia_mask.find_first(); i != Util::BitSet::npos; i = free_ia_mask.find_next(i)) {
                const typename InteractionList::ElementType& params = src_ia_list[i];

                if (tgt_atom_mask.test(params.getAtom1Index()) &&
                    tgt_atom_mask.test(params.getAtom2Index())) {

                    tgt_ia_list.addElement(params);
                    free_ia_mask.reset(i);
                }
            }
        }

        template <typename InteractionList>
        void extractFragmentMMFF94InteractionParams3(const InteractionList& src_ia_list, InteractionList& tgt_ia_list,
                                                     const Util::BitSet& tgt_atom_mask)
        {
            for (typename InteractionList::ConstElementIterator it = src_ia_list.getElementsBegin(), end = src_ia_list.getElementsEnd(); it != end; ++it) {
                const typename InteractionList::ElementType& params = *it;

                if (tgt_atom_mask.test(params.getAtom1Index()) &&
                    tgt_atom_mask.test(params.getAtom2Index()) &&
                    tgt_atom_mask.test(params.getAtom3Index())) {

                    tgt_ia_list.addElement(params);
                }
            }
        }

        template <typename InteractionList>
        void extractFragmentMMFF94InteractionParams3(const InteractionList& src_ia_list, InteractionList& tgt_ia_list,
                                                     Util::BitSet& free_ia_mask, const Util::BitSet& tgt_atom_mask)
        {
            for (Util::BitSet::size_type i = free_ia_mask.find_first(); i != Util::BitSet::npos; i = free_ia_mask.find_next(i)) {
                const typename InteractionList::ElementType& params = src_ia_list[i];

                if (tgt_atom_mask.test(params.getAtom1Index()) &&
                    tgt_atom_mask.test(params.getAtom2Index()) &&
                    tgt_atom_mask.test(params.getAtom3Index())) {

                    tgt_ia_list.addElement(params);
                    free_ia_mask.reset(i);
                }
            }
        }

        template <typename InteractionList>
        void extractFragmentMMFF94InteractionParams4(const InteractionList& src_ia_list, InteractionList& tgt_ia_list,
                                                     const Util::BitSet& tgt_atom_mask)
        {
            for (typename InteractionList::ConstElementIterator it = src_ia_list.getElementsBegin(), end = src_ia_list.getElementsEnd(); it != end; ++it) {
                const typename InteractionList::ElementType& params = *it;

                if (tgt_atom_mask.test(params.getAtom1Index()) &&
                    tgt_atom_mask.test(params.getAtom2Index()) &&
                    tgt_atom_mask.test(params.getAtom3Index()) &&
                    tgt_atom_mask.test(params.getAtom4Index())) {

                    tgt_ia_list.addElement(params);
                }
            }
        }

        template <typename InteractionList>
        void extractFragmentMMFF94InteractionParams4(const InteractionList& src_ia_list, InteractionList& tgt_ia_list,
                                                     Util::BitSet& free_ia_mask, const Util::BitSet& tgt_atom_mask)
        {
            for (Util::BitSet::size_type i = free_ia_mask.find_first(); i != Util::BitSet::npos; i = free_ia_mask.find_next(i)) {
                const typename InteractionList::ElementType& params = src_ia_list[i];

                if (tgt_atom_mask.test(params.getAtom1Index()) &&
                    tgt_atom_mask.test(params.getAtom2Index()) &&
                    tgt_atom_mask.test(params.getAtom3Index()) &&
                    tgt_atom_mask.test(params.getAtom4Index())) {

                    tgt_ia_list.addElement(params);
                    free_ia_mask.reset(i);
                }
            }
        }
    } // namespace ConfGen
} // namespace CDPL

#endif // CDPL_CONFGEN_UTILITYFUNCTIONS_HPP

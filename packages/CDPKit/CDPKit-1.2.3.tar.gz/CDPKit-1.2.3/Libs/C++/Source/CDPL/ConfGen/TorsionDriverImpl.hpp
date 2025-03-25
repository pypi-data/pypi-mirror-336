/* 
 * TorsionDriverImpl.hpp 
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
 * \brief Definition of the class CDPL::ConfGen::TorsionDriverImpl.
 */

#ifndef CDPL_CONFGEN_TORSIONDRIVERIMPL_HPP
#define CDPL_CONFGEN_TORSIONDRIVERIMPL_HPP

#include <memory>
#include <vector>
#include <cstddef>

#include "CDPL/ConfGen/TorsionDriverSettings.hpp"
#include "CDPL/ConfGen/TorsionLibrary.hpp"
#include "CDPL/ConfGen/TorsionRuleMatcher.hpp"
#include "CDPL/ConfGen/ConformerDataArray.hpp"
#include "CDPL/ConfGen/LogMessageCallbackFunction.hpp"
#include "CDPL/Chem/SubstructureSearch.hpp"
#include "CDPL/Chem/FragmentList.hpp"
#include "CDPL/Util/BitSet.hpp"

#include "FragmentTree.hpp"
#include "FragmentTreeNode.hpp"
#include "ForceFieldInteractionMask.hpp"


namespace CDPL
{

    namespace ForceField
    {

        class MMFF94InteractionData;
        class MMFF94InteractionParameterizer;
    } // namespace ForceField

    namespace ConfGen
    {

        class TorsionDriverImpl
        {

          public:
            typedef ConformerDataArray::const_iterator ConstConformerIterator;

            TorsionDriverImpl();

            ~TorsionDriverImpl();

            TorsionDriverSettings& getSettings();

            void clearTorsionLibraries();

            void addTorsionLibrary(const TorsionLibrary::SharedPointer& lib);

            void setup(const Chem::MolecularGraph& molgraph);
            void setup(const Chem::MolecularGraph& molgraph, const Util::BitSet& bond_mask);

            template <typename BondIter>
            void setup(const Chem::FragmentList& frags, const Chem::MolecularGraph& molgraph,
                       const BondIter& bonds_beg, const BondIter& bonds_end);

            void setMMFF94Parameters(const ForceField::MMFF94InteractionData& ia_data, ForceFieldInteractionMask& ia_mask);
            void setMMFF94Parameters(const ForceField::MMFF94InteractionData& ia_data);
            bool setMMFF94Parameters();

            void clearInputCoordinates();
            void clearInputCoordinates(std::size_t frag_idx);

            void addInputCoordinates(const Math::Vector3DArray& coords);
            void addInputCoordinates(const Math::Vector3DArray& coords, std::size_t frag_idx);
            void addInputCoordinates(const ConformerData& conf_data, std::size_t frag_idx);
            void addInputCoordinates(const ConformerData::SharedPointer& conf_data, std::size_t frag_idx);

            void setInputCoordinates(const Math::Vector3DArray& coords);
            void setInputCoordinates(const Math::Vector3DArray& coords, std::size_t frag_idx);
            void setInputCoordinates(const ConformerData& conf_data, std::size_t frag_idx);
            void setInputCoordinates(const ConformerData::SharedPointer& conf_data, std::size_t frag_idx);

            std::size_t getNumFragments() const;

            const Chem::Fragment& getFragment(std::size_t idx) const;

            FragmentTreeNode& getFragmentNode(std::size_t idx) const;

            void setAbortCallback(const CallbackFunction& func);

            const CallbackFunction& getAbortCallback() const;

            void setTimeoutCallback(const CallbackFunction& func);

            const CallbackFunction& getTimeoutCallback() const;

            void setLogMessageCallback(const LogMessageCallbackFunction& func);

            const LogMessageCallbackFunction& getLogMessageCallback() const;

            unsigned int generateConformers();

            std::size_t getNumConformers() const;

            ConformerData& getConformer(std::size_t idx);

            ConstConformerIterator getConformersBegin() const;
            ConstConformerIterator getConformersEnd() const;

          private:
            TorsionDriverImpl(const TorsionDriverImpl&);

            TorsionDriverImpl& operator=(const TorsionDriverImpl&);

            template <typename ConfData>
            void doAddInputCoordinates(const ConfData& conf_data, std::size_t frag_idx) const;

            void assignTorsionAngles(FragmentTreeNode* node);

            const ConfGen::TorsionRuleMatch* getTorsionRuleAngles(const Chem::Bond& bond, FragmentTreeNode* node, std::size_t rot_sym);

            void addOffsetAngles(double angle, double offs);
            double getAngleOffset(const Chem::Atom& atom) const;
            
            std::size_t getRotationalSymmetry(const Chem::Bond& bond);

            const Chem::Atom* getFirstNeighborAtom(const Chem::Atom* ctr_atom, const Chem::Atom* excl_atom,
                                                   const FragmentTreeNode* node) const;

            typedef std::unique_ptr<ForceField::MMFF94InteractionParameterizer> MMFF94ParameterizerPtr;
            typedef std::unique_ptr<ForceField::MMFF94InteractionData>          MMFF94InteractionDataPtr;
            typedef std::vector<const Chem::Bond*>                              BondList;
            typedef std::vector<TorsionLibrary::SharedPointer>                  TorsionLibraryList;
            typedef ConfGen::FragmentTreeNode::DoubleArray                      AngleList;

            TorsionDriverSettings      settings;
            TorsionLibraryList         torLibs;
            FragmentTree               fragTree;
            TorsionRuleMatcher         torRuleMatcher;
            Chem::SubstructureSearch   subSearch;
            Chem::FragmentList         fragments;
            MMFF94ParameterizerPtr     mmff94Parameterizer;
            MMFF94InteractionDataPtr   mmff94Data;
            Util::BitSet               rotBondMask;
            BondList                   rotBonds;
            ForceFieldInteractionMask  mmff94InteractionMask;
            LogMessageCallbackFunction logCallback;
            AngleList                  workingAngles;
        };
    } // namespace ConfGen
} // namespace CDPL


// Implementation

template <typename BondIter>
void CDPL::ConfGen::TorsionDriverImpl::setup(const Chem::FragmentList& frags, const Chem::MolecularGraph& molgraph,
                                             const BondIter& bonds_beg, const BondIter& bonds_end)
{
    fragTree.build(frags, molgraph, bonds_beg, bonds_end);

    assignTorsionAngles(fragTree.getRoot());
}

#endif // CDPL_CONFGEN_TORSIONDRIVERIMPL_HPP

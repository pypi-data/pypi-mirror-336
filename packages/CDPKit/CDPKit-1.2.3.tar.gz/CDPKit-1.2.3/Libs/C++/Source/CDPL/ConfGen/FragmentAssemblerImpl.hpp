/* 
 * FragmentAssemblerImpl.hpp 
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
 * \brief Definition of the class CDPL::ConfGen::FragmentAssemblerImpl.
 */

#ifndef CDPL_CONFGEN_FRAGMENTASSEMBLERIMPL_HPP
#define CDPL_CONFGEN_FRAGMENTASSEMBLERIMPL_HPP

#include <memory>
#include <utility>
#include <vector>
#include <cstddef>
#include <functional>

#include "CDPL/ConfGen/FragmentAssemblerSettings.hpp"
#include "CDPL/ConfGen/TorsionRuleMatcher.hpp"
#include "CDPL/ConfGen/CanonicalFragment.hpp"
#include "CDPL/ConfGen/FragmentLibrary.hpp"
#include "CDPL/ConfGen/ConformerDataArray.hpp"
#include "CDPL/Chem/FragmentList.hpp"
#include "CDPL/Util/ObjectPool.hpp"
#include "CDPL/Util/BitSet.hpp"

#include "FragmentTree.hpp"
#include "FragmentConformerGeneratorImpl.hpp"
#include "MMFF94BondLengthTable.hpp"


namespace CDPL
{

    namespace ConfGen
    {

        class FragmentAssemblerImpl
        {

            typedef ForceField::MMFF94InteractionData MMFF94InteractionData;

          public:
            typedef ConformerDataArray::const_iterator ConstConformerIterator;

            typedef std::function<double(std::size_t, std::size_t)> BondLengthFunction;

            FragmentAssemblerImpl();

            ~FragmentAssemblerImpl();

            FragmentAssemblerSettings& getSettings();

            void clearFragmentLibraries();

            void addFragmentLibrary(const FragmentLibrary::SharedPointer& lib);

            void setAbortCallback(const CallbackFunction& func);

            const CallbackFunction& getAbortCallback() const;

            void setTimeoutCallback(const CallbackFunction& func);

            const CallbackFunction& getTimeoutCallback() const;

            void setLogMessageCallback(const LogMessageCallbackFunction& func);

            const LogMessageCallbackFunction& getLogMessageCallback() const;

            void setBondLengthFunction(const BondLengthFunction& func);

            const BondLengthFunction& getBondLengthFunction() const;

            unsigned int assemble(const Chem::MolecularGraph& molgraph,
                                  const Chem::MolecularGraph& parent_molgraph,
                                  const Chem::MolecularGraph* fixed_substr,
                                  const Math::Vector3DArray* fixed_substr_coords);

            std::size_t getNumConformers() const;

            ConformerData& getConformer(std::size_t idx);

            ConstConformerIterator getConformersBegin() const;
            ConstConformerIterator getConformersEnd() const;

            const Util::BitSet& getInvertibleNitrogenMask() const;

          private:
            FragmentAssemblerImpl(const FragmentAssemblerImpl&);

            FragmentAssemblerImpl& operator=(const FragmentAssemblerImpl&);

            void init(const Chem::MolecularGraph& parent_molgraph);

            bool processFixedSubstruct(const Chem::MolecularGraph& molgraph,
                                       const Chem::MolecularGraph& parent_molgraph,
                                       const Chem::MolecularGraph* fixed_substr,
                                       const Math::Vector3DArray* fixed_substr_coords);

            std::size_t getNumFixedSubstructBonds(const Chem::MolecularGraph& frag) const;

            void buildFragmentTree(const Chem::MolecularGraph& molgraph,
                                   const Chem::MolecularGraph& parent_molgraph);

            unsigned int getFragmentConformers();

            bool copyInputCoordinates(unsigned int frag_type, const Chem::Fragment& frag,
                                      FragmentTreeNode* node);
            bool fetchConformersFromFragmentLibrary(unsigned int frag_type, const Chem::Fragment& frag,
                                                    FragmentTreeNode* node);
            bool fetchConformersFromFragmentCache(unsigned int frag_type, const Chem::Fragment& frag,
                                                  FragmentTreeNode* node);
            unsigned int generateFragmentConformers(unsigned int frag_type, const Chem::Fragment& frag,
                                                    FragmentTreeNode* node);

            bool setNodeConformers(unsigned int frag_type, const Chem::Fragment& frag,
                                   FragmentTreeNode* node, const ConformerDataArray& confs);

            void initCanonicalFragment(const Chem::Fragment& frag, FragmentTreeNode* frag_node, bool strip_aro_subst);

            void buildCanonicalFragmentAtomIndexMap(const Chem::Fragment&   frag,
                                                    const FragmentTreeNode* frag_node);

            void postprocChainFragment(bool fix_stereo, const Chem::Fragment& frag, FragmentTreeNode* node);

            void fixChainAtomConfigurations(bool have_inv_n, const Chem::Fragment& frag,
                                            FragmentTreeNode* node);
            void fixChainBondConfigurations(const Chem::Fragment& frag, FragmentTreeNode* node);

            void enumChainFragmentNitrogens(const Chem::Fragment& frag, FragmentTreeNode* node);

            void fixBondLengths(const Chem::Fragment& frag, FragmentTreeNode* node);

            bool enumRingFragmentNitrogens(const Chem::Fragment& frag, FragmentTreeNode* node);

            void invertConfiguration(const Chem::Atom& ctr_atom, const Chem::Atom& fixed_atom1, const Chem::Atom& fixed_atom2,
                                     const Chem::Atom& inv_atom, const Chem::Fragment& frag, FragmentTreeNode* node, bool inplace);
            void invertConfiguration(const Chem::Bond& bond, const Chem::Fragment& frag, FragmentTreeNode* node);

            std::size_t getInvertibleNitrogens(const Chem::Fragment& frag, FragmentTreeNode* node);

            void assignLinkBondTorsions(FragmentTreeNode* node);

            const TorsionRuleMatch* getMatchingTorsionRule(const Chem::Bond& bond);

            double getBondLength(std::size_t atom1_idx, std::size_t atom2_idx);

            const Chem::Atom* getNeighborAtom(const Chem::Atom& atom, const Chem::Atom& excl_atom,
                                              FragmentTreeNode* node) const;

            ConformerData::SharedPointer allocConformerData();

            unsigned int invokeCallbacks() const;

            typedef Util::ObjectPool<ConformerData>             ConformerDataCache;
            typedef std::vector<const Chem::Bond*>              BondList;
            typedef std::pair<std::size_t, std::size_t>         IndexPair;
            typedef std::vector<IndexPair>                      IndexPairList;
            typedef std::vector<FragmentLibrary::SharedPointer> FragmentLibraryList;
            typedef std::unique_ptr<MMFF94BondLengthTable>      BondLengthTablePtr;

            ConformerDataCache             confDataCache;
            FragmentAssemblerSettings      settings;
            const Chem::MolecularGraph*    fixedSubstruct;
            const Math::Vector3DArray*     fixedSubstructCoords;
            FragmentLibraryList            fragLibs;
            CallbackFunction               abortCallback;
            CallbackFunction               timeoutCallback;
            LogMessageCallbackFunction     logCallback;
            BondLengthFunction             bondLengthFunc;
            BondList                       fragSplitBonds;
            Chem::FragmentList             fragments;
            FragmentTree                   fragTree;
            TorsionRuleMatcher             torRuleMatcher;
            FragmentConformerGeneratorImpl fragConfGen;
            CanonicalFragment              canonFrag;
            IndexPairList                  canonFragAtomIdxMap;
            Chem::Fragment                 fixedCanonFragSubstruct;
            Math::Vector3DArray            fixedCanonFragSubstructCoords;
            BondLengthTablePtr             bondLengthTable;
            Util::BitSet                   invertibleNMask;
            Util::BitSet                   invertedNMask;
            Util::BitSet                   tmpBitSet;
        };
    } // namespace ConfGen
} // namespace CDPL

#endif // CDPL_CONFGEN_FRAGMENTASSEMBLERIMPL_HPP

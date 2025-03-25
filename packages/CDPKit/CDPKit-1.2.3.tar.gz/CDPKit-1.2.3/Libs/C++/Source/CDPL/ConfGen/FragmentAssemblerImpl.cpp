/* 
 * FragmentAssemblerImpl.cpp 
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
#include <cmath>
#include <mutex>
#include <functional>

#include "CDPL/ConfGen/BondFunctions.hpp"
#include "CDPL/ConfGen/MolecularGraphFunctions.hpp"
#include "CDPL/ConfGen/ReturnCode.hpp"
#include "CDPL/ConfGen/NitrogenEnumerationMode.hpp"
#include "CDPL/ConfGen/FragmentType.hpp"
#include "CDPL/ConfGen/TorsionLibrary.hpp"
#include "CDPL/Chem/MolecularGraphFunctions.hpp"
#include "CDPL/Chem/Entity3DFunctions.hpp"
#include "CDPL/Chem/AtomFunctions.hpp"
#include "CDPL/Chem/BondFunctions.hpp"
#include "CDPL/Chem/AtomType.hpp"
#include "CDPL/Chem/AtomConfiguration.hpp"
#include "CDPL/Chem/BondConfiguration.hpp"
#include "CDPL/MolProp/AtomFunctions.hpp"
#include "CDPL/MolProp/BondFunctions.hpp"
#include "CDPL/Math/Quaternion.hpp"
#include "CDPL/ForceField/UtilityFunctions.hpp"
#include "CDPL/ForceField/Exceptions.hpp"

#include "FragmentAssemblerImpl.hpp"
#include "FragmentTreeNode.hpp"
#include "TorsionLibraryDataReader.hpp"
#include "FallbackTorsionLibrary.hpp"
#include "FragmentConformerCache.hpp"
#include "UtilityFunctions.hpp"


using namespace CDPL;


namespace
{

   const char* ASSEMBLER_TOR_LIB_DATA = 
       " <library name=\"FragmentAssemblerTorsionLibrary\">"
       "  <category name=\"GG\" atomType1=\"*\" atomType2=\"*\">"
       "   <rule pattern=\"[*,#1:1]~[*X3:2]=[*X2:3]=[*X3]~[*,#1:4]\">"
       "    <torsions>"
       "     <angle value=\"90.0\" tolerance1=\"0.0\" tolerance2=\"0.0\" score=\"0.0\"/>"
       "    </torsions>"
       "   </rule>"
       "   <rule pattern=\"[*,#1:1]~[*X3:2]=[*X2:3]=[*X2]=[*X3]~[*,#1:4]\">"
       "    <torsions>"
       "     <angle value=\"0.0\" tolerance1=\"0.0\" tolerance2=\"0.0\" score=\"0.0\"/>"
       "    </torsions>"
       "   </rule>"
       "  </category>"
       " </library>";

    ConfGen::TorsionLibrary::SharedPointer assemblerTorLib(new ConfGen::TorsionLibrary());

    std::once_flag initAssemblerTorLibFlag;

    void initAssemblerTorLib() 
    {
        ConfGen::TorsionLibraryDataReader().read(ASSEMBLER_TOR_LIB_DATA, *assemblerTorLib);
    }

    bool compTorsionAngleEntryScore(const ConfGen::TorsionRule::AngleEntry& entry1, const ConfGen::TorsionRule::AngleEntry& entry2)
    {
        return (entry1.getScore() < entry2.getScore());
    } 

    constexpr std::size_t MAX_TREE_CONF_DATA_CACHE_SIZE = 500;
    constexpr std::size_t MAX_CONF_DATA_CACHE_SIZE      = 500;

    constexpr double MAX_PLANAR_ATOM_GEOM_OOP_ANGLE     = 15.0 / 180.0 * M_PI;
}


ConfGen::FragmentAssemblerImpl::FragmentAssemblerImpl():
    confDataCache(MAX_CONF_DATA_CACHE_SIZE), settings(FragmentAssemblerSettings::DEFAULT),
    fragTree(MAX_TREE_CONF_DATA_CACHE_SIZE)
{
    fragLibs.push_back(FragmentLibrary::get());

    torRuleMatcher.findUniqueMappingsOnly(true);
    torRuleMatcher.findAllRuleMappings(false);
    torRuleMatcher.stopAtFirstMatchingRule(true);
} 

ConfGen::FragmentAssemblerImpl::~FragmentAssemblerImpl() {}

ConfGen::FragmentAssemblerSettings& ConfGen::FragmentAssemblerImpl::getSettings()
{
    return settings;
}

void ConfGen::FragmentAssemblerImpl::clearFragmentLibraries()
{
    fragLibs.clear();
}

void ConfGen::FragmentAssemblerImpl::addFragmentLibrary(const FragmentLibrary::SharedPointer& lib)
{
    fragLibs.push_back(lib);
}

void ConfGen::FragmentAssemblerImpl::setAbortCallback(const CallbackFunction& func)
{
    abortCallback = func;

    fragTree.setAbortCallback(func);
    fragConfGen.setAbortCallback(func);
}

const ConfGen::CallbackFunction& ConfGen::FragmentAssemblerImpl::getAbortCallback() const
{
    return abortCallback;
}

void ConfGen::FragmentAssemblerImpl::setTimeoutCallback(const CallbackFunction& func)
{
    timeoutCallback = func;

    fragTree.setTimeoutCallback(func);
    fragConfGen.setTimeoutCallback(func);
}

const ConfGen::CallbackFunction& ConfGen::FragmentAssemblerImpl::getTimeoutCallback() const
{
    return timeoutCallback;
}

void ConfGen::FragmentAssemblerImpl::setLogMessageCallback(const LogMessageCallbackFunction& func)
{
    logCallback = func;
}

const ConfGen::LogMessageCallbackFunction& ConfGen::FragmentAssemblerImpl::getLogMessageCallback() const
{
    return logCallback;
}

void ConfGen::FragmentAssemblerImpl::setBondLengthFunction(const BondLengthFunction& func)
{
    bondLengthFunc = func;
}

const ConfGen::FragmentAssemblerImpl::BondLengthFunction& ConfGen::FragmentAssemblerImpl::getBondLengthFunction() const
{
    return bondLengthFunc;
}

std::size_t ConfGen::FragmentAssemblerImpl::getNumConformers() const
{
    return fragTree.getRoot()->getNumConformers();
}

ConfGen::ConformerData& ConfGen::FragmentAssemblerImpl::getConformer(std::size_t idx)
{
    return fragTree.getRoot()->getConformer(idx);
}

ConfGen::FragmentAssemblerImpl::ConstConformerIterator ConfGen::FragmentAssemblerImpl::getConformersBegin() const
{
    return fragTree.getRoot()->getConformers().begin();
}

ConfGen::FragmentAssemblerImpl::ConstConformerIterator ConfGen::FragmentAssemblerImpl::getConformersEnd() const
{
    return fragTree.getRoot()->getConformers().end();
}

const Util::BitSet& ConfGen::FragmentAssemblerImpl::getInvertibleNitrogenMask() const
{
    return invertibleNMask;
}

unsigned int ConfGen::FragmentAssemblerImpl::assemble(const Chem::MolecularGraph& molgraph, 
                                                      const Chem::MolecularGraph& parent_molgraph,
                                                      const Chem::MolecularGraph* fixed_substr,
                                                      const Math::Vector3DArray* fixed_substr_coords)
{
    init(parent_molgraph);

    if (processFixedSubstruct(molgraph, parent_molgraph, fixed_substr, fixed_substr_coords))
        return ReturnCode::SUCCESS;
    
    buildFragmentTree(molgraph, parent_molgraph);

    unsigned int ret_code = getFragmentConformers();

    if (ret_code != ReturnCode::SUCCESS)
        return ret_code;

    assignLinkBondTorsions(fragTree.getRoot());

    return fragTree.getRoot()->generateConformers();
}

void ConfGen::FragmentAssemblerImpl::init(const Chem::MolecularGraph& parent_molgraph)
{
    std::call_once(initAssemblerTorLibFlag, &initAssemblerTorLib);

    fragConfGen.getSettings() = settings.getFragmentBuildSettings();

    invertibleNMask.resize(parent_molgraph.getNumAtoms());
    invertibleNMask.reset();
}

bool ConfGen::FragmentAssemblerImpl::processFixedSubstruct(const Chem::MolecularGraph& molgraph,
                                                           const Chem::MolecularGraph& parent_molgraph,
                                                           const Chem::MolecularGraph* fixed_substr,
                                                           const Math::Vector3DArray* fixed_substr_coords)
{
    fixedSubstruct = fixed_substr;
    fixedSubstructCoords = fixed_substr_coords;

    if (!fixed_substr)
        return false;

    if (!fixed_substr_coords) { // sanity check
        fixedSubstruct = 0;
        return false;
    }
    
    std::size_t fss_bond_cnt = getNumFixedSubstructBonds(molgraph);
    
    if (fss_bond_cnt == molgraph.getNumBonds()) {
        fragTree.getRoot()->clearConformers();

        ConformerData::SharedPointer conf = confDataCache.get();

        *conf = *fixed_substr_coords;
        conf->setEnergy(0.0);
        
        fragTree.getRoot()->addConformer(conf);
        return true;
    }
  
    if (fss_bond_cnt == 0)
        fixedSubstruct = 0;

    return false;
}

std::size_t ConfGen::FragmentAssemblerImpl::getNumFixedSubstructBonds(const Chem::MolecularGraph& frag) const
{
    if (!fixedSubstruct)
        return 0;
    
    std::size_t count = 0;
    
    for (auto& bond : frag.getBonds())
        if (fixedSubstruct->containsBond(bond) && fixedSubstruct->containsAtom(bond.getBegin()) &&
            fixedSubstruct->containsAtom(bond.getEnd()))
            count++;

    return count;
}

void ConfGen::FragmentAssemblerImpl::buildFragmentTree(const Chem::MolecularGraph& molgraph, 
                                                       const Chem::MolecularGraph& parent_molgraph)
{
    using namespace Chem;

    std::size_t num_bonds = molgraph.getNumBonds();

    tmpBitSet.resize(num_bonds);
    tmpBitSet.reset();
    fragSplitBonds.clear();

    for (std::size_t i = 0; i < num_bonds; i++) {
        const Bond& bond = molgraph.getBond(i);

        if (fixedSubstruct && fixedSubstruct->containsBond(bond) &&
            fixedSubstruct->containsAtom(bond.getBegin()) &&
            fixedSubstruct->containsAtom(bond.getEnd()) && 
            MolProp::getExplicitBondCount(bond.getBegin(), *fixedSubstruct) > 1 &&
            MolProp::getExplicitBondCount(bond.getEnd(), *fixedSubstruct) > 1)
            continue;
        
        if (!isFragmentLinkBond(bond, molgraph))
            continue;

        const Atom& atom1 = bond.getBegin();
        const Atom& atom2 = bond.getEnd();

        if (!getAromaticityFlag(atom1) && !getAromaticityFlag(atom2) && MolProp::isHydrogenRotor(bond, molgraph))
            continue;
        
        tmpBitSet.set(i);
        fragSplitBonds.push_back(&bond);
    }

    splitIntoFragments(molgraph, fragments, tmpBitSet, false);

    fragTree.build(fragments, parent_molgraph, fragSplitBonds.begin(), fragSplitBonds.end());
}

unsigned int ConfGen::FragmentAssemblerImpl::getFragmentConformers() 
{
    using namespace Chem;

    if (!bondLengthFunc) {
        if (!bondLengthTable.get()) 
            bondLengthTable.reset(new MMFF94BondLengthTable());

        try {
            bondLengthTable->setup(*fragTree.getMolecularGraph(), settings.getFragmentBuildSettings().strictForceFieldParameterization());

        } catch (const ForceField::Error& e) {
            if (logCallback)
                logCallback("Setup of MMFF94 bond-length table failed: " + std::string(e.what()) + '\n');

            return ReturnCode::FORCEFIELD_SETUP_FAILED;
        }
    }

    for (std::size_t i = 0, num_frags = fragTree.getNumFragments(); i < num_frags; i++) {
        const Fragment& frag = *fragTree.getFragment(i); 
        FragmentTreeNode* frag_node = fragTree.getFragmentNode(i); 
        unsigned int frag_type = perceiveFragmentType(frag);

        canonFrag.clear();

        std::size_t fss_bond_cnt = getNumFixedSubstructBonds(frag);
    
        if (fixedSubstruct && fss_bond_cnt == frag.getNumBonds()) {
            if (logCallback) {
                initCanonicalFragment(frag, frag_node, false);

                canonFrag.perceiveSSSR();
                perceiveComponents(canonFrag, true);

                logCallback("Build fragment " + getSMILES(canonFrag) + ":\n");
                logCallback(" Type: " + fragmentTypeToString(frag_type, true) + '\n');
                logCallback(" Hash Code: " + std::to_string(canonFrag.getHashCode()) + "\n");
                logCallback(" Coordinates source: fixed substructure\n");
            }

            ConformerData::SharedPointer conf = allocConformerData();

            *conf = *fixedSubstructCoords;
        
            frag_node->addConformer(conf);

        } else if (fixedSubstruct && fss_bond_cnt > 0) {
            initCanonicalFragment(frag, frag_node, false);

            if (logCallback) {
                canonFrag.perceiveSSSR();
                perceiveComponents(canonFrag, true);

                logCallback("Build fragment " + getSMILES(canonFrag) + ":\n");
                logCallback(" Type: " + fragmentTypeToString(frag_type, true) + '\n');
                logCallback(" Hash Code: " + std::to_string(canonFrag.getHashCode()) + "\n");
            }
            
            unsigned int ret_code = generateFragmentConformers(frag_type, frag, frag_node);

            if (ret_code != ReturnCode::SUCCESS) {
                if (logCallback)
                    logCallback(" Coordinates generation failed!\n");

                return ret_code;
            }
                
        } else if (!(!settings.generateCoordinatesFromScratch() &&
                     (!settings.enumerateRings() || frag_type != FragmentType::FLEXIBLE_RING_SYSTEM) &&
                     copyInputCoordinates(frag_type, frag, frag_node))) {

            initCanonicalFragment(frag, frag_node, true);

            if (logCallback) {
                canonFrag.perceiveSSSR();
                perceiveComponents(canonFrag, true);

                logCallback("Build fragment " + getSMILES(canonFrag) + ":\n");
                logCallback(" Type: " + fragmentTypeToString(frag_type, true) + '\n');
                logCallback(" Hash Code: " + std::to_string(canonFrag.getHashCode()) + "\n");
            }
     
            if (!fetchConformersFromFragmentLibrary(frag_type, frag, frag_node) && !fetchConformersFromFragmentCache(frag_type, frag, frag_node)) {
                unsigned int ret_code = generateFragmentConformers(frag_type, frag, frag_node);

                if (ret_code != ReturnCode::SUCCESS) {
                    if (logCallback)
                        logCallback(" Coordinates generation failed!\n");

                    return ret_code;
                }
            }
        }

        unsigned int ret_code = invokeCallbacks();

        if (ret_code != ReturnCode::SUCCESS) {
            if (logCallback)
                logCallback(" Processing terminated!\n");

            return ret_code;
        }

        if (logCallback) 
            logCallback(" Num. conformers: " + std::to_string(frag_node->getNumConformers()) + '\n');
    }

    return ReturnCode::SUCCESS;
}

void ConfGen::FragmentAssemblerImpl::initCanonicalFragment(const Chem::Fragment& frag, FragmentTreeNode* frag_node, bool strip_aro_subst) 
{
    if (canonFrag.getNumAtoms() != 0)
        return;
        
    canonFrag.create(frag, *fragTree.getMolecularGraph(), true, strip_aro_subst);

    buildCanonicalFragmentAtomIndexMap(frag, frag_node);
}

void ConfGen::FragmentAssemblerImpl::buildCanonicalFragmentAtomIndexMap(const Chem::Fragment& frag, 
                                                                        const FragmentTreeNode* frag_node)
{
    const FragmentTreeNode::IndexArray& atom_inds = frag_node->getAtomIndices();
    const CanonicalFragment::AtomMapping& entry_atom_map = canonFrag.getAtomMapping();

    canonFragAtomIdxMap.clear();

    for (std::size_t i = 0, num_atoms = frag.getNumAtoms(); i < num_atoms; i++)
        canonFragAtomIdxMap.push_back(IndexPair(canonFrag.getAtomIndex(*entry_atom_map[i]), atom_inds[i]));
}

bool ConfGen::FragmentAssemblerImpl::copyInputCoordinates(unsigned int frag_type, const Chem::Fragment& frag, 
                                                          FragmentTreeNode* node)
{
    using namespace Chem;

    ConformerData::SharedPointer coords = allocConformerData();
    Math::Vector3DArray::StorageType& coords_data = coords->getData();
    FragmentTreeNode::IndexArray atom_inds = node->getAtomIndices();
    bool fix_bond_lens = false;

    for (std::size_t i = 0, num_atoms = atom_inds.size(); i < num_atoms; i++) {
        try {
            coords_data[atom_inds[i]] = get3DCoordinates(frag.getAtom(i));

        } catch (const Base::ItemNotFound& e) { 
            // see if at least heavy atom coordinates are available and then generate missing hydrogens

            initCanonicalFragment(frag, node, true);

            if (!fragConfGen.generateConformerFromInputCoordinates(canonFrag)) 
                return false;

            Math::Vector3DArray::StorageType& entry_coords_data = fragConfGen.getConformer(0).getData();

            for (IndexPairList::const_iterator it = canonFragAtomIdxMap.begin(), end = canonFragAtomIdxMap.end(); it != end; ++it) {
                const IndexPair& idx_mapping = *it;
            
                coords_data[idx_mapping.second] = entry_coords_data[idx_mapping.first];
            }

            fix_bond_lens = true;
            break;
        }
    }

    node->addConformer(coords);
    
    if (fix_bond_lens)
        fixBondLengths(frag, node);
    
    if (frag_type == FragmentType::CHAIN)
        postprocChainFragment(false, frag, node);

    else if (frag_type == FragmentType::FLEXIBLE_RING_SYSTEM)
        enumRingFragmentNitrogens(frag, node);

    if (logCallback)
        logCallback(" Coordinates source: input\n");

    return true;
}

bool ConfGen::FragmentAssemblerImpl::fetchConformersFromFragmentLibrary(unsigned int frag_type, const Chem::Fragment& frag, 
                                                                        FragmentTreeNode* node)
{
    using namespace Chem;

    for (FragmentLibraryList::const_reverse_iterator it = fragLibs.rbegin(), end = fragLibs.rend(); it != end; ++it) {
        const FragmentLibraryEntry::SharedPointer& entry_ptr = (*it)->getEntry(canonFrag.getHashCode());

        if (!entry_ptr)
            continue;

        if (!setNodeConformers(frag_type, frag, node, entry_ptr->getData()))
            continue;

        if (logCallback)
            logCallback(" Coordinates source: library\n");

        return true;
    }

    return false;
}

bool ConfGen::FragmentAssemblerImpl::fetchConformersFromFragmentCache(unsigned int frag_type, const Chem::Fragment& frag, 
                                                                      FragmentTreeNode* node)
{
    std::lock_guard<std::mutex> cache_lock(FragmentConformerCache::getMutex());
    const ConformerDataArray* cache_confs = FragmentConformerCache::getEntry(canonFrag.getHashCode());

    if (!cache_confs)
        return false;

    if (!setNodeConformers(frag_type, frag, node, *cache_confs))
        return false;

    if (logCallback)
        logCallback(" Coordinates source: cache\n");

    return true;
}

bool ConfGen::FragmentAssemblerImpl::setNodeConformers(unsigned int frag_type, const Chem::Fragment& frag, 
                                                       FragmentTreeNode* node, const ConformerDataArray& confs)
{
    std::size_t num_confs = confs.size();

    if (num_confs == 0)
        return false;

    if (confs.front()->size() != canonFrag.getNumAtoms())  // sanity check
        return false;

    if (frag_type == FragmentType::CHAIN)
        num_confs = 1;

    else if (frag_type == FragmentType::FLEXIBLE_RING_SYSTEM && !settings.enumerateRings()) {
        double lowest_e = confs[0]->getEnergy();

        for (std::size_t i = 1; i < num_confs; i++) {
            if (confs[i]->getEnergy() != lowest_e) {
                num_confs = i;
                break;
            }
        }
    }

    for (std::size_t i = 0; i < num_confs; i++) {
        ConformerData::SharedPointer conf_data = allocConformerData();
        Math::Vector3DArray::StorageType& conf_coords_data = conf_data->getData();
        const Math::Vector3DArray::StorageType& cache_conf_coords_data = confs[i]->getData();

        for (IndexPairList::const_iterator it = canonFragAtomIdxMap.begin(), end = canonFragAtomIdxMap.end(); it != end; ++it) {
            const IndexPair& idx_mapping = *it;

            conf_coords_data[idx_mapping.second] = cache_conf_coords_data[idx_mapping.first];
        }

        node->addConformer(conf_data);
    }

    fixBondLengths(frag, node);

    if (frag_type == FragmentType::CHAIN)
        postprocChainFragment(true, frag, node);

    else if (frag_type == FragmentType::FLEXIBLE_RING_SYSTEM)
        enumRingFragmentNitrogens(frag, node);
    
    return true;
}

unsigned int ConfGen::FragmentAssemblerImpl::generateFragmentConformers(unsigned int frag_type, const Chem::Fragment& frag, 
                                                                        FragmentTreeNode* node)
{
    fixedCanonFragSubstruct.clear();

    if (fixedSubstruct) {
        auto& atom_mpg = canonFrag.getAtomMapping();
        
        for (auto& bond : frag.getBonds()) {
            if (!fixedSubstruct->containsBond(bond) || !fixedSubstruct->containsAtom(bond.getBegin()) ||
                !fixedSubstruct->containsAtom(bond.getEnd()))
                continue;

            auto canon_atom1 = atom_mpg[frag.getAtomIndex(bond.getBegin())];
            auto canon_atom2 = atom_mpg[frag.getAtomIndex(bond.getEnd())];
            auto canon_bond = canon_atom1->findBondToAtom(*canon_atom2);

            if (canon_bond)
                fixedCanonFragSubstruct.addBond(*canon_bond);
        }

        if (fixedCanonFragSubstruct.getNumBonds() > 0) {
            fixedCanonFragSubstructCoords.resize(canonFrag.getNumAtoms());

            for (auto& idx_mapping : canonFragAtomIdxMap)
                fixedCanonFragSubstructCoords[idx_mapping.first] = (*fixedSubstructCoords)[idx_mapping.second];
        }
    }
    
    canonFrag.perceiveSSSR();

    auto ret_code = fragConfGen.generate(canonFrag, frag_type, fixedCanonFragSubstruct.getNumBonds() == 0 ?
                                         nullptr : &fixedCanonFragSubstruct, &fixedCanonFragSubstructCoords);

    if (ret_code != ReturnCode::SUCCESS && ret_code != ReturnCode::FRAGMENT_CONF_GEN_TIMEOUT) 
        return ret_code;

    auto num_confs = fragConfGen.getNumConformers();

    if (frag_type == FragmentType::FLEXIBLE_RING_SYSTEM && !settings.enumerateRings()) {
        auto lowest_e = fragConfGen.getConformer(0).getEnergy();

        for (std::size_t i = 1; i < num_confs; i++) {
            if (fragConfGen.getConformer(i).getEnergy() > lowest_e) {
                num_confs = i;
                break;
            }
        }
    }

    for (std::size_t i = 0; i < num_confs; i++) {
        auto conf_data = allocConformerData();
        auto& conf_coords_data = conf_data->getData();
        auto& gen_conf_coords_data = fragConfGen.getConformer(i).getData();

        for (auto& idx_mapping : canonFragAtomIdxMap)
            conf_coords_data[idx_mapping.second] = gen_conf_coords_data[idx_mapping.first];

        node->addConformer(conf_data);
    }

    if (fixedCanonFragSubstruct.getNumBonds() > 0) {
        if (enumRingFragmentNitrogens(frag, node))
            enumChainFragmentNitrogens(frag, node);
        
    } else {
        {
            std::lock_guard<std::mutex> cache_lock(FragmentConformerCache::getMutex());

            FragmentConformerCache::addEntry(canonFrag.getHashCode(), fragConfGen.getConformersBegin(), fragConfGen.getConformersEnd());
        }
        
        fixBondLengths(frag, node);

        if (frag_type == FragmentType::CHAIN)
            postprocChainFragment(true, frag, node);
        else if (frag_type == FragmentType::FLEXIBLE_RING_SYSTEM)
            enumRingFragmentNitrogens(frag, node);
    }
    
    if (logCallback) {
        if (fixedCanonFragSubstruct.getNumBonds() == 0)
            logCallback(" Coordinates source: generated\n");
        else
            logCallback(" Coordinates source: fixed substructure/generated\n");
    }
    
    return ReturnCode::SUCCESS;
}

void ConfGen::FragmentAssemblerImpl::fixBondLengths(const Chem::Fragment& frag, FragmentTreeNode* node)
{
    using namespace Chem;
    using namespace MolProp;

    const Util::BitSet& core_atom_mask = node->getCoreAtomMask();

    ConformerDataArray::const_iterator confs_beg = node->getConformers().begin();
    ConformerDataArray::const_iterator confs_end = node->getConformers().end();

    for (Fragment::ConstBondIterator it = frag.getBondsBegin(), end = frag.getBondsEnd(); it != end; ++it) {
        const Bond& bond = *it;
        
        if (getRingFlag(bond))
            continue;

        const Atom& atom1 = bond.getBegin();
        const Atom& atom2 = bond.getEnd();
        std::size_t atom1_idx = fragTree.getMolecularGraph()->getAtomIndex(atom1);
        std::size_t atom2_idx = fragTree.getMolecularGraph()->getAtomIndex(atom2);

        if (getAromaticityFlag(atom2) && getType(atom1) != AtomType::H && 
            getAromaticBondCount(atom2, frag) == 2 && getExplicitBondCount(atom1, frag) == 1) {

            std::swap(atom1_idx, atom2_idx);

        } else if (!(getAromaticityFlag(atom1) && getType(atom2) != AtomType::H && 
                     getAromaticBondCount(atom1, frag) == 2 && getExplicitBondCount(atom2, frag) == 1)) {

            if (core_atom_mask.test(atom1_idx)) {
                if (core_atom_mask.test(atom2_idx))
                    continue;

            } else if (!core_atom_mask.test(atom2_idx))
                continue;
            else
                std::swap(atom1_idx, atom2_idx);
        }

        double bond_len = getBondLength(atom1_idx, atom2_idx);

        if (bond_len <= 0.0)
            continue;

        for (ConformerDataArray::const_iterator conf_it = confs_beg; conf_it != confs_end; ++conf_it) {
            Math::Vector3DArray::StorageType& conf_coords_data = (*conf_it)->getData();

            conf_coords_data[atom2_idx].minusAssign(conf_coords_data[atom1_idx]);
            conf_coords_data[atom2_idx] *= bond_len / length(conf_coords_data[atom2_idx]);
            conf_coords_data[atom2_idx].plusAssign(conf_coords_data[atom1_idx]);
        }
    }
}

void ConfGen::FragmentAssemblerImpl::postprocChainFragment(bool fix_stereo, const Chem::Fragment& frag, FragmentTreeNode* node)
{
    bool have_inv_n = (getInvertibleNitrogens(frag, node) > 0);

    if (fix_stereo) {
        fixChainAtomConfigurations(have_inv_n, frag, node);
        fixChainBondConfigurations(frag, node);
    }

    if (have_inv_n)
        enumChainFragmentNitrogens(frag, node);
}

void ConfGen::FragmentAssemblerImpl::fixChainAtomConfigurations(bool have_inv_n, const Chem::Fragment& frag, FragmentTreeNode* node)
{
    using namespace Chem;

    const Math::Vector3DArray& coords = *node->getConformers().front();
    const MolecularGraph& parent_molgraph = *fragTree.getMolecularGraph();

    const FragmentTreeNode::IndexArray& atom_inds = node->getAtomIndices();

    for (std::size_t i = 0, num_atoms = frag.getNumAtoms(); i < num_atoms; i++) {
        if (have_inv_n && invertedNMask.test(atom_inds[i]))
            continue;

        const Atom& atom = frag.getAtom(i);
        const StereoDescriptor& descr = getStereoDescriptor(atom);
        unsigned int config = descr.getConfiguration();

        if (config != AtomConfiguration::R && config != AtomConfiguration::S)
            continue;

        if (!descr.isValid(atom))
            continue;

        std::size_t num_ref_atoms = descr.getNumReferenceAtoms();
        const Chem::Atom* const* ref_atoms = descr.getReferenceAtoms();
        bool descr_valid = true;

        for (std::size_t i = 0; i < num_ref_atoms; i++) {
            if (!frag.containsAtom(*ref_atoms[i])) {
                descr_valid = false;
                break;
            }
        }

        if (!descr_valid)
            continue;

        if (calcConfiguration(atom, parent_molgraph, descr, coords) == config) 
            continue;

        const Atom* nbr_atoms[4];
        Atom::ConstBondIterator b_it = atom.getBondsBegin();
        std::size_t num_nbr_atoms = 0;
        
        for (Atom::ConstAtomIterator a_it = atom.getAtomsBegin(), a_end = atom.getAtomsEnd(); a_it != a_end; ++a_it, ++b_it) {
            const Atom& nbr_atom = *a_it;

            if (!frag.containsAtom(nbr_atom) || !frag.containsBond(*b_it))
                continue;

            if (num_nbr_atoms < 4)
                nbr_atoms[num_nbr_atoms] = &nbr_atom;

            num_nbr_atoms++;
        }

        if (num_nbr_atoms < 3 || num_nbr_atoms > 4)
            continue;
        
        invertConfiguration(atom, *nbr_atoms[0], *nbr_atoms[1], *nbr_atoms[2], frag, node, true);

        if (num_nbr_atoms > 3)
            invertConfiguration(atom, *nbr_atoms[0], *nbr_atoms[1], *nbr_atoms[3], frag, node, true);
    }
}

void ConfGen::FragmentAssemblerImpl::fixChainBondConfigurations(const Chem::Fragment& frag, FragmentTreeNode* node)
{
    using namespace Chem;

    const Math::Vector3DArray& coords = *node->getConformers().front();
    const MolecularGraph& parent_molgraph = *fragTree.getMolecularGraph();

    for (Fragment::ConstBondIterator it = frag.getBondsBegin(), end = frag.getBondsEnd(); it != end; ++it) {
        const Bond& bond = *it;
        const StereoDescriptor& descr = getStereoDescriptor(bond);
        unsigned int config = descr.getConfiguration();

        if (config != BondConfiguration::CIS && config != BondConfiguration::TRANS)
            continue;

        if (!descr.isValid(bond)) 
            continue;

        const Atom* const* ref_atoms = descr.getReferenceAtoms();
        bool descr_valid = true;
    
        for (std::size_t i = 0; i < 4; i++) {
            if (!frag.containsAtom(*ref_atoms[i])) {
                descr_valid = false;
                break;
            }
        }

        if (!descr_valid) 
            continue;

        if (calcConfiguration(bond, parent_molgraph, descr, coords) == config)
            continue;

        invertConfiguration(bond, frag, node);
    }
}

void ConfGen::FragmentAssemblerImpl::enumChainFragmentNitrogens(const Chem::Fragment& frag, FragmentTreeNode* node)
{
    using namespace Chem;

    const MolecularGraph& parent_molgraph = *fragTree.getMolecularGraph();

    for (Util::BitSet::size_type i = invertedNMask.find_first(); i != Util::BitSet::npos; i = invertedNMask.find_next(i)) {
        const Atom& atom = parent_molgraph.getAtom(i);

        if (getRingFlag(atom))
            continue;
        
        const Atom* nbr_atoms[3];
        const Atom** nbr_atoms_it = nbr_atoms;
        const Atom* non_fixed_nbr = 0;
        
        Atom::ConstBondIterator b_it = atom.getBondsBegin();

        for (Atom::ConstAtomIterator a_it = atom.getAtomsBegin(), a_end = atom.getAtomsEnd(); a_it != a_end; ++a_it, ++b_it) {
            const Atom& nbr_atom = *a_it;
            const Bond& bond = *b_it;
            
            if (!frag.containsAtom(nbr_atom) || !frag.containsBond(bond))
                continue;
            
            *nbr_atoms_it++ = &nbr_atom;
            
            if (fixedSubstruct && fixedSubstruct->containsBond(bond) && fixedSubstruct->containsAtom(bond.getBegin()) &&
                fixedSubstruct->containsAtom(bond.getEnd()))
                continue;

            non_fixed_nbr = &nbr_atom;
        }

        if (nbr_atoms_it != &nbr_atoms[3]) // sanity check
            continue;

        if (non_fixed_nbr == nbr_atoms[2])
            invertConfiguration(atom, *nbr_atoms[0], *nbr_atoms[1], *nbr_atoms[2], frag, node, false);
        else if (non_fixed_nbr == nbr_atoms[1])
            invertConfiguration(atom, *nbr_atoms[0], *nbr_atoms[2], *nbr_atoms[1], frag, node, false);
        else if (non_fixed_nbr == nbr_atoms[0])
            invertConfiguration(atom, *nbr_atoms[1], *nbr_atoms[2], *nbr_atoms[0], frag, node, false);
    }
}

bool ConfGen::FragmentAssemblerImpl::enumRingFragmentNitrogens(const Chem::Fragment& frag, FragmentTreeNode* node)
{
    using namespace Chem;

    if (getInvertibleNitrogens(frag, node) == 0) 
        return false;

    const MolecularGraph& parent_molgraph = *fragTree.getMolecularGraph();

    for (Util::BitSet::size_type i = invertedNMask.find_first(); i != Util::BitSet::npos; i = invertedNMask.find_next(i)) {
        const Atom& atom = parent_molgraph.getAtom(i);
        const Atom* ring_nbr1 = 0;
        const Atom* ring_nbr2 = 0;
        const Atom* subst_nbr = 0;

        Atom::ConstBondIterator b_it = atom.getBondsBegin();

        for (Atom::ConstAtomIterator a_it = atom.getAtomsBegin(), a_end = atom.getAtomsEnd(); a_it != a_end; ++a_it, ++b_it) {
            const Atom& nbr_atom = *a_it;
            const Bond& bond = *b_it;

            if (!frag.containsAtom(nbr_atom) || !frag.containsBond(bond))
                continue;

            if (getRingFlag(bond)) {
                if (!ring_nbr1)
                    ring_nbr1 = &nbr_atom;
                else
                    ring_nbr2 = &nbr_atom;

            } else 
                subst_nbr = &nbr_atom;
        }

        if (!subst_nbr || !ring_nbr2) // sanity check
            continue;

        invertConfiguration(atom, *ring_nbr1, *ring_nbr2, *subst_nbr, frag, node, false);
    }

    return true;
}

void ConfGen::FragmentAssemblerImpl::invertConfiguration(const Chem::Atom& ctr_atom, const Chem::Atom& fixed_atom1, const Chem::Atom& fixed_atom2, 
                                                         const Chem::Atom& inv_atom, const Chem::Fragment& frag, FragmentTreeNode* node, bool inplace)
{
    using namespace Chem;

    const MolecularGraph& parent_molgraph = *fragTree.getMolecularGraph();
    const FragmentTreeNode::IndexArray& atom_inds = node->getAtomIndices();
    std::size_t num_atoms = atom_inds.size();

    tmpBitSet.resize(num_atoms);

    std::size_t atom_idx = frag.getAtomIndex(ctr_atom);

    tmpBitSet.reset();
    tmpBitSet.set(atom_idx);

    markReachableAtoms(inv_atom, frag, tmpBitSet, false);

    tmpBitSet.reset(atom_idx);

    std::size_t ctr_atom_idx = parent_molgraph.getAtomIndex(ctr_atom);
    std::size_t fixed_atom1_idx = parent_molgraph.getAtomIndex(fixed_atom1);
    std::size_t fixed_atom2_idx = parent_molgraph.getAtomIndex(fixed_atom2);
    std::size_t inv_atom_idx = parent_molgraph.getAtomIndex(inv_atom);
    Math::Vector3D fixed_atom1_vec;
    Math::Vector3D fixed_atom2_vec;
    Math::Vector3D inv_atom_vec;
    Math::Vector3D plane_normal;
    Math::Vector3D rot_axis;
    Math::DQuaternion rot_quat;

    for (std::size_t i = 0, num_confs = node->getNumConformers(); i < num_confs; i++) {
        const ConformerData::SharedPointer& conf_data = node->getConformers()[i];
        Math::Vector3DArray::StorageType& conf_coords_data = conf_data->getData();
        const Math::Vector3D& ctr_atom_pos = conf_coords_data[ctr_atom_idx];
            
        fixed_atom1_vec.assign(conf_coords_data[fixed_atom1_idx] - ctr_atom_pos);
        fixed_atom2_vec.assign(conf_coords_data[fixed_atom2_idx] - ctr_atom_pos);
        plane_normal.assign(crossProd(fixed_atom1_vec, fixed_atom2_vec));

        double plane_normal_norm = length(plane_normal);

        if (plane_normal_norm == 0.0) // sanity check
            continue;

        inv_atom_vec.assign(conf_coords_data[inv_atom_idx] - ctr_atom_pos);

        double inv_atom_vec_norm = length(inv_atom_vec);

        if (inv_atom_vec_norm == 0.0) // sanity check
            continue;

        double oop_angle = M_PI * 0.5 - std::acos(angleCos(inv_atom_vec, plane_normal, plane_normal_norm * inv_atom_vec_norm, true));

        rot_axis.assign(crossProd(inv_atom_vec, plane_normal));

        double rot_axis_norm = length(rot_axis);

        if (rot_axis_norm == 0.0) // sanity check
            continue;

        double cos_w2 = std::cos(-oop_angle);
        double sin_w2 = std::sin(-oop_angle);

        rot_quat.set(cos_w2, sin_w2 * rot_axis[0] / rot_axis_norm, sin_w2 * rot_axis[1] / rot_axis_norm, 
                     sin_w2 * rot_axis[2] / rot_axis_norm); // rotate by -2 * oop_angle

        if (!inplace) {
            ConformerData::SharedPointer inv_conf = allocConformerData();
            Math::Vector3DArray::StorageType& inv_conf_coords_data = inv_conf->getData();

            for (std::size_t j = 0; j < num_atoms; j++) {
                atom_idx = atom_inds[j];

                if (!tmpBitSet.test(j)) {
                    inv_conf_coords_data[atom_idx] = conf_coords_data[atom_idx];
                    continue;
                }

                const Math::Vector3D& subst_atom_pos = conf_coords_data[atom_idx];

                inv_atom_vec.assign(subst_atom_pos - ctr_atom_pos);
                inv_conf_coords_data[atom_idx].assign(rotate(rot_quat, inv_atom_vec) + ctr_atom_pos);
            }

            node->addConformer(inv_conf);

        } else {
            for (Util::BitSet::size_type j = tmpBitSet.find_first(); j != Util::BitSet::npos; j = tmpBitSet.find_next(j)) {
                Math::Vector3D& subst_atom_pos = conf_coords_data[atom_inds[j]];

                inv_atom_vec.assign(subst_atom_pos - ctr_atom_pos);
                subst_atom_pos.assign(rotate(rot_quat, inv_atom_vec) + ctr_atom_pos);
            }
        }
    }
}

void ConfGen::FragmentAssemblerImpl::invertConfiguration(const Chem::Bond& bond, const Chem::Fragment& frag, FragmentTreeNode* node)
{
    const FragmentTreeNode::IndexArray& atom_inds = node->getAtomIndices();

    std::size_t bond_atom1_idx = frag.getAtomIndex(bond.getBegin());
    std::size_t bond_atom2_idx = frag.getAtomIndex(bond.getEnd());
    std::size_t num_atoms = atom_inds.size();

    tmpBitSet.resize(num_atoms);
    tmpBitSet.reset();
    tmpBitSet.set(bond_atom1_idx);

    markReachableAtoms(bond.getEnd(), frag, tmpBitSet, false);

    tmpBitSet.reset(bond_atom1_idx);
    tmpBitSet.reset(bond_atom2_idx);

    Math::Vector3D rot_axis;
    Math::Vector3D subst_atom_vec;
    Math::DQuaternion rot_quat;

    for (std::size_t i = 0, num_confs = node->getNumConformers(); i < num_confs; i++) {
        const ConformerData::SharedPointer& conf_data = node->getConformers()[i];
        Math::Vector3DArray::StorageType& conf_coords_data = conf_data->getData();
        const Math::Vector3D& bond_atom2_pos = conf_coords_data[atom_inds[bond_atom2_idx]];
            
        rot_axis.assign(bond_atom2_pos - conf_coords_data[atom_inds[bond_atom1_idx]]);

        double rot_axis_norm = length(rot_axis);

        if (rot_axis_norm == 0.0) // sanity check
            continue;

        rot_quat.set(0.0, rot_axis[0] / rot_axis_norm, rot_axis[1] / rot_axis_norm, rot_axis[2] / rot_axis_norm); // rotate by 180°

        for (Util::BitSet::size_type j = tmpBitSet.find_first(); j != Util::BitSet::npos; j = tmpBitSet.find_next(j)) {
            Math::Vector3D& subst_atom_pos = conf_coords_data[atom_inds[j]];

            subst_atom_vec.assign(subst_atom_pos - bond_atom2_pos);
            subst_atom_pos.assign(rotate(rot_quat, subst_atom_vec) + bond_atom2_pos);
        }
    }
}

std::size_t ConfGen::FragmentAssemblerImpl::getInvertibleNitrogens(const Chem::Fragment& frag, FragmentTreeNode* node)
{
    using namespace Chem;

    unsigned int n_enum_mode = settings.getNitrogenEnumerationMode();

    if (n_enum_mode == NitrogenEnumerationMode::NONE)
        return 0;

    const Math::Vector3DArray::StorageType& coords_data = node->getConformers().front()->getData();
    const Util::BitSet& core_atom_mask = node->getCoreAtomMask();
    const FragmentTreeNode::IndexArray& atom_inds = node->getAtomIndices();
    const MolecularGraph& parent_molgraph = *fragTree.getMolecularGraph();

    invertedNMask.resize(parent_molgraph.getNumAtoms());
    invertedNMask.reset();

    std::size_t inv_n_cnt = 0;

    for (std::size_t i = 0, num_atoms = frag.getNumAtoms(); i < num_atoms; i++) {
        std::size_t parent_atom_idx = atom_inds[i];

        if (!core_atom_mask.test(parent_atom_idx))
            continue;

        const Atom& atom = frag.getAtom(i);

        if (getType(atom) != AtomType::N)
            continue;

        std::size_t h_bond_count = 0;
        std::size_t ring_bond_count = 0;
        std::size_t fixed_bond_count = 0;
        std::size_t fixed_ring_bond_count = 0;
        std::size_t nbr_atom_indices[3];
        std::size_t j = 0;

        Atom::ConstBondIterator b_it = atom.getBondsBegin();

        for (Atom::ConstAtomIterator a_it = atom.getAtomsBegin(), a_end = atom.getAtomsEnd(); a_it != a_end; ++a_it, ++b_it) {
            const Atom& nbr_atom = *a_it;
            const Bond& bond = *b_it;

            if (!frag.containsAtom(nbr_atom) || !frag.containsBond(bond))
                continue;

            if (j == 3) {
                j = 0;
                break;
            }

            bool ring_bond = getRingFlag(bond);
            
            if (ring_bond && ++ring_bond_count > 2)
                break;
   
            if (fixedSubstruct && fixedSubstruct->containsBond(bond) && fixedSubstruct->containsAtom(bond.getBegin()) &&
                fixedSubstruct->containsAtom(bond.getEnd())) {

                if (++fixed_bond_count > 2)
                    break;

                if (ring_bond)
                    fixed_ring_bond_count++;
            }
                
            if (getOrder(bond) != 1)
                break;

            if (getType(nbr_atom) == AtomType::H && (++h_bond_count > 1))
                break;

            nbr_atom_indices[j++] = parent_molgraph.getAtomIndex(nbr_atom);
        }

        if (j != 3)
            continue;

        if (fixed_ring_bond_count != 0 && fixed_bond_count != fixed_ring_bond_count)
            continue;
        
        double oop_angle = ForceField::calcOutOfPlaneAngle<double>(coords_data[nbr_atom_indices[0]].getData(), coords_data[parent_atom_idx].getData(),
                                                                   coords_data[nbr_atom_indices[1]].getData(), coords_data[nbr_atom_indices[2]].getData());

        if (std::abs(oop_angle) <= MAX_PLANAR_ATOM_GEOM_OOP_ANGLE) 
            continue;

        invertibleNMask.set(parent_atom_idx);

        if (n_enum_mode == NitrogenEnumerationMode::UNSPECIFIED_STEREO) {
            const StereoDescriptor& descr = getStereoDescriptor(atom);
            unsigned int config = descr.getConfiguration();

            if (descr.isValid(atom) && (config == AtomConfiguration::R || config == AtomConfiguration::S)) {
                std::size_t num_ref_atoms = descr.getNumReferenceAtoms();
                const Chem::Atom* const* ref_atoms = descr.getReferenceAtoms();
                bool descr_valid = true;

                for (std::size_t j = 0; j < num_ref_atoms; j++) {
                    if (!frag.containsAtom(*ref_atoms[j])) {
                        descr_valid = false;
                        break;
                    }
                }

                if (descr_valid)
                    continue;
            }
        }

        invertedNMask.set(parent_atom_idx);
        inv_n_cnt++;
    }

    if (logCallback)
        logCallback(" Num. inv. nitrogens: " + std::to_string(inv_n_cnt) + '\n');

    return inv_n_cnt;
}

void ConfGen::FragmentAssemblerImpl::assignLinkBondTorsions(FragmentTreeNode* node) 
{
    using namespace Chem;
    using namespace std::placeholders;
    
    if (!node->hasChildren())
        return;

    assignLinkBondTorsions(node->getLeftChild());
    assignLinkBondTorsions(node->getRightChild());

    const Bond* bond = node->getSplitBond();

    if (!bond)
        return;

    const Atom* const* bond_atoms = node->getSplitBondAtoms();
    const TorsionRuleMatch* match = getMatchingTorsionRule(*bond);

    if (match && match->getRule().getNumAngles() > 0) {
        TorsionRule::ConstAngleEntryIterator it = std::max_element(match->getRule().getAnglesBegin(), match->getRule().getAnglesEnd(),
                                                                   std::bind(&compTorsionAngleEntryScore, _1, _2));
        node->addTorsionAngle(it->getAngle());

        const Atom* const* match_atoms = match->getAtoms();
                
        if (match_atoms[1] == bond_atoms[0])
            node->setTorsionReferenceAtoms(match_atoms[0], match_atoms[3]);
        else
            node->setTorsionReferenceAtoms(match_atoms[3], match_atoms[0]);
    
        return;
    }

    if (getOrder(*bond) == 2) {
        // torsion setup for potential stereo double bonds

        const StereoDescriptor& descr = getStereoDescriptor(*bond);
        unsigned int config = descr.getConfiguration();

        if ((config == BondConfiguration::CIS || config == BondConfiguration::TRANS) && descr.isValid(*bond)) {
            const Atom* const* ref_atoms = descr.getReferenceAtoms();
            bool descr_valid = true;
            
            for (std::size_t i = 0; i < 4; i++) {
                if (!node->containsAtom(*ref_atoms[i])) {
                    descr_valid = false;
                    break;
                }
            }
        
            if (descr_valid) {
                // choose angle that results in desired configuration

                if (ref_atoms[1] == bond_atoms[0])
                    node->setTorsionReferenceAtoms(ref_atoms[0], ref_atoms[3]);
                else
                    node->setTorsionReferenceAtoms(ref_atoms[3], ref_atoms[0]);

                node->addTorsionAngle(config == BondConfiguration::CIS ? 0.0 : 180.0);
                return;
            }
        } 
    }

    // choose trans configuration of arbitrary substituent atoms

    const Atom* ref_atom1 = getNeighborAtom(*bond_atoms[0], *bond_atoms[1], node);

    if (!ref_atom1)
        return;

    const Atom* ref_atom2 = getNeighborAtom(*bond_atoms[1], *bond_atoms[0], node);

    if (!ref_atom2)
        return;

    node->setTorsionReferenceAtoms(ref_atom1, ref_atom2);
    node->addTorsionAngle(180.0);
}

const ConfGen::TorsionRuleMatch* ConfGen::FragmentAssemblerImpl::getMatchingTorsionRule(const Chem::Bond& bond)
{
    const Chem::MolecularGraph& molgraph = *fragTree.getMolecularGraph();

    torRuleMatcher.setTorsionLibrary(assemblerTorLib);

    if (torRuleMatcher.findMatches(bond, molgraph, false)) 
        return &torRuleMatcher.getMatch(0); 

    if (getOrder(bond) == 1) {
        torRuleMatcher.setTorsionLibrary(TorsionLibrary::get());

        if (torRuleMatcher.findMatches(bond, molgraph, false)) 
            return &torRuleMatcher.getMatch(0); 

        torRuleMatcher.setTorsionLibrary(getFallbackTorsionLibrary());

        if (torRuleMatcher.findMatches(bond, molgraph, false)) 
            return &torRuleMatcher.getMatch(0); 
    }

    return 0;
}

double ConfGen::FragmentAssemblerImpl::getBondLength(std::size_t atom1_idx, std::size_t atom2_idx)
{
    if (bondLengthFunc)
        return bondLengthFunc(atom1_idx, atom2_idx);

    return bondLengthTable->get(atom1_idx, atom2_idx);
}

const Chem::Atom* ConfGen::FragmentAssemblerImpl::getNeighborAtom(const Chem::Atom& atom, const Chem::Atom& excl_atom, 
                                                                  FragmentTreeNode* node) const
{
    using namespace Chem;

    const MolecularGraph& molgraph = *fragTree.getMolecularGraph();
    Atom::ConstAtomIterator atoms_end = atom.getAtomsEnd();
    Atom::ConstBondIterator b_it = atom.getBondsBegin();

    for (Atom::ConstAtomIterator a_it = atom.getAtomsBegin(); a_it != atoms_end; ++a_it, ++b_it) {
        const Atom& nbr_atom = *a_it;

        if (&nbr_atom == &excl_atom)
            continue;

        if (!node->containsAtom(nbr_atom))
            continue;

        if (!molgraph.containsBond(*b_it))
            continue;

        return &nbr_atom;
    }

    return 0;
}

ConfGen::ConformerData::SharedPointer ConfGen::FragmentAssemblerImpl::allocConformerData()
{
    ConformerData::SharedPointer conf_data = confDataCache.get();

    conf_data->resize(fragTree.getMolecularGraph()->getNumAtoms());
    conf_data->setEnergy(0.0);

    return conf_data;
}

unsigned int ConfGen::FragmentAssemblerImpl::invokeCallbacks() const
{
    if (abortCallback && abortCallback())
        return ReturnCode::ABORTED;

    if (timeoutCallback && timeoutCallback())
        return ReturnCode::TIMEOUT;    

    return ReturnCode::SUCCESS;
}

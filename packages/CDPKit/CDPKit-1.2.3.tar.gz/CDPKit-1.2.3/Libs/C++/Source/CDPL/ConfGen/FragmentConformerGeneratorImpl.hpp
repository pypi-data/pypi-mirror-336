/* 
 * FragmentConformerGeneratorImpl.hpp 
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
 * \brief Definition of the class CDPL::ConfGen::FragmentConformerGeneratorImpl.
 */

#ifndef CDPL_CONFGEN_FRAGMENTCONFORMERGENERATORIMPL_HPP
#define CDPL_CONFGEN_FRAGMENTCONFORMERGENERATORIMPL_HPP

#include <vector>
#include <cstddef>

#include "CDPL/ConfGen/FragmentConformerGeneratorSettings.hpp"
#include "CDPL/ConfGen/ConformerDataArray.hpp"
#include "CDPL/ConfGen/DGStructureGenerator.hpp"
#include "CDPL/ConfGen/CallbackFunction.hpp"
#include "CDPL/ConfGen/LogMessageCallbackFunction.hpp"
#include "CDPL/ForceField/MMFF94InteractionParameterizer.hpp"
#include "CDPL/ForceField/MMFF94InteractionData.hpp"
#include "CDPL/ForceField/MMFF94GradientCalculator.hpp"
#include "CDPL/ForceField/ElasticPotentialList.hpp"
#include "CDPL/Chem/Hydrogen3DCoordinatesCalculator.hpp"
#include "CDPL/Chem/AutomorphismGroupSearch.hpp"
#include "CDPL/Chem/ComponentSet.hpp"
#include "CDPL/Math/BFGSMinimizer.hpp"
#include "CDPL/Math/VectorArrayAlignmentCalculator.hpp"
#include "CDPL/Util/BitSet.hpp"
#include "CDPL/Util/ObjectPool.hpp"
#include "CDPL/Internal/Timer.hpp"


namespace CDPL
{

    namespace ConfGen
    {

        class FragmentConformerGeneratorImpl
        {

          public:
            typedef ConformerDataArray::const_iterator ConstConformerIterator;

            FragmentConformerGeneratorImpl();

            FragmentConformerGeneratorSettings& getSettings();

            const FragmentConformerGeneratorSettings& getSettings() const;

            void setAbortCallback(const CallbackFunction& func);

            const CallbackFunction& getAbortCallback() const;

            void setTimeoutCallback(const CallbackFunction& func);

            const CallbackFunction& getTimeoutCallback() const;

            void setLogMessageCallback(const LogMessageCallbackFunction& func);

            const LogMessageCallbackFunction& getLogMessageCallback() const;

            unsigned int generate(const Chem::MolecularGraph& molgraph, unsigned int frag_type,
                                  const Chem::MolecularGraph* fixed_substr,
                                  const Math::Vector3DArray* fixed_substr_coords);

            void setConformers(Chem::MolecularGraph& molgraph) const;

            std::size_t getNumConformers() const;

            ConformerData& getConformer(std::size_t idx);

            ConstConformerIterator getConformersBegin() const;

            ConstConformerIterator getConformersEnd() const;

            bool generateConformerFromInputCoordinates(const Chem::MolecularGraph& molgraph);

          private:
            typedef Util::ObjectPool<ConformerData> ConformerDataCache;
            typedef std::vector<const Chem::Atom*>  AtomList;

            FragmentConformerGeneratorImpl(const FragmentConformerGeneratorImpl&);

            FragmentConformerGeneratorImpl& operator=(const FragmentConformerGeneratorImpl&);

            void init(const Chem::MolecularGraph& molgraph);

            void processFixedSubstructure();
            
            bool generateConformerFromInputCoordinates(ConformerDataArray& conf_array);

            bool setupForceField();

            void setupRandomConformerGeneration(bool reg_stereo);

            bool generateHydrogenCoordsAndMinimize(ConformerData& conf_data);

            double calcEnergy(const Math::Vector3DArray::StorageType& coords);
            double calcGradient(const Math::Vector3DArray::StorageType& coords,
                                Math::Vector3DArray::StorageType& grad);
            
            unsigned int generateChainConformer();
            unsigned int generateRigidRingConformer();
            unsigned int generateFlexibleRingConformers();

            void addSymmetryMappedConformers(const ConformerData& conf_data, double rmsd, std::size_t max_num_out_confs);
            void addMirroredConformer(const ConformerData& conf_data, double rmsd, std::size_t max_num_out_confs);

            unsigned int generateRandomConformer(ConformerData& conf);

            bool checkRMSD(const Math::Vector3DArray& conf_coords, double min_rmsd);

            ConformerData::SharedPointer getRingAtomCoordinates(const Math::Vector3DArray& conf_coords);

            void getRingAtomIndices();
            void getSymmetryMappings();
            void getNeighborHydrogens(const Chem::Atom& atom, AtomList& nbr_list) const;

            std::size_t calcNumChainConfSamples() const;
            std::size_t calcNumSmallRingSystemConfSamples() const;
            std::size_t calcNumMacrocyclicRingSystemConfSamples() const;

            ConformerData::SharedPointer allocConformerData();

            unsigned int invokeCallbacks() const;
            bool         timedout(std::size_t timeout) const;

            bool has3DCoordinates(const Chem::Atom& atom) const;

            typedef ForceField::MMFF94GradientCalculator<double>                  MMFF94GradientCalculator;
            typedef ForceField::MMFF94InteractionParameterizer                    MMFF94InteractionParameterizer;
            typedef ForceField::MMFF94InteractionData                             MMFF94InteractionData;
            typedef ForceField::ElasticPotentialList                              ElasticPotentialList;
            typedef Math::BFGSMinimizer<Math::Vector3DArray::StorageType, double> BFGSMinimizer;
            typedef Math::VectorArrayAlignmentCalculator<Math::Vector3DArray>     AlignmentCalculator;
            typedef std::vector<std::size_t>                                      IndexList;
            
            ConformerDataCache                    confDataCache;
            CallbackFunction                      abortCallback;
            CallbackFunction                      timeoutCallback;
            LogMessageCallbackFunction            logCallback;
            Internal::Timer                       timer;
            const Chem::MolecularGraph*           molGraph;
            const Chem::MolecularGraph*           fixedSubstruct;
            const Math::Vector3DArray*            fixedSubstructCoords;
            std::size_t                           numAtoms;
            MMFF94InteractionParameterizer        mmff94Parameterizer;
            MMFF94InteractionData                 mmff94Data;
            MMFF94GradientCalculator              mmff94GradientCalc;
            BFGSMinimizer                         energyMinimizer;
            ElasticPotentialList                  elasticPotentials;
            DGStructureGenerator                  dgStructureGen;
            Chem::Hydrogen3DCoordinatesCalculator hCoordsCalc;
            Chem::AutomorphismGroupSearch         symMappingSearch;
            AlignmentCalculator                   alignmentCalc;
            Chem::ComponentSet                    fixedSubstructFrags;
            Math::Vector3DArray::StorageType      energyGradient;
            IndexList                             ringAtomIndices;
            IndexList                             symMappings;
            AtomList                              nbrHydrogens1;
            AtomList                              nbrHydrogens2;
            Chem::Fragment                        symMappingSearchMolGraph;
            Util::BitSet                          coreAtomMask;
            ConformerDataArray                    ringAtomCoords;
            ConformerDataArray                    outputConfs;
            ConformerDataArray                    workingConfs;
            FragmentConformerGeneratorSettings    settings;
        };
    } // namespace ConfGen
} // namespace CDPL

#endif // CDPL_CONFGEN_FRAGMENTCONFORMERGENERATORIMPL_HPP

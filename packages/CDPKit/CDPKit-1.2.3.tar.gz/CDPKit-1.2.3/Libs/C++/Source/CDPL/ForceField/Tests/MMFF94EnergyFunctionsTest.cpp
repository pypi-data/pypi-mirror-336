/* 
 * MMFF94EnergyFunctionsTest.cpp 
 *
 * This file is part of the Chemical Data Processing Toolkit
 *
 * Copyright (C) 2003 Thomas Seidel <thomas.seidel@univie.ac.at>
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program; see the file COPYING. If not, write to
 * the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 */


#include <cstddef>
#include <cmath>

#include <boost/test/auto_unit_test.hpp>

#include "CDPL/ForceField/MMFF94BondStretchingInteractionParameterizer.hpp"
#include "CDPL/ForceField/MMFF94AngleBendingInteractionParameterizer.hpp"
#include "CDPL/ForceField/MMFF94StretchBendInteractionParameterizer.hpp"
#include "CDPL/ForceField/MMFF94OutOfPlaneBendingInteractionParameterizer.hpp"
#include "CDPL/ForceField/MMFF94OutOfPlaneBendingParameterTable.hpp"
#include "CDPL/ForceField/MMFF94TorsionInteractionParameterizer.hpp"
#include "CDPL/ForceField/MMFF94TorsionParameterTable.hpp"
#include "CDPL/ForceField/MMFF94VanDerWaalsInteractionParameterizer.hpp"
#include "CDPL/ForceField/MMFF94ElectrostaticInteractionParameterizer.hpp"
#include "CDPL/ForceField/MMFF94EnergyFunctions.hpp"
#include "CDPL/ForceField/MolecularGraphFunctions.hpp"
#include "CDPL/Chem/MolecularGraphFunctions.hpp"
#include "CDPL/Chem/Entity3DContainerFunctions.hpp"
#include "CDPL/Chem/AtomFunctions.hpp"

#include "MMFF94TestData.hpp"
#include "TestUtils.hpp"


BOOST_AUTO_TEST_CASE(MMFF94BondStretchingEnergyFunctionTest)
{
    using namespace CDPL;
    using namespace Testing;

    OptimolLogReader::BondStretchingInteractionList ia_list;
    OptimolLogReader::EnergyData energies;

    ForceField::MMFF94BondStretchingInteractionParameterizer parameterizer;
    ForceField::MMFF94BondStretchingInteractionList found_ia_list;
    Math::Vector3DArray coords;

//double max_en_diff = 0;

    for (std::size_t mol_idx = 0; mol_idx < MMFF94TestData::DYN_TEST_MOLECULES.size(); mol_idx++) {
        const Chem::Molecule& mol = *MMFF94TestData::DYN_TEST_MOLECULES[mol_idx];
        const std::string& mol_name = getName(mol);

        BOOST_CHECK(MMFF94TestData::DYN_LOG_READER.getBondStretchingInteractions(mol_name, ia_list));

        parameterizer.parameterize(mol, found_ia_list, true);

        BOOST_CHECK_MESSAGE(found_ia_list.getSize() == ia_list.size(), "Bond stretching interaction count mismatch for molecule #" << mol_idx << " (" << mol_name << "): " <<
                            found_ia_list.getSize() << " != " << ia_list.size());
        coords.clear();
        get3DCoordinates(mol, coords);

        for (std::size_t i = 0; i < ia_list.size(); i++) {
            bool iaction_found = false;

            for (std::size_t j = 0; j < found_ia_list.getSize(); j++) {
                const ForceField::MMFF94BondStretchingInteraction& iaction = found_ia_list[j];

                if ((iaction.getAtom1Index() == ia_list[i].atom1Idx && iaction.getAtom2Index() == ia_list[i].atom2Idx) ||
                    (iaction.getAtom1Index() == ia_list[i].atom2Idx && iaction.getAtom2Index() == ia_list[i].atom1Idx)) {

                    double energy = ForceField::calcMMFF94BondStretchingEnergy<double>(iaction, coords);
        
                    BOOST_CHECK_MESSAGE(std::abs(energy - ia_list[i].energy) < 0.00332, 
                                        "Energy mismatch for bond stretching interaction #" << ia_list[i].atom1Idx << "(" << 
                                        getMOL2Name(mol.getAtom(ia_list[i].atom1Idx)) << ")-#" << ia_list[i].atom2Idx << "(" << 
                                        getMOL2Name(mol.getAtom(ia_list[i].atom2Idx)) << ") of molecule #" << mol_idx << " (" << mol_name <<
                                        "): calc. " << energy << " != " << ia_list[i].energy);
        
                    iaction_found = true;
                    break;
                }
            }

            BOOST_CHECK_MESSAGE(iaction_found, "Bond stretching interaction #" << ia_list[i].atom1Idx << "(" << getMOL2Name(mol.getAtom(ia_list[i].atom1Idx)) << 
                                ")-#" << ia_list[i].atom2Idx << "(" << getMOL2Name(mol.getAtom(ia_list[i].atom2Idx)) << ") of molecule #" << mol_idx << " (" << mol_name <<
                                ") has not been found");
        }

        BOOST_CHECK(MMFF94TestData::DYN_LOG_READER.getEnergies(mol_name, energies));

        double energy = ForceField::calcMMFF94BondStretchingEnergy<double>(found_ia_list.getElementsBegin(), found_ia_list.getElementsEnd(), coords);
        
        //max_en_diff = std::max(max_en_diff, std::abs(energy - energies.bondStretching));
            
        BOOST_CHECK_MESSAGE(std::abs(energy - energies.bondStretching) < 0.00552, 
                            "Total bond stretching energy mismatch for molecule #" << mol_idx << " (" << mol_name <<
                            "): calc. " << energy << " != " << energies.bondStretching);
    }

    //BOOST_MESSAGE("Max. energy difference: " << max_en_diff); 
}

BOOST_AUTO_TEST_CASE(MMFF94AngleBendingEnergyFunctionTest)
{
    using namespace CDPL;
    using namespace Testing;

    OptimolLogReader::AngleBendingInteractionList ia_list;
    OptimolLogReader::EnergyData energies;

    ForceField::MMFF94AngleBendingInteractionParameterizer parameterizer;
    ForceField::MMFF94AngleBendingInteractionList found_ia_list;
    Math::Vector3DArray coords;

    //double max_en_diff = 0;

    for (std::size_t mol_idx = 0; mol_idx < MMFF94TestData::DYN_TEST_MOLECULES.size(); mol_idx++) {
        const Chem::Molecule& mol = *MMFF94TestData::DYN_TEST_MOLECULES[mol_idx];
        const std::string& mol_name = getName(mol);

        BOOST_CHECK(MMFF94TestData::DYN_LOG_READER.getAngleBendingInteractions(mol_name, ia_list));

        parameterizer.parameterize(mol, found_ia_list, true);

        BOOST_CHECK_MESSAGE(found_ia_list.getSize() == ia_list.size(), "Angle bending interaction count mismatch for molecule #" << mol_idx << " (" << mol_name << "): " <<
                            found_ia_list.getSize() << " != " << ia_list.size());

        coords.clear();
        get3DCoordinates(mol, coords);

        for (std::size_t i = 0; i < ia_list.size(); i++) {
            bool iaction_found = false;
            std::size_t term_atom1_idx = TestUtils::getAtomIndex(mol, ia_list[i].termAtom1Name);
            std::size_t term_atom2_idx = TestUtils::getAtomIndex(mol, ia_list[i].termAtom2Name);

            for (std::size_t j = 0; j < found_ia_list.getSize(); j++) {
                const ForceField::MMFF94AngleBendingInteraction& iaction = found_ia_list[j];

                if (iaction.getCenterAtomIndex() != ia_list[i].ctrAtomIdx)
                    continue;

                if ((iaction.getTerminalAtom1Index() == term_atom1_idx && iaction.getTerminalAtom2Index() == term_atom2_idx) ||
                    (iaction.getTerminalAtom1Index() == term_atom2_idx && iaction.getTerminalAtom2Index() == term_atom1_idx)) {
        
                    double energy = ForceField::calcMMFF94AngleBendingEnergy<double>(iaction, coords);
        
                    BOOST_CHECK_MESSAGE(std::abs(energy - ia_list[i].energy) < 0.0376, 
                                        "Energy mismatch for angle bending interaction #" << term_atom1_idx << "(" << 
                                        ia_list[i].termAtom1Name << ")-#" << ia_list[i].ctrAtomIdx << "(" << 
                                        getMOL2Name(mol.getAtom(ia_list[i].ctrAtomIdx)) << ")-#" << term_atom2_idx << "(" << 
                                        ia_list[i].termAtom2Name << ") of molecule #" << mol_idx << " (" << mol_name << "): calc. " << 
                                        energy << " != " << ia_list[i].energy);
        
                    iaction_found = true;
                    break;
                }
            }
        
            BOOST_CHECK_MESSAGE(iaction_found, "Angle bending interaction #" << term_atom1_idx << "(" << 
                                ia_list[i].termAtom1Name << ")-#" << ia_list[i].ctrAtomIdx << "(" << 
                                getMOL2Name(mol.getAtom(ia_list[i].ctrAtomIdx)) << ")-#" << term_atom2_idx << "(" << 
                                ia_list[i].termAtom2Name << ") of molecule #" << mol_idx << " (" << mol_name << ") has not been found");
        }

        BOOST_CHECK(MMFF94TestData::DYN_LOG_READER.getEnergies(mol_name, energies));

        double energy = ForceField::calcMMFF94AngleBendingEnergy<double>(found_ia_list.getElementsBegin(), found_ia_list.getElementsEnd(), coords);
        
        //max_en_diff = std::max(max_en_diff, std::abs(energy - energies.angleBending));
            
        BOOST_CHECK_MESSAGE(std::abs(energy - energies.angleBending) < 0.0704, 
                            "Total angle bending energy mismatch for molecule #" << mol_idx << " (" << mol_name <<
                            "): calc. " << energy << " != " << energies.angleBending);
    }

    //BOOST_MESSAGE("Max. energy difference: " << max_en_diff); 
}

BOOST_AUTO_TEST_CASE(MMFF94StretchBendEnergyFunctionTest)
{
    using namespace CDPL;
    using namespace Testing;

    OptimolLogReader::StretchBendInteractionList ia_list;
    OptimolLogReader::EnergyData energies;

    ForceField::MMFF94AngleBendingInteractionParameterizer ab_parameterizer;
    ForceField::MMFF94BondStretchingInteractionParameterizer bs_parameterizer;
    ForceField::MMFF94StretchBendInteractionParameterizer sb_parameterizer;
    ForceField::MMFF94StretchBendInteractionList found_ia_list;
    ForceField::MMFF94AngleBendingInteractionList ab_ia_list;
    ForceField::MMFF94BondStretchingInteractionList bs_ia_list;
    Math::Vector3DArray coords;

    //double max_en_diff = 0;

    for (std::size_t mol_idx = 0; mol_idx < MMFF94TestData::DYN_TEST_MOLECULES.size(); mol_idx++) {
        const Chem::Molecule& mol = *MMFF94TestData::DYN_TEST_MOLECULES[mol_idx];
        const std::string& mol_name = getName(mol);

        BOOST_CHECK(MMFF94TestData::DYN_LOG_READER.getStretchBendInteractions(mol_name, ia_list));

        for (std::size_t i = 0; i < ia_list.size(); i++) {
            for (std::size_t j = i + 1; j < ia_list.size(); j++) {
                if (ia_list[i].ctrAtomIdx == ia_list[j].ctrAtomIdx &&
                    ia_list[i].termAtom1Name == ia_list[j].termAtom2Name &&
                    ia_list[i].termAtom2Name == ia_list[j].termAtom1Name) {

                    ia_list[i].energy += ia_list[j].energy;

                    ia_list.erase(ia_list.begin() + j);
                    break;
                }
            }
        }

        bs_parameterizer.parameterize(mol, bs_ia_list, true);
        ab_parameterizer.parameterize(mol, ab_ia_list, true);
        sb_parameterizer.parameterize(mol, bs_ia_list, ab_ia_list, found_ia_list, true);

        BOOST_CHECK_MESSAGE(found_ia_list.getSize() == ia_list.size(), "Stretch-bend interaction count mismatch for molecule #" << mol_idx << " (" << mol_name << "): " <<
                            found_ia_list.getSize() << " != " << ia_list.size());

        coords.clear();
        get3DCoordinates(mol, coords);

        for (std::size_t i = 0; i < ia_list.size(); i++) {
            bool iaction_found = false;
            std::size_t term_atom1_idx = TestUtils::getAtomIndex(mol, ia_list[i].termAtom1Name);
            std::size_t term_atom2_idx = TestUtils::getAtomIndex(mol, ia_list[i].termAtom2Name);

            for (std::size_t j = 0; j < found_ia_list.getSize(); j++) {
                const ForceField::MMFF94StretchBendInteraction& iaction = found_ia_list[j];

                if (iaction.getCenterAtomIndex() != ia_list[i].ctrAtomIdx)
                    continue;

                if ((iaction.getTerminalAtom1Index() == term_atom1_idx && iaction.getTerminalAtom2Index() == term_atom2_idx) ||
                    (iaction.getTerminalAtom1Index() == term_atom2_idx && iaction.getTerminalAtom2Index() == term_atom1_idx)) {

                    double energy = ForceField::calcMMFF94StretchBendEnergy<double>(iaction, coords);
        
                    BOOST_CHECK_MESSAGE(std::abs(energy - ia_list[i].energy) < 0.00257, 
                                        "Energy mismatch for stretch-bend interaction #" << term_atom1_idx << "(" << 
                                        ia_list[i].termAtom1Name << ")-#" << ia_list[i].ctrAtomIdx << "(" << 
                                        getMOL2Name(mol.getAtom(ia_list[i].ctrAtomIdx)) << ")-#" << term_atom2_idx << "(" << 
                                        ia_list[i].termAtom2Name << ") of molecule #" << mol_idx << " (" << mol_name << "): calc. " << 
                                        energy << " != " << ia_list[i].energy);

                    iaction_found = true;
                    break;
                }
            }
        
            BOOST_CHECK_MESSAGE(iaction_found, "Stretch-bend interaction #" << term_atom1_idx << "(" << 
                                ia_list[i].termAtom1Name << ")-#" << ia_list[i].ctrAtomIdx << "(" << 
                                getMOL2Name(mol.getAtom(ia_list[i].ctrAtomIdx)) << ")-#" << term_atom2_idx << "(" << 
                                ia_list[i].termAtom2Name << ") of molecule #" << mol_idx << " (" << mol_name << ") has not been found");
        }

        BOOST_CHECK(MMFF94TestData::DYN_LOG_READER.getEnergies(mol_name, energies));

        double energy = ForceField::calcMMFF94StretchBendEnergy<double>(found_ia_list.getElementsBegin(), found_ia_list.getElementsEnd(), coords);
        
        //max_en_diff = std::max(max_en_diff, std::abs(energy - energies.stretchBend));
            
        BOOST_CHECK_MESSAGE(std::abs(energy - energies.stretchBend) < 0.00422, 
                            "Total stretch-bend energy mismatch for molecule #" << mol_idx << " (" << mol_name <<
                            "): calc. " << energy << " != " << energies.stretchBend);
    }  

    //BOOST_MESSAGE("Max. energy difference: " << max_en_diff); 
}

BOOST_AUTO_TEST_CASE(MMFF94OutOfPlaneBendingEnergyFunctionTest)
{
    using namespace CDPL;
    using namespace Testing;

    OptimolLogReader::OutOfPlaneBendingInteractionList ia_list;
    OptimolLogReader::EnergyData energies;

    ForceField::MMFF94OutOfPlaneBendingInteractionParameterizer parameterizer;
    ForceField::MMFF94OutOfPlaneBendingInteractionList found_ia_list;
    Math::Vector3DArray coords;

    //double max_en_diff = 0;

    for (bool stat = false; !stat; stat = true) {
        OptimolLogReader& log_reader = (stat ? MMFF94TestData::STAT_LOG_READER : MMFF94TestData::DYN_LOG_READER);
        const MMFF94TestData::MoleculeList& mols = (stat ? MMFF94TestData::STAT_TEST_MOLECULES : MMFF94TestData::DYN_TEST_MOLECULES);

        parameterizer.setOutOfPlaneBendingParameterTable(ForceField::MMFF94OutOfPlaneBendingParameterTable::get(stat));

        for (std::size_t mol_idx = 0; mol_idx < mols.size(); mol_idx++) {
            const Chem::Molecule& mol = *mols[mol_idx];
            const std::string& mol_name = getName(mol);

            BOOST_CHECK(log_reader.getOutOfPlaneBendingInteractions(mol_name, ia_list));

            parameterizer.parameterize(mol, found_ia_list, true);

            BOOST_CHECK_MESSAGE(found_ia_list.getSize() == ia_list.size(), "Out-Of-Plane bending interaction count mismatch for molecule #" << mol_idx << " (" << mol_name << "): " <<
                                found_ia_list.getSize() << " != " << ia_list.size());

            coords.clear();
            get3DCoordinates(mol, coords);

            for (std::size_t i = 0; i < ia_list.size(); i++) {
                bool iaction_found = false;
                std::size_t term_atom1_idx = TestUtils::getAtomIndex(mol, ia_list[i].termAtom1Name);
                std::size_t term_atom2_idx = TestUtils::getAtomIndex(mol, ia_list[i].termAtom2Name);
                std::size_t ctr_atom_idx = TestUtils::getAtomIndex(mol, ia_list[i].ctrAtomName);

                for (std::size_t j = 0; j < found_ia_list.getSize(); j++) {
                    const ForceField::MMFF94OutOfPlaneBendingInteraction& iaction = found_ia_list[j];

                    if (iaction.getCenterAtomIndex() != ctr_atom_idx)
                        continue;

                    if (iaction.getOutOfPlaneAtomIndex() != ia_list[i].oopAtomIdx)
                        continue;

                    if ((iaction.getTerminalAtom1Index() == term_atom1_idx && iaction.getTerminalAtom2Index() == term_atom2_idx) ||
                        (iaction.getTerminalAtom1Index() == term_atom2_idx && iaction.getTerminalAtom2Index() == term_atom1_idx)) {

                        double energy = ForceField::calcMMFF94OutOfPlaneBendingEnergy<double>(iaction, coords);

                        BOOST_CHECK_MESSAGE(std::abs(energy - ia_list[i].energy) < 0.0009, 
                                            "Energy mismatch for out-of-plane bending interaction <#" << term_atom1_idx << "(" << 
                                            ia_list[i].termAtom1Name << ")-#" << ctr_atom_idx << "(" << 
                                            ia_list[i].ctrAtomName << ")-#" << term_atom2_idx << "(" << 
                                            ia_list[i].termAtom2Name << ")>~#" << ia_list[i].oopAtomIdx << "(" << 
                                            getMOL2Name(mol.getAtom(ia_list[i].oopAtomIdx)) << ") of molecule #" << mol_idx << 
                                            " (" << mol_name << "): calc. " << energy << " != " << energy);

                        iaction_found = true;
                        break;
                    }
                }
        
                BOOST_CHECK_MESSAGE(iaction_found, "Out-Of-Plane bending interaction <#" << term_atom1_idx << "(" << 
                                    ia_list[i].termAtom1Name << ")-#" << ctr_atom_idx << "(" << 
                                    ia_list[i].ctrAtomName << ")-#" << term_atom2_idx << "(" << 
                                    ia_list[i].termAtom2Name << ")>~#" << ia_list[i].oopAtomIdx << "(" << 
                                    getMOL2Name(mol.getAtom(ia_list[i].oopAtomIdx)) << ") of molecule #" << mol_idx << 
                                    " (" << mol_name << ") has not been found");
            }

            BOOST_CHECK(log_reader.getEnergies(mol_name, energies));

            double energy = ForceField::calcMMFF94OutOfPlaneBendingEnergy<double>(found_ia_list.getElementsBegin(), found_ia_list.getElementsEnd(), coords);
        
            //max_en_diff = std::max(max_en_diff, std::abs(energy - energies.outOfPlaneBending));
            
            BOOST_CHECK_MESSAGE(std::abs(energy - energies.outOfPlaneBending) < 0.00168, 
                                "Total out-of-plane bending energy mismatch for molecule #" << mol_idx << " (" << mol_name <<
                                "): calc. " << energy << " != " << energies.outOfPlaneBending);
        }
    }

    //BOOST_MESSAGE("Max. energy difference: " << max_en_diff); 
}

BOOST_AUTO_TEST_CASE(MMFF94TorsionEnergyFunctionTest)
{
    using namespace CDPL;
    using namespace Testing;

    OptimolLogReader::TorsionInteractionList ia_list;
    OptimolLogReader::EnergyData energies;

    ForceField::MMFF94TorsionInteractionParameterizer parameterizer;
    ForceField::MMFF94TorsionInteractionList found_ia_list;
    Math::Vector3DArray coords;

    //double max_en_diff = 0;

    for (bool stat = false; !stat; stat = true) {
        OptimolLogReader& log_reader = (stat ? MMFF94TestData::STAT_LOG_READER : MMFF94TestData::DYN_LOG_READER);
        const MMFF94TestData::MoleculeList& mols = (stat ? MMFF94TestData::STAT_TEST_MOLECULES : MMFF94TestData::DYN_TEST_MOLECULES);

        parameterizer.setTorsionParameterTable(ForceField::MMFF94TorsionParameterTable::get(stat));

        for (std::size_t mol_idx = 0; mol_idx <    mols.size(); mol_idx++) {
            const Chem::Molecule& mol =    *mols[mol_idx];
            const std::string& mol_name = getName(mol);

            BOOST_CHECK(log_reader.getTorsionInteractions(mol_name, ia_list));

            parameterizer.parameterize(mol, found_ia_list, true);

            BOOST_CHECK_MESSAGE(found_ia_list.getSize() == ia_list.size(), "Torsion interaction count mismatch for molecule #" << mol_idx << " (" << mol_name << "): " <<
                                found_ia_list.getSize() << " != " << ia_list.size());

            coords.clear();
            get3DCoordinates(mol, coords);

            for (std::size_t i = 0; i < ia_list.size(); i++) {
                bool iaction_found = false;
                std::size_t term_atom1_idx = TestUtils::getAtomIndex(mol, ia_list[i].termAtom1Name);
                std::size_t term_atom2_idx = TestUtils::getAtomIndex(mol, ia_list[i].termAtom2Name);

                for (std::size_t j = 0; j < found_ia_list.getSize(); j++) {
                    const ForceField::MMFF94TorsionInteraction& iaction = found_ia_list[j];

                    if (!((iaction.getTerminalAtom1Index() == term_atom1_idx && iaction.getCenterAtom1Index() == ia_list[i].ctrAtom1Idx && 
                           iaction.getCenterAtom2Index() == ia_list[i].ctrAtom2Idx && iaction.getTerminalAtom2Index() == term_atom2_idx) ||
                          (iaction.getTerminalAtom2Index() == term_atom1_idx && iaction.getCenterAtom2Index() == ia_list[i].ctrAtom1Idx && 
                           iaction.getCenterAtom1Index() == ia_list[i].ctrAtom2Idx && iaction.getTerminalAtom1Index() == term_atom2_idx)))
                        continue;

                    double energy = ForceField::calcMMFF94TorsionEnergy<double>(iaction, coords);
        
                    BOOST_CHECK_MESSAGE(std::abs(energy - ia_list[i].energy) < 0.00122, 
                                        "Energy mismatch for torsion interaction #" << term_atom1_idx << "(" << 
                                        ia_list[i].termAtom1Name << ")-#" << ia_list[i].ctrAtom1Idx << "(" << 
                                        getMOL2Name(mol.getAtom(ia_list[i].ctrAtom1Idx)) << ")-#" << ia_list[i].ctrAtom2Idx << "(" << 
                                        getMOL2Name(mol.getAtom(ia_list[i].ctrAtom2Idx)) << ")-#" << term_atom2_idx << "(" << 
                                        ia_list[i].termAtom2Name << ") of molecule #" << mol_idx << 
                                        " (" << mol_name << "): calc. " << energy << " != " << ia_list[i].energy);
    
                    iaction_found = true;
                    break;
                }
        
                BOOST_CHECK_MESSAGE(iaction_found, "Torsion interaction #" << term_atom1_idx << "(" << 
                                    ia_list[i].termAtom1Name << ")-#" << ia_list[i].ctrAtom1Idx << "(" << 
                                    getMOL2Name(mol.getAtom(ia_list[i].ctrAtom1Idx)) << ")-#" << ia_list[i].ctrAtom2Idx << "(" << 
                                    getMOL2Name(mol.getAtom(ia_list[i].ctrAtom2Idx)) << ")-#" << term_atom2_idx << "(" << 
                                    ia_list[i].termAtom2Name << ") of molecule #" << mol_idx << 
                                    " (" << mol_name << ") has not been found");
            }

            BOOST_CHECK(log_reader.getEnergies(mol_name, energies));

            double energy = ForceField::calcMMFF94TorsionEnergy<double>(found_ia_list.getElementsBegin(), found_ia_list.getElementsEnd(), coords);
        
            //max_en_diff = std::max(max_en_diff, std::abs(energy - energies.torsion));
            
            BOOST_CHECK_MESSAGE(std::abs(energy - energies.torsion) < 0.00141, 
                                "Total torsion energy mismatch for molecule #" << mol_idx << " (" << mol_name <<
                                "): calc. " << energy << " != " << energies.torsion);
        }
    }

    //BOOST_MESSAGE("Max. energy difference: " << max_en_diff); 
}

BOOST_AUTO_TEST_CASE(MMFF94VanDerWaalsEnergyFunctionTest)
{
    using namespace CDPL;
    using namespace Testing;

    OptimolLogReader::VanDerWaalsInteractionList ia_list;
    OptimolLogReader::EnergyData energies;

    ForceField::MMFF94VanDerWaalsInteractionParameterizer parameterizer;
    ForceField::MMFF94VanDerWaalsInteractionList found_ia_list;
    Math::Vector3DArray coords;

    //double max_en_diff = 0;

    for (std::size_t mol_idx = 0; mol_idx < MMFF94TestData::DYN_TEST_MOLECULES.size(); mol_idx++) {
        const Chem::Molecule& mol = *MMFF94TestData::DYN_TEST_MOLECULES[mol_idx];
        const std::string& mol_name = getName(mol);

        BOOST_CHECK(MMFF94TestData::DYN_LOG_READER.getVanDerWaalsInteractions(mol_name, ia_list));

        parameterizer.parameterize(mol, found_ia_list, true);

        //BOOST_CHECK_MESSAGE(found_ia_list.getSize() == ia_list.size(), "Van der Waals interaction count mismatch for molecule #" << mol_idx << " (" << mol_name << "): " <<
        //                    found_ia_list.getSize() << " != " << ia_list.size());
    
        coords.clear();
        get3DCoordinates(mol, coords);

        for (std::size_t i = 0; i < ia_list.size(); i++) {
            bool iaction_found = false;

            for (std::size_t j = 0; j < found_ia_list.getSize(); j++) {
                const ForceField::MMFF94VanDerWaalsInteraction& iaction = found_ia_list[j];

                if ((iaction.getAtom1Index() == ia_list[i].atom1Idx && iaction.getAtom2Index() == ia_list[i].atom2Idx) ||
                    (iaction.getAtom1Index() == ia_list[i].atom2Idx && iaction.getAtom2Index() == ia_list[i].atom1Idx)) {

                    double energy = ForceField::calcMMFF94VanDerWaalsEnergy<double>(iaction, coords);
           
                    BOOST_CHECK_MESSAGE(std::abs(energy - ia_list[i].energy) < 0.00415, 
                                        "Energy mismatch for van der Waals interaction #" << ia_list[i].atom1Idx << "(" << 
                                        getMOL2Name(mol.getAtom(ia_list[i].atom1Idx)) << ")-#" << ia_list[i].atom2Idx << "(" << 
                                        getMOL2Name(mol.getAtom(ia_list[i].atom2Idx)) << ") of molecule #" << mol_idx << " (" << mol_name <<
                                        "): calc. " << energy << " != " << ia_list[i].energy);

                    iaction_found = true;
                    break;
                }
            }
        
            BOOST_CHECK_MESSAGE(iaction_found, "Van der Waals interaction #" << ia_list[i].atom1Idx << "(" << getMOL2Name(mol.getAtom(ia_list[i].atom1Idx)) << 
                                ")-#" << ia_list[i].atom2Idx << "(" << getMOL2Name(mol.getAtom(ia_list[i].atom2Idx)) << ") of molecule #" << mol_idx << " (" << mol_name <<
                                ") has not been found");
        }

        BOOST_CHECK(MMFF94TestData::DYN_LOG_READER.getEnergies(mol_name, energies));

        double energy = ForceField::calcMMFF94VanDerWaalsEnergy<double>(found_ia_list.getElementsBegin(), found_ia_list.getElementsEnd(), coords);
        
        //max_en_diff = std::max(max_en_diff, std::abs(energy - energies.vanDerWaals));
            
        BOOST_CHECK_MESSAGE(std::abs(energy - energies.vanDerWaals) < 0.00621, 
                            "Total van der Waals energy mismatch for molecule #" << mol_idx << " (" << mol_name <<
                            "): calc. " << energy << " != " << energies.vanDerWaals);
    }

    //BOOST_MESSAGE("Max. energy difference: " << max_en_diff); 
}

BOOST_AUTO_TEST_CASE(MMFF94ElectrostaticEnergyFunctionTest)
{
    using namespace CDPL;
    using namespace Testing;

    OptimolLogReader::EnergyData energies;

    ForceField::MMFF94ElectrostaticInteractionParameterizer parameterizer;
    ForceField::MMFF94ElectrostaticInteractionList found_ia_list;
    Math::Vector3DArray coords;

    //double max_en_diff = 0;

    for (std::size_t mol_idx = 0; mol_idx < MMFF94TestData::DYN_TEST_MOLECULES.size(); mol_idx++) {
        Chem::Molecule& mol = *MMFF94TestData::DYN_TEST_MOLECULES[mol_idx];
        const std::string& mol_name = getName(mol);

        BOOST_CHECK(MMFF94TestData::DYN_LOG_READER.getEnergies(mol_name, energies));

        ForceField::calcMMFF94AtomCharges(mol, true, false);

        parameterizer.parameterize(mol, found_ia_list, true);
    
        coords.clear();
        get3DCoordinates(mol, coords);

        double energy = ForceField::calcMMFF94ElectrostaticEnergy<double>(found_ia_list.getElementsBegin(), found_ia_list.getElementsEnd(), coords);

        //max_en_diff = std::max(max_en_diff, std::abs(energy - energies.electrostatic));
            
        BOOST_CHECK_MESSAGE(std::abs(energy - energies.electrostatic) < 0.0075, 
                            "Total electrostatic energy mismatch for molecule #" << mol_idx << " (" << mol_name <<
                            "): calc. " << energy << " != " << energies.electrostatic);
    }

    //BOOST_MESSAGE("Max. energy difference: " << max_en_diff);
}

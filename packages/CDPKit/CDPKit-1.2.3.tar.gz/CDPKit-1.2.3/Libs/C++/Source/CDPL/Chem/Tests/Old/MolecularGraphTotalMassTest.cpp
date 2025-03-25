/* 
 * MolecularGraphTotalMassTest.cpp 
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


#include <string>
#include <cstdlib>
#include <fstream>

#include <boost/test/auto_unit_test.hpp>
#include <boost/test/floating_point_comparison.hpp>

#include "CDPL/Chem/Molecule.hpp"
#include "CDPL/Chem/JMEMoleculeReader.hpp"
#include "CDPL/Chem/MolecularGraphProperties.hpp"
#include "CDPL/Chem/AtomContainerProperties.hpp"

#include "TestUtils.hpp"


BOOST_AUTO_TEST_CASE(MolecularGraphTotalMassTest)
{
    using namespace CDPL;
    using namespace Chem;

    Molecule mol;

//-----

    BOOST_CHECK(mol.getProperty(MolecularGraphProperty::TOTAL_MASS, false, false).isEmpty());

    BOOST_CHECK_SMALL(mol.getProperty<double>(MolecularGraphProperty::TOTAL_MASS), 0.000001);

    BOOST_CHECK(!mol.getProperty(MolecularGraphProperty::TOTAL_MASS, false, false).isEmpty());

//-----

    std::ifstream ifs(std::string(std::string(std::getenv("CDPKIT_TEST_DATA_DIR")) + "/Morphine.jme").c_str());

    BOOST_CHECK(ifs);

    BOOST_CHECK(JMEMoleculeReader(ifs).read(mol));

//-----

    BOOST_CHECK(mol.getProperty(MolecularGraphProperty::TOTAL_MASS, false, false).isEmpty());

    BOOST_CHECK_CLOSE(mol.getProperty<double>(MolecularGraphProperty::TOTAL_MASS), 285.349, 0.01);

    BOOST_CHECK(!mol.getProperty(MolecularGraphProperty::TOTAL_MASS, false, false).isEmpty());

//-----

    TestUtils::checkDependency(mol, MolecularGraphProperty::TOTAL_MASS, mol, AtomContainerProperty::MASS);
    TestUtils::checkDependency(mol, MolecularGraphProperty::TOTAL_MASS, mol, MolecularGraphProperty::IMPLICIT_H_COUNT);
}

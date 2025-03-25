/* 
 * AtomTypeTest.cpp 
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

#include <boost/test/auto_unit_test.hpp>

#include "CDPL/Chem/Molecule.hpp"
#include "CDPL/Chem/Atom.hpp"
#include "CDPL/Chem/AtomProperties.hpp"
#include "CDPL/Chem/AtomTypeDB.hpp"
#include "CDPL/Chem/AtomTypes.hpp"


BOOST_AUTO_TEST_CASE(AtomTypeTest)
{
    using namespace CDPL;
    using namespace Chem;
   
    Molecule mol;
    Atom& atom = mol.addAtom();

    BOOST_CHECK(atom.getProperty(AtomProperty::TYPE, false, false).isEmpty());

    BOOST_CHECK(atom.getProperty<unsigned int>(AtomProperty::TYPE) == AtomType::UNKNOWN);

    BOOST_CHECK(!atom.getProperty(AtomProperty::TYPE, false, false).isEmpty());

    BOOST_CHECK(!atom.getProperty(AtomProperty::SYMBOL, false, false).isEmpty());

    BOOST_CHECK(atom.getProperty<std::string>(AtomProperty::SYMBOL) == "");

//-----

    atom.setProperty(AtomProperty::SYMBOL, std::string("C"));
    atom.setProperty(AtomProperty::TYPE, AtomType::N);

    BOOST_CHECK(!atom.getProperty(AtomProperty::TYPE, false, false).isEmpty());
    BOOST_CHECK(!atom.getProperty(AtomProperty::SYMBOL, false, false).isEmpty());

    BOOST_CHECK(atom.getProperty<unsigned int>(AtomProperty::TYPE) == AtomType::N);

    BOOST_CHECK(!atom.getProperty(AtomProperty::TYPE, false, false).isEmpty());
    BOOST_CHECK(!atom.getProperty(AtomProperty::SYMBOL, false, false).isEmpty());

    BOOST_CHECK(atom.getProperty<std::string>(AtomProperty::SYMBOL) == "C");

    BOOST_CHECK(!atom.getProperty(AtomProperty::SYMBOL, false, false).isEmpty());
    BOOST_CHECK(!atom.getProperty(AtomProperty::TYPE, false, false).isEmpty());

    atom.removeProperty(AtomProperty::TYPE);

//-----

    for (unsigned int atom_type = 0; atom_type < AtomType::MAX_TYPE + 10; atom_type++) {
        atom.setProperty(AtomProperty::SYMBOL, AtomTypeDB::getSymbol(atom_type));

        BOOST_CHECK(atom.getProperty(AtomProperty::TYPE, false, false).isEmpty());
    
        BOOST_CHECK(atom.getProperty<unsigned int>(AtomProperty::TYPE) == (atom_type > AtomType::MAX_TYPE ? AtomType::UNKNOWN : atom_type));

        BOOST_CHECK(!atom.getProperty(AtomProperty::TYPE, false, false).isEmpty());
    }
}


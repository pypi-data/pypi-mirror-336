/* 
 * MOL2MoleculeTypeExport.cpp 
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


#include <boost/python.hpp>

#include "CDPL/Chem/MOL2MoleculeType.hpp"

#include "NamespaceExports.hpp"


namespace 
{

    struct MOL2MoleculeType {};
}


void CDPLPythonChem::exportMOL2MoleculeTypes()
{
    using namespace boost;
    using namespace CDPL;

    python::class_<MOL2MoleculeType, boost::noncopyable>("MOL2MoleculeType", python::no_init)
        .def_readonly("UNKNOWN", &Chem::MOL2MoleculeType::UNKNOWN)
        .def_readonly("SMALL", &Chem::MOL2MoleculeType::SMALL)
        .def_readonly("BIOPOLYMER", &Chem::MOL2MoleculeType::BIOPOLYMER)
        .def_readonly("PROTEIN", &Chem::MOL2MoleculeType::PROTEIN)
        .def_readonly("NUCLEIC_ACID", &Chem::MOL2MoleculeType::NUCLEIC_ACID)
        .def_readonly("SACCHARIDE", &Chem::MOL2MoleculeType::SACCHARIDE);
}

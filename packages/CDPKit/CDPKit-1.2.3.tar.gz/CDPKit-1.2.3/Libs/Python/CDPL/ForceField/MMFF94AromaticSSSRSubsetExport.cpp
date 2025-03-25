/* 
 * MMFF94AromaticSSSRSubsetExport.cpp 
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

#include "CDPL/ForceField/MMFF94AromaticSSSRSubset.hpp"
#include "CDPL/Chem/MolecularGraph.hpp"

#include "ClassExports.hpp"


void CDPLPythonForceField::exportMMFF94AromaticSSSRSubset()
{
    using namespace boost;
    using namespace CDPL;

    python::class_<ForceField::MMFF94AromaticSSSRSubset, ForceField::MMFF94AromaticSSSRSubset::SharedPointer,
                   python::bases<Chem::FragmentList>, boost::noncopyable>("MMFF94AromaticSSSRSubset", python::no_init)
        .def(python::init<>(python::arg("self")))
        .def(python::init<const Chem::MolecularGraph&>((python::arg("self"), python::arg("molgraph")))
             [python::with_custodian_and_ward<1, 2>()])
        .def("extract", static_cast<void (ForceField::MMFF94AromaticSSSRSubset::*)(const Chem::MolecularGraph&)>
             (&ForceField::MMFF94AromaticSSSRSubset::extract), (python::arg("self"), python::arg("molgraph")), 
             python::with_custodian_and_ward<1, 2>())
        .def("extract", static_cast<void (ForceField::MMFF94AromaticSSSRSubset::*)(const Chem::MolecularGraph&, const Chem::FragmentList&)>
             (&ForceField::MMFF94AromaticSSSRSubset::extract), (python::arg("self"), python::arg("molgraph"), python::arg("sssr")), 
             python::with_custodian_and_ward<1, 2>());
}

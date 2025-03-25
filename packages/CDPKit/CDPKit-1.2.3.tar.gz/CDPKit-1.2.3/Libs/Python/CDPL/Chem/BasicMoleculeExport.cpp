/* 
 * BasicMoleculeExport.cpp 
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

#include "CDPL/Chem/BasicMolecule.hpp"

#include "ClassExports.hpp"


void CDPLPythonChem::exportBasicMolecule()
{
    using namespace boost;
    using namespace CDPL;

    void (Chem::BasicMolecule::*copyBasicMolFunc)(const Chem::BasicMolecule&) = &Chem::BasicMolecule::copy;
    void (Chem::BasicMolecule::*copyMolFunc)(const Chem::Molecule&) = &Chem::BasicMolecule::copy;
    void (Chem::BasicMolecule::*copyMolGraphFunc)(const Chem::MolecularGraph&) = &Chem::BasicMolecule::copy;

    void (Chem::BasicMolecule::*appendBasicMolFunc)(const Chem::BasicMolecule&) = &Chem::BasicMolecule::append;
    void (Chem::BasicMolecule::*appendMolFunc)(const Chem::Molecule&) = &Chem::BasicMolecule::append;
    void (Chem::BasicMolecule::*appendMolGraphFunc)(const Chem::MolecularGraph&) = &Chem::BasicMolecule::append;

    Chem::BasicMolecule& (Chem::BasicMolecule::*assignBasicMolFunc)(const Chem::BasicMolecule&) = &Chem::BasicMolecule::operator=;
    Chem::Molecule& (Chem::Molecule::*assignMolFunc)(const Chem::Molecule&) = &Chem::Molecule::operator=;
    Chem::Molecule& (Chem::Molecule::*assignMolGraphFunc)(const Chem::MolecularGraph&) = &Chem::Molecule::operator=;

    Chem::BasicMolecule& (Chem::BasicMolecule::*addBasicMolFunc)(const Chem::BasicMolecule&) = &Chem::BasicMolecule::operator+=;
    Chem::Molecule& (Chem::Molecule::*addMolFunc)(const Chem::Molecule&) = &Chem::Molecule::operator+=;
    Chem::Molecule& (Chem::Molecule::*addMolGraphFunc)(const Chem::MolecularGraph&) = &Chem::Molecule::operator+=;

    python::class_<Chem::BasicMolecule, Chem::BasicMolecule::SharedPointer,
                   python::bases<Chem::Molecule> >("BasicMolecule", python::no_init)
        .def(python::init<>(python::arg("self")))
        .def(python::init<const Chem::BasicMolecule&>((python::arg("self"), python::arg("mol"))))
        .def(python::init<const Chem::Molecule&>((python::arg("self"), python::arg("mol"))))
        .def(python::init<const Chem::MolecularGraph&>((python::arg("self"), python::arg("molgraph"))))
        .def("copy", copyBasicMolFunc, (python::arg("self"), python::arg("mol")))
        .def("copy", copyMolFunc, (python::arg("self"), python::arg("mol")))
        .def("copy", copyMolGraphFunc, (python::arg("self"), python::arg("molgraph")))
        .def("append", appendBasicMolFunc, (python::arg("self"), python::arg("mol")))
        .def("append", appendMolFunc, (python::arg("self"), python::arg("mol")))
        .def("append", appendMolGraphFunc, (python::arg("self"), python::arg("molgraph")))
        .def("assign", assignBasicMolFunc, (python::arg("self"), python::arg("mol")), python::return_self<>())
        .def("assign", assignMolFunc, (python::arg("self"), python::arg("mol")), python::return_self<>())
        .def("assign", assignMolGraphFunc, (python::arg("self"), python::arg("molgraph")), python::return_self<>())
        .def("__iadd__", addBasicMolFunc, (python::arg("self"), python::arg("mol")), python::return_self<>())
        .def("__iadd__", addMolFunc, (python::arg("self"), python::arg("mol")), python::return_self<>())
        .def("__iadd__", addMolGraphFunc, (python::arg("self"), python::arg("molgraph")), python::return_self<>());
}

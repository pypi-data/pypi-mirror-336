/* 
 * MMTFMoleculeReaderExport.cpp 
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

#include "CDPL/Biomol/MMTFMoleculeReader.hpp"
#include "CDPL/Biomol/MMTFGZMoleculeReader.hpp"
#include "CDPL/Biomol/MMTFBZ2MoleculeReader.hpp"
#include "CDPL/Util/FileDataReader.hpp"

#include "ClassExports.hpp"


void CDPLPythonBiomol::exportMMTFMoleculeReader()
{
    using namespace boost;
    using namespace CDPL;

    python::class_<Biomol::MMTFMoleculeReader, python::bases<Base::DataReader<Chem::Molecule> >, 
        boost::noncopyable>("MMTFMoleculeReader", python::no_init)
        .def(python::init<std::istream&>((python::arg("self"), python::arg("is")))
             [python::with_custodian_and_ward<1, 2>()]);

    python::class_<Util::FileDataReader<Biomol::MMTFMoleculeReader>, python::bases<Base::DataReader<Chem::Molecule> >, 
        boost::noncopyable>("FileMMTFMoleculeReader", python::no_init)
        .def(python::init<const std::string&, std::ios_base::openmode>(
                 (python::arg("self"), python::arg("file_name"), python::arg("mode") = std::ios_base::in | std::ios_base::binary)));

    python::class_<Biomol::MMTFGZMoleculeReader, python::bases<Base::DataReader<Chem::Molecule> >, 
        boost::noncopyable>("MMTFGZMoleculeReader", python::no_init)
        .def(python::init<std::istream&>((python::arg("self"), python::arg("is")))
             [python::with_custodian_and_ward<1, 2>()]);

    python::class_<Util::FileDataReader<Biomol::MMTFGZMoleculeReader>, python::bases<Base::DataReader<Chem::Molecule> >, 
        boost::noncopyable>("FileMMTFGZMoleculeReader", python::no_init)
        .def(python::init<const std::string&, std::ios_base::openmode>(
                 (python::arg("self"), python::arg("file_name"), python::arg("mode") = std::ios_base::in | std::ios_base::binary)));

    python::class_<Biomol::MMTFBZ2MoleculeReader, python::bases<Base::DataReader<Chem::Molecule> >, 
        boost::noncopyable>("MMTFBZ2MoleculeReader", python::no_init)
        .def(python::init<std::istream&>((python::arg("self"), python::arg("is")))
             [python::with_custodian_and_ward<1, 2>()]);

    python::class_<Util::FileDataReader<Biomol::MMTFBZ2MoleculeReader>, python::bases<Base::DataReader<Chem::Molecule> >, 
        boost::noncopyable>("FileMMTFBZ2MoleculeReader", python::no_init)
        .def(python::init<const std::string&, std::ios_base::openmode>(
                 (python::arg("self"), python::arg("file_name"), python::arg("mode") = std::ios_base::in | std::ios_base::binary)));
}

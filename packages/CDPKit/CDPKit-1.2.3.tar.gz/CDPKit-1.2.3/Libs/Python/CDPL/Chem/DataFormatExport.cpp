/* 
 * DataFormatExport.cpp 
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

#include "CDPL/Chem/DataFormat.hpp"
#include "CDPL/Base/DataFormat.hpp"

#include "NamespaceExports.hpp"


namespace 
{

    struct DataFormat {};
}


void CDPLPythonChem::exportDataFormats()
{
    using namespace boost;
    using namespace CDPL;

    python::class_<DataFormat, boost::noncopyable>("DataFormat", python::no_init)
        .def_readonly("JME", &Chem::DataFormat::JME)
        .def_readonly("CDF", &Chem::DataFormat::CDF)
        .def_readonly("CDF_GZ", &Chem::DataFormat::CDF_GZ)
        .def_readonly("CDF_BZ2", &Chem::DataFormat::CDF_BZ2)
        .def_readonly("MOL", &Chem::DataFormat::MOL)
        .def_readonly("RDF", &Chem::DataFormat::RDF)
        .def_readonly("RDF_GZ", &Chem::DataFormat::RDF_GZ)
        .def_readonly("RDF_BZ2", &Chem::DataFormat::RDF_BZ2)
        .def_readonly("RXN", &Chem::DataFormat::RXN)
        .def_readonly("SDF", &Chem::DataFormat::SDF)
        .def_readonly("SDF_GZ", &Chem::DataFormat::SDF_GZ)
        .def_readonly("SDF_BZ2", &Chem::DataFormat::SDF_BZ2)
        .def_readonly("SMARTS", &Chem::DataFormat::SMARTS)
        .def_readonly("SMILES", &Chem::DataFormat::SMILES)
        .def_readonly("SMILES_GZ", &Chem::DataFormat::SMILES_GZ)
        .def_readonly("SMILES_BZ2", &Chem::DataFormat::SMILES_BZ2)
        .def_readonly("INCHI", &Chem::DataFormat::INCHI)
        .def_readonly("MOL2", &Chem::DataFormat::MOL2)
        .def_readonly("MOL2_GZ", &Chem::DataFormat::MOL2_GZ)
        .def_readonly("MOL2_BZ2", &Chem::DataFormat::MOL2_BZ2)
        .def_readonly("XYZ", &Chem::DataFormat::XYZ)
        .def_readonly("XYZ_GZ", &Chem::DataFormat::XYZ_GZ)
        .def_readonly("XYZ_BZ2", &Chem::DataFormat::XYZ_BZ2)
        .def_readonly("CML", &Chem::DataFormat::CML)
        .def_readonly("CML_GZ", &Chem::DataFormat::CML_GZ)
        .def_readonly("CML_BZ2", &Chem::DataFormat::CML_BZ2)
        ;
}

/* 
 * DefaultPharmacophoreGeneratorExport.cpp 
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

#include "CDPL/Pharm/DefaultPharmacophoreGenerator.hpp"
#include "CDPL/Chem/MolecularGraph.hpp"
#include "CDPL/Pharm/Pharmacophore.hpp"

#include "ClassExports.hpp"


void CDPLPythonPharm::exportDefaultPharmacophoreGenerator()
{
    using namespace boost;
    using namespace CDPL;

    python::class_<Pharm::DefaultPharmacophoreGenerator, python::bases<Pharm::PharmacophoreGenerator>,
                   boost::noncopyable> cls("DefaultPharmacophoreGenerator", python::no_init);
    python::scope scope = cls;

    python::enum_<Pharm::DefaultPharmacophoreGenerator::Configuration>("Configuration")
        .value("PI_NI_ON_CHARGED_GROUPS_ONLY", Pharm::DefaultPharmacophoreGenerator::PI_NI_ON_CHARGED_GROUPS_ONLY)
        .value("STATIC_H_DONORS", Pharm::DefaultPharmacophoreGenerator::STATIC_H_DONORS)
        .value("DEFAULT_CONFIG", Pharm::DefaultPharmacophoreGenerator::DEFAULT_CONFIG)
        .export_values();

    cls
        .def(python::init<int>((python::arg("self"), python::arg("config") = Pharm::DefaultPharmacophoreGenerator::DEFAULT_CONFIG)))
        .def(python::init<const Chem::MolecularGraph&, Pharm::Pharmacophore&, int>(
                 (python::arg("self"), python::arg("molgraph"), python::arg("pharm"),
                  python::arg("config") = Pharm::DefaultPharmacophoreGenerator::DEFAULT_CONFIG)))
        .def(python::init<const Pharm::DefaultPharmacophoreGenerator&>((python::arg("self"), python::arg("gen"))))
        .def("applyConfiguration", &Pharm::DefaultPharmacophoreGenerator::applyConfiguration, (python::arg("self"), python::arg("config")));
}

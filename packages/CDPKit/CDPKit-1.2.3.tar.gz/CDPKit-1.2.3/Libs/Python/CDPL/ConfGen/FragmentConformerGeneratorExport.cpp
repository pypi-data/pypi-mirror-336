/* 
 * FragmentConformerGeneratorExport.cpp 
 *
 * This file is part of the Utilical Data Processing Toolkit
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

#include "CDPL/ConfGen/FragmentConformerGenerator.hpp"
#include "CDPL/Chem/MolecularGraph.hpp"

#include "Base/ObjectIdentityCheckVisitor.hpp"
//#include "Base/CopyAssOp.hpp"

#include "ClassExports.hpp"


void CDPLPythonConfGen::exportFragmentConformerGenerator()
{
    using namespace boost;
    using namespace CDPL;

    python::class_<ConfGen::FragmentConformerGenerator, boost::noncopyable>("FragmentConformerGenerator", python::no_init)
        .def(python::init<>(python::arg("self")))
//        .def(python::init<const ConfGen::FragmentConformerGenerator&>((python::arg("self"), python::arg("gen"))))
        .def(CDPLPythonBase::ObjectIdentityCheckVisitor<ConfGen::FragmentConformerGenerator>())
//        .def("assign", CDPLPythonBase::copyAssOp<ConfGen::FragmentConformerGenerator>(), 
//             (python::arg("self"), python::arg("gen")), python::return_self<>())
        .def("setAbortCallback", &ConfGen::FragmentConformerGenerator::setAbortCallback, 
             (python::arg("self"), python::arg("func")))
        .def("getAbortCallback", &ConfGen::FragmentConformerGenerator::getAbortCallback, 
             python::arg("self"), python::return_internal_reference<>())
        .def("setTimeoutCallback", &ConfGen::FragmentConformerGenerator::setTimeoutCallback, 
             (python::arg("self"), python::arg("func")))
        .def("getTimeoutCallback", &ConfGen::FragmentConformerGenerator::getTimeoutCallback, 
             python::arg("self"), python::return_internal_reference<>())
        .def("setLogMessageCallback", &ConfGen::FragmentConformerGenerator::setLogMessageCallback, 
             (python::arg("self"), python::arg("func")))
        .def("getLogMessageCallback", &ConfGen::FragmentConformerGenerator::getLogMessageCallback, 
             python::arg("self"), python::return_internal_reference<>())
        .def("generate", 
             static_cast<unsigned int (ConfGen::FragmentConformerGenerator::*)
             (const Chem::MolecularGraph&)>
             (&ConfGen::FragmentConformerGenerator::generate), 
             (python::arg("self"), python::arg("molgraph")))
        .def("generate", 
             static_cast<unsigned int (ConfGen::FragmentConformerGenerator::*)
             (const Chem::MolecularGraph&, const Chem::MolecularGraph&, const Math::Vector3DArray&)>
             (&ConfGen::FragmentConformerGenerator::generate), 
             (python::arg("self"), python::arg("molgraph"), python::arg("fixed_substr"), python::arg("fixed_substr_coords")))
        .def("generate", 
             static_cast<unsigned int (ConfGen::FragmentConformerGenerator::*)
             (const Chem::MolecularGraph&, unsigned int)>
             (&ConfGen::FragmentConformerGenerator::generate), 
             (python::arg("self"), python::arg("molgraph"), python::arg("frag_type")))
        .def("generate", 
             static_cast<unsigned int (ConfGen::FragmentConformerGenerator::*)
             (const Chem::MolecularGraph&, unsigned int, const Chem::MolecularGraph&, const Math::Vector3DArray&)>
             (&ConfGen::FragmentConformerGenerator::generate), 
             (python::arg("self"), python::arg("molgraph"), python::arg("frag_type"), python::arg("fixed_substr"),
              python::arg("fixed_substr_coords")))
        .def("setConformers", &ConfGen::FragmentConformerGenerator::setConformers,
             (python::arg("self"), python::arg("molgraph")))
        .def("getNumConformers", &ConfGen::FragmentConformerGenerator::getNumConformers, python::arg("self"))
        .def("getConformer", 
             static_cast<ConfGen::ConformerData& (ConfGen::FragmentConformerGenerator::*)(std::size_t)>
             (&ConfGen::FragmentConformerGenerator::getConformer),
             (python::arg("self"), python::arg("conf_idx")), python::return_internal_reference<>())
        .def("__getitem__", 
             static_cast<ConfGen::ConformerData& (ConfGen::FragmentConformerGenerator::*)(std::size_t)>
             (&ConfGen::FragmentConformerGenerator::getConformer),
             (python::arg("self"), python::arg("conf_idx")), python::return_internal_reference<>())
        .def("getSettings", 
             static_cast<ConfGen::FragmentConformerGeneratorSettings& (ConfGen::FragmentConformerGenerator::*)()>
             (&ConfGen::FragmentConformerGenerator::getSettings), 
             python::arg("self"), python::return_internal_reference<>())
        .add_property("numConformers", &ConfGen::FragmentConformerGenerator::getNumConformers)
        .add_property("settings", 
                      python::make_function(static_cast<ConfGen::FragmentConformerGeneratorSettings& (ConfGen::FragmentConformerGenerator::*)()>
                                            (&ConfGen::FragmentConformerGenerator::getSettings),
                                            python::return_internal_reference<>()))
        .add_property("abortCallback", 
                      python::make_function(&ConfGen::FragmentConformerGenerator::getAbortCallback,
                                            python::return_internal_reference<>()),
                      &ConfGen::FragmentConformerGenerator::setAbortCallback)
        .add_property("timeoutCallback", 
                      python::make_function(&ConfGen::FragmentConformerGenerator::getTimeoutCallback,
                                            python::return_internal_reference<>()),
                      &ConfGen::FragmentConformerGenerator::setTimeoutCallback)
        .add_property("logMessageCallback", 
                      python::make_function(&ConfGen::FragmentConformerGenerator::getLogMessageCallback,
                                            python::return_internal_reference<>()),
                      &ConfGen::FragmentConformerGenerator::setLogMessageCallback);
}

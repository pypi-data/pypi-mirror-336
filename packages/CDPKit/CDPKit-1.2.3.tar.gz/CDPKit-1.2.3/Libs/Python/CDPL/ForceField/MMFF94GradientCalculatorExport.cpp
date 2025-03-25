/* 
 * MMFF94GradientCalculatorExport.cpp 
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

#include "CDPL/ForceField/MMFF94GradientCalculator.hpp"
#include "CDPL/Math/VectorArray.hpp"

#include "Base/ObjectIdentityCheckVisitor.hpp"
#include "Base/CopyAssOp.hpp"

#include "ClassExports.hpp"


void CDPLPythonForceField::exportMMFF94GradientCalculator()
{
    using namespace boost;
    using namespace CDPL;

    typedef ForceField::MMFF94GradientCalculator<double> CalculatorType;

    python::class_<CalculatorType>("MMFF94GradientCalculator", python::no_init)
        .def(python::init<>(python::arg("self")))
        .def(python::init<const CalculatorType&>((python::arg("self"), python::arg("calc")))[python::with_custodian_and_ward<1, 2>()])
        .def(python::init<const ForceField::MMFF94InteractionData&, std::size_t>(
                 (python::arg("self"), python::arg("ia_data"), python::arg("num_atoms"))))
        .def(CDPLPythonBase::ObjectIdentityCheckVisitor<CalculatorType>())
        .def("assign", CDPLPythonBase::copyAssOp<CalculatorType>(),
             (python::arg("self"), python::arg("calc")), python::return_self<python::with_custodian_and_ward<1, 2> >())
        .def("setEnabledInteractionTypes", &CalculatorType::setEnabledInteractionTypes, (python::arg("self"), python::arg("types")))
        .def("getEnabledInteractionTypes", &CalculatorType::getEnabledInteractionTypes, python::arg("self"))
        .def("setup", &CalculatorType::setup, (python::arg("self"), python::arg("ia_data"), python::arg("num_atoms")),
             python::with_custodian_and_ward<1, 2>())
        .def("__call__", &CalculatorType::operator()<Math::Vector3DArray>, 
             (python::arg("self"), python::arg("coords")),
             python::return_value_policy<python::copy_const_reference>())
        .def("__call__", &CalculatorType::operator()<Math::Vector3DArray, Math::Vector3DArray>, 
             (python::arg("self"), python::arg("coords"), python::arg("grad")),
             python::return_value_policy<python::copy_const_reference>())
        .def("getTotalEnergy", &CalculatorType::getTotalEnergy, python::arg("self"),
             python::return_value_policy<python::copy_const_reference>())
        .def("getBondStretchingEnergy", &CalculatorType::getBondStretchingEnergy, python::arg("self"),
             python::return_value_policy<python::copy_const_reference>())
        .def("getAngleBendingEnergy", &CalculatorType::getAngleBendingEnergy, python::arg("self"),
             python::return_value_policy<python::copy_const_reference>())
        .def("getStretchBendEnergy", &CalculatorType::getStretchBendEnergy, python::arg("self"),
             python::return_value_policy<python::copy_const_reference>())
        .def("getOutOfPlaneBendingEnergy", &CalculatorType::getOutOfPlaneBendingEnergy, python::arg("self"),
             python::return_value_policy<python::copy_const_reference>())
        .def("getTorsionEnergy", &CalculatorType::getTorsionEnergy, python::arg("self"),
             python::return_value_policy<python::copy_const_reference>())
        .def("getElectrostaticEnergy", &CalculatorType::getElectrostaticEnergy, python::arg("self"),
             python::return_value_policy<python::copy_const_reference>())
        .def("getVanDerWaalsEnergy", &CalculatorType::getVanDerWaalsEnergy, python::arg("self"),
             python::return_value_policy<python::copy_const_reference>())
        .def("setFixedAtomMask", &CalculatorType::setFixedAtomMask, (python::arg("self"), python::arg("mask")))
        .def("resetFixedAtomMask", &CalculatorType::resetFixedAtomMask, python::arg("self"))
        .def("getFixedAtomMask", &CalculatorType::getFixedAtomMask, python::arg("self"),
             python::return_internal_reference<>())
        .add_property("enabledInteractionTypes", &CalculatorType::getEnabledInteractionTypes, 
                      &CalculatorType::setEnabledInteractionTypes)
        .add_property("totalEnergy", python::make_function(&CalculatorType::getTotalEnergy,
                                                           python::return_value_policy<python::copy_const_reference>()))
        .add_property("bondStretchingEnergy", python::make_function(&CalculatorType::getBondStretchingEnergy,
                                                                    python::return_value_policy<python::copy_const_reference>()))
        .add_property("angleBendingEnergy", python::make_function(&CalculatorType::getAngleBendingEnergy,
                                                                  python::return_value_policy<python::copy_const_reference>()))
        .add_property("stretchBendEnergy", python::make_function(&CalculatorType::getStretchBendEnergy,
                                                                 python::return_value_policy<python::copy_const_reference>()))
        .add_property("outOfPlaneBendingEnergy", python::make_function(&CalculatorType::getOutOfPlaneBendingEnergy,
                                                                       python::return_value_policy<python::copy_const_reference>()))
        .add_property("torsionEnergy", python::make_function(&CalculatorType::getTorsionEnergy,
                                                             python::return_value_policy<python::copy_const_reference>()))
        .add_property("electrostaticEnergy", python::make_function(&CalculatorType::getElectrostaticEnergy,
                                                                   python::return_value_policy<python::copy_const_reference>()))
        .add_property("vanDerWaalsEnergy", python::make_function(&CalculatorType::getVanDerWaalsEnergy,
                                                                 python::return_value_policy<python::copy_const_reference>()))
        .add_property("fixedAtomMask", python::make_function(&CalculatorType::getFixedAtomMask,
                                                             python::return_internal_reference<>()));
}

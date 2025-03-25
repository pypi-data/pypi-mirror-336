/* 
 * ParallelPiPiInteractionConstraintExport.cpp 
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

#include "CDPL/Pharm/ParallelPiPiInteractionConstraint.hpp"
#include "CDPL/Pharm/Feature.hpp"

#include "Base/ObjectIdentityCheckVisitor.hpp"
#include "Base/CopyAssOp.hpp"

#include "ClassExports.hpp"


namespace
{

    bool callOperator(CDPL::Pharm::ParallelPiPiInteractionConstraint& constr, 
                      CDPL::Pharm::Feature& ftr1, CDPL::Pharm::Feature& ftr2)
    {
        return constr(ftr1, ftr2);
    }
}


void CDPLPythonPharm::exportParallelPiPiInteractionConstraint()
{
    using namespace boost;
    using namespace CDPL;

    python::class_<Pharm::ParallelPiPiInteractionConstraint, boost::noncopyable>("ParallelPiPiInteractionConstraint", python::no_init)
        .def(python::init<const Pharm::ParallelPiPiInteractionConstraint&>((python::arg("self"), python::arg("constr"))))
        .def(python::init<double, double, double, double>((python::arg("self"),
                                                         python::arg("min_v_dist") = Pharm::ParallelPiPiInteractionConstraint::DEF_MIN_V_DISTANCE, 
                                                         python::arg("max_v_dist") = Pharm::ParallelPiPiInteractionConstraint::DEF_MAX_V_DISTANCE,
                                                         python::arg("max_h_dist") = Pharm::ParallelPiPiInteractionConstraint::DEF_MAX_H_DISTANCE,
                                                         python::arg("max_ang") = Pharm::ParallelPiPiInteractionConstraint::DEF_MAX_ANGLE)))
        .def(CDPLPythonBase::ObjectIdentityCheckVisitor<Pharm::ParallelPiPiInteractionConstraint>())
        .def("getMinVDistance", &Pharm::ParallelPiPiInteractionConstraint::getMinVDistance, python::arg("self"))
        .def("getMaxVDistance", &Pharm::ParallelPiPiInteractionConstraint::getMaxVDistance, python::arg("self"))
        .def("getMaxHDistance", &Pharm::ParallelPiPiInteractionConstraint::getMaxHDistance, python::arg("self"))
        .def("getMaxAngle", &Pharm::ParallelPiPiInteractionConstraint::getMaxAngle, python::arg("self"))
        .def("assign", CDPLPythonBase::copyAssOp<Pharm::ParallelPiPiInteractionConstraint>(), 
             (python::arg("self"), python::arg("constr")), python::return_self<>())
        .def("__call__", &callOperator, (python::arg("self"), python::arg("ftr1"), python::arg("ftr2")))
        .add_property("minVDistance", &Pharm::ParallelPiPiInteractionConstraint::getMinVDistance)
        .add_property("maxVDistance", &Pharm::ParallelPiPiInteractionConstraint::getMaxVDistance)
        .add_property("maxHDistance", &Pharm::ParallelPiPiInteractionConstraint::getMaxHDistance)
        .add_property("maxAngle", &Pharm::ParallelPiPiInteractionConstraint::getMaxAngle)
        .def_readonly("DEF_MIN_V_DISTANCE", Pharm::ParallelPiPiInteractionConstraint::DEF_MIN_V_DISTANCE)
        .def_readonly("DEF_MAX_V_DISTANCE", Pharm::ParallelPiPiInteractionConstraint::DEF_MAX_V_DISTANCE)
        .def_readonly("DEF_MAX_H_DISTANCE", Pharm::ParallelPiPiInteractionConstraint::DEF_MAX_H_DISTANCE)
        .def_readonly("DEF_MAX_ANGLE", Pharm::ParallelPiPiInteractionConstraint::DEF_MAX_ANGLE);
}

/* 
 * CationPiInteractionScoreExport.cpp 
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

#include "CDPL/Pharm/CationPiInteractionScore.hpp"

#include "Base/CopyAssOp.hpp"

#include "ClassExports.hpp"


void CDPLPythonPharm::exportCationPiInteractionScore()
{
    using namespace boost;
    using namespace CDPL;

    python::class_<Pharm::CationPiInteractionScore, Pharm::CationPiInteractionScore::SharedPointer,
                   python::bases<Pharm::FeatureInteractionScore>, boost::noncopyable>("CationPiInteractionScore", python::no_init)
        .def(python::init<const Pharm::CationPiInteractionScore&>((python::arg("self"), python::arg("score"))))
        .def(python::init<bool, double, double, double>((python::arg("self"), python::arg("aro_cat"), 
                                                         python::arg("min_dist") = Pharm::CationPiInteractionScore::DEF_MIN_DISTANCE, 
                                                         python::arg("max_dist") = Pharm::CationPiInteractionScore::DEF_MAX_DISTANCE,
                                                         python::arg("max_ang") = Pharm::CationPiInteractionScore::DEF_MAX_ANGLE)))
        .def("setDistanceScoringFunction", &Pharm::CationPiInteractionScore::setDistanceScoringFunction, (python::arg("self"), python::arg("func")))
        .def("setAngleScoringFunction", &Pharm::CationPiInteractionScore::setAngleScoringFunction, (python::arg("self"), python::arg("func")))
        .def("getMinDistance", &Pharm::CationPiInteractionScore::getMinDistance, python::arg("self"))
        .def("getMaxDistance", &Pharm::CationPiInteractionScore::getMaxDistance, python::arg("self"))
        .def("getMaxAngle", &Pharm::CationPiInteractionScore::getMaxAngle, python::arg("self"))
        .def("assign", CDPLPythonBase::copyAssOp<Pharm::CationPiInteractionScore>(), 
             (python::arg("self"), python::arg("constr")), python::return_self<>())
        .add_property("minDistance", &Pharm::CationPiInteractionScore::getMinDistance)
        .add_property("maxDistance", &Pharm::CationPiInteractionScore::getMaxDistance)
        .add_property("maxAngle", &Pharm::CationPiInteractionScore::getMaxAngle)
        .def_readonly("DEF_MIN_DISTANCE", Pharm::CationPiInteractionScore::DEF_MIN_DISTANCE)
        .def_readonly("DEF_MAX_DISTANCE", Pharm::CationPiInteractionScore::DEF_MAX_DISTANCE)
        .def_readonly("DEF_MAX_ANGLE", Pharm::CationPiInteractionScore::DEF_MAX_ANGLE);
}

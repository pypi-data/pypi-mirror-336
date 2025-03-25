/* 
 * ParallelPiPiInteractionScoreExport.cpp 
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

#include "CDPL/Pharm/ParallelPiPiInteractionScore.hpp"

#include "Base/CopyAssOp.hpp"

#include "ClassExports.hpp"


void CDPLPythonPharm::exportParallelPiPiInteractionScore()
{
    using namespace boost;
    using namespace CDPL;

    python::class_<Pharm::ParallelPiPiInteractionScore, Pharm::ParallelPiPiInteractionScore::SharedPointer,
                   python::bases<Pharm::FeatureInteractionScore>, boost::noncopyable>("ParallelPiPiInteractionScore", python::no_init)
        .def(python::init<const Pharm::ParallelPiPiInteractionScore&>((python::arg("self"), python::arg("score"))))
        .def(python::init<double, double, double, double>((python::arg("self"),
                                                         python::arg("min_v_dist") = Pharm::ParallelPiPiInteractionScore::DEF_MIN_V_DISTANCE, 
                                                         python::arg("max_v_dist") = Pharm::ParallelPiPiInteractionScore::DEF_MAX_V_DISTANCE,
                                                         python::arg("max_h_dist") = Pharm::ParallelPiPiInteractionScore::DEF_MAX_H_DISTANCE,
                                                         python::arg("max_ang") = Pharm::ParallelPiPiInteractionScore::DEF_MAX_ANGLE)))
        .def("setDistanceScoringFunction", &Pharm::ParallelPiPiInteractionScore::setDistanceScoringFunction, (python::arg("self"), python::arg("func")))
        .def("setAngleScoringFunction", &Pharm::ParallelPiPiInteractionScore::setAngleScoringFunction, (python::arg("self"), python::arg("func")))
        .def("getMinVDistance", &Pharm::ParallelPiPiInteractionScore::getMinVDistance, python::arg("self"))
        .def("getMaxVDistance", &Pharm::ParallelPiPiInteractionScore::getMaxVDistance, python::arg("self"))
        .def("getMaxHDistance", &Pharm::ParallelPiPiInteractionScore::getMaxHDistance, python::arg("self"))
        .def("getMaxAngle", &Pharm::ParallelPiPiInteractionScore::getMaxAngle, python::arg("self"))
        .def("assign", CDPLPythonBase::copyAssOp<Pharm::ParallelPiPiInteractionScore>(), 
             (python::arg("self"), python::arg("constr")), python::return_self<>())
        .add_property("minVDistance", &Pharm::ParallelPiPiInteractionScore::getMinVDistance)
        .add_property("maxVDistance", &Pharm::ParallelPiPiInteractionScore::getMaxVDistance)
        .add_property("maxHDistance", &Pharm::ParallelPiPiInteractionScore::getMaxHDistance)
        .add_property("maxAngle", &Pharm::ParallelPiPiInteractionScore::getMaxAngle)
        .def_readonly("DEF_MIN_V_DISTANCE", Pharm::ParallelPiPiInteractionScore::DEF_MIN_V_DISTANCE)
        .def_readonly("DEF_MAX_V_DISTANCE", Pharm::ParallelPiPiInteractionScore::DEF_MAX_V_DISTANCE)
        .def_readonly("DEF_MAX_H_DISTANCE", Pharm::ParallelPiPiInteractionScore::DEF_MAX_H_DISTANCE)
        .def_readonly("DEF_MAX_ANGLE", Pharm::ParallelPiPiInteractionScore::DEF_MAX_ANGLE);
}

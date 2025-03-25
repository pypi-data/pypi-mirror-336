/* 
 * HydrophobicInteractionConstraintExport.cpp 
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

#include "CDPL/Pharm/HydrophobicInteractionConstraint.hpp"
#include "CDPL/Pharm/Feature.hpp"

#include "ClassExports.hpp"


void CDPLPythonPharm::exportHydrophobicInteractionConstraint()
{
    using namespace boost;
    using namespace CDPL;

    python::class_<Pharm::HydrophobicInteractionConstraint, python::bases<Pharm::FeatureDistanceConstraint>,
                   boost::noncopyable>("HydrophobicInteractionConstraint", python::no_init)
        .def(python::init<const Pharm::HydrophobicInteractionConstraint&>((python::arg("self"), python::arg("constr"))))
        .def(python::init<double, double>((python::arg("self"), 
                                           python::arg("min_dist") = Pharm::HydrophobicInteractionConstraint::DEF_MIN_DISTANCE,
                                           python::arg("max_dist") = Pharm::HydrophobicInteractionConstraint::DEF_MAX_DISTANCE)))
        .def_readonly("DEF_MIN_DISTANCE", Pharm::HydrophobicInteractionConstraint::DEF_MIN_DISTANCE)
        .def_readonly("DEF_MAX_DISTANCE", Pharm::HydrophobicInteractionConstraint::DEF_MAX_DISTANCE);
}

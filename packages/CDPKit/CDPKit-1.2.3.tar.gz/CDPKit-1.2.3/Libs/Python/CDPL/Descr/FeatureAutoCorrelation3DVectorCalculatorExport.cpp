/* 
 * FeatureAutoCorrelation3DVectorCalculatorExport.cpp 
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

#include "CDPL/Descr/FeatureAutoCorrelation3DVectorCalculator.hpp"
#include "CDPL/Pharm/FeatureContainer.hpp"

#include "Base/ObjectIdentityCheckVisitor.hpp"
#include "Base/CopyAssOp.hpp"

#include "ClassExports.hpp"


namespace
{

    void calculate(CDPL::Descr::FeatureAutoCorrelation3DVectorCalculator& calculator, CDPL::Pharm::FeatureContainer& cntnr, CDPL::Math::DVector& vec)
    {
        calculator.calculate(cntnr, vec);
    }
}


void CDPLPythonDescr::exportFeatureAutoCorrelation3DVectorCalculator()
{
    using namespace boost;
    using namespace CDPL;

    python::class_<Descr::FeatureAutoCorrelation3DVectorCalculator, boost::noncopyable>("FeatureAutoCorrelation3DVectorCalculator", python::no_init)
        .def(python::init<>(python::arg("self")))
        .def(python::init<const Descr::FeatureAutoCorrelation3DVectorCalculator&>((python::arg("self"), python::arg("calc"))))
        .def(python::init<Pharm::FeatureContainer&, Math::DVector&>(
                 (python::arg("self"), python::arg("cntnr"), python::arg("vec"))))
        .def(CDPLPythonBase::ObjectIdentityCheckVisitor<Descr::FeatureAutoCorrelation3DVectorCalculator>())    
        .def("assign", CDPLPythonBase::copyAssOp<Descr::FeatureAutoCorrelation3DVectorCalculator>(), 
             (python::arg("self"), python::arg("calc")), python::return_self<>())
        .def("setEntityPairWeightFunction", &Descr::FeatureAutoCorrelation3DVectorCalculator::setEntityPairWeightFunction, 
             (python::arg("self"), python::arg("func")))
        .def("setEntity3DCoordinatesFunction", &Descr::FeatureAutoCorrelation3DVectorCalculator::setEntity3DCoordinatesFunction, 
             (python::arg("self"), python::arg("func")))
        .def("setNumSteps", &Descr::FeatureAutoCorrelation3DVectorCalculator::setNumSteps, 
             (python::arg("self"), python::arg("num_steps")))
        .def("getNumSteps", &Descr::FeatureAutoCorrelation3DVectorCalculator::getNumSteps, python::arg("self"))
        .def("setRadiusIncrement", &Descr::FeatureAutoCorrelation3DVectorCalculator::setRadiusIncrement, 
             (python::arg("self"), python::arg("radius_inc")))
        .def("getRadiusIncrement", &Descr::FeatureAutoCorrelation3DVectorCalculator::getRadiusIncrement, python::arg("self"))
        .def("setStartRadius", &Descr::FeatureAutoCorrelation3DVectorCalculator::setStartRadius, 
             (python::arg("self"), python::arg("start_radius")))
        .def("getStartRadius", &Descr::FeatureAutoCorrelation3DVectorCalculator::getStartRadius, python::arg("self"))
        .def("calculate", &calculate, (python::arg("self"), python::arg("cntnr"), python::arg("vec")))
        .add_property("startRadius", &Descr::FeatureAutoCorrelation3DVectorCalculator::getStartRadius,
                      &Descr::FeatureAutoCorrelation3DVectorCalculator::setStartRadius)
        .add_property("radiusIncrement", &Descr::FeatureAutoCorrelation3DVectorCalculator::getRadiusIncrement,
                      &Descr::FeatureAutoCorrelation3DVectorCalculator::setRadiusIncrement)
        .add_property("numSteps", &Descr::FeatureAutoCorrelation3DVectorCalculator::getNumSteps,
                      &Descr::FeatureAutoCorrelation3DVectorCalculator::setNumSteps);
}

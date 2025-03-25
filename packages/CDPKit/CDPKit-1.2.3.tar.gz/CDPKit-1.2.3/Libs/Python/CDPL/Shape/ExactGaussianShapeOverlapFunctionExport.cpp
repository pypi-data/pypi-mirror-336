/* 
 * ExactGaussianShapeOverlapFunctionExport.cpp 
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

#include "CDPL/Shape/ExactGaussianShapeOverlapFunction.hpp"
#include "CDPL/Shape/GaussianShapeFunction.hpp"

#include "ClassExports.hpp"


void CDPLPythonShape::exportExactGaussianShapeOverlapFunction()
{
    using namespace boost;
    using namespace CDPL;

    python::class_<Shape::ExactGaussianShapeOverlapFunction, Shape::ExactGaussianShapeOverlapFunction::SharedPointer,
                   python::bases<Shape::GaussianShapeOverlapFunction> >("ExactGaussianShapeOverlapFunction", python::no_init)
        .def(python::init<>(python::arg("self")))
        .def(python::init<const Shape::GaussianShapeFunction&, const Shape::GaussianShapeFunction&>
             ((python::arg("self"), python::arg("ref_shape_func"), python::arg("ovl_shape_func")))
             [python::with_custodian_and_ward<1, 2, python::with_custodian_and_ward<1, 3> >()])
        .def(python::init<const Shape::ExactGaussianShapeOverlapFunction&>((python::arg("self"), python::arg("func")))[python::with_custodian_and_ward<1, 2>()])
        .def("assign", &Shape::ExactGaussianShapeOverlapFunction::operator=, (python::arg("self"), python::arg("func")),
             python::return_self<python::with_custodian_and_ward<1, 2> >());
}

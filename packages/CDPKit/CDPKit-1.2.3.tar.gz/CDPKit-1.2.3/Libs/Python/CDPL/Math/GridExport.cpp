/* 
 * GridExport.cpp 
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

#include "CDPL/Math/Grid.hpp"
#include "CDPL/Math/IO.hpp"

#include "Base/ObjectIdentityCheckVisitor.hpp"

#include "GridExpression.hpp"
#include "GridVisitor.hpp"
#include "InitFunctionGeneratorVisitor.hpp"
#include "AssignFunctionGeneratorVisitor.hpp"
#include "ClassExports.hpp"


namespace
{

    template <typename GridType>
    struct GridExport
    {

        GridExport(const char* name) {
            using namespace boost;
            using namespace CDPLPythonMath;

            typedef typename GridType::SizeType SizeType;
            typedef typename GridType::ValueType ValueType;

            python::class_<GridType, typename GridType::SharedPointer>(name, python::no_init)
                .def(python::init<>(python::arg("self")))
                .def(python::init<const GridType&>((python::arg("self"), python::arg("g"))))
                .def(python::init<SizeType, SizeType, SizeType>(
                         (python::arg("self"), python::arg("m"), python::arg("n"), python::arg("o"))))
                .def(python::init<SizeType, SizeType, SizeType, const ValueType&>(
                         (python::arg("self"), python::arg("m"), python::arg("n"), python::arg("o"), python::arg("v"))))
                .def("resize", &GridType::resize, 
                     (python::arg("self"), python::arg("m"), python::arg("n"), python::arg("o"), python::arg("preserve") = true,
                      python::arg("v") = ValueType()))
                .def("clear", &GridType::clear, (python::arg("self"), python::arg("v") = ValueType()))
                .def(CDPLPythonBase::ObjectIdentityCheckVisitor<GridType>())
                .def(InitFunctionGeneratorVisitor<GridType, ConstGridExpression>("e"))
                .def(AssignFunctionGeneratorVisitor<GridType, ConstGridExpression>("e"))
                .def(ConstGridVisitor<GridType>())
                .def(ConstGridContainerVisitor<GridType>())
                .def(GridAssignAndSwapVisitor<GridType>())
                .def(GridVisitor<GridType>())
                .def(GridNDArrayInitVisitor<GridType>())
                .def(GridNDArrayAssignVisitor<GridType, true>())
                .def(GridContainerVisitor<GridType>());
        }
    };
}       


void CDPLPythonMath::exportGridTypes()
{
    using namespace CDPL;

    GridExport<Math::FGrid>("FGrid");
    GridExport<Math::DGrid>("DGrid");
}

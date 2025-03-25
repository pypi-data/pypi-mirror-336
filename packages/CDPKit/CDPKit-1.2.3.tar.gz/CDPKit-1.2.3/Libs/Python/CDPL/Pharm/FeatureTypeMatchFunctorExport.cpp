/* 
 * FeatureTypeMatchFunctorExport.cpp 
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

#include "CDPL/Pharm/FeatureTypeMatchFunctor.hpp"
#include "CDPL/Pharm/Feature.hpp"

#include "Base/ObjectIdentityCheckVisitor.hpp"
#include "Base/CopyAssOp.hpp"

#include "ClassExports.hpp"


namespace
{

    bool callOperator(CDPL::Pharm::FeatureTypeMatchFunctor& func, 
                      CDPL::Pharm::Feature& ftr1, CDPL::Pharm::Feature& ftr2)
    {
        return func(ftr1, ftr2);
    }
}


void CDPLPythonPharm::exportFeatureTypeMatchFunctor()
{
    using namespace boost;
    using namespace CDPL;

    python::class_<Pharm::FeatureTypeMatchFunctor, boost::noncopyable>("FeatureTypeMatchFunctor", python::no_init)
        .def(python::init<const Pharm::FeatureTypeMatchFunctor&>((python::arg("self"), python::arg("func"))))
        .def(python::init<>(python::arg("self")))
        .def(CDPLPythonBase::ObjectIdentityCheckVisitor<Pharm::FeatureTypeMatchFunctor>())
        .def("assign", CDPLPythonBase::copyAssOp<Pharm::FeatureTypeMatchFunctor>(), 
             (python::arg("self"), python::arg("func")), python::return_self<>())
        .def("__call__", &callOperator, (python::arg("self"), python::arg("ftr1"), python::arg("ftr2")));
}

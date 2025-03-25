/* 
 * ControlParameterFunctionExport.cpp 
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

#include "CDPL/Base/ControlParameterContainer.hpp"
#include "CDPL/ConfGen/ControlParameterFunctions.hpp"

#include "FunctionExports.hpp"


#define MAKE_CONTROL_PARAM_FUNC_WRAPPERS(TYPE, FUNC_INFIX)                           \
TYPE get##FUNC_INFIX##ParameterWrapper(CDPL::Base::ControlParameterContainer& cntnr) \
{                                                                                    \
    return CDPL::ConfGen::get##FUNC_INFIX##Parameter(cntnr);                           \
}                                                                                    \
                                                                                     \
bool has##FUNC_INFIX##ParameterWrapper(CDPL::Base::ControlParameterContainer& cntnr) \
{                                                                                    \
    return CDPL::ConfGen::has##FUNC_INFIX##Parameter(cntnr);                           \
}

#define EXPORT_CONTROL_PARAM_FUNCS(FUNC_INFIX, ARG_NAME)                                                                          \
python::def("get"#FUNC_INFIX"Parameter", &get##FUNC_INFIX##ParameterWrapper, python::arg("cntnr"));                               \
python::def("has"#FUNC_INFIX"Parameter", &has##FUNC_INFIX##ParameterWrapper, python::arg("cntnr"));                               \
python::def("clear"#FUNC_INFIX"Parameter", &ConfGen::clear##FUNC_INFIX##Parameter, python::arg("cntnr"));                           \
python::def("set"#FUNC_INFIX"Parameter", &ConfGen::set##FUNC_INFIX##Parameter, (python::arg("cntnr"), python::arg(#ARG_NAME))); 


namespace
{

    MAKE_CONTROL_PARAM_FUNC_WRAPPERS(bool, StrictErrorChecking)
}


void CDPLPythonConfGen::exportControlParameterFunctions()
{
    using namespace boost;
    using namespace CDPL;

    EXPORT_CONTROL_PARAM_FUNCS(StrictErrorChecking, strict)
}

/* 
 * AtomPropertyExport.cpp 
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

#include "CDPL/Vis/AtomProperty.hpp"
#include "CDPL/Base/LookupKey.hpp"

#include "NamespaceExports.hpp"


namespace 
{

    struct AtomProperty {};
}


void CDPLPythonVis::exportAtomProperties()
{
    using namespace boost;
    using namespace CDPL;

    python::class_<AtomProperty, boost::noncopyable>("AtomProperty", python::no_init)
        .def_readonly("COLOR", &Vis::AtomProperty::COLOR)
        .def_readonly("RADICAL_ELECTRON_DOT_SIZE", &Vis::AtomProperty::RADICAL_ELECTRON_DOT_SIZE)
        .def_readonly("LABEL_FONT", &Vis::AtomProperty::LABEL_FONT)
        .def_readonly("LABEL_MARGIN", &Vis::AtomProperty::LABEL_MARGIN)
        .def_readonly("LABEL_SIZE", &Vis::AtomProperty::LABEL_SIZE)
        .def_readonly("SECONDARY_LABEL_FONT", &Vis::AtomProperty::SECONDARY_LABEL_FONT)
        .def_readonly("SECONDARY_LABEL_SIZE", &Vis::AtomProperty::SECONDARY_LABEL_SIZE)
        .def_readonly("CONFIGURATION_LABEL_FONT", &Vis::AtomProperty::CONFIGURATION_LABEL_FONT)
        .def_readonly("CONFIGURATION_LABEL_SIZE", &Vis::AtomProperty::CONFIGURATION_LABEL_SIZE)
        .def_readonly("CONFIGURATION_LABEL_COLOR", &Vis::AtomProperty::CONFIGURATION_LABEL_COLOR)
        .def_readonly("CUSTOM_LABEL_FONT", &Vis::AtomProperty::CUSTOM_LABEL_FONT)
        .def_readonly("CUSTOM_LABEL_SIZE", &Vis::AtomProperty::CUSTOM_LABEL_SIZE)
        .def_readonly("CUSTOM_LABEL_COLOR", &Vis::AtomProperty::CUSTOM_LABEL_COLOR)
        .def_readonly("CUSTOM_LABEL", &Vis::AtomProperty::CUSTOM_LABEL)
        .def_readonly("HIGHLIGHTED_FLAG", &Vis::AtomProperty::HIGHLIGHTED_FLAG)
        .def_readonly("HIGHLIGHT_AREA_BRUSH", &Vis::AtomProperty::HIGHLIGHT_AREA_BRUSH)
        .def_readonly("HIGHLIGHT_AREA_OUTLINE_PEN", &Vis::AtomProperty::HIGHLIGHT_AREA_OUTLINE_PEN)
        ;
}

/* 
 * FromPythonConverterRegistration.cpp 
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


#include "CDPL/Vis/Color.hpp"
#include "CDPL/Vis/Font.hpp"
#include "CDPL/Vis/Rectangle2D.hpp"
#include "CDPL/Vis/SizeSpecification.hpp"
#include "CDPL/Vis/ColorTable.hpp"

#include "Base/GenericAnyFromPythonConverter.hpp"

#include "ConverterRegistration.hpp"


void CDPLPythonVis::registerFromPythonConverters()
{
    using namespace CDPL;

    CDPLPythonBase::GenericAnyFromPythonConverter<const Vis::Color&>();
    CDPLPythonBase::GenericAnyFromPythonConverter<const Vis::Font&>();
    CDPLPythonBase::GenericAnyFromPythonConverter<const Vis::Rectangle2D&>();
    CDPLPythonBase::GenericAnyFromPythonConverter<const Vis::SizeSpecification&>();
    CDPLPythonBase::GenericAnyFromPythonConverter<const Vis::ColorTable::SharedPointer&>();
}

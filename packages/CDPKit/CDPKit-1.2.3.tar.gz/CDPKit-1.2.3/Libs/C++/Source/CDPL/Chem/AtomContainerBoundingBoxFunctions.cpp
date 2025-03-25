/* 
 * AtomContainerBoundingBoxFunction.cpp 
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


#include "StaticInit.hpp"

#include "CDPL/Chem/AtomContainerFunctions.hpp"
#include "CDPL/Chem/UtilityFunctions.hpp"
#include "CDPL/Chem/AtomContainer.hpp"
#include "CDPL/Chem/Atom.hpp"


using namespace CDPL; 


void Chem::calcBoundingBox(const AtomContainer& cntnr, Math::Vector3D& min, Math::Vector3D& max, const Atom3DCoordinatesFunction& coords_func, bool reset)
{
    for (AtomContainer::ConstAtomIterator it = cntnr.getAtomsBegin(), end = cntnr.getAtomsEnd(); it != end; ++it) {
        const Math::Vector3D& coords = coords_func(*it);

        extendBoundingBox(min, max, coords, reset);
        reset = false;
    }
}    

bool Chem::insideBoundingBox(const AtomContainer& cntnr, const Math::Vector3D& min, const Math::Vector3D& max, const Atom3DCoordinatesFunction& coords_func)
{
    for (AtomContainer::ConstAtomIterator it = cntnr.getAtomsBegin(), end = cntnr.getAtomsEnd(); it != end; ++it) {
        const Math::Vector3D& coords = coords_func(*it);

        if (insideBoundingBox(min, max, coords))
            continue;

        return false;
    }

    return true;
}

bool Chem::intersectsBoundingBox(const AtomContainer& cntnr, const Math::Vector3D& min, const Math::Vector3D& max, const Atom3DCoordinatesFunction& coords_func)
{
    for (AtomContainer::ConstAtomIterator it = cntnr.getAtomsBegin(), end = cntnr.getAtomsEnd(); it != end; ++it) {
        const Math::Vector3D& coords = coords_func(*it);

        if (insideBoundingBox(min, max, coords))
            return true;
    }

    return false;
}


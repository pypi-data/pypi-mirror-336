/* 
 * AtomContainerFunctions.hpp 
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

/**
 * \file
 * \brief Declaration of functions that operate on Chem::AtomContainer instances.
 */

#ifndef CDPL_CHEM_ATOMCONTAINERFUNCTIONS_HPP
#define CDPL_CHEM_ATOMCONTAINERFUNCTIONS_HPP

#include <cstddef>

#include "CDPL/Chem/APIPrefix.hpp"
#include "CDPL/Chem/AtomPredicate.hpp"
#include "CDPL/Chem/Atom3DCoordinatesFunction.hpp"
#include "CDPL/Math/Matrix.hpp"
#include "CDPL/Math/VectorArray.hpp"
#include "CDPL/Util/BitSet.hpp"


namespace CDPL
{

    namespace Chem
    {

        class AtomContainer;
        class Fragment;
        class Molecule;


        CDPL_CHEM_API bool hasCoordinates(const AtomContainer& cntnr, std::size_t dim);


        CDPL_CHEM_API void get2DCoordinates(const AtomContainer& cntnr, Math::Vector2DArray& coords, bool append = false);

        CDPL_CHEM_API void set2DCoordinates(AtomContainer& cntnr, const Math::Vector2DArray& coords);

        CDPL_CHEM_API void transform2DCoordinates(AtomContainer& cntnr, const Math::Matrix3D& mtx);


        CDPL_CHEM_API void get3DCoordinates(const AtomContainer& cntnr, Math::Vector3DArray& coords, const Atom3DCoordinatesFunction& coords_func, bool append = false);


        CDPL_CHEM_API void clearConformations(AtomContainer& cntnr);

        CDPL_CHEM_API std::size_t getNumConformations(const AtomContainer& cntnr);

        CDPL_CHEM_API void applyConformation(AtomContainer& cntnr, std::size_t conf_idx);

        CDPL_CHEM_API void getConformation(const AtomContainer& cntnr, std::size_t conf_idx, Math::Vector3DArray& coords, bool append = false);

        CDPL_CHEM_API void setConformation(AtomContainer& cntnr, std::size_t conf_idx, const Math::Vector3DArray& coords);

        CDPL_CHEM_API void addConformation(AtomContainer& cntnr, const Math::Vector3DArray& coords);

        CDPL_CHEM_API void transformConformation(AtomContainer& cntnr, std::size_t conf_idx, const Math::Matrix4D& mtx);

        CDPL_CHEM_API void transformConformations(AtomContainer& cntnr, const Math::Matrix4D& mtx);

        /*
         * \since 1.1
         */
        CDPL_CHEM_API bool alignConformations(AtomContainer& cntnr, const Util::BitSet& ref_atoms, const Math::Vector3DArray& ref_coords);

        /*
         * \since 1.1
         */
        CDPL_CHEM_API bool alignConformations(AtomContainer& cntnr, const AtomContainer& ref_atoms, const Math::Vector3DArray& ref_coords);

        /*
         * \since 1.1
         */
        CDPL_CHEM_API bool alignConformations(AtomContainer& cntnr, const Util::BitSet& ref_atoms);

        /*
         * \since 1.1
         */
        CDPL_CHEM_API bool alignConformations(AtomContainer& cntnr, const AtomContainer& ref_atoms);

        
        CDPL_CHEM_API std::size_t getMaxComponentGroupID(const AtomContainer& cntnr);

        CDPL_CHEM_API std::size_t getMaxAtomMappingID(const AtomContainer& cntnr);


        CDPL_CHEM_API std::size_t createAtomTypeMask(const AtomContainer& cntnr, Util::BitSet& mask, unsigned int type, bool reset = true, bool strict = true);


        CDPL_CHEM_API void copyAtomsIf(const AtomContainer& cntnr, Molecule& mol, const AtomPredicate& pred, bool append = false);

        CDPL_CHEM_API void copyAtomsIf(const AtomContainer& cntnr, Fragment& frag, const AtomPredicate& pred, bool append = false);

        CDPL_CHEM_API void copyAtomsIfNot(const AtomContainer& cntnr, Molecule& mol, const AtomPredicate& pred, bool append = false);

        CDPL_CHEM_API void copyAtomsIfNot(const AtomContainer& cntnr, Fragment& frag, const AtomPredicate& pred, bool append = false);


        CDPL_CHEM_API bool calcCenterOfMass(const AtomContainer& cntnr, const Atom3DCoordinatesFunction& coords_func, Math::Vector3D& ctr);

        CDPL_CHEM_API bool calcCentroid(const AtomContainer& cntnr, const Atom3DCoordinatesFunction& coords_func, Math::Vector3D& ctr);

        CDPL_CHEM_API void calcBoundingBox(const AtomContainer& cntnr, Math::Vector3D& min, Math::Vector3D& max, const Atom3DCoordinatesFunction& coords_func, bool reset = true);

        CDPL_CHEM_API bool insideBoundingBox(const AtomContainer& cntnr, const Math::Vector3D& min, const Math::Vector3D& max, const Atom3DCoordinatesFunction& coords_func);

        CDPL_CHEM_API bool intersectsBoundingBox(const AtomContainer& cntnr, const Math::Vector3D& min, const Math::Vector3D& max, const Atom3DCoordinatesFunction& coords_func);
    } // namespace Chem
} // namespace CDPL

#endif // CDPL_CHEM_ATOMCONTAINERFUNCTIONS_HPP

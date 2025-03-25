/* 
 * AtomPropertyDefault.hpp 
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
 * \brief Definition of constants in namespace CDPL::Biomol::AtomPropertyDefault.
 */

#ifndef CDPL_BIOMOL_ATOMPROPERTYDEFAULT_HPP
#define CDPL_BIOMOL_ATOMPROPERTYDEFAULT_HPP

#include <cstddef>

#include "CDPL/Biomol/APIPrefix.hpp"


namespace CDPL
{

    namespace Biomol
    {

        /**
         * \brief Provides default values for built-in Chem::Atom properties.
         */
        namespace AtomPropertyDefault
        {

            extern CDPL_BIOMOL_API const std::size_t MODEL_NUMBER;
            extern CDPL_BIOMOL_API const double      B_FACTOR;
            extern CDPL_BIOMOL_API const double      OCCUPANCY;
            extern CDPL_BIOMOL_API const bool        RESIDUE_LEAVING_ATOM_FLAG;
            extern CDPL_BIOMOL_API const bool        RESIDUE_LINKING_ATOM_FLAG;
            extern CDPL_BIOMOL_API const char        RESIDUE_INSERTION_CODE;
        } // namespace AtomPropertyDefault
    } // namespace Biomol
} // namespace CDPL

#endif // CDPL_BIOMOL_ATOMPROPERTYDEFAULT_HPP

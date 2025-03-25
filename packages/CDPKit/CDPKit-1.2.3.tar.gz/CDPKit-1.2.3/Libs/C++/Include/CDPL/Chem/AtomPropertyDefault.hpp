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
 * \brief Definition of constants in namespace CDPL::Chem::AtomPropertyDefault.
 */

#ifndef CDPL_CHEM_ATOMPROPERTYDEFAULT_HPP
#define CDPL_CHEM_ATOMPROPERTYDEFAULT_HPP

#include <string>
#include <cstddef>

#include "CDPL/Chem/APIPrefix.hpp"
#include "CDPL/Chem/StereoDescriptor.hpp"
#include "CDPL/Chem/MatchConstraintList.hpp"


namespace CDPL
{

    namespace Chem
    {

        /**
         * \brief Provides default values for built-in Chem::Atom properties.
         */
        namespace AtomPropertyDefault
        {

            extern CDPL_CHEM_API const std::string                        SYMBOL;
            extern CDPL_CHEM_API const std::string                        NAME;
            extern CDPL_CHEM_API const long                               FORMAL_CHARGE;
            extern CDPL_CHEM_API const std::size_t                        ISOTOPE;
            extern CDPL_CHEM_API const std::size_t                        UNPAIRED_ELECTRON_COUNT;
            extern CDPL_CHEM_API const unsigned int                       TYPE;
            extern CDPL_CHEM_API const unsigned int                       RADICAL_TYPE;
            extern CDPL_CHEM_API const unsigned int                       SYBYL_TYPE;
            extern CDPL_CHEM_API const unsigned int                       REACTION_CENTER_STATUS;
            extern CDPL_CHEM_API const StereoDescriptor                   STEREO_DESCRIPTOR;
            extern CDPL_CHEM_API const std::size_t                        COMPONENT_GROUP_ID;
            extern CDPL_CHEM_API const std::size_t                        ATOM_MAPPING_ID;
            extern CDPL_CHEM_API const MatchConstraintList::SharedPointer MATCH_CONSTRAINTS;
            extern CDPL_CHEM_API const double                             MOL2_CHARGE;
            extern CDPL_CHEM_API const std::string                        MOL2_NAME;
            extern CDPL_CHEM_API const bool                               MDL_DB_STEREO_CARE_FLAG;
        } // namespace AtomPropertyDefault
    } // namespace Chem
} // namespace CDPL

#endif // CDPL_CHEM_ATOMPROPERTYDEFAULT_HPP

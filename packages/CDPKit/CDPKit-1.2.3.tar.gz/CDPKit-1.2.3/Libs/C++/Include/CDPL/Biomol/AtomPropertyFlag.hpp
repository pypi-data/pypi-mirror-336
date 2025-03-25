/* 
 * AtomPropertyFlag.hpp 
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
 * \brief Definition of constants in namespace CDPL::Biomol::AtomPropertyFlag.
 */

#ifndef CDPL_BIOMOL_ATOMPROPERTYFLAG_HPP
#define CDPL_BIOMOL_ATOMPROPERTYFLAG_HPP


namespace CDPL
{

    namespace Biomol
    {

        /**
         * \brief Provides flags for the specification of basic Chem::Atom properties.
         */
        namespace AtomPropertyFlag
        {

            /**
             * \brief Represents an empty set of atom properties.
             */
            constexpr unsigned int NONE = 0x0;

            /**
             * \brief Represents the default set of atom properties.
             */
            constexpr unsigned int DEFAULT = 0x80000000;

            constexpr unsigned int RESIDUE_CODE = 0x400;

            constexpr unsigned int RESIDUE_SEQ_NO = 0x800;

            constexpr unsigned int RESIDUE_INS_CODE = 0x1000;

            constexpr unsigned int CHAIN_ID = 0x2000;

            constexpr unsigned int MODEL_NUMBER = 0x4000;
        } // namespace AtomPropertyFlag
    } // namespace Biomol
} // namespace CDPL

#endif // CDPL_BIOMOL_ATOMPROPERTYFLAG_HPP

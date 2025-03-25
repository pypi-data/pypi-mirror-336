/* 
 * SybylBondType.hpp 
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
 * \brief Definition of constants in namespace CDPL::Chem::SybylBondType.
 */

#ifndef CDPL_CHEM_SYBYLBONDTYPE_HPP
#define CDPL_CHEM_SYBYLBONDTYPE_HPP


namespace CDPL
{

    namespace Chem
    {

        /**
         * \brief Provides constants for the specification of the <em>Tripos Sybyl</em> bond type.
         */
        namespace SybylBondType
        {

            /**
             * \brief Specifies an unknown bond (cannot be determined from the parameter tables).
             */
            constexpr unsigned int UNKNOWN = 0;

            /**
             * \brief Specifies a single bond.
             */
            constexpr unsigned int SINGLE = 1;

            /**
             * \brief Specifies a double bond.
             */
            constexpr unsigned int DOUBLE = 2;

            /**
             * \brief Specifies a triple bond.
             */
            constexpr unsigned int TRIPLE = 3;

            /**
             * \brief Specifies an aromatic bond.
             */
            constexpr unsigned int AROMATIC = 4;

            /**
             * \brief Specifies an amide bond.
             */
            constexpr unsigned int AMIDE = 5;

            /**
             * \brief Specifies a dummy bond.
             */
            constexpr unsigned int DUMMY = 6;

            /**
             * \brief Specifies a pseudo bond.
             */
            constexpr unsigned int NOT_CONNECTED = 7;
        } // namespace SybylBondType
    } // namespace Chem
} // namespace CDPL

#endif // CDPL_CHEM_SYBYLBONDTYPE_HPP

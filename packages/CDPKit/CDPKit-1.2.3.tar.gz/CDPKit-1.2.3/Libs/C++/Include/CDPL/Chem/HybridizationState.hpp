/* 
 * HybridizationState.hpp 
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
 * \brief Definition of constants in namespace CDPL::Chem::HybridizationState.
 */

#ifndef CDPL_CHEM_HYBRIDIZATIONSTATE_HPP
#define CDPL_CHEM_HYBRIDIZATIONSTATE_HPP


namespace CDPL
{

    namespace Chem
    {

        /**
         * \brief Provides constants for the specification of atom hybridization states.
         */
        namespace HybridizationState
        {

            /**
             * \brief Specifies an unknown hybridization state.
             */
            constexpr unsigned int UNKNOWN = 0;

            /**
             * \brief Specifies the hybridization state \e sp.
             */
            constexpr unsigned int SP = 1;

            /**
             * \brief Specifies the hybridization state \e sp<sup>1</sup>.
             */
            constexpr unsigned int SP1 = SP;

            /**
             * \brief Specifies the hybridization state \e sp<sup>2</sup>.
             */
            constexpr unsigned int SP2 = 2;

            /**
             * \brief Specifies the hybridization state \e sp<sup>3</sup>.
             */
            constexpr unsigned int SP3 = 3;

            /**
             * \brief Specifies the hybridization \e dp.
             */
            constexpr unsigned int DP = 4;

            /**
             * \brief Specifies the hybridization state \e sd<sup>3</sup>.
             */
            constexpr unsigned int SD3 = 5;

            /**
             * \brief Specifies the hybridization state \e sp<sup>2</sup>d.
             */
            constexpr unsigned int SP2D = 6;

            /**
             * \brief Specifies the hybridization state \e sp<sup>3</sup>d.
             */
            constexpr unsigned int SP3D = 7;

            /**
             * \brief Specifies the hybridization state \e sp<sup>3</sup>d<sup>2</sup>.
             */
            constexpr unsigned int SP3D2 = 8;

            /**
             * \brief Specifies the hybridization state \e sp<sup>3</sup>d<sup>3</sup>.
             */
            constexpr unsigned int SP3D3 = 9;
        } // namespace HybridizationState
    } // namespace Chem
} // namespace CDPL

#endif // CDPL_CHEM_HYBRIDIZATIONSTATE_HPP

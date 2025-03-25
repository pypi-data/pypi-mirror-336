/* 
 * ConformerSamplingMode.hpp 
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
 * \brief Definition of constants in namespace CDPL::ConfGen::ConformerSamplingMode.
 */

#ifndef CDPL_CONFGEN_CONFORMERSAMPLINGMODE_HPP
#define CDPL_CONFGEN_CONFORMERSAMPLINGMODE_HPP


namespace CDPL
{

    namespace ConfGen
    {

        /**
         * \brief Provides constants used to specify the employed conformer sampling method.
         */
        namespace ConformerSamplingMode
        {

            constexpr unsigned int AUTO       = 0;
            constexpr unsigned int SYSTEMATIC = 1;
            constexpr unsigned int STOCHASTIC = 2;
        } // namespace ConformerSamplingMode
    } // namespace ConfGen
} // namespace CDPL

#endif // CDPL_CONFGEN_CONFORMERSAMPLINGMODE_HPP

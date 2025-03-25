/* 
 * CDFFormatData.hpp
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


#ifndef CDPL_GRAIL_CDFFORMATDATA_HPP
#define CDPL_GRAIL_CDFFORMATDATA_HPP

#include <cstdint>

#include "CDPL/Internal/CDFFormatData.hpp"


namespace CDPL
{

    namespace GRAIL
    {

        namespace CDF
        {

            using namespace Internal::CDF;

            typedef std::uint32_t UIntType;

            constexpr std::uint8_t INTERACTION_SCORE_GRID_RECORD_ID     = 4;
            constexpr std::uint8_t INTERACTION_SCORE_GRID_SET_RECORD_ID = 5;

            constexpr std::uint8_t CURR_FORMAT_VERSION = 1;

            namespace AttributedGridProperty
            {

                constexpr unsigned int PROPERTY_HANDLER_ID = 1;

                constexpr unsigned int FEATURE_TYPE        = 1;
                constexpr unsigned int TARGET_FEATURE_TYPE = 2;
            } // namespace AttributedGridProperty
        } // namespace CDF
    } // namespace GRAIL
} // namespace CDPL

#endif // CDPL_GRAIL_CDFFORMATDATA_HPP

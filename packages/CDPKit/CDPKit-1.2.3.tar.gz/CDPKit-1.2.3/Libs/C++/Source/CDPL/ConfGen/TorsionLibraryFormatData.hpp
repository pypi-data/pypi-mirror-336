/* 
 * TorsionLibraryFormatData.hpp
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


#ifndef CDPL_CONFGEN_TORSIONLIBRARYFORMATDATA_HPP
#define CDPL_CONFGEN_TORSIONLIBRARYFORMATDATA_HPP

#include <string>


namespace CDPL
{

    namespace ConfGen
    {

        namespace TorsionLibraryFormatData
        {

            namespace Element
            {

                const std::string LIBRARY            = "library";
                const std::string CATEGORY           = "category";
                const std::string RULE               = "rule";
                const std::string ANGLE_LIST         = "torsions";
                const std::string ANGLE              = "angle";
                const std::string NOTE               = "note";
                const std::string HISTOGRAM          = "histogram";
                const std::string HISTOGRAM2         = "histogram2";
                const std::string HISTOGRAM_SHIFTED  = "histogram_shifted";
                const std::string HISTOGRAM2_SHIFTED = "histogram2_shifted";
                const std::string BIN                = "bin";
            } // namespace Element

            namespace Attribute
            {

                const std::string CATEGORY_NAME       = "name";
                const std::string CATEGORY_PATTERN    = "pattern";
                const std::string CATEGORY_ATOM_TYPE1 = "atomType1";
                const std::string CATEGORY_ATOM_TYPE2 = "atomType2";

                const std::string RULE_PATTERN = "pattern";

                const std::string ANGLE_VALUE      = "value";
                const std::string ANGLE_TOLERANCE1 = "tolerance1";
                const std::string ANGLE_TOLERANCE2 = "tolerance2";
                const std::string ANGLE_SCORE      = "score";
            } // namespace Attribute
        } // namespace TorsionLibraryFormatData
    } // namespace ConfGen
} // namespace CDPL

#endif // CDPL_CONFGEN_TORSIONLIBRARYFORMATDATA_HPP

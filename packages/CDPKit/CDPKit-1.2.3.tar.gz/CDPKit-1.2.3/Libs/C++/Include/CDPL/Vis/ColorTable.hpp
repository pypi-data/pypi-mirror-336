/* 
 * ColorTable.hpp 
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
 * \brief Definition of the type CDPL::Vis::ColorTable.
 */

#ifndef CDPL_VIS_COLORTABLE_HPP
#define CDPL_VIS_COLORTABLE_HPP

#include "CDPL/Vis/APIPrefix.hpp"
#include "CDPL/Vis/Color.hpp"
#include "CDPL/Util/Map.hpp"


namespace CDPL
{

    namespace Vis
    {

        /**
         * \brief A container for the storage and lookup of Vis::Color objects that are associated with a
         *        numeric identifier.
         */
        class CDPL_VIS_API ColorTable : public Util::Map<std::size_t, Color>
        {

          public:
            typedef std::shared_ptr<ColorTable> SharedPointer;

            ColorTable():
                Map<std::size_t, Color>() {}

            template <typename Iter>
            ColorTable(const Iter& beg, const Iter& end):
                Map<std::size_t, Color>(beg, end)
            {}

          private:
            const char* getClassName() const;
        };
    } // namespace Vis
} // namespace CDPL

#endif // CDPL_VIS_COLORTABLE_HPP

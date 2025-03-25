/* 
 * FileFunctions.hpp 
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
 * \brief Declaration of filesystem-related functions
 */

#ifndef CDPL_UTIL_FILEFUNCTIONS_HPP
#define CDPL_UTIL_FILEFUNCTIONS_HPP

#include <string>

#include "CDPL/Util/APIPrefix.hpp"


namespace CDPL
{

    namespace Util
    {

        CDPL_UTIL_API std::string genCheckedTempFilePath(const std::string& dir = "",
                                                         const std::string& ptn = "%%%%-%%%%-%%%%-%%%%");

        CDPL_UTIL_API bool checkIfSameFile(const std::string& path1, const std::string& path2);

        CDPL_UTIL_API bool fileExists(const std::string& path);
    } // namespace Util
} // namespace CDPL

#endif // CDPL_UTIL_FILEFUNCTIONS_HPP

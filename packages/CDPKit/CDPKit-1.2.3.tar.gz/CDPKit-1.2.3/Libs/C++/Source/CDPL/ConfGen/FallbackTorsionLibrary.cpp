/* 
 * TorsionDriverImpl.cpp 
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


#include "StaticInit.hpp"

#include <mutex>

#include "FallbackTorsionLibrary.hpp"
#include "TorsionLibraryDataReader.hpp"


using namespace CDPL;


namespace
{

    // clang-format off
    
    const char* FALLBACK_TOR_LIB_DATA =
        #include "FallbackTorsionLibrary.xml.str"
        ;

    // clang-format on
    
    std::once_flag initFallbackTorLibFlag;

    ConfGen::TorsionLibrary::SharedPointer fallbackTorLib;

    void initFallbackTorLib()
    {
        fallbackTorLib.reset(new ConfGen::TorsionLibrary());

        ConfGen::TorsionLibraryDataReader().read(FALLBACK_TOR_LIB_DATA, *fallbackTorLib);
    }
} // namespace


const ConfGen::TorsionLibrary::SharedPointer& ConfGen::getFallbackTorsionLibrary()
{
    std::call_once(initFallbackTorLibFlag, &initFallbackTorLib);

    return fallbackTorLib;
}

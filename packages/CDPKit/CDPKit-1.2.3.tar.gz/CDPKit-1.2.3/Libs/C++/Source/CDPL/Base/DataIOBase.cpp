/* 
 * DataIOBase.cpp 
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

#include <functional>
#include <algorithm>

#include "CDPL/Base/DataIOBase.hpp"


using namespace CDPL;


std::size_t Base::DataIOBase::registerIOCallback(const IOCallbackFunction& cb)
{
    std::size_t id = 0;
    std::size_t num_callbacks = callbacks.size();

    for ( ; id < num_callbacks && std::find_if(callbacks.begin(), callbacks.end(),
                                               std::bind(std::equal_to<std::size_t>(),
                                                         std::bind(&CallbackListEntry::first, std::placeholders::_1),
                                                         id)) != callbacks.end(); id++);
    callbacks.push_back(CallbackListEntry(id, cb));

    return id;
}

void Base::DataIOBase::unregisterIOCallback(std::size_t id)
{
    callbacks.erase(std::remove_if(callbacks.begin(), callbacks.end(), std::bind(std::equal_to<std::size_t>(),
                                                                                 std::bind(&CallbackListEntry::first, std::placeholders::_1),
                                                                                 id)),
                    callbacks.end());
}

void Base::DataIOBase::clearIOCallbacks()
{
    callbacks.clear();
}

void Base::DataIOBase::invokeIOCallbacks(double progress) const
{
    std::for_each(callbacks.begin(), callbacks.end(), std::bind(&IOCallbackFunction::operator(),
                                                                std::bind(&CallbackListEntry::second, std::placeholders::_1), 
                                                                std::ref(*this), progress));
}

Base::DataIOBase& Base::DataIOBase::operator=(const DataIOBase& io_base)
{
    if (&io_base == this)
        return *this;

    ControlParameterContainer::operator=(io_base);

    return *this;
}

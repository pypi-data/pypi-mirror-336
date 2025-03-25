/* 
 * MMFF94SymbolicToNumericAtomTypeMap.cpp 
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

#include <sstream>
#include <mutex>

#include <boost/iostreams/device/array.hpp>
#include <boost/iostreams/stream.hpp>

#include "CDPL/ForceField/MMFF94SymbolicToNumericAtomTypeMap.hpp"
#include "CDPL/Base/Exceptions.hpp"

#include "MMFF94ParameterData.hpp"
#include "DataIOUtilities.hpp"


using namespace CDPL;


namespace
{

    ForceField::MMFF94SymbolicToNumericAtomTypeMap::SharedPointer
        builtinMap(new ForceField::MMFF94SymbolicToNumericAtomTypeMap());

    std::once_flag initBuiltinMapFlag;

    void initBuiltinMap()
    {
        builtinMap->loadDefaults();
    }
} // namespace


ForceField::MMFF94SymbolicToNumericAtomTypeMap::SharedPointer
    ForceField::MMFF94SymbolicToNumericAtomTypeMap::defaultMap = builtinMap;


ForceField::MMFF94SymbolicToNumericAtomTypeMap::MMFF94SymbolicToNumericAtomTypeMap() {}

void ForceField::MMFF94SymbolicToNumericAtomTypeMap::addEntry(const std::string& sym_type,
                                                              unsigned int       num_type)
{
    entries.insert(DataStorage::value_type(sym_type, num_type));
}

unsigned int
ForceField::MMFF94SymbolicToNumericAtomTypeMap::getEntry(const std::string& sym_type) const
{
    DataStorage::const_iterator it = entries.find(sym_type);

    if (it == entries.end())
        return 0;

    return it->second;
}

std::size_t ForceField::MMFF94SymbolicToNumericAtomTypeMap::getNumEntries() const
{
    return entries.size();
}

void ForceField::MMFF94SymbolicToNumericAtomTypeMap::clear()
{
    entries.clear();
}

ForceField::MMFF94SymbolicToNumericAtomTypeMap::ConstEntryIterator
ForceField::MMFF94SymbolicToNumericAtomTypeMap::getEntriesBegin() const
{
    return entries.begin();
}

ForceField::MMFF94SymbolicToNumericAtomTypeMap::ConstEntryIterator
ForceField::MMFF94SymbolicToNumericAtomTypeMap::getEntriesEnd() const
{
    return entries.end();
}

ForceField::MMFF94SymbolicToNumericAtomTypeMap::EntryIterator
ForceField::MMFF94SymbolicToNumericAtomTypeMap::getEntriesBegin()
{
    return entries.begin();
}

ForceField::MMFF94SymbolicToNumericAtomTypeMap::EntryIterator
ForceField::MMFF94SymbolicToNumericAtomTypeMap::getEntriesEnd()
{
    return entries.end();
}

ForceField::MMFF94SymbolicToNumericAtomTypeMap::ConstEntryIterator
ForceField::MMFF94SymbolicToNumericAtomTypeMap::begin() const
{
    return entries.begin();
}

ForceField::MMFF94SymbolicToNumericAtomTypeMap::ConstEntryIterator
ForceField::MMFF94SymbolicToNumericAtomTypeMap::end() const
{
    return entries.end();
}

ForceField::MMFF94SymbolicToNumericAtomTypeMap::EntryIterator
ForceField::MMFF94SymbolicToNumericAtomTypeMap::begin()
{
    return entries.begin();
}

ForceField::MMFF94SymbolicToNumericAtomTypeMap::EntryIterator
ForceField::MMFF94SymbolicToNumericAtomTypeMap::end()
{
    return entries.end();
}

bool ForceField::MMFF94SymbolicToNumericAtomTypeMap::removeEntry(const std::string& sym_type)
{
    return entries.erase(sym_type);
}

ForceField::MMFF94SymbolicToNumericAtomTypeMap::EntryIterator
ForceField::MMFF94SymbolicToNumericAtomTypeMap::removeEntry(const EntryIterator& it)
{
    return entries.erase(it);
}

void ForceField::MMFF94SymbolicToNumericAtomTypeMap::load(std::istream& is)
{
    std::string  line;
    std::string  sym_type;
    unsigned int num_type;

    while (readMMFF94DataLine(is, line,
                              "MMFF94SymbolicToNumericAtomTypeMap: error while reading numeric "
                              "atom type definition entry")) {
        std::istringstream line_iss(line);

        if (!(line_iss >> sym_type))
            throw Base::IOError(
                "MMFF94SymbolicToNumericAtomTypeMap: error while reading symbolic atom type");

        if (!(line_iss >> num_type))
            throw Base::IOError(
                "MMFF94SymbolicToNumericAtomTypeMap: error while reading numeric atom type");

        addEntry(sym_type, num_type);
    }
}

void ForceField::MMFF94SymbolicToNumericAtomTypeMap::loadDefaults()
{
    boost::iostreams::stream<boost::iostreams::array_source>
        is(MMFF94ParameterData::SYMBOLIC_TO_NUMERIC_ATOM_TYPE_MAPPING,
           MMFF94ParameterData::SYMBOLIC_TO_NUMERIC_ATOM_TYPE_MAPPING_LEN);
    load(is);
}

void ForceField::MMFF94SymbolicToNumericAtomTypeMap::set(const SharedPointer& map)
{
    defaultMap = (!map ? builtinMap : map);
}

const ForceField::MMFF94SymbolicToNumericAtomTypeMap::SharedPointer&
ForceField::MMFF94SymbolicToNumericAtomTypeMap::get()
{
    std::call_once(initBuiltinMapFlag, &initBuiltinMap);

    return defaultMap;
}

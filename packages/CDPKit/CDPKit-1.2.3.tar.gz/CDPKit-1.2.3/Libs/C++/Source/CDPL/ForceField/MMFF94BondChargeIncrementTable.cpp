/* 
 * MMFF94BondChargeIncrementTable.cpp 
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
#include <functional>

#include <boost/iostreams/device/array.hpp>
#include <boost/iostreams/stream.hpp>

#include "CDPL/ForceField/MMFF94BondChargeIncrementTable.hpp"
#include "CDPL/Base/Exceptions.hpp"

#include "MMFF94ParameterData.hpp"
#include "DataIOUtilities.hpp"


using namespace CDPL;


namespace
{

    ForceField::MMFF94BondChargeIncrementTable::SharedPointer
        builtinTable(new ForceField::MMFF94BondChargeIncrementTable());

    std::once_flag initBuiltinTableFlag;

    void initBuiltinTable()
    {
        builtinTable->loadDefaults();
    }

    std::uint32_t
    lookupKey(std::uint32_t bond_type_idx, std::uint32_t atom1_type, std::uint32_t atom2_type)
    {
        if (atom1_type < atom2_type)
            return ((atom1_type << 16) + (atom2_type << 8) + bond_type_idx);

        return ((atom2_type << 16) + (atom1_type << 8) + bond_type_idx);
    }

    const ForceField::MMFF94BondChargeIncrementTable::Entry NOT_FOUND;
} // namespace


ForceField::MMFF94BondChargeIncrementTable::SharedPointer
    ForceField::MMFF94BondChargeIncrementTable::defaultTable = builtinTable;


ForceField::MMFF94BondChargeIncrementTable::Entry::Entry():
    bondTypeIdx(0), atom1Type(0), atom2Type(0), chargeIncr(0), initialized(false)
{}

ForceField::MMFF94BondChargeIncrementTable::Entry::Entry(unsigned int bond_type_idx,
                                                         unsigned int atom1_type,
                                                         unsigned int atom2_type,
                                                         double       bond_chg_inc):
    bondTypeIdx(bond_type_idx),
    atom1Type(atom1_type), atom2Type(atom2_type), chargeIncr(bond_chg_inc), initialized(true)
{}

unsigned int ForceField::MMFF94BondChargeIncrementTable::Entry::getBondTypeIndex() const
{
    return bondTypeIdx;
}

unsigned int ForceField::MMFF94BondChargeIncrementTable::Entry::getAtom1Type() const
{
    return atom1Type;
}

unsigned int ForceField::MMFF94BondChargeIncrementTable::Entry::getAtom2Type() const
{
    return atom2Type;
}

double ForceField::MMFF94BondChargeIncrementTable::Entry::getChargeIncrement() const
{
    return chargeIncr;
}

ForceField::MMFF94BondChargeIncrementTable::Entry::operator bool() const
{
    return initialized;
}


ForceField::MMFF94BondChargeIncrementTable::MMFF94BondChargeIncrementTable() {}

void ForceField::MMFF94BondChargeIncrementTable::addEntry(unsigned int bond_type_idx,
                                                          unsigned int atom1_type,
                                                          unsigned int atom2_type,
                                                          double       bond_chg_inc)
{
    entries.insert(
        DataStorage::value_type(lookupKey(bond_type_idx, atom1_type, atom2_type),
                                Entry(bond_type_idx, atom1_type, atom2_type, bond_chg_inc)));
}

const ForceField::MMFF94BondChargeIncrementTable::Entry&
ForceField::MMFF94BondChargeIncrementTable::getEntry(unsigned int bond_type_idx,
                                                     unsigned int atom1_type,
                                                     unsigned int atom2_type) const
{
    DataStorage::const_iterator it = entries.find(lookupKey(bond_type_idx, atom1_type, atom2_type));

    if (it == entries.end())
        return NOT_FOUND;

    return it->second;
}

std::size_t ForceField::MMFF94BondChargeIncrementTable::getNumEntries() const
{
    return entries.size();
}

void ForceField::MMFF94BondChargeIncrementTable::clear()
{
    entries.clear();
}

bool ForceField::MMFF94BondChargeIncrementTable::removeEntry(unsigned int bond_type_idx,
                                                             unsigned int atom1_type,
                                                             unsigned int atom2_type)
{
    return entries.erase(lookupKey(bond_type_idx, atom1_type, atom2_type));
}

ForceField::MMFF94BondChargeIncrementTable::EntryIterator
ForceField::MMFF94BondChargeIncrementTable::removeEntry(const EntryIterator& it)
{
    return EntryIterator(entries.erase(it.base()),
                         std::bind<Entry&>(&DataStorage::value_type::second,
                                           std::placeholders::_1));
}

ForceField::MMFF94BondChargeIncrementTable::ConstEntryIterator
ForceField::MMFF94BondChargeIncrementTable::getEntriesBegin() const
{
    return ConstEntryIterator(entries.begin(),
                              std::bind(&DataStorage::value_type::second, std::placeholders::_1));
}

ForceField::MMFF94BondChargeIncrementTable::ConstEntryIterator
ForceField::MMFF94BondChargeIncrementTable::getEntriesEnd() const
{
    return ConstEntryIterator(entries.end(),
                              std::bind(&DataStorage::value_type::second, std::placeholders::_1));
}

ForceField::MMFF94BondChargeIncrementTable::EntryIterator
ForceField::MMFF94BondChargeIncrementTable::getEntriesBegin()
{
    return EntryIterator(entries.begin(), std::bind<Entry&>(&DataStorage::value_type::second,
                                                            std::placeholders::_1));
}

ForceField::MMFF94BondChargeIncrementTable::EntryIterator
ForceField::MMFF94BondChargeIncrementTable::getEntriesEnd()
{
    return EntryIterator(entries.end(), std::bind<Entry&>(&DataStorage::value_type::second,
                                                          std::placeholders::_1));
}

ForceField::MMFF94BondChargeIncrementTable::ConstEntryIterator
ForceField::MMFF94BondChargeIncrementTable::begin() const
{
    return ConstEntryIterator(entries.begin(),
                              std::bind(&DataStorage::value_type::second, std::placeholders::_1));
}

ForceField::MMFF94BondChargeIncrementTable::ConstEntryIterator
ForceField::MMFF94BondChargeIncrementTable::end() const
{
    return ConstEntryIterator(entries.end(),
                              std::bind(&DataStorage::value_type::second, std::placeholders::_1));
}

ForceField::MMFF94BondChargeIncrementTable::EntryIterator
ForceField::MMFF94BondChargeIncrementTable::begin()
{
    return EntryIterator(entries.begin(), std::bind<Entry&>(&DataStorage::value_type::second,
                                                            std::placeholders::_1));
}

ForceField::MMFF94BondChargeIncrementTable::EntryIterator
ForceField::MMFF94BondChargeIncrementTable::end()
{
    return EntryIterator(entries.end(), std::bind<Entry&>(&DataStorage::value_type::second,
                                                          std::placeholders::_1));
}

void ForceField::MMFF94BondChargeIncrementTable::load(std::istream& is)
{
    std::string  line;
    unsigned int bond_type_idx;
    unsigned int atom1_type;
    unsigned int atom2_type;
    double       bond_chg_inc;

    while (readMMFF94DataLine(is, line,
                              "MMFF94BondChargeIncrementTable: error while reading bond charge "
                              "increment parameter entry")) {
        std::istringstream line_iss(line);

        if (!(line_iss >> bond_type_idx))
            throw Base::IOError(
                "MMFF94BondChargeIncrementTable: error while reading bond type index");

        if (!(line_iss >> atom1_type))
            throw Base::IOError(
                "MMFF94BondChargeIncrementTable: error while reading type of first atom");

        if (!(line_iss >> atom2_type))
            throw Base::IOError(
                "MMFF94BondChargeIncrementTable: error while reading type of second atom");

        if (!(line_iss >> bond_chg_inc))
            throw Base::IOError(
                "MMFF94BondChargeIncrementTable: error while reading bond charge increment");

        addEntry(bond_type_idx, atom1_type, atom2_type, bond_chg_inc);
    }
}

void ForceField::MMFF94BondChargeIncrementTable::loadDefaults()
{
    boost::iostreams::stream<boost::iostreams::array_source>
        is(MMFF94ParameterData::BOND_CHARGE_INCREMENT_PARAMETERS,
           MMFF94ParameterData::BOND_CHARGE_INCREMENT_PARAMETERS_LEN);
    load(is);
}

void ForceField::MMFF94BondChargeIncrementTable::set(const SharedPointer& table)
{
    defaultTable = (!table ? builtinTable : table);
}

const ForceField::MMFF94BondChargeIncrementTable::SharedPointer&
ForceField::MMFF94BondChargeIncrementTable::get()
{
    std::call_once(initBuiltinTableFlag, &initBuiltinTable);

    return defaultTable;
}

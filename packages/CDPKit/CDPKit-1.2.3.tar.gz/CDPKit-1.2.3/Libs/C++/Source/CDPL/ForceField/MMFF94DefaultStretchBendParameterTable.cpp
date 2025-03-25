/* 
 * MMFF94DefaultStretchBendParameterTable.cpp 
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

#include "CDPL/ForceField/MMFF94DefaultStretchBendParameterTable.hpp"
#include "CDPL/Base/Exceptions.hpp"

#include "MMFF94ParameterData.hpp"
#include "DataIOUtilities.hpp"


using namespace CDPL;


namespace
{

    ForceField::MMFF94DefaultStretchBendParameterTable::SharedPointer
        builtinTable(new ForceField::MMFF94DefaultStretchBendParameterTable());

    std::once_flag initBuiltinTableFlag;

    void initBuiltinTable()
    {
        builtinTable->loadDefaults();
    }

    std::uint32_t lookupKey(std::uint32_t term_atom1_pte_row, std::uint32_t ctr_atom_pte_row,
                            std::uint32_t term_atom2_pte_row)
    {
        if (term_atom1_pte_row < term_atom2_pte_row)
            return ((term_atom1_pte_row << 16) + (ctr_atom_pte_row << 8) + term_atom2_pte_row);

        return ((term_atom2_pte_row << 16) + (ctr_atom_pte_row << 8) + term_atom1_pte_row);
    }

    const ForceField::MMFF94DefaultStretchBendParameterTable::Entry NOT_FOUND;
} // namespace


ForceField::MMFF94DefaultStretchBendParameterTable::SharedPointer
    ForceField::MMFF94DefaultStretchBendParameterTable::defaultTable = builtinTable;


ForceField::MMFF94DefaultStretchBendParameterTable::Entry::Entry():
    termAtom1PTERow(0), ctrAtomPTERow(0), termAtom2PTERow(0), ijkForceConst(0), kjiForceConst(0),
    initialized(false)
{}

ForceField::MMFF94DefaultStretchBendParameterTable::Entry::Entry(unsigned int term_atom1_pte_row,
                                                                 unsigned int ctr_atom_pte_row,
                                                                 unsigned int term_atom2_pte_row,
                                                                 double       ijk_force_const,
                                                                 double       kji_force_const):
    termAtom1PTERow(term_atom1_pte_row),
    ctrAtomPTERow(ctr_atom_pte_row), termAtom2PTERow(term_atom2_pte_row),
    ijkForceConst(ijk_force_const), kjiForceConst(kji_force_const), initialized(true)
{}

unsigned int
ForceField::MMFF94DefaultStretchBendParameterTable::Entry::getTerminalAtom1PTERow() const
{
    return termAtom1PTERow;
}

unsigned int ForceField::MMFF94DefaultStretchBendParameterTable::Entry::getCenterAtomPTERow() const
{
    return ctrAtomPTERow;
}

unsigned int
ForceField::MMFF94DefaultStretchBendParameterTable::Entry::getTerminalAtom2PTERow() const
{
    return termAtom2PTERow;
}

double ForceField::MMFF94DefaultStretchBendParameterTable::Entry::getIJKForceConstant() const
{
    return ijkForceConst;
}

double ForceField::MMFF94DefaultStretchBendParameterTable::Entry::getKJIForceConstant() const
{
    return kjiForceConst;
}

ForceField::MMFF94DefaultStretchBendParameterTable::Entry::operator bool() const
{
    return initialized;
}


ForceField::MMFF94DefaultStretchBendParameterTable::MMFF94DefaultStretchBendParameterTable() {}

void ForceField::MMFF94DefaultStretchBendParameterTable::addEntry(unsigned int term_atom1_pte_row,
                                                                  unsigned int ctr_atom_pte_row,
                                                                  unsigned int term_atom2_pte_row,
                                                                  double       ijk_force_const,
                                                                  double       kji_force_const)
{
    entries.insert(
        DataStorage::value_type(lookupKey(term_atom1_pte_row, ctr_atom_pte_row, term_atom2_pte_row),
                                Entry(term_atom1_pte_row, ctr_atom_pte_row, term_atom2_pte_row,
                                      ijk_force_const, kji_force_const)));
}

const ForceField::MMFF94DefaultStretchBendParameterTable::Entry&
ForceField::MMFF94DefaultStretchBendParameterTable::getEntry(unsigned int term_atom1_pte_row,
                                                             unsigned int ctr_atom_pte_row,
                                                             unsigned int term_atom2_pte_row) const
{
    DataStorage::const_iterator it =
        entries.find(lookupKey(term_atom1_pte_row, ctr_atom_pte_row, term_atom2_pte_row));

    if (it == entries.end())
        return NOT_FOUND;

    return it->second;
}

std::size_t ForceField::MMFF94DefaultStretchBendParameterTable::getNumEntries() const
{
    return entries.size();
}

void ForceField::MMFF94DefaultStretchBendParameterTable::clear()
{
    entries.clear();
}

bool ForceField::MMFF94DefaultStretchBendParameterTable::removeEntry(
    unsigned int term_atom1_pte_row, unsigned int ctr_atom_pte_row, unsigned int term_atom2_pte_row)
{
    return entries.erase(lookupKey(term_atom1_pte_row, ctr_atom_pte_row, term_atom2_pte_row));
}

ForceField::MMFF94DefaultStretchBendParameterTable::EntryIterator
ForceField::MMFF94DefaultStretchBendParameterTable::removeEntry(const EntryIterator& it)
{
    return EntryIterator(entries.erase(it.base()),
                         std::bind<Entry&>(&DataStorage::value_type::second,
                                           std::placeholders::_1));
}

ForceField::MMFF94DefaultStretchBendParameterTable::ConstEntryIterator
ForceField::MMFF94DefaultStretchBendParameterTable::getEntriesBegin() const
{
    return ConstEntryIterator(entries.begin(),
                              std::bind(&DataStorage::value_type::second, std::placeholders::_1));
}

ForceField::MMFF94DefaultStretchBendParameterTable::ConstEntryIterator
ForceField::MMFF94DefaultStretchBendParameterTable::getEntriesEnd() const
{
    return ConstEntryIterator(entries.end(),
                              std::bind(&DataStorage::value_type::second, std::placeholders::_1));
}

ForceField::MMFF94DefaultStretchBendParameterTable::EntryIterator
ForceField::MMFF94DefaultStretchBendParameterTable::getEntriesBegin()
{
    return EntryIterator(entries.begin(), std::bind<Entry&>(&DataStorage::value_type::second,
                                                            std::placeholders::_1));
}

ForceField::MMFF94DefaultStretchBendParameterTable::EntryIterator
ForceField::MMFF94DefaultStretchBendParameterTable::getEntriesEnd()
{
    return EntryIterator(entries.end(), std::bind<Entry&>(&DataStorage::value_type::second,
                                                          std::placeholders::_1));
}

ForceField::MMFF94DefaultStretchBendParameterTable::ConstEntryIterator
ForceField::MMFF94DefaultStretchBendParameterTable::begin() const
{
    return ConstEntryIterator(entries.begin(),
                              std::bind(&DataStorage::value_type::second, std::placeholders::_1));
}

ForceField::MMFF94DefaultStretchBendParameterTable::ConstEntryIterator
ForceField::MMFF94DefaultStretchBendParameterTable::end() const
{
    return ConstEntryIterator(entries.end(),
                              std::bind(&DataStorage::value_type::second, std::placeholders::_1));
}

ForceField::MMFF94DefaultStretchBendParameterTable::EntryIterator
ForceField::MMFF94DefaultStretchBendParameterTable::begin()
{
    return EntryIterator(entries.begin(), std::bind<Entry&>(&DataStorage::value_type::second,
                                                            std::placeholders::_1));
}

ForceField::MMFF94DefaultStretchBendParameterTable::EntryIterator
ForceField::MMFF94DefaultStretchBendParameterTable::end()
{
    return EntryIterator(entries.end(), std::bind<Entry&>(&DataStorage::value_type::second,
                                                          std::placeholders::_1));
}

void ForceField::MMFF94DefaultStretchBendParameterTable::load(std::istream& is)
{
    std::string  line;
    unsigned int term_atom1_pte_row;
    unsigned int ctr_atom_pte_row;
    unsigned int term_atom2_pte_row;
    double       ijk_force_const;
    double       kji_force_const;

    while (readMMFF94DataLine(is, line,
                              "MMFF94DefaultStretchBendParameterTable: error while reading default "
                              "stretch-bend parameter entry")) {
        std::istringstream line_iss(line);

        if (!(line_iss >> term_atom1_pte_row))
            throw Base::IOError("MMFF94DefaultStretchBendParameterTable: error while reading "
                                "terminal atom 1 PTE row");

        if (!(line_iss >> ctr_atom_pte_row))
            throw Base::IOError(
                "MMFF94DefaultStretchBendParameterTable: error while reading center atom PTE row");

        if (!(line_iss >> term_atom2_pte_row))
            throw Base::IOError("MMFF94DefaultStretchBendParameterTable: error while reading "
                                "terminal atom 2 PTE row");

        if (!(line_iss >> ijk_force_const))
            throw Base::IOError(
                "MMFF94DefaultStretchBendParameterTable: error while reading IJK force constant");

        if (!(line_iss >> kji_force_const))
            throw Base::IOError(
                "MMFF94DefaultStretchBendParameterTable: error while reading KJI force constant");

        addEntry(term_atom1_pte_row, ctr_atom_pte_row, term_atom2_pte_row, ijk_force_const,
                 kji_force_const);
    }
}

void ForceField::MMFF94DefaultStretchBendParameterTable::loadDefaults()
{
    boost::iostreams::stream<boost::iostreams::array_source>
        is(MMFF94ParameterData::DEFAULT_STRETCH_BEND_PARAMETERS,
           MMFF94ParameterData::DEFAULT_STRETCH_BEND_PARAMETERS_LEN);
    load(is);
}

void ForceField::MMFF94DefaultStretchBendParameterTable::set(const SharedPointer& table)
{
    defaultTable = (!table ? builtinTable : table);
}

const ForceField::MMFF94DefaultStretchBendParameterTable::SharedPointer&
ForceField::MMFF94DefaultStretchBendParameterTable::get()
{
    std::call_once(initBuiltinTableFlag, &initBuiltinTable);

    return defaultTable;
}

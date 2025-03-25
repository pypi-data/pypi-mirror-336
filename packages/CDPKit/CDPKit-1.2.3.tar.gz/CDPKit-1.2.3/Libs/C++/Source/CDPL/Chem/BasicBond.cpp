/* 
 * BasicBond.cpp 
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

#include <algorithm>
#include <cassert>

#include "CDPL/Chem/BasicBond.hpp"
#include "CDPL/Chem/BasicAtom.hpp"
#include "CDPL/Chem/BasicMolecule.hpp"
#include "CDPL/Base/Exceptions.hpp"


using namespace CDPL;


Chem::BasicBond::BasicBond(BasicMolecule* mol): molecule(mol) 
{
    atoms[0] = 0;
    atoms[1] = 0;
}

Chem::BasicBond::~BasicBond() {}

std::size_t Chem::BasicBond::getIndex() const
{
    return index;
}

const Chem::Molecule& Chem::BasicBond::getMolecule() const
{
    return *molecule;
}

Chem::Molecule& Chem::BasicBond::getMolecule()
{
    return *molecule;
}

const Chem::Atom& Chem::BasicBond::getBegin() const
{
    assert(atoms[0]);

    return *atoms[0];
}

const Chem::Atom& Chem::BasicBond::getEnd() const
{
    assert(atoms[1]);

    return *atoms[1];
}

Chem::Atom& Chem::BasicBond::getBegin()
{
    assert(atoms[0]);
    
    return *atoms[0];
}

Chem::Atom& Chem::BasicBond::getEnd()
{
    assert(atoms[1]);

    return *atoms[1];
}

std::size_t Chem::BasicBond::getNumAtoms() const
{
    assert(atoms[0] && atoms[1]);

    return 2;
}

const Chem::Atom& Chem::BasicBond::getAtom(std::size_t idx) const
{
    if (idx >= 2)
        throw Base::IndexError("BasicBond: atom index out of bounds");

    return *atoms[idx];
}

Chem::Atom& Chem::BasicBond::getAtom(std::size_t idx)
{
    if (idx >= 2)
        throw Base::IndexError("BasicBond: atom index out of bounds");

    return *atoms[idx];
}

bool Chem::BasicBond::containsAtom(const Atom& atom) const
{
    return (atoms[0] == &atom || atoms[1] == &atom);
}

std::size_t Chem::BasicBond::getAtomIndex(const Atom& atom) const
{
    if (atoms[0] == &atom)
        return 0;

    if (atoms[1] == &atom)
        return 1;

    throw Base::ItemNotFound("BasicBond: argument atom not a member");
}

const Chem::Atom& Chem::BasicBond::getNeighbor(const Atom& atom) const
{
    if (atoms[0] == &atom)
        return *atoms[1];

    if (atoms[1] == &atom)
        return *atoms[0];

    throw Base::ItemNotFound("BasicBond: argument atom not a member");
}

Chem::Atom& Chem::BasicBond::getNeighbor(const Atom& atom)
{
    if (atoms[0] == &atom)
        return *atoms[1];

    if (atoms[1] == &atom)
        return *atoms[0];

    throw Base::ItemNotFound("BasicBond: argument atom not a member");
}

Chem::BasicBond& Chem::BasicBond::operator=(const BasicBond& bond) 
{
    if (this == &bond)
        return *this;

    Bond::operator=(bond);

    return *this;
}

void Chem::BasicBond::setIndex(std::size_t idx)
{
    index = idx;
}

void Chem::BasicBond::setBegin(BasicAtom& atom)
{
    atoms[0] = &atom;
}

void Chem::BasicBond::setEnd(BasicAtom& atom)
{
    atoms[1] = &atom;
}

void Chem::BasicBond::orderAtoms(const AtomCompareFunction& func)
{
    if (func(*atoms[0], *atoms[1]))
        return;

    std::swap(atoms[0], atoms[1]);
}

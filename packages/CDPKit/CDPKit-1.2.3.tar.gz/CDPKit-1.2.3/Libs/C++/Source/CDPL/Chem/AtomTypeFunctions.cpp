/* 
 * AtomTypeFunctions.cpp 
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

#include "CDPL/Chem/AtomFunctions.hpp"
#include "CDPL/Chem/AtomDictionary.hpp"
#include "CDPL/Chem/AtomType.hpp"


using namespace CDPL; 


const std::string& Chem::getSymbolForType(const Atom& atom)
{
    return AtomDictionary::getSymbol(getType(atom));
}

unsigned int Chem::getTypeForSymbol(const Atom& atom)
{
    return AtomDictionary::getType(getSymbol(atom));
}

unsigned int Chem::getGenericType(const Atom& atom)
{
    unsigned int atom_type = getType(atom);

    if (atom_type == AtomType::UNKNOWN || (atom_type > AtomType::MAX_ATOMIC_NO && atom_type <= AtomType::MAX_TYPE))
        return atom_type; 

    if (atom_type > AtomType::MAX_TYPE)
        return AtomType::UNKNOWN; 

    if (atom_type == AtomType::N || atom_type == AtomType::O || atom_type == AtomType::S || atom_type == AtomType::P)
        return AtomType::HET;

    if (AtomDictionary::isHalogen(atom_type))
        return AtomType::X;

    if (AtomDictionary::isMetal(atom_type))
        return AtomType::M;

    if (atom_type == AtomType::C)
        return AtomType::A;
    
    if (atom_type == AtomType::H)
        return AtomType::QH;

    return AtomType::Q; 
}

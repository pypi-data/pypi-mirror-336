/* 
 * JMEMolecularGraphWriter.cpp 
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

#include <ostream>

#include "CDPL/Chem/JMEMolecularGraphWriter.hpp"
#include "CDPL/Base/Exceptions.hpp"

#include "JMEDataWriter.hpp"


using namespace CDPL;


Chem::JMEMolecularGraphWriter::JMEMolecularGraphWriter(std::ostream& os): 
    output(os), state(os.good()), writer(new JMEDataWriter(*this)) {}

Chem::JMEMolecularGraphWriter::~JMEMolecularGraphWriter() {}

Base::DataWriter<Chem::MolecularGraph>& Chem::JMEMolecularGraphWriter::write(const MolecularGraph& molgraph)
{
    state = false;

    try {
        state = writer->writeMolGraph(output, molgraph);

    } catch (const std::exception& e) {
        throw Base::IOError("JMEMolecularGraphWriter: " + std::string(e.what()));
    }

    invokeIOCallbacks(1.0);

    return *this;
}

Chem::JMEMolecularGraphWriter::operator const void*() const
{
    return (state ? this : 0);
}

bool Chem::JMEMolecularGraphWriter::operator!() const
{
    return !state;
}

/* 
 * MMTFDataWriter.hpp 
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


#ifndef CDPL_BIOMOL_MMTFDATAWRITER_HPP
#define CDPL_BIOMOL_MMTFDATAWRITER_HPP

#include <iosfwd>
#include <vector>
#include <cstddef>

#include <mmtf.hpp>

#include "CDPL/Math/Vector.hpp"
#include "CDPL/Util/BitSet.hpp"


namespace CDPL
{

    namespace Chem
    {

        class Atom;
        class MolecularGraph;
    } // namespace Chem

    namespace Biomol
    {

        class MMTFDataWriter
        {

          public:
            MMTFDataWriter() {}

            bool writeRecord(std::ostream& os, const Chem::MolecularGraph& molgraph);

          private:
            void init(const Chem::MolecularGraph& molgraph);

            void clearStructureData();
            void clearResidueData();

            bool outputStructureData(std::ostream& os, const Chem::MolecularGraph& molgraph);

            std::size_t createStructureData(const Chem::MolecularGraph& molgraph);

            void addAtomData(const Chem::Atom& atom, const Math::Vector3D& coords, long& atom_serial);
            void createResidueBondData(std::size_t start_atom_idx, std::size_t end_atom_idx, const Chem::MolecularGraph& molgraph);
            void addResidueTypeIndex();
            void createGlobalBondData(const Chem::MolecularGraph& molgraph);
            void setStructureMetaData(const Chem::MolecularGraph& molgraph);

            typedef std::vector<const Chem::Atom*> AtomArray;
            typedef std::vector<std::size_t>       AtomIndexArray;

            AtomArray           atoms;
            AtomIndexArray      atomIndices;
            mmtf::StructureData structData;
            mmtf::GroupType     residueData;
            Util::BitSet        resBondMask;
        };
    } // namespace Biomol
} // namespace CDPL

#endif // CDPL_BIOMOL_MMTFDATAWRITER_HPP

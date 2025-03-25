/* -*- mode: c++; c-basic-offset: 4; tab-width: 4; indent-tabs-mode: t -*- */

/* 
 * MolecularGraphUtilityFunctions.cpp 
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
#include <functional>

#include "CDPL/Biomol/MolecularGraphFunctions.hpp"
#include "CDPL/Biomol/AtomFunctions.hpp"
#include "CDPL/Chem/Atom.hpp"
#include "CDPL/Chem/Bond.hpp"
#include "CDPL/Chem/AtomFunctions.hpp"
#include "CDPL/Chem/Entity3DFunctions.hpp"
#include "CDPL/Chem/AtomContainerFunctions.hpp"
#include "CDPL/Chem/AtomType.hpp"
#include "CDPL/MolProp/AtomFunctions.hpp"
#include "CDPL/Math/VectorArrayFunctions.hpp"


using namespace CDPL;


void Biomol::extractResidueSubstructures(const Chem::MolecularGraph& molgraph, const Chem::MolecularGraph& parent_molgraph,
                                         Chem::Fragment& res_substructs, bool cnctd_only, unsigned int flags, bool append)
{
    if (!append)
        res_substructs.clear();

    std::for_each(molgraph.getAtomsBegin(), molgraph.getAtomsEnd(),
                  std::bind(&extractResidueSubstructure, std::placeholders::_1, std::ref(parent_molgraph), std::ref(res_substructs),
                            cnctd_only, flags, true));
}

void Biomol::extractProximalAtoms(const Chem::MolecularGraph& core, const Chem::MolecularGraph& macromol,
                                  Chem::Fragment& env_atoms, double max_dist, bool inc_core_atoms, bool append)
{
    extractProximalAtoms(core, macromol, env_atoms,
                         static_cast<const Math::Vector3D& (*)(const Chem::Entity3D&)>(&Chem::get3DCoordinates), max_dist, inc_core_atoms, append);
}

void Biomol::extractProximalAtoms(const Chem::MolecularGraph& core, const Chem::MolecularGraph& macromol,
                                  Chem::Fragment& env_atoms, const Chem::Atom3DCoordinatesFunction& coords_func,
                                  double max_dist, bool inc_core_atoms, bool append)
{
    using namespace Chem;

    if (!append)
        env_atoms.clear();

    if (core.getNumAtoms() == 0)
        return;

    Math::Vector3DArray core_coords;
    get3DCoordinates(core, core_coords, coords_func);

    Math::Vector3D core_ctr;
    calcCentroid(core_coords, core_ctr);

    double bsphere_rad = 0.0;

    for (Math::Vector3DArray::ConstElementIterator it = core_coords.getElementsBegin(), end = core_coords.getElementsEnd(); it != end; ++it)
        bsphere_rad = std::max(bsphere_rad, length(*it - core_ctr));

    bsphere_rad += max_dist;

    for (MolecularGraph::ConstAtomIterator it = macromol.getAtomsBegin(), end = macromol.getAtomsEnd(); it != end; ++it) {
        const Atom&           atom     = *it;
        const Math::Vector3D& atom_pos = coords_func(atom);

        if (length(atom_pos - core_ctr) > bsphere_rad)
            continue;

        if (!inc_core_atoms && core.containsAtom(atom))
            continue;

        if (env_atoms.containsAtom(atom))
            continue;

        for (Math::Vector3DArray::ConstElementIterator c_it = core_coords.getElementsBegin(), c_end = core_coords.getElementsEnd(); c_it != c_end; ++c_it) {
            if (length(atom_pos - *c_it) <= max_dist) {
                env_atoms.addAtom(atom);
                break;
            }
        }
    }
}

void Biomol::extractEnvironmentResidues(const Chem::MolecularGraph& core, const Chem::MolecularGraph& macromol,
                                        Chem::Fragment& env_residues, double max_dist, bool append)
{
    extractEnvironmentResidues(core, macromol, env_residues,
                               static_cast<const Math::Vector3D& (*)(const Chem::Entity3D&)>(&Chem::get3DCoordinates), max_dist, append);
}

void Biomol::extractEnvironmentResidues(const Chem::MolecularGraph& core, const Chem::MolecularGraph& macromol,
                                        Chem::Fragment& env_residues, const Chem::Atom3DCoordinatesFunction& coords_func,
                                        double max_dist, bool append)
{
    using namespace Chem;

    if (!append)
        env_residues.clear();

    if (core.getNumAtoms() == 0)
        return;

    Math::Vector3DArray core_coords;
    get3DCoordinates(core, core_coords, coords_func);

    Math::Vector3D core_ctr;
    calcCentroid(core_coords, core_ctr);

    double bsphere_rad = 0.0;

    for (Math::Vector3DArray::ConstElementIterator it = core_coords.getElementsBegin(), end = core_coords.getElementsEnd(); it != end; ++it)
        bsphere_rad = std::max(bsphere_rad, length(*it - core_ctr));

    bsphere_rad += max_dist;

    for (MolecularGraph::ConstAtomIterator it = macromol.getAtomsBegin(), end = macromol.getAtomsEnd(); it != end; ++it) {
        const Atom& atom     = *it;
        const Math::Vector3D& atom_pos = coords_func(atom);

        if (length(atom_pos - core_ctr) > bsphere_rad)
            continue;

        if (core.containsAtom(atom) || env_residues.containsAtom(atom))
            continue;

        for (Math::Vector3DArray::ConstElementIterator c_it = core_coords.getElementsBegin(), c_end = core_coords.getElementsEnd(); c_it != c_end; ++c_it) {
            if (length(atom_pos - *c_it) <= max_dist) {
                extractResidueSubstructure(atom, macromol, env_residues, true, Chem::AtomPropertyFlag::DEFAULT, true);
                break;
            }
        }
    }

    std::size_t num_atoms = env_residues.getNumAtoms();

    for (std::size_t i = 0; i < num_atoms; i++) {
        const Atom& env_atom = env_residues.getAtom(i);
        Atom::ConstBondIterator b_it = env_atom.getBondsBegin();

        for (Atom::ConstAtomIterator a_it = env_atom.getAtomsBegin(), a_end = env_atom.getAtomsEnd(); a_it != a_end; ++a_it, ++b_it) {
            const Atom& nbr_atom = *a_it;

            if (!env_residues.containsAtom(nbr_atom))
                continue;

            const Bond& nbr_bond = *b_it;

            if (!macromol.containsBond(nbr_bond))
                continue;

            env_residues.addBond(nbr_bond);
        }
    }
}

void Biomol::setHydrogenResidueSequenceInfo(Chem::MolecularGraph& molgraph, bool overwrite, unsigned int flags)
{
    using namespace Chem;

    if (flags == AtomPropertyFlag::DEFAULT)
        flags = AtomPropertyFlag::RESIDUE_CODE |
                AtomPropertyFlag::RESIDUE_SEQ_NO |
                AtomPropertyFlag::RESIDUE_INS_CODE |
                AtomPropertyFlag::CHAIN_ID |
                AtomPropertyFlag::MODEL_NUMBER;

    for (MolecularGraph::AtomIterator it = molgraph.getAtomsBegin(), end = molgraph.getAtomsEnd(); it != end; ++it) {
        Atom& atom = *it;

        if (getType(atom) != AtomType::H)
            continue;

        if (atom.getNumAtoms() != 1 && MolProp::getHeavyAtomCount(atom, molgraph) != 1)
            continue;

        const Atom& prnt_atom = atom.getAtom(0);

        if (getType(prnt_atom) == AtomType::H)
            overwrite = false;

        if (overwrite) {
            if (flags & AtomPropertyFlag::RESIDUE_CODE) {
                if (hasResidueCode(prnt_atom))
                    setResidueCode(atom, getResidueCode(prnt_atom));
                else
                    clearResidueCode(atom);
            }

            if (flags & AtomPropertyFlag::MODEL_NUMBER) {
                if (hasModelNumber(prnt_atom))
                    setModelNumber(atom, getModelNumber(prnt_atom));
                else
                    clearModelNumber(atom);
            }

            if (flags & AtomPropertyFlag::RESIDUE_SEQ_NO) {
                if (hasResidueSequenceNumber(prnt_atom))
                    setResidueSequenceNumber(atom, getResidueSequenceNumber(prnt_atom));
                else
                    clearResidueSequenceNumber(atom);
            }

            if (flags & AtomPropertyFlag::CHAIN_ID) {
                if (hasChainID(prnt_atom))
                    setChainID(atom, getChainID(prnt_atom));
                else
                    clearChainID(atom);
            }

            if (flags & AtomPropertyFlag::RESIDUE_INS_CODE) {
                if (hasResidueInsertionCode(prnt_atom))
                    setResidueInsertionCode(atom, getResidueInsertionCode(prnt_atom));
                else
                    clearResidueInsertionCode(atom);
            }

        } else {
            if ((flags & AtomPropertyFlag::RESIDUE_CODE) && !hasResidueCode(atom) && hasResidueCode(prnt_atom))
                setResidueCode(atom, getResidueCode(prnt_atom));

            if ((flags & AtomPropertyFlag::MODEL_NUMBER) && !hasModelNumber(atom) && hasModelNumber(prnt_atom))
                setModelNumber(atom, getModelNumber(prnt_atom));

            if ((flags & AtomPropertyFlag::RESIDUE_SEQ_NO) && !hasResidueSequenceNumber(atom) && hasResidueSequenceNumber(prnt_atom))
                setResidueSequenceNumber(atom, getResidueSequenceNumber(prnt_atom));

            if ((flags & AtomPropertyFlag::CHAIN_ID) && !hasChainID(atom) && hasChainID(prnt_atom))
                setChainID(atom, getChainID(prnt_atom));

            if ((flags & AtomPropertyFlag::RESIDUE_INS_CODE) && !hasResidueInsertionCode(atom) && hasResidueInsertionCode(prnt_atom))
                setResidueInsertionCode(atom, getResidueInsertionCode(prnt_atom));
        }
    }
}

bool Biomol::matchesResidueInfo(const Chem::MolecularGraph& molgraph, const char* res_code, const char* chain_id, long res_seq_no,
                                char ins_code, std::size_t model_no)
{
    if ((res_code != 0) && (getResidueCode(molgraph) != res_code))
        return false;

    if ((chain_id != 0) && (getChainID(molgraph) != chain_id))
        return false;

    if ((res_seq_no != IGNORE_SEQUENCE_NO) && (getResidueSequenceNumber(molgraph) != res_seq_no))
        return false;

    if ((ins_code != 0) && (getResidueInsertionCode(molgraph) != ins_code))
        return false;

    if ((model_no != 0) && (getModelNumber(molgraph) != model_no))
        return false;

    return true;
}

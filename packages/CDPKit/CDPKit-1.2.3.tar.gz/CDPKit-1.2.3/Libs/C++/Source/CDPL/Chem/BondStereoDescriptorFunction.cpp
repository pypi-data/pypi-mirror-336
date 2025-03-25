/* 
 * BondStereoDescriptorFunction.cpp 
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

#include "CDPL/Chem/BondFunctions.hpp"
#include "CDPL/Chem/AtomFunctions.hpp"
#include "CDPL/Chem/Entity3DFunctions.hpp"
#include "CDPL/Chem/Bond.hpp"
#include "CDPL/Chem/Atom.hpp"
#include "CDPL/Chem/Molecule.hpp"
#include "CDPL/Chem/StereoDescriptor.hpp"
#include "CDPL/Chem/BondConfiguration.hpp"
#include "CDPL/Chem/HybridizationState.hpp"
#include "CDPL/Chem/AtomPropertyFlag.hpp"
#include "CDPL/Chem/BondStereoFlag.hpp"
#include "CDPL/Internal/AtomFunctions.hpp"


using namespace CDPL; 


namespace
{
    
    void translateBondStereoDescriptors(Chem::Molecule& tgt_mol, const Chem::MolecularGraph& src_molgraph)
    {
        using namespace Chem;
        
        if (tgt_mol.getNumAtoms() < src_molgraph.getNumAtoms())
            return;

        if (tgt_mol.getNumBonds() < src_molgraph.getNumBonds())
            return;

        std::size_t atom_idx_offs = tgt_mol.getNumAtoms() - src_molgraph.getNumAtoms();
        std::size_t bond_idx_offs = tgt_mol.getNumBonds() - src_molgraph.getNumBonds();
        
        MolecularGraph::ConstBondIterator bonds_end = src_molgraph.getBondsEnd();
        std::size_t i = bond_idx_offs;
        std::size_t num_tgt_bonds = tgt_mol.getNumBonds();

        for (MolecularGraph::ConstBondIterator b_it = src_molgraph.getBondsBegin(); b_it != bonds_end && i < num_tgt_bonds; ++b_it, i++) {
            const Bond& bond = *b_it;
            Bond& tgt_bond = tgt_mol.getBond(i);
            const StereoDescriptor& stereo_desc = getStereoDescriptor(bond);

            if (stereo_desc.getNumReferenceAtoms() == 0)
                continue;

            const Atom* const* ref_atoms = stereo_desc.getReferenceAtoms();

            try {
                setStereoDescriptor(tgt_bond,
                                    StereoDescriptor(stereo_desc.getConfiguration(),
                                                     tgt_mol.getAtom(src_molgraph.getAtomIndex(*ref_atoms[0]) + atom_idx_offs),
                                                     tgt_mol.getAtom(src_molgraph.getAtomIndex(*ref_atoms[1]) + atom_idx_offs),
                                                     tgt_mol.getAtom(src_molgraph.getAtomIndex(*ref_atoms[2]) + atom_idx_offs),
                                                     tgt_mol.getAtom(src_molgraph.getAtomIndex(*ref_atoms[3]) + atom_idx_offs)));
            } catch (const Base::IndexError& e) {
                clearStereoDescriptor(tgt_bond);
            } catch (const Base::ItemNotFound& e) {
                clearStereoDescriptor(tgt_bond);
            }
        }
    }
    
    struct Init
    {

        Init() {
            Chem::Molecule::registerCopyPostprocessingFunction(&translateBondStereoDescriptors);
        }
    } init;
    
    Chem::StereoDescriptor makeStereoDescriptor(unsigned int config, const Chem::Bond& bond, const Chem::MolecularGraph& molgraph)
    {
        using namespace Chem;

        const Atom* ref_atoms[2] = { 0, 0 };

        for (std::size_t i = 0; i < 2; i++) {
            for (std::size_t j = 0; j < bond.getAtom(i).getNumAtoms(); j++) {
                if (&bond.getAtom(i).getBond(j) == &bond)
                    continue;

                if (molgraph.containsAtom(bond.getAtom(i).getAtom(j)) && molgraph.containsBond(bond.getAtom(i).getBond(j))) {
                    ref_atoms[i] = &bond.getAtom(i).getAtom(j);
                    break;
                }
            }

            if (!ref_atoms[i])
                return StereoDescriptor(config);
        }

        return StereoDescriptor(config, *ref_atoms[0], bond.getBegin(), bond.getEnd(), *ref_atoms[1]);
    }

    const Chem::StereoDescriptor DEF_DESCRIPTOR = Chem::StereoDescriptor(Chem::BondConfiguration::UNDEF);
}


Chem::StereoDescriptor Chem::calcStereoDescriptor(const Bond& bond, const MolecularGraph& molgraph, std::size_t dim)
{
    const Atom* bond_atoms[2] = { &bond.getBegin(), &bond.getEnd() };

    for (std::size_t i = 0; i < 2; i++) {
        std::size_t num_bonds = Internal::getExplicitBondCount(*bond_atoms[i], molgraph);

        if (num_bonds < 2 || num_bonds > 3)
            return StereoDescriptor(BondConfiguration::NONE);

        if (getHybridizationState(*bond_atoms[i]) != HybridizationState::SP2)
            return StereoDescriptor(BondConfiguration::NONE);

        if ((num_bonds + getImplicitHydrogenCount(*bond_atoms[i])) > 3)
            return false;
    }

    bool has_either_bond = false;

    if (dim != 3 && dim != 0) {
        unsigned int bnd_stereo = get2DStereoFlag(bond);

        if (bnd_stereo == BondStereoFlag::EITHER || bnd_stereo == BondStereoFlag::REVERSE_EITHER) {
            if (dim == 2)
                return makeStereoDescriptor(BondConfiguration::EITHER, bond, molgraph);

            has_either_bond = true;
        }
    }

    const Atom* ref_atoms[2] = { 0, 0 };

    for (std::size_t i = 0; i < 2; i++) {
        Atom::ConstAtomIterator atoms_end = bond_atoms[i]->getAtomsEnd();
        Atom::ConstBondIterator b_it = bond_atoms[i]->getBondsBegin();

        for (Atom::ConstAtomIterator a_it = bond_atoms[i]->getAtomsBegin(); a_it != atoms_end; ++a_it, ++b_it) {
            const Bond& nbr_bond = *b_it;

            if (&nbr_bond == &bond)
                continue;

            if (!molgraph.containsBond(nbr_bond))
                continue;

            const Atom* nbr_atom = &*a_it;

            if (!molgraph.containsAtom(*nbr_atom))
                continue;

            if (dim != 3 && dim != 0) {
                unsigned int bnd_stereo = get2DStereoFlag(nbr_bond);

                if ((bnd_stereo == BondStereoFlag::EITHER || bnd_stereo == BondStereoFlag::REVERSE_EITHER)) {
                    if (dim == 2)
                        return makeStereoDescriptor(BondConfiguration::EITHER, bond, molgraph);

                    has_either_bond = true;
                }
            }

            if (!ref_atoms[i])
                ref_atoms[i] = nbr_atom;
        }

        if (!ref_atoms[i])
            return StereoDescriptor(BondConfiguration::NONE);
    }

    if (dim != 2 && dim != 3) {
        const StereoDescriptor& stereo_desc = getStereoDescriptor(bond);
        unsigned int config = stereo_desc.getConfiguration();

        if ((config == BondConfiguration::CIS || config == BondConfiguration::TRANS) && stereo_desc.isValid(bond)) {
            const Atom* const* sto_ref_atoms = stereo_desc.getReferenceAtoms();
            const Atom* old_ref_atoms[2];

            if (sto_ref_atoms[1] == bond_atoms[1] && sto_ref_atoms[2] == bond_atoms[0]) {
                old_ref_atoms[0] = sto_ref_atoms[3];
                old_ref_atoms[1] = sto_ref_atoms[0];

            } else {
                old_ref_atoms[0] = sto_ref_atoms[0];
                old_ref_atoms[1] = sto_ref_atoms[3];
            }    

            if ((ref_atoms[0] == old_ref_atoms[0]) ^ (ref_atoms[1] == old_ref_atoms[1]))
                config = (config == BondConfiguration::CIS ? BondConfiguration::TRANS : BondConfiguration::CIS);

            return StereoDescriptor(config, *ref_atoms[0], *bond_atoms[0], *bond_atoms[1], *ref_atoms[1]);
        }

        if (config == BondConfiguration::EITHER || config == BondConfiguration::NONE)
            return StereoDescriptor(config, *ref_atoms[0], *bond_atoms[0], *bond_atoms[1], *ref_atoms[1]);

        if (dim == 0)
            return StereoDescriptor(BondConfiguration::UNDEF, *ref_atoms[0], *bond_atoms[0], *bond_atoms[1], *ref_atoms[1]);
    }

    if (dim != 2) {
        try {
            const Math::Vector3D& ligand1_coords = get3DCoordinates(*ref_atoms[0]);
            const Math::Vector3D& ligand2_coords = get3DCoordinates(*ref_atoms[1]);
            const Math::Vector3D& atom1_coords = get3DCoordinates(*bond_atoms[0]);
            const Math::Vector3D& atom2_coords = get3DCoordinates(*bond_atoms[1]);

            double tmp = innerProd(crossProd(ligand1_coords - atom1_coords, atom2_coords - atom1_coords), 
                                   crossProd(ligand2_coords - atom2_coords, atom1_coords - atom2_coords));

            return (tmp < 0.0 ? StereoDescriptor(BondConfiguration::CIS, *ref_atoms[0], *bond_atoms[0], *bond_atoms[1], *ref_atoms[1]) : 
                    tmp > 0.0 ? StereoDescriptor(BondConfiguration::TRANS, *ref_atoms[0], *bond_atoms[0], *bond_atoms[1], *ref_atoms[1]) :
                    StereoDescriptor(BondConfiguration::UNDEF, *ref_atoms[0], *bond_atoms[0], *bond_atoms[1], *ref_atoms[1]));    

        } catch (const Base::ItemNotFound& e) {
            if (dim == 3)
                throw e;
        }
    }

    if (has_either_bond) 
        return StereoDescriptor(BondConfiguration::EITHER, *ref_atoms[0], *bond_atoms[0], *bond_atoms[1], *ref_atoms[1]);

    try {
        const Math::Vector2D& ligand1_coords = get2DCoordinates(*ref_atoms[0]);
        const Math::Vector2D& ligand2_coords = get2DCoordinates(*ref_atoms[1]);
        const Math::Vector2D& atom1_coords = get2DCoordinates(*bond_atoms[0]);
        const Math::Vector2D& atom2_coords = get2DCoordinates(*bond_atoms[1]);

        double tmp = ((atom2_coords[0] - ligand1_coords[0]) * (atom1_coords[1] - ligand1_coords[1])
                      - (atom2_coords[1] - ligand1_coords[1]) * (atom1_coords[0] - ligand1_coords[0]))
            * ((atom1_coords[0] - ligand2_coords[0]) * (atom2_coords[1] - ligand2_coords[1])
               - (atom1_coords[1] - ligand2_coords[1]) * (atom2_coords[0] - ligand2_coords[0]));

        return (tmp > 0.0 ? StereoDescriptor(BondConfiguration::TRANS, *ref_atoms[0], *bond_atoms[0], *bond_atoms[1], *ref_atoms[1]) :
                tmp < 0.0 ? StereoDescriptor(BondConfiguration::CIS, *ref_atoms[0], *bond_atoms[0], *bond_atoms[1], *ref_atoms[1]) :
                StereoDescriptor(BondConfiguration::UNDEF, *ref_atoms[0], *bond_atoms[0], *bond_atoms[1], *ref_atoms[1]));  

    } catch (const Base::ItemNotFound& e) {
        if (dim == 2)
            throw e;
    }

    return StereoDescriptor(BondConfiguration::UNDEF, *ref_atoms[0], *bond_atoms[0], *bond_atoms[1], *ref_atoms[1]);
}

unsigned int Chem::calcConfiguration(const Bond& bond, const MolecularGraph& molgraph, const StereoDescriptor& descr, const Math::Vector3DArray& coords)
{
    std::size_t num_ref_atoms = descr.getNumReferenceAtoms();

    if (num_ref_atoms != 4)
        return BondConfiguration::NONE;

    const Math::Vector3D& ligand1_coords = coords[molgraph.getAtomIndex(*descr.getReferenceAtoms()[0])];
    const Math::Vector3D& atom1_coords = coords[molgraph.getAtomIndex(*descr.getReferenceAtoms()[1])];
    const Math::Vector3D& atom2_coords = coords[molgraph.getAtomIndex(*descr.getReferenceAtoms()[2])];
    const Math::Vector3D& ligand2_coords = coords[molgraph.getAtomIndex(*descr.getReferenceAtoms()[3])];

    double tmp = innerProd(crossProd(ligand1_coords - atom1_coords, atom2_coords - atom1_coords), 
                           crossProd(ligand2_coords - atom2_coords, atom1_coords - atom2_coords));
        
    if (tmp > 0.0)
        return BondConfiguration::TRANS;

    if (tmp < 0.0)
        return BondConfiguration::CIS;

    return BondConfiguration::UNDEF;
}

/* 
 * PSDScreeningDBAccessor.cpp 
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

#include "CDPL/Pharm/PSDScreeningDBAccessor.hpp"
#include "CDPL/Pharm/Pharmacophore.hpp"
#include "CDPL/Chem/Molecule.hpp"

#include "PSDScreeningDBAccessorImpl.hpp"


using namespace CDPL;


Pharm::PSDScreeningDBAccessor::PSDScreeningDBAccessor():
    impl(new PSDScreeningDBAccessorImpl())
{}

Pharm::PSDScreeningDBAccessor::PSDScreeningDBAccessor(const std::string& name):
    impl(new PSDScreeningDBAccessorImpl())
{
    impl->open(name);
}
    
Pharm::PSDScreeningDBAccessor::~PSDScreeningDBAccessor() {}

void Pharm::PSDScreeningDBAccessor::open(const std::string& name)
{
    impl->open(name);
}

void Pharm::PSDScreeningDBAccessor::close()
{
    impl->close();
}

const std::string& Pharm::PSDScreeningDBAccessor::getDatabaseName() const
{
    return impl->getDatabaseName();
}

std::size_t Pharm::PSDScreeningDBAccessor::getNumMolecules() const
{
    return impl->getNumMolecules();
}

std::size_t Pharm::PSDScreeningDBAccessor::getNumPharmacophores() const
{
    return impl->getNumPharmacophores();
}

std::size_t Pharm::PSDScreeningDBAccessor::getNumPharmacophores(std::size_t mol_idx) const
{
    return impl->getNumPharmacophores(mol_idx);
}

void Pharm::PSDScreeningDBAccessor::getMolecule(std::size_t mol_idx, Chem::Molecule& mol, bool overwrite) const
{
    if (overwrite)
        mol.clear();

    impl->getMolecule(mol_idx, mol);
}

void Pharm::PSDScreeningDBAccessor::getPharmacophore(std::size_t pharm_idx, Pharmacophore& pharm, bool overwrite) const
{
    if (overwrite)
        pharm.clear();

    impl->getPharmacophore(pharm_idx, pharm);
}

void Pharm::PSDScreeningDBAccessor::getPharmacophore(std::size_t mol_idx, std::size_t mol_conf_idx, Pharmacophore& pharm, bool overwrite) const
{
    if (overwrite)
        pharm.clear();

    impl->getPharmacophore(mol_idx, mol_conf_idx, pharm);
}

std::size_t Pharm::PSDScreeningDBAccessor::getMoleculeIndex(std::size_t pharm_idx) const
{
    return impl->getMoleculeIndex(pharm_idx);
}

std::size_t Pharm::PSDScreeningDBAccessor::getConformationIndex(std::size_t pharm_idx) const
{
    return impl->getConformationIndex(pharm_idx);
}

const Pharm::FeatureTypeHistogram& Pharm::PSDScreeningDBAccessor::getFeatureCounts(std::size_t pharm_idx) const
{
    return impl->getFeatureCounts(pharm_idx);
}

const Pharm::FeatureTypeHistogram& Pharm::PSDScreeningDBAccessor::getFeatureCounts(std::size_t mol_idx, std::size_t mol_conf_idx) const
{
    return impl->getFeatureCounts(mol_idx, mol_conf_idx);
}

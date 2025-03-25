/* 
 * AromaticFeatureGenerator.cpp 
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
#include <iterator>
#include <functional>

#include "CDPL/Pharm/AromaticFeatureGenerator.hpp"
#include "CDPL/Pharm/Pharmacophore.hpp"
#include "CDPL/Pharm/Feature.hpp"
#include "CDPL/Pharm/FeatureFunctions.hpp"
#include "CDPL/Chem/MolecularGraph.hpp"
#include "CDPL/Chem/Atom.hpp"
#include "CDPL/Chem/Entity3DFunctions.hpp"
#include "CDPL/Math/Vector.hpp"


using namespace CDPL; 


constexpr double       Pharm::AromaticFeatureGenerator::DEF_FEATURE_TOL;
constexpr unsigned int Pharm::AromaticFeatureGenerator::DEF_FEATURE_TYPE;
constexpr unsigned int Pharm::AromaticFeatureGenerator::DEF_FEATURE_GEOM;


Pharm::AromaticFeatureGenerator::AromaticFeatureGenerator(): 
    featureType(DEF_FEATURE_TYPE), featureGeom(DEF_FEATURE_GEOM), featureTol(DEF_FEATURE_TOL) 
{}

Pharm::AromaticFeatureGenerator::AromaticFeatureGenerator(const AromaticFeatureGenerator& gen):
    PatternBasedFeatureGenerator(gen), featureType(gen.featureType), featureGeom(gen.featureGeom),
    featureTol(gen.featureTol)
{}

Pharm::AromaticFeatureGenerator::AromaticFeatureGenerator(const Chem::MolecularGraph& molgraph, Pharmacophore& pharm):
    featureType(DEF_FEATURE_TYPE), featureGeom(DEF_FEATURE_GEOM), featureTol(DEF_FEATURE_TOL) 
{
    generate(molgraph, pharm);
}

Pharm::AromaticFeatureGenerator::~AromaticFeatureGenerator() {}

void Pharm::AromaticFeatureGenerator::setFeatureType(unsigned int type)
{
    featureType = type;
}

unsigned int Pharm::AromaticFeatureGenerator::getFeatureType() const
{
    return featureType;
}

void Pharm::AromaticFeatureGenerator::setFeatureGeometry(unsigned int geom)
{
    featureGeom = geom;
}

unsigned int Pharm::AromaticFeatureGenerator::getFeatureGeometry() const
{
    return featureGeom;
}

void Pharm::AromaticFeatureGenerator::setFeatureTolerance(double tol)
{
    featureTol = tol;
}

double Pharm::AromaticFeatureGenerator::getFeatureTolerance() const
{
    return featureTol;
}

Pharm::AromaticFeatureGenerator& Pharm::AromaticFeatureGenerator::operator=(const AromaticFeatureGenerator& gen)
{
    if (this == &gen)
        return *this;

    PatternBasedFeatureGenerator::operator=(gen);
    featureType = gen.featureType;
    featureGeom = gen.featureGeom;
    featureTol = gen.featureTol; 

    return *this;
}

Pharm::FeatureGenerator::SharedPointer Pharm::AromaticFeatureGenerator::clone() const
{
    return FeatureGenerator::SharedPointer(new AromaticFeatureGenerator(*this));
}

void Pharm::AromaticFeatureGenerator::addNonPatternFeatures(const Chem::MolecularGraph& molgraph, Pharmacophore& pharm)
{
    using namespace Chem;

    aromSSSRSubset.extract(molgraph);
    ringAtomMask.resize(molgraph.getNumAtoms());

    const FragmentList::BaseType& sssr_subset = aromSSSRSubset;

    for (FragmentList::BaseType::ConstElementIterator it = sssr_subset.getElementsBegin(), end = sssr_subset.getElementsEnd(); it != end; ++it) {
        const Fragment& ring = **it;

        ringAtomMask.reset();

        std::for_each(ring.getAtomsBegin(), ring.getAtomsEnd(),
                      std::bind(static_cast<Util::BitSet& (Util::BitSet::*)(Util::BitSet::size_type, bool)>
                                (&Util::BitSet::set), std::ref(ringAtomMask), 
                                std::bind(&AtomContainer::getAtomIndex, &molgraph, std::placeholders::_1), true));

        if (isContainedInExMatchList(ringAtomMask) || isContainedInIncMatchList(ringAtomMask))
            continue;

        featureAtoms.clear();

        std::transform(ring.getAtomsBegin(), ring.getAtomsEnd(), 
                       std::back_inserter(featureAtoms), [](const Atom& atom) { return &atom; });

        Feature& feature = pharm.addFeature();

        setType(feature, featureType);
        setTolerance(feature, featureTol);
        setGeometry(feature, featureGeom);
        setSubstructure(feature, *it);

        Math::Vector3D pos, orient;

        if (calcPlaneFeatureOrientation(featureAtoms, orient, pos)) {
            set3DCoordinates(feature, pos);
            setOrientation(feature, orient);
        }
    } 
}

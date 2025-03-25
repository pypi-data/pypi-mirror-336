/* 
 * FeaturePositionMatchFunctor.cpp 
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

#include "CDPL/Pharm/FeaturePositionMatchFunctor.hpp"
#include "CDPL/Pharm/Feature.hpp"
#include "CDPL/Pharm/FeatureFunctions.hpp"
#include "CDPL/Chem/Entity3DFunctions.hpp"
#include "CDPL/Math/VectorAdapter.hpp"
#include "CDPL/Math/VectorProxy.hpp"


using namespace CDPL; 


bool Pharm::FeaturePositionMatchFunctor::queryMode() const
{
    return qryMode;
}

double Pharm::FeaturePositionMatchFunctor::operator()(const Feature& ftr1, const Feature& ftr2) const
{
    const Math::Vector3D& pos1 = get3DCoordinates(ftr1);
    const Math::Vector3D& pos2 = get3DCoordinates(ftr2);
    Math::Vector3D tmp(pos2);

    tmp.minusAssign(pos1);
 
    double dist = length(tmp);
    double tol = (qryMode ? getTolerance(ftr1) : std::max(getTolerance(ftr1), getTolerance(ftr2)));
    double score = 1.0 - (dist / tol);

    return (dist < 0.0 ? 0.0 : score);
}

double Pharm::FeaturePositionMatchFunctor::operator()(const Feature& ftr1, const Feature& ftr2, const Math::Matrix4D& xform) const
{
    const Math::Vector3D& pos1 = get3DCoordinates(ftr1);
    const Math::Vector3D& pos2 = get3DCoordinates(ftr2);

    Math::Vector3D trans_pos2;

    trans_pos2.assign(range(prod(xform, homog(pos2)), 0, 3));
    trans_pos2.minusAssign(pos1);
 
    double dist = length(trans_pos2);
    double tol = (qryMode ? getTolerance(ftr1) : std::max(getTolerance(ftr1), getTolerance(ftr2)));
    double score = 1.0 - (dist / tol);

    return (dist < 0.0 ? 0.0 : score);
}

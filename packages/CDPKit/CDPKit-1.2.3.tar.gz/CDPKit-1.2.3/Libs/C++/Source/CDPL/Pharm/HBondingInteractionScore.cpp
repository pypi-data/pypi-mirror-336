/* 
 * HBondingInteractionScore.cpp 
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

#include <cmath>
#include <functional>

#include "CDPL/Pharm/HBondingInteractionScore.hpp"
#include "CDPL/Pharm/Feature.hpp"
#include "CDPL/Pharm/FeatureFunctions.hpp"
#include "CDPL/Pharm/FeatureGeometry.hpp"
#include "CDPL/Math/SpecialFunctions.hpp"
#include "CDPL/Chem/Entity3DFunctions.hpp"


using namespace CDPL;


namespace
{

    constexpr double DEF_DONOR_TO_H_DIST      = 1.05;
    constexpr double DEF_H_BOND_TO_AXIS_ANGLE = 65.0;
}


constexpr double Pharm::HBondingInteractionScore::DEF_MIN_HB_LENGTH;
constexpr double Pharm::HBondingInteractionScore::DEF_MAX_HB_LENGTH;
constexpr double Pharm::HBondingInteractionScore::DEF_MIN_AHD_ANGLE;
constexpr double Pharm::HBondingInteractionScore::DEF_MAX_ACC_ANGLE;


Pharm::HBondingInteractionScore::HBondingInteractionScore(bool don_acc, double min_len, double max_len, double min_ahd_ang, double max_acc_ang): 
    donAccOrder(don_acc), minLength(min_len), maxLength(max_len), minAHDAngle(min_ahd_ang), 
    maxAccAngle(max_acc_ang), distScoringFunc(std::bind(&Math::generalizedBell<double>, std::placeholders::_1, 0.5, 10, 0.0)),
    accAngleScoringFunc(std::bind(&Math::generalizedBell<double>, std::placeholders::_1, 0.5, 5.0, 0.0)),
    ahdAngleScoringFunc(std::bind(&Math::generalizedBell<double>, std::placeholders::_1, 0.5, 2.5, 0.0)) {}

double Pharm::HBondingInteractionScore::getMinLength() const
{
    return minLength;
}

double Pharm::HBondingInteractionScore::getMaxLength() const
{
    return maxLength;
}

double Pharm::HBondingInteractionScore::getMinAHDAngle() const
{
    return minAHDAngle;
}

double Pharm::HBondingInteractionScore::getMaxAcceptorAngle() const
{
    return maxAccAngle;
}

void Pharm::HBondingInteractionScore::setDistanceScoringFunction(const DistanceScoringFunction& func)
{
    distScoringFunc = func;
}

void Pharm::HBondingInteractionScore::setAcceptorAngleScoringFunction(const AngleScoringFunction& func)
{
    accAngleScoringFunc = func;
}

void Pharm::HBondingInteractionScore::setAHDAngleScoringFunction(const AngleScoringFunction& func)
{
    ahdAngleScoringFunc = func;
}

double Pharm::HBondingInteractionScore::operator()(const Feature& ftr1, const Feature& ftr2) const
{
    const Feature& don_ftr = (donAccOrder ? ftr1 : ftr2);
    const Feature& acc_ftr = (donAccOrder ? ftr2 : ftr1);
    const Math::Vector3D& don_pos = get3DCoordinates(don_ftr);
    const Math::Vector3D& acc_pos = get3DCoordinates(acc_ftr);
    unsigned int don_geom = getGeometry(don_ftr);
    Math::Vector3D h_acc_vec;
    double score = 1.0;

    if ((don_geom == FeatureGeometry::VECTOR || don_geom == FeatureGeometry::SPHERE) && hasOrientation(don_ftr)) {
        const Math::Vector3D& orient = getOrientation(don_ftr);

        if (don_geom == FeatureGeometry::VECTOR) { 
            Math::Vector3D don_h_vec(orient * DEF_DONOR_TO_H_DIST);
        
            h_acc_vec.assign(acc_pos - (don_pos + don_h_vec));

            double hb_len = length(h_acc_vec);
            double ctr_dev = (hb_len - (maxLength + minLength) * 0.5) / (maxLength - minLength);

            score = distScoringFunc(ctr_dev);

            h_acc_vec /= hb_len;

            double ahd_ang = std::acos(angleCos(-orient, h_acc_vec, 1)) * 180.0 / M_PI;
            double opt_ang_dev = (180.0 - ahd_ang) * 0.5 / (180.0 - minAHDAngle); 

            score *= ahdAngleScoringFunc(opt_ang_dev);
            
        } else {
            h_acc_vec.assign(acc_pos - don_pos);
            
            double don_acc_vec_len = length(h_acc_vec);
            double hda_ang = std::abs(std::acos(angleCos(orient, h_acc_vec, don_acc_vec_len)) - DEF_H_BOND_TO_AXIS_ANGLE / 180.0 * M_PI);
            double hb_len = std::sqrt(DEF_DONOR_TO_H_DIST * DEF_DONOR_TO_H_DIST + don_acc_vec_len * don_acc_vec_len - 2 * DEF_DONOR_TO_H_DIST * don_acc_vec_len * std::cos(hda_ang));
            double ctr_dev = (hb_len - (maxLength + minLength) * 0.5) / (maxLength - minLength);

            score = distScoringFunc(ctr_dev);

            double ahd_ang = std::acos((DEF_DONOR_TO_H_DIST * DEF_DONOR_TO_H_DIST - don_acc_vec_len * don_acc_vec_len + hb_len * hb_len) / (2 * DEF_DONOR_TO_H_DIST * hb_len)) * 180.0 / M_PI;
            double opt_ang_dev = (180.0 - ahd_ang) * 0.5 / (180.0 - minAHDAngle);

            score *= ahdAngleScoringFunc(opt_ang_dev);
            h_acc_vec /= don_acc_vec_len;
        }
        
    } else {
        h_acc_vec.assign(acc_pos - don_pos);

        double don_acc_vec_len = length(h_acc_vec);
        double hb_len = don_acc_vec_len - DEF_DONOR_TO_H_DIST;
        double ctr_dev = (hb_len - (maxLength + minLength) * 0.5) / (maxLength - minLength);

        score = distScoringFunc(ctr_dev);

        h_acc_vec /= don_acc_vec_len;
    }

    if (hasOrientation(acc_ftr)) {
        const Math::Vector3D& acc_vec = getOrientation(acc_ftr);
        double acc_ang = std::acos(angleCos(h_acc_vec, acc_vec, 1)) * 180.0 / M_PI;
        double opt_ang_dev = acc_ang * 0.5 / maxAccAngle; 

        score *= accAngleScoringFunc(opt_ang_dev);
    }

    return score * getWeight(ftr2);
}

double Pharm::HBondingInteractionScore::operator()(const Math::Vector3D& ftr1_pos, const Feature& ftr2) const
{
    if (donAccOrder) {
        Math::Vector3D h_acc_vec(get3DCoordinates(ftr2) - ftr1_pos);

        double don_acc_vec_len = length(h_acc_vec);
        double hb_len = don_acc_vec_len - DEF_DONOR_TO_H_DIST;
        double ctr_dev = (hb_len - (maxLength + minLength) * 0.5) / (maxLength - minLength);
        double score = distScoringFunc(ctr_dev);

        h_acc_vec /= don_acc_vec_len;

        if (hasOrientation(ftr2)) {
            const Math::Vector3D& acc_vec = getOrientation(ftr2);
            double acc_ang = std::acos(angleCos(h_acc_vec, acc_vec, 1)) * 180.0 / M_PI;
            double opt_ang_dev = acc_ang * 0.5 / maxAccAngle; 

            score *= accAngleScoringFunc(opt_ang_dev);
        }
        
        return score * getWeight(ftr2);
    }

    unsigned int don_geom = getGeometry(ftr2);

    if ((don_geom == FeatureGeometry::VECTOR || don_geom == FeatureGeometry::SPHERE) && hasOrientation(ftr2)) {
        const Math::Vector3D& orient = getOrientation(ftr2);
        
        if (don_geom == FeatureGeometry::VECTOR) { 
            Math::Vector3D don_h_vec(orient * DEF_DONOR_TO_H_DIST);
            Math::Vector3D h_acc_vec(ftr1_pos - (get3DCoordinates(ftr2) + don_h_vec));

            double hb_len = length(h_acc_vec);
            double ctr_dev = (hb_len - (maxLength + minLength) * 0.5) / (maxLength - minLength);
            double score = distScoringFunc(ctr_dev);

            h_acc_vec /= hb_len;

            double ahd_ang = std::acos(angleCos(-orient, h_acc_vec, 1)) * 180.0 / M_PI;
            double opt_ang_dev = (180.0 - ahd_ang) * 0.5 / (180.0 - minAHDAngle); 

            return score * ahdAngleScoringFunc(opt_ang_dev) * getWeight(ftr2);
        }

        Math::Vector3D don_acc_vec(ftr1_pos - get3DCoordinates(ftr2));
            
        double don_acc_vec_len = length(don_acc_vec);
        double hda_ang = std::abs(std::acos(angleCos(orient, don_acc_vec, don_acc_vec_len)) - DEF_H_BOND_TO_AXIS_ANGLE / 180.0 * M_PI);
        double hb_len = std::sqrt(DEF_DONOR_TO_H_DIST * DEF_DONOR_TO_H_DIST + don_acc_vec_len * don_acc_vec_len - 2 * DEF_DONOR_TO_H_DIST * don_acc_vec_len * std::cos(hda_ang));
        double ctr_dev = (hb_len - (maxLength + minLength) * 0.5) / (maxLength - minLength);

        double score = distScoringFunc(ctr_dev);

        double ahd_ang = std::acos((DEF_DONOR_TO_H_DIST * DEF_DONOR_TO_H_DIST - don_acc_vec_len * don_acc_vec_len + hb_len * hb_len) / (2 * DEF_DONOR_TO_H_DIST * hb_len)) * 180.0 / M_PI;
        double opt_ang_dev = (180.0 - ahd_ang) * 0.5 / (180.0 - minAHDAngle);

        return score * ahdAngleScoringFunc(opt_ang_dev) * getWeight(ftr2);
    }

    double don_acc_vec_len = length(ftr1_pos - get3DCoordinates(ftr2));
    double hb_len = don_acc_vec_len - DEF_DONOR_TO_H_DIST;
    double ctr_dev = (hb_len - (maxLength + minLength) * 0.5) / (maxLength - minLength);

    return distScoringFunc(ctr_dev) * getWeight(ftr2);
}



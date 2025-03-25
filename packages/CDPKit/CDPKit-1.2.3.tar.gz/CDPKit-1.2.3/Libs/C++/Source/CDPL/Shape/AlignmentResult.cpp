/* 
 * AlignmentResult.cpp 
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

#include "CDPL/Shape/AlignmentResult.hpp"


using namespace CDPL;


Shape::AlignmentResult::AlignmentResult():
    transform(), score(0.0), refShapeSetIdx(0), refShapeIdx(0), algdShapeIdx(0), refSelfOverlap(0.0),
    refColSelfOverlap(0.0), algdSelfOverlap(0.0), algdColSelfOverlap(0.0), overlap(0.0),
    colOverlap(0.0)
{}

const Math::Matrix4D& Shape::AlignmentResult::getTransform() const
{
    return transform;
}

void Shape::AlignmentResult::setTransform(const Math::Matrix4D& xform)
{
    transform = xform;
}

double Shape::AlignmentResult::getScore() const
{
    return score;
}

void Shape::AlignmentResult::setScore(double score)
{
    this->score = score;
}

std::size_t Shape::AlignmentResult::getReferenceShapeSetIndex() const 
{
    return refShapeSetIdx;
}

void Shape::AlignmentResult::setReferenceShapeSetIndex(std::size_t idx)
{
    refShapeSetIdx = idx;
}

std::size_t Shape::AlignmentResult::getReferenceShapeIndex() const 
{
    return refShapeIdx;
}

void Shape::AlignmentResult::setReferenceShapeIndex(std::size_t idx)
{
    refShapeIdx = idx;
}

std::size_t Shape::AlignmentResult::getAlignedShapeIndex() const 
{
    return algdShapeIdx;
}

void Shape::AlignmentResult::setAlignedShapeIndex(std::size_t idx)
{
    algdShapeIdx = idx;
}

double Shape::AlignmentResult::getReferenceSelfOverlap() const 
{
    return refSelfOverlap;
}

void Shape::AlignmentResult::setReferenceSelfOverlap(double overlap)
{
    refSelfOverlap = overlap;
}

double Shape::AlignmentResult::getReferenceColorSelfOverlap() const 
{
    return refColSelfOverlap;
}

void Shape::AlignmentResult::setReferenceColorSelfOverlap(double overlap)
{
    refColSelfOverlap = overlap;
}

double Shape::AlignmentResult::getAlignedSelfOverlap() const 
{
    return algdSelfOverlap;
}

void Shape::AlignmentResult::setAlignedSelfOverlap(double overlap)
{
    algdSelfOverlap = overlap;
}

double Shape::AlignmentResult::getAlignedColorSelfOverlap() const 
{
    return algdColSelfOverlap;
}

void Shape::AlignmentResult::setAlignedColorSelfOverlap(double overlap)
{
    algdColSelfOverlap = overlap;
}

double Shape::AlignmentResult::getOverlap() const 
{
    return overlap;
}

void Shape::AlignmentResult::setOverlap(double overlap)
{
    this->overlap = overlap;
}

double Shape::AlignmentResult::getColorOverlap() const 
{
    return colOverlap;
}
                
void Shape::AlignmentResult::setColorOverlap(double overlap)
{
    colOverlap = overlap;
}

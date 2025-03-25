/* 
 * UtilityFunctions.hpp 
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

/**
 * \file
 * \brief Declaration of miscellaneous utility functions.
 */

#ifndef CDPL_SHAPE_UTILITYFUNCTIONS_HPP
#define CDPL_SHAPE_UTILITYFUNCTIONS_HPP

#include "CDPL/Shape/APIPrefix.hpp"
#include "CDPL/Shape/QuaternionTransformation.hpp"
#include "CDPL/Math/Vector.hpp"
#include "CDPL/Math/Matrix.hpp"


namespace CDPL
{

    namespace Shape
    {

        class GaussianShapeFunction;

        CDPL_SHAPE_API void calcQuadrupoleTensorEigenDecomposition(const Math::Matrix3D& quad_tensor, Math::Matrix3D& eigen_vecs,
                                                                   Math::Vector3D& eigen_vals);

        CDPL_SHAPE_API void calcPrincipalAxes(const Math::Matrix3D& quad_tensor, Math::Vector3D& x_axis, Math::Vector3D& y_axis,
                                              Math::Vector3D& z_axis, Math::Vector3D& moments);

        CDPL_SHAPE_API unsigned int perceiveSymmetryClass(const Math::Vector3D& moments, double eq_thresh = 0.15);

        CDPL_SHAPE_API unsigned int calcCenterAlignmentTransforms(const Shape::GaussianShapeFunction& func, Math::Matrix4D& to_ctr_xform,
                                                                  Math::Matrix4D& from_ctr_xform, double mom_eq_thresh = 0.15);

        CDPL_SHAPE_API void matrixToQuaternion(const Math::Matrix4D& mtx, QuaternionTransformation& quat);

        CDPL_SHAPE_API void quaternionToMatrix(const QuaternionTransformation& quat, Math::Matrix4D& mtx);
    } // namespace Shape
} // namespace CDPL

#endif // CDPL_SHAPE_UTILITYFUNCTIONS_HPP

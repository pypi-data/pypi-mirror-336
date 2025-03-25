#
# This file is part of the Chemical Data Processing Toolkit
#
# Copyright (C) Thomas Seidel <thomas.seidel@univie.ac.at>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; see the file COPYING. If not, write to
# the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
#

##
# \brief 
#
class FastGaussianShapeOverlapFunction(GaussianShapeOverlapFunction):

    ##
    # \brief 
    #
    DEF_RADIUS_SCALING_FACTOR = 1.4

    ##
    # \brief Initializes the \e %FastGaussianShapeOverlapFunction instance.
    # 
    def __init__() -> None: pass

    ##
    # \brief Initializes the \e %FastGaussianShapeOverlapFunction instance.
    # \param ref_shape_func 
    # \param ovl_shape_func 
    # 
    def __init__(ref_shape_func: GaussianShapeFunction, ovl_shape_func: GaussianShapeFunction) -> None: pass

    ##
    # \brief Initializes a copy of the \e %FastGaussianShapeOverlapFunction instance \a func.
    # \param func The \e %FastGaussianShapeOverlapFunction instance to copy.
    # 
    def __init__(func: FastGaussianShapeOverlapFunction) -> None: pass

    ##
    # \brief Replaces the current state of \a self with a copy of the state of the \c %FastGaussianShapeOverlapFunction instance \a func.
    # \param func The \c %FastGaussianShapeOverlapFunction instance to copy.
    # \return \a self
    # 
    def assign(func: FastGaussianShapeOverlapFunction) -> FastGaussianShapeOverlapFunction: pass

    ##
    # \brief 
    # \param enable 
    #
    def proximityOptimization(enable: bool) -> None: pass

    ##
    # \brief 
    # \return 
    #
    def proximityOptimization() -> bool: pass

    ##
    # \brief 
    # \param factor 
    #
    def setRadiusScalingFactor(factor: float) -> None: pass

    ##
    # \brief 
    # \return 
    #
    def getRadiusScalingFactor() -> float: pass

    ##
    # \brief 
    # \param enable 
    #
    def fastExpFunction(enable: bool) -> None: pass

    ##
    # \brief 
    # \return 
    #
    def fastExpFunction() -> bool: pass

    proximityOpt = property(proximityOptimization, proximityOptimization)

    radiusScalingFactor = property(getRadiusScalingFactor, setRadiusScalingFactor)

    fastExpFunc = property(fastExpFunction, fastExpFunction)

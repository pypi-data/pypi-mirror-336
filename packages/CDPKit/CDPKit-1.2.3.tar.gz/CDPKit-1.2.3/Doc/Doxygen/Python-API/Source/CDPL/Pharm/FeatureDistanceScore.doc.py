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
# \brief FeatureDistanceScore.
# 
class FeatureDistanceScore(FeatureInteractionScore):

    ##
    # \brief Initializes a copy of the \e %FeatureDistanceScore instance \a score.
    # \param score The \e %FeatureDistanceScore instance to copy.
    # 
    def __init__(score: FeatureDistanceScore) -> None: pass

    ##
    # \brief Constructs a <tt>FeatureDistanceScore</tt> functor with a minimum feature distance of <em>min_dist</em> and maximum distance of <em>max_dist</em>.
    # 
    # \param min_dist The minimum feature pair distance.
    # \param max_dist The maximum feature pair distance.
    # 
    def __init__(min_dist: float, max_dist: float) -> None: pass

    ##
    # \brief 
    # \param func 
    #
    def setDistanceScoringFunction(func: DoubleDoubleFunctor) -> None: pass

    ##
    # \brief 
    # \return 
    #
    def getMinDistance() -> float: pass

    ##
    # \brief 
    # \return 
    #
    def getMaxDistance() -> float: pass

    ##
    # \brief Replaces the current state of \a self with a copy of the state of the \c %FeatureDistanceScore instance \a func.
    # \param func The \c %FeatureDistanceScore instance to copy.
    # \return \a self
    # 
    def assign(func: FeatureDistanceScore) -> FeatureDistanceScore: pass

    minDistance = property(getMinDistance)

    maxDistance = property(getMaxDistance)

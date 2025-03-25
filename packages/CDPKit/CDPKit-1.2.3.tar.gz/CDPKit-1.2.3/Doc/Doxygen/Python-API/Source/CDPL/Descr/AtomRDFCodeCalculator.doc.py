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
# \brief AtomRDFCodeCalculator.
# 
# \see [\ref CITB, \ref HBMD]
# 
class AtomRDFCodeCalculator(Boost.Python.instance):

    ##
    # \brief Constructs the <tt>AtomRDFCodeCalculator</tt> instance.
    # 
    def __init__() -> None: pass

    ##
    # \brief Initializes a copy of the \e %AtomRDFCodeCalculator instance \a calc.
    # \param calc The \e %AtomRDFCodeCalculator instance to copy.
    # 
    def __init__(calc: AtomRDFCodeCalculator) -> None: pass

    ##
    # \brief Initializes the \e %AtomRDFCodeCalculator instance.
    # \param cntnr 
    # \param rdf_code 
    # 
    def __init__(cntnr: Chem.AtomContainer, rdf_code: Math.DVector) -> None: pass

    ##
    # \brief Returns the numeric identifier (ID) of the wrapped C++ class instance.
    # 
    # Different Python \c %AtomRDFCodeCalculator instances may reference the same underlying C++ class instance. The commonly used Python expression
    # <tt>a is not b</tt> thus cannot tell reliably whether the two \c %AtomRDFCodeCalculator instances \e a and \e b reference different C++ objects. 
    # The numeric identifier returned by this method allows to correctly implement such an identity test via the simple expression
    # <tt>a.getObjectID() != b.getObjectID()</tt>.
    # 
    # \return The numeric ID of the internally referenced C++ class instance.
    # 
    def getObjectID() -> int: pass

    ##
    # \brief Replaces the current state of \a self with a copy of the state of the \c %AtomRDFCodeCalculator instance \a calc.
    # \param calc The \c %AtomRDFCodeCalculator instance to copy.
    # \return \a self
    # 
    def assign(calc: AtomRDFCodeCalculator) -> AtomRDFCodeCalculator: pass

    ##
    # \brief 
    # \param func 
    #
    def setEntityPairWeightFunction(func: Chem.DoubleAtom2Functor) -> None: pass

    ##
    # \brief 
    # \param func 
    #
    def setEntity3DCoordinatesFunction(func: Chem.Atom3DCoordinatesFunction) -> None: pass

    ##
    # \brief 
    # \param num_steps 
    #
    def setNumSteps(num_steps: int) -> None: pass

    ##
    # \brief 
    # \return 
    #
    def getNumSteps() -> int: pass

    ##
    # \brief 
    # \param radius_inc 
    #
    def setRadiusIncrement(radius_inc: float) -> None: pass

    ##
    # \brief 
    # \return 
    #
    def getRadiusIncrement() -> float: pass

    ##
    # \brief 
    # \param start_radius 
    #
    def setStartRadius(start_radius: float) -> None: pass

    ##
    # \brief 
    # \return 
    #
    def getStartRadius() -> float: pass

    ##
    # \brief 
    # \param factor 
    #
    def setSmoothingFactor(factor: float) -> None: pass

    ##
    # \brief 
    # \return 
    #
    def getSmoothingFactor() -> float: pass

    ##
    # \brief 
    # \param factor 
    #
    def setScalingFactor(factor: float) -> None: pass

    ##
    # \brief 
    # \return 
    #
    def getScalingFactor() -> float: pass

    ##
    # \brief 
    # \param enable 
    #
    def enableDistanceToIntervalCenterRounding(enable: bool) -> None: pass

    ##
    # \brief 
    # \return 
    #
    def distanceToIntervalsCenterRoundingEnabled() -> bool: pass

    ##
    # \brief 
    # \param cntnr 
    # \param rdf_code 
    #
    def calculate(cntnr: Chem.AtomContainer, rdf_code: Math.DVector) -> None: pass

    objectID = property(getObjectID)

    distanceToIntervalCenterRounding = property(distanceToIntervalsCenterRoundingEnabled, enableDistanceToIntervalCenterRounding)

    smoothingFactor = property(getSmoothingFactor, setSmoothingFactor)

    scalingFactor = property(getScalingFactor, setScalingFactor)

    startRadius = property(getStartRadius, setStartRadius)

    radiusIncrement = property(getRadiusIncrement, setRadiusIncrement)

    numSteps = property(getNumSteps, setNumSteps)

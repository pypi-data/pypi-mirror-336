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
# \brief MoleculeRDFDescriptorCalculator.
# 
# \see [\ref CITB, \ref HBMD]
# 
class MoleculeRDFDescriptorCalculator(Boost.Python.instance):

    ##
    # \brief Constructs the <tt>MoleculeRDFDescriptorCalculator</tt> instance.
    # 
    def __init__() -> None: pass

    ##
    # \brief Initializes a copy of the \e %MoleculeRDFDescriptorCalculator instance \a calc.
    # \param calc The \e %MoleculeRDFDescriptorCalculator instance to copy.
    # 
    def __init__(calc: MoleculeRDFDescriptorCalculator) -> None: pass

    ##
    # \brief Initializes the \e %MoleculeRDFDescriptorCalculator instance.
    # \param cntnr 
    # \param descr 
    # 
    def __init__(cntnr: Chem.AtomContainer, descr: Math.DVector) -> None: pass

    ##
    # \brief Returns the numeric identifier (ID) of the wrapped C++ class instance.
    # 
    # Different Python \c %MoleculeRDFDescriptorCalculator instances may reference the same underlying C++ class instance. The commonly used Python expression
    # <tt>a is not b</tt> thus cannot tell reliably whether the two \c %MoleculeRDFDescriptorCalculator instances \e a and \e b reference different C++ objects. 
    # The numeric identifier returned by this method allows to correctly implement such an identity test via the simple expression
    # <tt>a.getObjectID() != b.getObjectID()</tt>.
    # 
    # \return The numeric ID of the internally referenced C++ class instance.
    # 
    def getObjectID() -> int: pass

    ##
    # \brief Replaces the current state of \a self with a copy of the state of the \c %MoleculeRDFDescriptorCalculator instance \a calc.
    # \param calc The \c %MoleculeRDFDescriptorCalculator instance to copy.
    # \return \a self
    # 
    def assign(calc: MoleculeRDFDescriptorCalculator) -> MoleculeRDFDescriptorCalculator: pass

    ##
    # \brief Allows to specify the atom coordinates function.
    # 
    # \param func A Atom3DCoordinatesFunction instance that wraps the target function.
    # 
    # \note The coordinates function must be specified before calling calculate(), otherwise a zero distance for each atom pair will be used for the calculation.
    # 
    def setAtom3DCoordinatesFunction(func: Chem.Atom3DCoordinatesFunction) -> None: pass

    ##
    # \brief Allows to specify a custom atom pair weight function.
    # 
    # \param func A AtomPairWeightFunction instance that wraps the target function.
    # 
    def setAtomPairWeightFunction(func: Chem.DoubleAtom2UIntFunctor) -> None: pass

    ##
    # \brief Sets the number of desired radius incrementation steps.
    # 
    # The number of performed radius incrementation steps defines the size of the calculated <em>RDF</em> code vector which is equal to the number of steps plus <em>1</em>.
    # 
    # \param num_steps The number of radius incrementation steps.
    # 
    # \note The default number of steps is <em>99</em>.
    # 
    def setNumSteps(num_steps: int) -> None: pass

    ##
    # \brief Returns the number of performed radius incrementation steps.
    # 
    # \return The number of performed radius incrementation steps.
    # 
    def getNumSteps() -> int: pass

    ##
    # \brief Sets the radius step size between successive <em>RDF</em> code elements.
    # 
    # \param radius_inc The radius step size.
    # 
    # \note The default radius step size is <em>0.1</em>&Aring;.
    # 
    def setRadiusIncrement(radius_inc: float) -> None: pass

    ##
    # \brief Returns the radius step size between successive <em>RDF</em> code elements.
    # 
    # \return The applied radius step size.
    # 
    def getRadiusIncrement() -> float: pass

    ##
    # \brief Sets the starting value of the radius.
    # 
    # \param start_radius The starting value of the radius.
    # 
    # \note The default starting radius is <em>0.0</em>&Aring;.
    # 
    def setStartRadius(start_radius: float) -> None: pass

    ##
    # \brief Returns the starting value of the radius.
    # 
    # \return The current radius starting value.
    # 
    def getStartRadius() -> float: pass

    ##
    # \brief Allows to specify the smoothing factor used in the calculation of atom pair <em>RDF</em> contributions.
    # 
    # \param factor The smoothing factor.
    # 
    # \note The default value of the smoothing factor is <em>1.0</em>.
    # 
    def setSmoothingFactor(factor: float) -> None: pass

    ##
    # \brief Returns the smoothing factor used in the calculation of atom pair <em>RDF</em> contributions.
    # 
    # \return The applied smoothing factor.
    # 
    def getSmoothingFactor() -> float: pass

    ##
    # \brief Allows to specify the scaling factor for the <em>RDF</em> code elements.
    # 
    # \param factor The scaling factor.
    # 
    # \note The default scaling factor is <em>1.0</em>.
    # 
    def setScalingFactor(factor: float) -> None: pass

    ##
    # \brief Returns the scaling factor applied to the <em>RDF</em> code elements.
    # 
    # \return The applied scaling factor.
    # 
    def getScalingFactor() -> float: pass

    ##
    # \brief Allows to specify whether atom pair distances should be rounded to the nearest radius interval center.
    # 
    # \param enable <tt>True</tt> if pair distances should be rounded, and <tt>False</tt> otherwise.
    # 
    # \note The default setting is not to round the atom pair distances.
    # 
    def enableDistanceToIntervalCenterRounding(enable: bool) -> None: pass

    ##
    # \brief Tells whether atom pair distances get rounded to the nearest radius interval centers.
    # 
    # \return <tt>True</tt> if pair distances get rounded, and <tt>False</tt> otherwise.
    # 
    def distanceToIntervalsCenterRoundingEnabled() -> bool: pass

    ##
    # \brief 
    # \param cntnr 
    # \param descr 
    #
    def calculate(cntnr: Chem.AtomContainer, descr: Math.DVector) -> None: pass

    objectID = property(getObjectID)

    distanceToIntervalCenterRounding = property(distanceToIntervalsCenterRoundingEnabled, enableDistanceToIntervalCenterRounding)

    smoothingFactor = property(getSmoothingFactor, setSmoothingFactor)

    scalingFactor = property(getScalingFactor, setScalingFactor)

    startRadius = property(getStartRadius, setStartRadius)

    radiusIncrement = property(getRadiusIncrement, setRadiusIncrement)

    numSteps = property(getNumSteps, setNumSteps)

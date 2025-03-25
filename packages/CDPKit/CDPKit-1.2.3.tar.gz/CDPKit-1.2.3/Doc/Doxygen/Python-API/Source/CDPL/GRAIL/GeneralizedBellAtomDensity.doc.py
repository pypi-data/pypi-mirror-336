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
# \brief GeneralizedBellAtomDensity.
# 
class GeneralizedBellAtomDensity(Boost.Python.instance):

    ##
    # \brief 
    #
    DEF_RADIUS_SCALING_FACTOR = 1.0

    ##
    # \brief 
    #
    DEF_PROBE_RADIUS = 0.0

    ##
    # \brief Initializes a copy of the \e %GeneralizedBellAtomDensity instance \a func.
    # \param func The \e %GeneralizedBellAtomDensity instance to copy.
    # 
    def __init__(func: GeneralizedBellAtomDensity) -> None: pass

    ##
    # \brief Initializes the \e %GeneralizedBellAtomDensity instance.
    # \param probe_radius 
    # \param rad_scaling_factor 
    # 
    def __init__(probe_radius: float = 0.0, rad_scaling_factor: float = 1.0) -> None: pass

    ##
    # \brief Returns the numeric identifier (ID) of the wrapped C++ class instance.
    # 
    # Different Python \c %GeneralizedBellAtomDensity instances may reference the same underlying C++ class instance. The commonly used Python expression
    # <tt>a is not b</tt> thus cannot tell reliably whether the two \c %GeneralizedBellAtomDensity instances \e a and \e b reference different C++ objects. 
    # The numeric identifier returned by this method allows to correctly implement such an identity test via the simple expression
    # <tt>a.getObjectID() != b.getObjectID()</tt>.
    # 
    # \return The numeric ID of the internally referenced C++ class instance.
    # 
    def getObjectID() -> int: pass

    ##
    # \brief 
    # \return 
    #
    def getProbeRadius() -> float: pass

    ##
    # \brief 
    # \return 
    #
    def getRadiusScalingFactor() -> float: pass

    ##
    # \brief Replaces the current state of \a self with a copy of the state of the \c %GeneralizedBellAtomDensity instance \a func.
    # \param func The \c %GeneralizedBellAtomDensity instance to copy.
    # \return \a self
    # 
    def assign(func: GeneralizedBellAtomDensity) -> GeneralizedBellAtomDensity: pass

    ##
    # \brief 
    # \param pos 
    # \param atom_pos 
    # \param atom 
    # \return 
    #
    def __call__(pos: Math.Vector3D, atom_pos: Math.Vector3D, atom: Chem.Atom) -> float: pass

    objectID = property(getObjectID)

    probeRadius = property(getProbeRadius)

    radiusScalingFactor = property(getRadiusScalingFactor)

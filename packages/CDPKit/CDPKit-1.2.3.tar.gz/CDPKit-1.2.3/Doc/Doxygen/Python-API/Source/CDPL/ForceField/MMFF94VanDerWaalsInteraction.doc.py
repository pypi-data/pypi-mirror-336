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
class MMFF94VanDerWaalsInteraction(Boost.Python.instance):

    ##
    # \brief 
    #
    class HDonorAcceptorType(Boost.Python.enum):

        ##
        # \brief NONE.
        #
        NONE = 0

        ##
        # \brief DONOR.
        #
        DONOR = 1

        ##
        # \brief ACCEPTOR.
        #
        ACCEPTOR = 2

    ##
    # \brief Initializes a copy of the \e %MMFF94VanDerWaalsInteraction instance \a iactn.
    # \param iactn The \e %MMFF94VanDerWaalsInteraction instance to copy.
    # 
    def __init__(iactn: MMFF94VanDerWaalsInteraction) -> None: pass

    ##
    # \brief Initializes the \e %MMFF94VanDerWaalsInteraction instance.
    # \param atom1_idx 
    # \param atom2_idx 
    # \param atom_params1 
    # \param atom_params2 
    # \param expo 
    # \param fact_b 
    # \param beta 
    # \param fact_darad 
    # \param fact_daeps 
    # 
    def __init__(atom1_idx: int, atom2_idx: int, atom_params1: MMFF94VanDerWaalsAtomParameters, atom_params2: MMFF94VanDerWaalsAtomParameters, expo: float, fact_b: float, beta: float, fact_darad: float, fact_daeps: float) -> None: pass

    ##
    # \brief 
    # \return 
    #
    def getAtom1Index() -> int: pass

    ##
    # \brief 
    # \return 
    #
    def getAtom2Index() -> int: pass

    ##
    # \brief 
    # \return 
    #
    def getEIJ() -> float: pass

    ##
    # \brief 
    # \return 
    #
    def getRIJ() -> float: pass

    ##
    # \brief 
    # \return 
    #
    def getRIJPow7() -> float: pass

    ##
    # \brief Replaces the current state of \a self with a copy of the state of the \c %MMFF94VanDerWaalsInteraction instance \a iactn.
    # \param iactn The \c %MMFF94VanDerWaalsInteraction instance to copy.
    # \return \a self
    # 
    def assign(iactn: MMFF94VanDerWaalsInteraction) -> MMFF94VanDerWaalsInteraction: pass

    ##
    # \brief Returns the numeric identifier (ID) of the wrapped C++ class instance.
    # 
    # Different Python \c %MMFF94VanDerWaalsInteraction instances may reference the same underlying C++ class instance. The commonly used Python expression
    # <tt>a is not b</tt> thus cannot tell reliably whether the two \c %MMFF94VanDerWaalsInteraction instances \e a and \e b reference different C++ objects. 
    # The numeric identifier returned by this method allows to correctly implement such an identity test via the simple expression
    # <tt>a.getObjectID() != b.getObjectID()</tt>.
    # 
    # \return The numeric ID of the internally referenced C++ class instance.
    # 
    def getObjectID() -> int: pass

    objectID = property(getObjectID)

    atom1Index = property(getAtom1Index)

    atom2Index = property(getAtom2Index)

    eIJ = property(getEIJ)

    rIJ = property(getRIJ)

    rIJPow7 = property(getRIJPow7)

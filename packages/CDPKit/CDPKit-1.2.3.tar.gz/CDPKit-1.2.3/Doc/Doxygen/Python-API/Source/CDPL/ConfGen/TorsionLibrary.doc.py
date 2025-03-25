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
class TorsionLibrary(TorsionCategory):

    ##
    # \brief Initializes the \e %TorsionLibrary instance.
    # 
    def __init__() -> None: pass

    ##
    # \brief Initializes a copy of the \e %TorsionLibrary instance \a lib.
    # \param lib The \e %TorsionLibrary instance to copy.
    # 
    def __init__(lib: TorsionLibrary) -> None: pass

    ##
    # \brief 
    # \param is 
    #
    def load(is: Base.IStream) -> None: pass

    ##
    # \brief 
    #
    def loadDefaults() -> None: pass

    ##
    # \brief 
    # \param os 
    #
    def save(os: Base.OStream) -> None: pass

    ##
    # \brief Replaces the current state of \a self with a copy of the state of the \c %TorsionLibrary instance \a lib.
    # \param lib The \c %TorsionLibrary instance to copy.
    # \return \a self
    # 
    def assign(lib: TorsionLibrary) -> TorsionLibrary: pass

    ##
    # \brief 
    # \param map 
    #
    @staticmethod
    def set(map: TorsionLibrary) -> None: pass

    ##
    # \brief 
    # \param  
    # \return 
    #
    @staticmethod
    def get(: ) -> TorsionLibrary: pass

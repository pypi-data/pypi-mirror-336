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
# \param e 
# \param s 
# \return 
#
def slice(e: FVectorExpression, s: Slice) -> FVectorSlice: pass

##
# \brief 
# \param e 
# \param start 
# \param stride 
# \param size 
# \return 
#
def slice(e: FVectorExpression, start: int, stride: int, size: int) -> FVectorSlice: pass

##
# \brief 
# \param e 
# \param r 
# \return 
#
def range(e: FVectorExpression, r: Range) -> FVectorRange: pass

##
# \brief 
# \param e 
# \param start 
# \param stop 
# \return 
#
def range(e: FVectorExpression, start: int, stop: int) -> FVectorRange: pass

##
# \brief 
# \param e 
# \return 
#
def homog(e: FVectorExpression) -> FHomogenousCoordsAdapter: pass

##
# \brief 
# \param e 
# \return 
#
def quat(e: FVectorExpression) -> FVectorQuaternionAdapter: pass

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
class DKabschAlgorithm(Boost.Python.instance):

    ##
    # \brief Initializes the \e %DKabschAlgorithm instance.
    # 
    def __init__() -> None: pass

    ##
    # \brief Initializes a copy of the \e %DKabschAlgorithm instance \a algo.
    # \param algo The \e %DKabschAlgorithm instance to copy.
    # 
    def __init__(algo: DKabschAlgorithm) -> None: pass

    ##
    # \brief Returns the numeric identifier (ID) of the wrapped C++ class instance.
    # 
    # Different Python \c %DKabschAlgorithm instances may reference the same underlying C++ class instance. The commonly used Python expression
    # <tt>a is not b</tt> thus cannot tell reliably whether the two \c %DKabschAlgorithm instances \e a and \e b reference different C++ objects. 
    # The numeric identifier returned by this method allows to correctly implement such an identity test via the simple expression
    # <tt>a.getObjectID() != b.getObjectID()</tt>.
    # 
    # \return The numeric ID of the internally referenced C++ class instance.
    # 
    def getObjectID() -> int: pass

    ##
    # \brief Replaces the current state of \a self with a copy of the state of the \c %DKabschAlgorithm instance \a algo.
    # \param algo The \c %DKabschAlgorithm instance to copy.
    # \return \a self
    # 
    def assign(algo: DKabschAlgorithm) -> DKabschAlgorithm: pass

    ##
    # \brief 
    # \return 
    #
    def getTransform() -> DMatrix: pass

    ##
    # \brief 
    # \param points 
    # \param ref_points 
    # \param do_center 
    # \param max_svd_iter 
    # \return 
    #
    def align(points: ConstFMatrixExpression, ref_points: ConstFMatrixExpression, do_center: bool = True, max_svd_iter: int = 0) -> bool: pass

    ##
    # \brief 
    # \param points 
    # \param ref_points 
    # \param do_center 
    # \param max_svd_iter 
    # \return 
    #
    def align(points: ConstDMatrixExpression, ref_points: ConstDMatrixExpression, do_center: bool = True, max_svd_iter: int = 0) -> bool: pass

    ##
    # \brief 
    # \param points 
    # \param ref_points 
    # \param weights 
    # \param do_center 
    # \param max_svd_iter 
    # \return 
    #
    def align(points: ConstFMatrixExpression, ref_points: ConstFMatrixExpression, weights: ConstFVectorExpression, do_center: bool = True, max_svd_iter: int = 0) -> bool: pass

    ##
    # \brief 
    # \param points 
    # \param ref_points 
    # \param weights 
    # \param do_center 
    # \param max_svd_iter 
    # \return 
    #
    def align(points: ConstDMatrixExpression, ref_points: ConstDMatrixExpression, weights: ConstDVectorExpression, do_center: bool = True, max_svd_iter: int = 0) -> bool: pass

    objectID = property(getObjectID)

    transform = property(getTransform)

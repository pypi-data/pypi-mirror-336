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
class DMatrixRow(Boost.Python.instance):

    ##
    # \brief Initializes a copy of the \e %DMatrixRow instance \a mr.
    # \param mr The \e %DMatrixRow instance to copy.
    # 
    def __init__(mr: DMatrixRow) -> None: pass

    ##
    # \brief Initializes the \e %DMatrixRow instance.
    # \param e 
    # \param i 
    # 
    def __init__(e: DMatrixExpression, i: int) -> None: pass

    ##
    # \brief 
    # \return 
    #
    def getIndex() -> int: pass

    ##
    # \brief Returns the numeric identifier (ID) of the wrapped C++ class instance.
    # 
    # Different Python \c %DMatrixRow instances may reference the same underlying C++ class instance. The commonly used Python expression
    # <tt>a is not b</tt> thus cannot tell reliably whether the two \c %DMatrixRow instances \e a and \e b reference different C++ objects. 
    # The numeric identifier returned by this method allows to correctly implement such an identity test via the simple expression
    # <tt>a.getObjectID() != b.getObjectID()</tt>.
    # 
    # \return The numeric ID of the internally referenced C++ class instance.
    # 
    def getObjectID() -> int: pass

    ##
    # \brief Replaces the current state of \a self with a copy of the state of the \c %ConstFVectorExpression instance \a e.
    # \param e The \c %ConstFVectorExpression instance to copy.
    # \return \a self
    # 
    def assign(e: ConstFVectorExpression) -> DMatrixRow: pass

    ##
    # \brief Replaces the current state of \a self with a copy of the state of the \c %ConstDVectorExpression instance \a e.
    # \param e The \c %ConstDVectorExpression instance to copy.
    # \return \a self
    # 
    def assign(e: ConstDVectorExpression) -> DMatrixRow: pass

    ##
    # \brief Replaces the current state of \a self with a copy of the state of the \c %ConstLVectorExpression instance \a e.
    # \param e The \c %ConstLVectorExpression instance to copy.
    # \return \a self
    # 
    def assign(e: ConstLVectorExpression) -> DMatrixRow: pass

    ##
    # \brief Replaces the current state of \a self with a copy of the state of the \c %ConstULVectorExpression instance \a e.
    # \param e The \c %ConstULVectorExpression instance to copy.
    # \return \a self
    # 
    def assign(e: ConstULVectorExpression) -> DMatrixRow: pass

    ##
    # \brief Replaces the current state of \a self with a copy of the state of the \c %DMatrixRow instance \a r.
    # \param r The \c %DMatrixRow instance to copy.
    # \return \a self
    # 
    def assign(r: DMatrixRow) -> DMatrixRow: pass

    ##
    # \brief Replaces the current state of \a self with a copy of the state of the \c %object instance \a a.
    # \param a The \c %object instance to copy.
    # \return \a self
    # 
    def assign(a: object) -> None: pass

    ##
    # \brief 
    # \return 
    #
    def isEmpty() -> bool: pass

    ##
    # \brief 
    # \return 
    #
    def getSize() -> int: pass

    ##
    # \brief 
    # \param i 
    # \return 
    #
    def getElement(i: int) -> float: pass

    ##
    # \brief 
    # \return 
    #
    def toArray() -> object: pass

    ##
    # \brief 
    # \param r 
    #
    def swap(r: DMatrixRow) -> None: pass

    ##
    # \brief 
    # \param i 
    # \param v 
    #
    def setElement(i: int, v: float) -> None: pass

    ##
    # \brief 
    # \return 
    #
    def getData() -> DMatrixExpression: pass

    ##
    # \brief Returns the result of the comparison operation <tt>self == r</tt>.
    # \param r The \c %DMatrixRow instance to be compared with.
    # \return The result of the comparison operation.
    # 
    def __eq__(r: DMatrixRow) -> bool: pass

    ##
    # \brief Returns the result of the comparison operation <tt>self == e</tt>.
    # \param e The \c %ConstDVectorExpression instance to be compared with.
    # \return The result of the comparison operation.
    # 
    def __eq__(e: ConstDVectorExpression) -> bool: pass

    ##
    # \brief Returns the result of the comparison operation <tt>self != r</tt>.
    # \param r The \c %DMatrixRow instance to be compared with.
    # \return The result of the comparison operation.
    # 
    def __ne__(r: DMatrixRow) -> bool: pass

    ##
    # \brief Returns the result of the comparison operation <tt>self != e</tt>.
    # \param e The \c %ConstDVectorExpression instance to be compared with.
    # \return The result of the comparison operation.
    # 
    def __ne__(e: ConstDVectorExpression) -> bool: pass

    ##
    # \brief 
    # \param i 
    # \return 
    #
    def __call__(i: int) -> float: pass

    ##
    # \brief 
    # \param i 
    # \return 
    #
    def __getitem__(i: int) -> float: pass

    ##
    # \brief 
    # \return 
    #
    def __len__() -> int: pass

    ##
    # \brief Returns a string representation of the \e %DMatrixRow instance.
    # \return The generated string representation.
    # 
    def __str__() -> str: pass

    ##
    # \brief 
    # \return 
    #
    def __pos__() -> DMatrixRow: pass

    ##
    # \brief 
    # \return 
    #
    def __neg__() -> ConstDVectorExpression: pass

    ##
    # \brief Returns the result of the addition operation <tt>self + e</tt>.
    # \param e Specifies the second addend.
    # \return A \c %ConstDVectorExpression instance holding the result of the addition.
    # 
    def __add__(e: ConstDVectorExpression) -> ConstDVectorExpression: pass

    ##
    # \brief Returns the result of the subtraction operation <tt>self - e</tt>.
    # \param e Specifies the subtrahend.
    # \return A \c %DMatrixRow instance holding the result of the subtraction.
    # 
    def __sub__(e: ConstDVectorExpression) -> ConstDVectorExpression: pass

    ##
    # \brief Returns the result of the multiplication operation <tt>self * t</tt>.
    # \param t Specifies the multiplier.
    # \return A \c %ConstDVectorExpression instance holding the result of the multiplication.
    # 
    def __mul__(t: float) -> ConstDVectorExpression: pass

    ##
    # \brief Returns the result of the multiplication operation <tt>self * e</tt>.
    # \param e Specifies the multiplier.
    # \return A \c %ConstDVectorExpression instance holding the result of the multiplication.
    # 
    def __mul__(e: ConstDMatrixExpression) -> ConstDVectorExpression: pass

    ##
    # \brief Returns the result of the division operation <tt>self / t</tt>.
    # \param t Specifies the divisor.
    # \return A \c %ConstDVectorExpression instance holding the result of the division.
    # 
    def __div__(t: float) -> ConstDVectorExpression: pass

    ##
    # \brief 
    # \param t 
    # \return 
    #
    def __truediv__(t: float) -> ConstDVectorExpression: pass

    ##
    # \brief 
    # \param t 
    # \return 
    #
    def __rmul__(t: float) -> ConstDVectorExpression: pass

    ##
    # \brief 
    # \param i 
    # \param v 
    #
    def __setitem__(i: int, v: float) -> None: pass

    ##
    # \brief Performs the in-place addition operation <tt>self += r</tt>.
    # \param r Specifies the second addend.
    # \return The updated \c %DMatrixRow instance \a self.
    # 
    def __iadd__(r: DMatrixRow) -> DMatrixRow: pass

    ##
    # \brief Performs the in-place addition operation <tt>self += e</tt>.
    # \param e Specifies the second addend.
    # \return The updated \c %DMatrixRow instance \a self.
    # 
    def __iadd__(e: ConstDVectorExpression) -> DMatrixRow: pass

    ##
    # \brief Performs the in-place subtraction operation <tt>self -= r</tt>.
    # \param r Specifies the subtrahend.
    # \return The updated \c %DMatrixRow instance \a self.
    # 
    def __isub__(r: DMatrixRow) -> DMatrixRow: pass

    ##
    # \brief Performs the in-place subtraction operation <tt>self -= e</tt>.
    # \param e Specifies the subtrahend.
    # \return The updated \c %DMatrixRow instance \a self.
    # 
    def __isub__(e: ConstDVectorExpression) -> DMatrixRow: pass

    ##
    # \brief Performs the in-place multiplication operation <tt>self *= t</tt>.
    # \param t Specifies the multiplier.
    # \return The updated \c %DMatrixRow instance \a self.
    # 
    def __imul__(t: float) -> DMatrixRow: pass

    ##
    # \brief Performs the in-place division operation <tt>self /= t</tt>.
    # \param t Specifies the divisor.
    # \return The updated \c %DMatrixRow instance \a self.
    # 
    def __idiv__(t: float) -> DMatrixRow: pass

    ##
    # \brief 
    # \param t 
    # \return 
    #
    def __itruediv__(t: float) -> DMatrixRow: pass

    objectID = property(getObjectID)

    size = property(getSize)

    data = property(getData)

    index = property(getIndex)

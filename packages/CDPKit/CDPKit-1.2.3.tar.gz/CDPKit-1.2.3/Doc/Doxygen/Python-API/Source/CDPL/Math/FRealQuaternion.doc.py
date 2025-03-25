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
class FRealQuaternion(Boost.Python.instance):

    ##
    # \brief Initializes the \e %FRealQuaternion instance.
    # 
    def __init__() -> None: pass

    ##
    # \brief Initializes a copy of the \e %FRealQuaternion instance \a q.
    # \param q The \e %FRealQuaternion instance to copy.
    # 
    def __init__(q: FRealQuaternion) -> None: pass

    ##
    # \brief Initializes the \e %FRealQuaternion instance.
    # \param r 
    # 
    def __init__(r: float) -> None: pass

    ##
    # \brief 
    # \param r 
    # \return 
    #
    def set(r: float = 0.0) -> FRealQuaternion: pass

    ##
    # \brief Returns the numeric identifier (ID) of the wrapped C++ class instance.
    # 
    # Different Python \c %FRealQuaternion instances may reference the same underlying C++ class instance. The commonly used Python expression
    # <tt>a is not b</tt> thus cannot tell reliably whether the two \c %FRealQuaternion instances \e a and \e b reference different C++ objects. 
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
    def getC1() -> float: pass

    ##
    # \brief 
    # \return 
    #
    def getC2() -> float: pass

    ##
    # \brief 
    # \return 
    #
    def getC3() -> float: pass

    ##
    # \brief 
    # \return 
    #
    def getC4() -> float: pass

    ##
    # \brief 
    # \return 
    #
    def toArray() -> object: pass

    ##
    # \brief Replaces the current state of \a self with a copy of the state of the \c %FRealQuaternion instance \a q.
    # \param q The \c %FRealQuaternion instance to copy.
    # \return \a self
    # 
    def assign(q: FRealQuaternion) -> FRealQuaternion: pass

    ##
    # \brief 
    # \param q 
    #
    def swap(q: FRealQuaternion) -> None: pass

    ##
    # \brief Performs the in-place addition operation <tt>self += t</tt>.
    # \param t Specifies the second addend.
    # \return The updated \c %FRealQuaternion instance \a self.
    # 
    def __iadd__(t: float) -> FRealQuaternion: pass

    ##
    # \brief Performs the in-place addition operation <tt>self += q</tt>.
    # \param q Specifies the second addend.
    # \return The updated \c %FRealQuaternion instance \a self.
    # 
    def __iadd__(q: object) -> FRealQuaternion: pass

    ##
    # \brief Performs the in-place subtraction operation <tt>self -= t</tt>.
    # \param t Specifies the subtrahend.
    # \return The updated \c %FRealQuaternion instance \a self.
    # 
    def __isub__(t: float) -> FRealQuaternion: pass

    ##
    # \brief Performs the in-place subtraction operation <tt>self -= q</tt>.
    # \param q Specifies the subtrahend.
    # \return The updated \c %FRealQuaternion instance \a self.
    # 
    def __isub__(q: object) -> FRealQuaternion: pass

    ##
    # \brief Performs the in-place multiplication operation <tt>self *= t</tt>.
    # \param t Specifies the multiplier.
    # \return The updated \c %FRealQuaternion instance \a self.
    # 
    def __imul__(t: float) -> FRealQuaternion: pass

    ##
    # \brief Performs the in-place multiplication operation <tt>self *= q</tt>.
    # \param q Specifies the multiplier.
    # \return The updated \c %FRealQuaternion instance \a self.
    # 
    def __imul__(q: object) -> FRealQuaternion: pass

    ##
    # \brief Performs the in-place division operation <tt>self /= t</tt>.
    # \param t Specifies the divisor.
    # \return The updated \c %FRealQuaternion instance \a self.
    # 
    def __idiv__(t: float) -> FRealQuaternion: pass

    ##
    # \brief Performs the in-place division operation <tt>self /= q</tt>.
    # \param q Specifies the divisor.
    # \return The updated \c %FRealQuaternion instance \a self.
    # 
    def __idiv__(q: object) -> FRealQuaternion: pass

    ##
    # \brief 
    # \param t 
    # \return 
    #
    def __itruediv__(t: float) -> FRealQuaternion: pass

    ##
    # \brief 
    # \param q 
    # \return 
    #
    def __itruediv__(q: object) -> FRealQuaternion: pass

    ##
    # \brief Returns the result of the comparison operation <tt>self == q</tt>.
    # \param q The \c %FRealQuaternion instance to be compared with.
    # \return The result of the comparison operation.
    # 
    def __eq__(q: FRealQuaternion) -> bool: pass

    ##
    # \brief Returns the result of the comparison operation <tt>self == q</tt>.
    # \param q The \c %ConstFQuaternionExpression instance to be compared with.
    # \return The result of the comparison operation.
    # 
    def __eq__(q: ConstFQuaternionExpression) -> bool: pass

    ##
    # \brief Returns the result of the comparison operation <tt>self != q</tt>.
    # \param q The \c %FRealQuaternion instance to be compared with.
    # \return The result of the comparison operation.
    # 
    def __ne__(q: FRealQuaternion) -> bool: pass

    ##
    # \brief Returns the result of the comparison operation <tt>self != q</tt>.
    # \param q The \c %ConstFQuaternionExpression instance to be compared with.
    # \return The result of the comparison operation.
    # 
    def __ne__(q: ConstFQuaternionExpression) -> bool: pass

    ##
    # \brief Returns a string representation of the \e %FRealQuaternion instance.
    # \return The generated string representation.
    # 
    def __str__() -> str: pass

    ##
    # \brief 
    # \return 
    #
    def __pos__() -> FRealQuaternion: pass

    ##
    # \brief 
    # \return 
    #
    def __neg__() -> ConstFQuaternionExpression: pass

    ##
    # \brief Returns the result of the addition operation <tt>self + t</tt>.
    # \param t Specifies the second addend.
    # \return A \c %ConstFQuaternionExpression instance holding the result of the addition.
    # 
    def __add__(t: float) -> ConstFQuaternionExpression: pass

    ##
    # \brief Returns the result of the addition operation <tt>self + e</tt>.
    # \param e Specifies the second addend.
    # \return A \c %ConstFQuaternionExpression instance holding the result of the addition.
    # 
    def __add__(e: ConstFQuaternionExpression) -> ConstFQuaternionExpression: pass

    ##
    # \brief 
    # \param t 
    # \return 
    #
    def __radd__(t: float) -> ConstFQuaternionExpression: pass

    ##
    # \brief Returns the result of the subtraction operation <tt>self - t</tt>.
    # \param t Specifies the subtrahend.
    # \return A \c %FRealQuaternion instance holding the result of the subtraction.
    # 
    def __sub__(t: float) -> ConstFQuaternionExpression: pass

    ##
    # \brief Returns the result of the subtraction operation <tt>self - e</tt>.
    # \param e Specifies the subtrahend.
    # \return A \c %FRealQuaternion instance holding the result of the subtraction.
    # 
    def __sub__(e: ConstFQuaternionExpression) -> ConstFQuaternionExpression: pass

    ##
    # \brief 
    # \param t 
    # \return 
    #
    def __rsub__(t: float) -> ConstFQuaternionExpression: pass

    ##
    # \brief Returns the result of the multiplication operation <tt>self * t</tt>.
    # \param t Specifies the multiplier.
    # \return A \c %ConstFQuaternionExpression instance holding the result of the multiplication.
    # 
    def __mul__(t: float) -> ConstFQuaternionExpression: pass

    ##
    # \brief Returns the result of the multiplication operation <tt>self * e</tt>.
    # \param e Specifies the multiplier.
    # \return A \c %ConstFQuaternionExpression instance holding the result of the multiplication.
    # 
    def __mul__(e: ConstFQuaternionExpression) -> ConstFQuaternionExpression: pass

    ##
    # \brief 
    # \param t 
    # \return 
    #
    def __rmul__(t: float) -> ConstFQuaternionExpression: pass

    ##
    # \brief Returns the result of the division operation <tt>self / t</tt>.
    # \param t Specifies the divisor.
    # \return A \c %ConstFQuaternionExpression instance holding the result of the division.
    # 
    def __div__(t: float) -> ConstFQuaternionExpression: pass

    ##
    # \brief Returns the result of the division operation <tt>self / e</tt>.
    # \param e Specifies the divisor.
    # \return A \c %ConstFQuaternionExpression instance holding the result of the division.
    # 
    def __div__(e: ConstFQuaternionExpression) -> ConstFQuaternionExpression: pass

    ##
    # \brief 
    # \param t 
    # \return 
    #
    def __truediv__(t: float) -> ConstFQuaternionExpression: pass

    ##
    # \brief 
    # \param t 
    # \return 
    #
    def __rdiv__(t: float) -> ConstFQuaternionExpression: pass

    objectID = property(getObjectID)

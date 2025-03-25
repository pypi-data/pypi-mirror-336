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
class TopologicalFeatureAlignment(Boost.Python.instance):

    ##
    # \brief Initializes the \e %TopologicalFeatureAlignment instance.
    # 
    def __init__() -> None: pass

    ##
    # \brief Initializes a copy of the \e %TopologicalFeatureAlignment instance \a alignment.
    # \param alignment The \e %TopologicalFeatureAlignment instance to copy.
    # 
    def __init__(alignment: TopologicalFeatureAlignment) -> None: pass

    ##
    # \brief Returns the numeric identifier (ID) of the wrapped C++ class instance.
    # 
    # Different Python \c %TopologicalFeatureAlignment instances may reference the same underlying C++ class instance. The commonly used Python expression
    # <tt>a is not b</tt> thus cannot tell reliably whether the two \c %TopologicalFeatureAlignment instances \e a and \e b reference different C++ objects. 
    # The numeric identifier returned by this method allows to correctly implement such an identity test via the simple expression
    # <tt>a.getObjectID() != b.getObjectID()</tt>.
    # 
    # \return The numeric ID of the internally referenced C++ class instance.
    # 
    def getObjectID() -> int: pass

    ##
    # \brief 
    # \param func 
    #
    def setEntityMatchFunction(func: BoolFeature2Functor) -> None: pass

    ##
    # \brief 
    # \return 
    #
    def getEntityMatchFunction() -> BoolFeature2Functor: pass

    ##
    # \brief 
    # \param func 
    #
    def setEntityPairMatchFunction(func: BoolFeature4Functor) -> None: pass

    ##
    # \brief 
    # \return 
    #
    def getEntityPairMatchFunction() -> BoolFeature4Functor: pass

    ##
    # \brief 
    # \param entity 
    # \param first_set 
    #
    def addEntity(entity: Feature, first_set: bool) -> None: pass

    ##
    # \brief 
    # \param first_set 
    #
    def clearEntities(first_set: bool) -> None: pass

    ##
    # \brief 
    # \param first_set 
    # \return 
    #
    def getNumEntities(first_set: bool) -> int: pass

    ##
    # \brief 
    # \param first_set 
    # \return 
    #
    def getEntities(first_set: bool) -> object: pass

    ##
    # \brief 
    # \param idx 
    # \param first_set 
    # \return 
    #
    def getEntity(idx: int, first_set: bool) -> Feature: pass

    ##
    # \brief 
    #
    def reset() -> None: pass

    ##
    # \brief 
    # \param mapping 
    # \return 
    #
    def nextAlignment(mapping: Util.STPairArray) -> bool: pass

    ##
    # \brief Replaces the current state of \a self with a copy of the state of the \c %TopologicalFeatureAlignment instance \a alignment.
    # \param alignment The \c %TopologicalFeatureAlignment instance to copy.
    # \return \a self
    # 
    def assign(alignment: TopologicalFeatureAlignment) -> TopologicalFeatureAlignment: pass

    objectID = property(getObjectID)

    entityMatchFunction = property(getEntityMatchFunction, setEntityMatchFunction)

    entityPairMatchFunction = property(getEntityPairMatchFunction, setEntityPairMatchFunction)

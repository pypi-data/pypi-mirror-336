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
# \brief FileScreeningHitCollector.
# 
class FileScreeningHitCollector(Boost.Python.instance):

    ##
    # \brief Initializes a copy of the \e %FileScreeningHitCollector instance \a collector.
    # \param collector The \e %FileScreeningHitCollector instance to copy.
    # 
    def __init__(collector: FileScreeningHitCollector) -> None: pass

    ##
    # \brief Initializes the \e %FileScreeningHitCollector instance.
    # \param writer 
    # 
    def __init__(writer: Chem.MolecularGraphWriterBase) -> None: pass

    ##
    # \brief Returns the numeric identifier (ID) of the wrapped C++ class instance.
    # 
    # Different Python \c %FileScreeningHitCollector instances may reference the same underlying C++ class instance. The commonly used Python expression
    # <tt>a is not b</tt> thus cannot tell reliably whether the two \c %FileScreeningHitCollector instances \e a and \e b reference different C++ objects. 
    # The numeric identifier returned by this method allows to correctly implement such an identity test via the simple expression
    # <tt>a.getObjectID() != b.getObjectID()</tt>.
    # 
    # \return The numeric ID of the internally referenced C++ class instance.
    # 
    def getObjectID() -> int: pass

    ##
    # \brief Replaces the current state of \a self with a copy of the state of the \c %FileScreeningHitCollector instance \a collector.
    # \param collector The \c %FileScreeningHitCollector instance to copy.
    # \return \a self
    # 
    def assign(collector: FileScreeningHitCollector) -> FileScreeningHitCollector: pass

    ##
    # \brief 
    # \param writer 
    #
    def setDataWriter(writer: Chem.MolecularGraphWriterBase) -> None: pass

    ##
    # \brief 
    # \return 
    #
    def getDataWriter() -> Chem.MolecularGraphWriterBase: pass

    ##
    # \brief 
    # \param align 
    #
    def alignHitMolecule(align: bool) -> None: pass

    ##
    # \brief 
    # \return 
    #
    def alignHitMolecule() -> bool: pass

    ##
    # \brief 
    # \param output 
    #
    def outputScoreProperty(output: bool) -> None: pass

    ##
    # \brief 
    # \return 
    #
    def outputScoreProperty() -> bool: pass

    ##
    # \brief 
    # \param output 
    #
    def outputDBNameProperty(output: bool) -> None: pass

    ##
    # \brief 
    # \return 
    #
    def outputDBNameProperty() -> bool: pass

    ##
    # \brief 
    # \param output 
    #
    def outputDBMoleculeIndexProperty(output: bool) -> None: pass

    ##
    # \brief 
    # \return 
    #
    def outputDBMoleculeIndexProperty() -> bool: pass

    ##
    # \brief 
    # \param output 
    #
    def outputMoleculeConfIndexProperty(output: bool) -> None: pass

    ##
    # \brief 
    # \return 
    #
    def outputMoleculeConfIndexProperty() -> bool: pass

    ##
    # \brief 
    # \param zero_based 
    #
    def outputZeroBasedIndices(zero_based: bool) -> None: pass

    ##
    # \brief 
    # \return 
    #
    def outputZeroBasedIndices() -> bool: pass

    ##
    # \brief 
    # \param hit 
    # \param score 
    # \return 
    #
    def __call__(hit: SearchHit, score: float) -> bool: pass

    objectID = property(getObjectID)

    dataWriter = property(getDataWriter, setDataWriter)

    alignHitMol = property(alignHitMolecule, alignHitMolecule)

    outputScoreProp = property(outputScoreProperty, outputScoreProperty)

    outputDBNameProp = property(outputDBNameProperty, outputDBNameProperty)

    outputDBMoleculeIndexProp = property(outputDBMoleculeIndexProperty, outputDBMoleculeIndexProperty)

    outputMoleculeConfIndexProp = property(outputMoleculeConfIndexProperty, outputMoleculeConfIndexProperty)

    outputZeroBasedInds = property(outputZeroBasedIndices, outputZeroBasedIndices)

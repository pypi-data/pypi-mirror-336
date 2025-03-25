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
# \brief A factory interface providing methods for the creation of Pharm.FeatureContainerWriterBase instances for data output in a particular storage format.
# 
class FeatureContainerOutputHandler(Boost.Python.instance):

    ##
    # \brief Initializes the \e %FeatureContainerOutputHandler instance.
    # 
    def __init__() -> None: pass

    ##
    # \brief Returns the numeric identifier (ID) of the wrapped C++ class instance.
    # 
    # Different Python \c %FeatureContainerOutputHandler instances may reference the same underlying C++ class instance. The commonly used Python expression
    # <tt>a is not b</tt> thus cannot tell reliably whether the two \c %FeatureContainerOutputHandler instances \e a and \e b reference different C++ objects. 
    # The numeric identifier returned by this method allows to correctly implement such an identity test via the simple expression
    # <tt>a.getObjectID() != b.getObjectID()</tt>.
    # 
    # \return The numeric ID of the internally referenced C++ class instance.
    # 
    def getObjectID() -> int: pass

    ##
    # \brief Returns a Base.DataFormat object that provides information about the handled output data format.
    # 
    # \return A Base.DataFormat object that provides information about the handled data format.
    # 
    def getDataFormat() -> Base.DataFormat: pass

    ##
    # \brief Creates a FeatureContainerWriterBase instance that will write the data to the I/O stream <em>ios</em>.
    # 
    # \param ios The I/O stream to write to.
    # 
    # \return The created FeatureContainerWriterBase instance.
    # 
    def createWriter(ios: Base.IOStream) -> FeatureContainerWriterBase: pass

    ##
    # \brief Creates a FeatureContainerWriterBase instance that will write the data to the file specified by <em>file_name</em>.
    # 
    # \param file_name The full path of the file to write to.
    # \param mode Flags specifying the file open-mode.
    # 
    # \return The created FeatureContainerWriterBase instance.
    # 
    def createWriter(file_name: str, mode: OpenMode = Base.IOStream.OpenMode(60)) -> FeatureContainerWriterBase: pass

    objectID = property(getObjectID)

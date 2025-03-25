/* 
 * Util.hpp 
 *
 * This file is part of the Chemical Data Processing Toolkit
 *
 * Copyright (C) 2003 Thomas Seidel <thomas.seidel@univie.ac.at>
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this library; see the file COPYING. If not, write to
 * the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 */

/**
 * \file
 * \brief A convenience header including everything that is defined in namespace CDPL::Util.
 */

#ifndef CDPL_UTIL_HPP
#define CDPL_UTIL_HPP

#include "CDPL/Util/Array.hpp"
#include "CDPL/Util/BitSet.hpp"
#include "CDPL/Util/BronKerboschAlgorithm.hpp"
#include "CDPL/Util/DGCoordinatesGenerator.hpp"
#include "CDPL/Util/Dereferencer.hpp"
#include "CDPL/Util/IndexedElementIterator.hpp"
#include "CDPL/Util/IndirectArray.hpp"
#include "CDPL/Util/Map.hpp"
#include "CDPL/Util/MultiMap.hpp"
#include "CDPL/Util/PropertyValue.hpp"
#include "CDPL/Util/PropertyValueProduct.hpp"
#include "CDPL/Util/StreamDataReader.hpp"
#include "CDPL/Util/CompoundDataReader.hpp"
#include "CDPL/Util/FileDataReader.hpp"
#include "CDPL/Util/FileDataWriter.hpp"
#include "CDPL/Util/MultiFormatDataReader.hpp"
#include "CDPL/Util/MultiFormatDataWriter.hpp"
#include "CDPL/Util/DefaultDataInputHandler.hpp"
#include "CDPL/Util/ObjectPool.hpp"
#include "CDPL/Util/ObjectStack.hpp"
#include "CDPL/Util/SequenceFunctions.hpp"
#include "CDPL/Util/FileRemover.hpp"
#include "CDPL/Util/FileFunctions.hpp"
#include "CDPL/Util/CompressionStreams.hpp"
#include "CDPL/Util/CompressedDataReader.hpp"
#include "CDPL/Util/CompressedDataWriter.hpp"

#endif // CDPL_UTIL_HPP

/* 
 * DataFormat.hpp 
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
 * \brief Provides the contents of namespace CDPL::Biomol::DataFormat.
 */

#ifndef CDPL_BIOMOL_DATAFORMAT_HPP
#define CDPL_BIOMOL_DATAFORMAT_HPP

#include "CDPL/Biomol/APIPrefix.hpp"


namespace CDPL
{

    namespace Base
    {

        class DataFormat;
    }

    namespace Biomol
    {

        /**
         * \brief Provides preinitialized Base::DataFormat objects for all supported biopolymer data formats.
         */
        namespace DataFormat
        {

            /**
             * \brief Provides meta-information about the <em>Brookhaven Protein Data Bank Format</em>
             *        [\ref PDB] format.
             */
            extern CDPL_BIOMOL_API const Base::DataFormat PDB;

            /**
             * \brief Provides meta-information about the gzip-compressed <em>Brookhaven Protein Data Bank Format</em>
             *        [\ref PDB] format.
             */
            extern CDPL_BIOMOL_API const Base::DataFormat PDB_GZ;

            /**
             * \brief Provides meta-information about the bzip2-compressed <em>Brookhaven Protein Data Bank Format</em>
             *        [\ref PDB] format.
             */
            extern CDPL_BIOMOL_API const Base::DataFormat PDB_BZ2;

            /**
             * \brief Provides meta-information about the <em>Macromolecular Crystallographic Information File Format</em>
             *        [\ref MMCIF] format.
             */
            extern CDPL_BIOMOL_API const Base::DataFormat MMCIF;

            /**
             * \brief Provides meta-information about the gzip-compressed <em>Macromolecular Crystallographic Information File Format</em>
             *        [\ref MMCIF] format.
             */
            extern CDPL_BIOMOL_API const Base::DataFormat MMCIF_GZ;

            /**
             * \brief Provides meta-information about the bzip2-compressed <em>Macromolecular Crystallographic Information File Format</em>
             *        [\ref MMCIF] format.
             */
            extern CDPL_BIOMOL_API const Base::DataFormat MMCIF_BZ2;

            /**
             * \brief Provides meta-information about the <em>Macromolecular Transmission Format</em>
             *        [\ref MMTF] format.
             * \since 1.2
             */
            extern CDPL_BIOMOL_API const Base::DataFormat MMTF;

            /**
             * \brief Provides meta-information about the gzip-compressed <em>Macromolecular Transmission Format</em>
             *        [\ref MMTF] format.
             * \since 1.2
             */
            extern CDPL_BIOMOL_API const Base::DataFormat MMTF_GZ;

            /**
             * \brief Provides meta-information about the bzip2-compressed <em>Macromolecular Transmission Format</em>
             *        [\ref MMTF] format.
             * \since 1.2
             */
            extern CDPL_BIOMOL_API const Base::DataFormat MMTF_BZ2;
        } // namespace DataFormat
    } // namespace Biomol
} // namespace CDPL

#endif // CDPL_BIOMOL_DATAFORMAT_HPP

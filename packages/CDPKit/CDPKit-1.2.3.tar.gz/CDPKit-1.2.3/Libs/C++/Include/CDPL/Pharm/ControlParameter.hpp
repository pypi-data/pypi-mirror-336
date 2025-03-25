/* 
 * ControlParameter.hpp 
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
 * \brief Definition of constants in namespace CDPL::Pharm::ControlParameter.
 */

#ifndef CDPL_PHARM_CONTROLPARAMETER_HPP
#define CDPL_PHARM_CONTROLPARAMETER_HPP

#include "CDPL/Pharm/APIPrefix.hpp"


namespace CDPL
{

    namespace Base
    {

        class LookupKey;
    }

    namespace Pharm
    {

        /**
         * \brief Provides keys for built-in control-parameters.
         */
        namespace ControlParameter
        {

            /**
             * \brief Specifies whether non-fatal recoverable I/O errors should be ignored or cause an I/O operation to fail.
             *
             * If the control-parameter is set to \c true, not only severe errors cause an I/O operation to fail, but also
             * non-fatal errors from which a recovery would be possible. 
             * If the control-parameter is set to \c false, I/O operations will proceed even if a non-fatal error has been
             * detected.
             *
             * \valuetype \c bool
             */
            extern CDPL_PHARM_API const Base::LookupKey STRICT_ERROR_CHECKING;

            /**
             * \since 1.2
             */
            extern CDPL_PHARM_API const Base::LookupKey CDF_OUTPUT_SINGLE_PRECISION_FLOATS;

            extern CDPL_PHARM_API const Base::LookupKey PSD_CREATION_MODE;

            extern CDPL_PHARM_API const Base::LookupKey PSD_ALLOW_DUPLICATES;
        } // namespace ControlParameter
    } // namespace Pharm
} // namespace CDPL

#endif // CDPL_PHARM_CONTROLPARAMETER_HPP

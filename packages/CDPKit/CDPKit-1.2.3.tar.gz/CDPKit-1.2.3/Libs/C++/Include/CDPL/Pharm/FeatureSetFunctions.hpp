/* 
 * FeatureSetFunctions.hpp 
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
 * \brief Declaration of functions that operate on Pharm::FeatureSet instances.
 */

#ifndef CDPL_PHARM_FEATURESETFUNCTIONS_HPP
#define CDPL_PHARM_FEATURESETFUNCTIONS_HPP

#include "CDPL/Pharm/APIPrefix.hpp"
#include "CDPL/Pharm/FeatureMapping.hpp"


namespace CDPL
{

    namespace Pharm
    {

        class FeatureSet;
        class FeatureMapping;

        CDPL_PHARM_API void getFeatures(FeatureSet& ftr_set, const FeatureMapping& mapping, bool first);

        /**
         * \since 1.2
         */
        CDPL_PHARM_API bool removePositionalDuplicates(FeatureSet& ftr_set, double pos_tol = 0.0);

        /**
         * \since 1.2
         */
        CDPL_PHARM_API bool removeFeaturesWithType(FeatureSet& ftr_set, unsigned int type);
        
    } // namespace Pharm
} // namespace CDPL

#endif // CDPL_PHARM_FEATURESETFUNCTIONS_HPP

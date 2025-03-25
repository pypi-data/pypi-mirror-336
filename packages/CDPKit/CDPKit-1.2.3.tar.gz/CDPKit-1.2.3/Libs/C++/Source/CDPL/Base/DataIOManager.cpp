/* 
 * DataIOManager.cpp 
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


#include "StaticInit.hpp"

#include "CDPL/Base/DataIOManager.hpp"

#ifdef _MSC_VER
# define _CDPL_BASE_API CDPL_BASE_API      
#else
# define _CDPL_BASE_API
#endif // _MSC_VER
 

using namespace CDPL;


template class _CDPL_BASE_API Base::DataIOManager<Chem::Molecule>;
        
template class _CDPL_BASE_API Base::DataIOManager<Chem::MolecularGraph>;
        
template class _CDPL_BASE_API Base::DataIOManager<Chem::Reaction>;

template class _CDPL_BASE_API Base::DataIOManager<Pharm::Pharmacophore>;

template class _CDPL_BASE_API Base::DataIOManager<Pharm::FeatureContainer>;

template class _CDPL_BASE_API Base::DataIOManager<Grid::RegularGrid<double, double> >;

template class _CDPL_BASE_API Base::DataIOManager<Grid::RegularGridSet<double, double> >;

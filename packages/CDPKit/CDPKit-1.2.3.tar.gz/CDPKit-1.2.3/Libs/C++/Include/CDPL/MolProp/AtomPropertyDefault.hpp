/* 
 * AtomPropertyDefault.hpp 
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
 * \brief Definition of constants in namespace CDPL::MolProp::AtomPropertyDefault.
 */

#ifndef CDPL_MOLPROP_ATOMPROPERTYDEFAULT_HPP
#define CDPL_MOLPROP_ATOMPROPERTYDEFAULT_HPP

#include "CDPL/MolProp/APIPrefix.hpp"


namespace CDPL
{

    namespace MolProp
    {

        /**
         * \brief Provides default values for built-in Chem::Atom properties.
         */
        namespace AtomPropertyDefault
        {

            extern CDPL_MOLPROP_API const unsigned int H_BOND_DONOR_TYPE;
            extern CDPL_MOLPROP_API const unsigned int H_BOND_ACCEPTOR_TYPE;
        } // namespace AtomPropertyDefault
    } // namespace MolProp
} // namespace CDPL

#endif // CDPL_MOLPROP_ATOMPROPERTYDEFAULT_HPP

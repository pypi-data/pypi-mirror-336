/* 
 * TopologicalAtomDistanceFunction.hpp 
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
 * \brief Type definition of generic wrapper class for storing an user-defined
 *        topological atom-pair distance function.
 */

#ifndef CDPL_FORCEFIELD_TOPOLOGICALATOMDISTANCEFUNCTION_HPP
#define CDPL_FORCEFIELD_TOPOLOGICALATOMDISTANCEFUNCTION_HPP

#include <cstddef>
#include <functional>


namespace CDPL
{

    namespace Chem
    {

        class Atom;
        class MolecularGraph;
    } // namespace Chem

    namespace ForceField
    {

        /**
         * \brief A generic wrapper class used to store a user-defined topological atom-pair distance function.
         */
        typedef std::function<std::size_t(const Chem::Atom&, const Chem::Atom&, const Chem::MolecularGraph&)> TopologicalAtomDistanceFunction;
    } // namespace ForceField
} // namespace CDPL

#endif // CDPL_FORCEFIELD_TOPOLOGICALATOMDISTANCEFUNCTION_HPP

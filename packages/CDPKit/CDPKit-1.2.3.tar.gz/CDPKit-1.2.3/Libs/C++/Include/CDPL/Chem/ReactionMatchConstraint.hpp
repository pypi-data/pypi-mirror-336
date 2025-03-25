/* 
 * ReactionMatchConstraint.hpp 
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
 * \brief Definition of constants in namespace CDPL::Chem::ReactionMatchConstraint.
 */

#ifndef CDPL_CHEM_REACTIONMATCHCONSTRAINT_HPP
#define CDPL_CHEM_REACTIONMATCHCONSTRAINT_HPP


namespace CDPL
{

    namespace Chem
    {

        /**
         * \brief Provides numerical identifiers for built-in Chem::Reaction matching constraints.
         */
        namespace ReactionMatchConstraint
        {

            /**
             * \brief Specifies a constraint which requires the target reaction to fulfill additional constraints
             *        specified by a Chem::MatchConstraintList object.
             */
            constexpr unsigned int CONSTRAINT_LIST = 0;

            /**
             * \brief Specifies a constraint which requires the target reaction to match the reactant to product
             *        atom mapping of the query reaction.
             */
            constexpr unsigned int ATOM_MAPPING = 1;

            /**
             * \brief Specifies a constraint which requires the target reaction to match any component level groupings
             *        defined by the query reaction.
             * 
             * Component level groupings specify whether the components of a query reaction have to be matched by a single
             * target reaction component (intramolecular reaction) or by different components of the target (intermolecular
             * reaction). 
             * <em>Daylight SMARTS</em> patterns [\ref SMARTS] allow to specify component groupings by parentheses that
             * enclose those components of the query which have to be part of the same target reaction component.
             */
            constexpr unsigned int COMPONENT_GROUPING = 2;
        } // namespace ReactionMatchConstraint
    } // namespace Chem
} // namespace CDPL

#endif // CDPL_CHEM_REACTIONMATCHCONSTRAINT_HPP

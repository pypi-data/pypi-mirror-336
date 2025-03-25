/* 
 * CIPSorter.cpp 
 *
 * This file is part of the Chemical Data Processing Toolkit
 *
 * Copyright (C) 2003 Thomas Seidel <thomas.seidel@univie.ac.at>
 *
 * Code based on a Java implementation of the CIP sequence rules by John Mayfield
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


#include <utility>

#include "CIPSorter.hpp"
#include "CIPSequenceRule.hpp"


using namespace CDPL;


Chem::CIPSortingResult Chem::CIPSorter::prioritise(const CIPDigraph::Node& node, CIPDigraph::EdgeList& edges, bool deep) const
{
    bool unique = true;
    bool found_wc = false;
    std::size_t num_pseudo_asym = 0;

    for (std::size_t i = 0, num_edges = edges.size(); i < num_edges && !found_wc; i++) {
        for (long j = i; j > 0; j--) {
            int cmp = compareLigands(node, *edges[j - 1], *edges[j], deep);

            if (cmp == CIPSequenceRule::COMP_TO_WILDCARD) {
                unique = false;
                found_wc = true;
                break;
            }

            // -2/+2 means we used Rule 5 (or more) and the ligands are mirror images
            if (cmp < -1 || cmp > 1)
                num_pseudo_asym++;

            if (cmp < 0) {
                std::swap(edges[j], edges[j - 1]);

            } else {
                if (cmp == 0)
                    unique = false;
                break;
            }
        }
    }

    return CIPSortingResult(unique, found_wc, num_pseudo_asym == 1);
}

int Chem::CIPSorter::compareLigands(const CIPDigraph::Node& node, const CIPDigraph::Edge& a, const CIPDigraph::Edge& b, bool deep) const
{
    // ensure 'up' edges are moved to the front
    if (!a.isBeg(node) && b.isBeg(node))
        return +1;

    if (a.isBeg(node) && !b.isBeg(node))
        return -1;

    for (std::size_t i = 0; i < numRules; i++) {
        int cmp = rules[i]->getComparison(a, b, deep);

        if (cmp != 0)
            return cmp;
    }

    return 0;
}

std::size_t Chem::CIPSorter::getNumGroups(const CIPDigraph::EdgeList& edges) const
{
    // would be nice to have this integrated whilst sorting - may provide a small speed increase
    // but as most of our lists are small we take use ugly sort then group approach
    std::size_t num_grps = 0;
    CIPDigraph::Edge* prev = 0;

    for (auto edge : edges) {
        if (!prev || compareLigands(prev->getBeg(), *prev, *edge, true) != 0)
            num_grps++;

        prev = edge;
    }

    return num_grps;
}

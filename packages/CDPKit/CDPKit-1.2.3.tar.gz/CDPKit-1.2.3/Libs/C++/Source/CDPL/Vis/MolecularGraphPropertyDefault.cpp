/* 
 * MolecularGraphPropertyDefault.cpp 
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

#include "CDPL/Vis/MolecularGraphPropertyDefault.hpp"


namespace CDPL
{

    namespace Vis
    {

        namespace MolecularGraphPropertyDefault
        {

            const ColorTable::SharedPointer ATOM_COLOR_TABLE                = ColorTable::SharedPointer(new ColorTable());
            const Color                     ATOM_COLOR                      = Color(0, 0, 0);
            const Font                      ATOM_LABEL_FONT                 = Font();
            const SizeSpecification         ATOM_LABEL_SIZE                 = SizeSpecification(10.0, false, false, true);
            const Font                      SECONDARY_ATOM_LABEL_FONT       = Font();
            const SizeSpecification         SECONDARY_ATOM_LABEL_SIZE       = SizeSpecification(6.0, false, false, true);
            const SizeSpecification         ATOM_LABEL_MARGIN               = SizeSpecification(2.0, false, false, true);
            const SizeSpecification         RADICAL_ELECTRON_DOT_SIZE       = SizeSpecification(1.0, false, false, true);
            const SizeSpecification         ATOM_HIGHLIGHT_AREA_SIZE        = SizeSpecification(16.0, false, false, true);
            const Brush                     ATOM_HIGHLIGHT_AREA_BRUSH       = Brush(Color(0.8, 0.8, 1.0));
            const Pen                       ATOM_HIGHLIGHT_AREA_OUTLINE_PEN = Pen(Color(0.6, 0.6, 0.75));
            const Font                      ATOM_CONFIGURATION_LABEL_FONT   = Font();
            const SizeSpecification         ATOM_CONFIGURATION_LABEL_SIZE   = SizeSpecification(8.0, false, false, true);
            const Color                     ATOM_CONFIGURATION_LABEL_COLOR  = Color(0, 0, 0);
            const Font                      ATOM_CUSTOM_LABEL_FONT          = Font();
            const SizeSpecification         ATOM_CUSTOM_LABEL_SIZE          = SizeSpecification(8.0, false, false, true);
            const Color                     ATOM_CUSTOM_LABEL_COLOR         = Color(0, 0, 0);

            const SizeSpecification         HIGHLIGHT_AREA_OUTLINE_WIDTH    = SizeSpecification(1.0, false, false, true);

            const Color             BOND_COLOR                      = Color(0, 0, 0);
            const SizeSpecification BOND_LINE_WIDTH                 = SizeSpecification(1.5, false, false, true);
            const SizeSpecification BOND_LINE_SPACING               = SizeSpecification(0.15, true, true, true);
            const SizeSpecification STEREO_BOND_WEDGE_WIDTH         = SizeSpecification(0.15, true, true, true);
            const SizeSpecification STEREO_BOND_HASH_SPACING        = SizeSpecification(0.1, true, true, true);
            const SizeSpecification REACTION_CENTER_LINE_LENGTH     = SizeSpecification(0.4, true, true, true);
            const SizeSpecification REACTION_CENTER_LINE_SPACING    = SizeSpecification(0.1, true, true, true);
            const SizeSpecification DOUBLE_BOND_TRIM_LENGTH         = SizeSpecification(0.1, true, true, true);
            const SizeSpecification TRIPLE_BOND_TRIM_LENGTH         = SizeSpecification(0.1, true, true, true);
            const Font              BOND_LABEL_FONT                 = Font();
            const SizeSpecification BOND_LABEL_SIZE                 = SizeSpecification(8.0, false, false, true);
            const SizeSpecification BOND_LABEL_MARGIN               = SizeSpecification(2.0, false, false, true);
            const SizeSpecification BOND_HIGHLIGHT_AREA_WIDTH       = SizeSpecification(12.0, false, false, true);
            const Brush             BOND_HIGHLIGHT_AREA_BRUSH       = Brush(Color(0.8, 0.8, 1.0));
            const Pen               BOND_HIGHLIGHT_AREA_OUTLINE_PEN = Pen(Color(0.6, 0.6, 0.75));
            const Font              BOND_CONFIGURATION_LABEL_FONT   = Font();
            const SizeSpecification BOND_CONFIGURATION_LABEL_SIZE   = SizeSpecification(8.0, false, false, true);
            const Color             BOND_CONFIGURATION_LABEL_COLOR  = Color(0, 0, 0);
            const Font              BOND_CUSTOM_LABEL_FONT          = Font();
            const SizeSpecification BOND_CUSTOM_LABEL_SIZE          = SizeSpecification(8.0, false, false, true);
            const Color             BOND_CUSTOM_LABEL_COLOR         = Color(0, 0, 0);

        } // namespace MolecularGraphPropertyDefault

        void initMolecularGraphPropertyDefaults() {}
    }
}

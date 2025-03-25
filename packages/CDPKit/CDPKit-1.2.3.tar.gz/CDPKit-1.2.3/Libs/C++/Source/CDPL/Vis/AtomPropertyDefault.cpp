/* 
 * AtomPropertyDefault.cpp 
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

#include "CDPL/Vis/AtomPropertyDefault.hpp"


namespace CDPL
{

    namespace Vis
    {

        namespace AtomPropertyDefault
        {

            const Color             COLOR                      = Color(0, 0, 0);
            const Font              LABEL_FONT                 = Font();
            const SizeSpecification LABEL_SIZE                 = SizeSpecification(10.0, false, false, true);
            const Font              SECONDARY_LABEL_FONT       = Font();
            const SizeSpecification SECONDARY_LABEL_SIZE       = SizeSpecification(6.0, false, false, true);
            const SizeSpecification LABEL_MARGIN               = SizeSpecification(2.0, false, false, true);
            const SizeSpecification RADICAL_ELECTRON_DOT_SIZE  = SizeSpecification(1.0, false, false, true);
            const Font              CONFIGURATION_LABEL_FONT   = Font();
            const SizeSpecification CONFIGURATION_LABEL_SIZE   = SizeSpecification(8.0, false, false, true);
            const Color             CONFIGURATION_LABEL_COLOR  = Color(0, 0, 0);
            const Font              CUSTOM_LABEL_FONT          = Font();
            const SizeSpecification CUSTOM_LABEL_SIZE          = SizeSpecification(8.0, false, false, true);
            const Color             CUSTOM_LABEL_COLOR         = Color(0, 0, 0);
            const std::string       CUSTOM_LABEL               = "";
            const bool              HIGHLIGHTED_FLAG           = false;
            const Brush             HIGHLIGHT_AREA_BRUSH       = Brush(Color(0.8, 0.8, 1.0));
            const Pen               HIGHLIGHT_AREA_OUTLINE_PEN = Pen(Color(0.6, 0.6, 0.75));

        } // namespace AtomPropertyDefault

        void initAtomPropertyDefaults() {}
    }
}

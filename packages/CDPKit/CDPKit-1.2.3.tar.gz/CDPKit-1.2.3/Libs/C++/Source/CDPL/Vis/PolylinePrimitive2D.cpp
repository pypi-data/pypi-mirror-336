/* 
 * PolylinePrimitive2D.cpp 
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

#include "CDPL/Vis/PolylinePrimitive2D.hpp"
#include "CDPL/Vis/Renderer2D.hpp"
#include "CDPL/Vis/Rectangle2D.hpp"


using namespace CDPL;


void Vis::PolylinePrimitive2D::render(Renderer2D& renderer) const
{
    renderer.setPen(pen);

    renderer.drawPolyline(*this);
}

void Vis::PolylinePrimitive2D::setPen(const Pen& pen)
{
    this->pen = pen;
}

const Vis::Pen& Vis::PolylinePrimitive2D::getPen() const
{
    return pen;
}

Vis::GraphicsPrimitive2D::SharedPointer Vis::PolylinePrimitive2D::clone() const
{
    return SharedPointer(new PolylinePrimitive2D(*this));
}

void Vis::PolylinePrimitive2D::getBounds(Rectangle2D& bounds, FontMetrics* fm) const
{
    PointArray2D::getBounds(bounds);

    if (pen.getLineStyle() != Pen::NO_LINE)
        bounds.addMargin(pen.getWidth() * 0.5, pen.getWidth() * 0.5);
}

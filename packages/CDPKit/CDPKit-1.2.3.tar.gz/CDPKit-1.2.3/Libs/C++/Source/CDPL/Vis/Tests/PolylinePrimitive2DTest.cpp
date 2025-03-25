/* 
 * PolylinePrimitive2DTest.cpp 
 *
 * This file is part of the Chemical Data Processing Toolkit
 *
 * Copyright (C) 2003 Thomas Seidel <thomas.seidel@univie.ac.at>
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program; see the file COPYING. If not, write to
 * the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 */


#include <cstddef>

#include <boost/test/auto_unit_test.hpp>

#include "CDPL/Config.hpp"
#include "CDPL/Vis/PolylinePrimitive2D.hpp"
#include "CDPL/Vis/Rectangle2D.hpp"
#include "CDPL/Vis/Pen.hpp"
#include "CDPL/Vis/Color.hpp"

#ifdef HAVE_CAIRO 
# ifdef HAVE_CAIRO_PNG_SUPPORT

# include <cairo.h>

# include "CDPL/Vis/CairoPointer.hpp"
# include "CDPL/Vis/CairoRenderer2D.hpp"

# endif // HAVE_CAIRO_PNG_SUPPORT
#endif // HAVE_CAIRO


namespace
{

    void checkClone(const CDPL::Vis::PolylinePrimitive2D& prim)
    {
        using namespace CDPL;
        using namespace Vis;

        GraphicsPrimitive2D::SharedPointer gp_clone_ptr = prim.clone();
        const PolylinePrimitive2D* prim_clone_ptr = static_cast<const PolylinePrimitive2D*>(gp_clone_ptr.get());

        BOOST_CHECK_EQUAL(prim_clone_ptr->getSize(), prim.getSize());
        BOOST_CHECK(prim_clone_ptr->getPen() == prim.getPen());

        for (std::size_t i = 0; i < prim.getSize(); i++)
            BOOST_CHECK((*prim_clone_ptr)[i] == prim[i]);
    }
}


BOOST_AUTO_TEST_CASE(PolylinePrimitive2DTest)
{
    using namespace CDPL;
    using namespace Vis;

    PolylinePrimitive2D plp;

    BOOST_CHECK(plp.getPen() == Pen());

    checkClone(plp);

    plp.setPen(Pen(Color::GREEN, Pen::DASH_LINE));

    BOOST_CHECK(plp.getPen() == Pen(Color::GREEN, Pen::DASH_LINE));

    checkClone(plp);

//-----

#ifdef HAVE_CAIRO 
# ifdef HAVE_CAIRO_PNG_SUPPORT

    CairoPointer<cairo_surface_t> surf_ptr(cairo_image_surface_create(CAIRO_FORMAT_ARGB32, 310, 1300));

    BOOST_CHECK(cairo_surface_status(surf_ptr.get()) == CAIRO_STATUS_SUCCESS);

    CairoPointer<cairo_t> ctxt_ptr(cairo_create(surf_ptr.get()));

    BOOST_CHECK(cairo_status(ctxt_ptr.get()) == CAIRO_STATUS_SUCCESS);

    CairoRenderer2D renderer(ctxt_ptr);

    Pen test_pens[] = {
        Pen(Color::BLACK, 0.0, Pen::NO_LINE, Pen::ROUND_CAP, Pen::MITER_JOIN),
        Pen(Color::BLACK, 0.5, Pen::SOLID_LINE, Pen::ROUND_CAP, Pen::BEVEL_JOIN),
        Pen(Color::BLACK, 0.5, Pen::DASH_LINE, Pen::ROUND_CAP, Pen::ROUND_JOIN),
        Pen(Color::BLACK, 0.5, Pen::DOT_LINE, Pen::ROUND_CAP, Pen::MITER_JOIN),
        Pen(Color::BLACK, 0.5, Pen::DASH_DOT_LINE, Pen::ROUND_CAP, Pen::BEVEL_JOIN),
        Pen(Color::BLACK, 0.5, Pen::DASH_DOT_DOT_LINE, Pen::ROUND_CAP, Pen::ROUND_JOIN),
        
        Pen(Color::RED, 1.0, Pen::NO_LINE, Pen::FLAT_CAP, Pen::BEVEL_JOIN),
        Pen(Color::RED, 1.0, Pen::SOLID_LINE, Pen::FLAT_CAP, Pen::ROUND_JOIN),
        Pen(Color::RED, 1.0, Pen::DASH_LINE, Pen::FLAT_CAP, Pen::MITER_JOIN),
        Pen(Color::RED, 1.0, Pen::DOT_LINE, Pen::FLAT_CAP, Pen::BEVEL_JOIN),
        Pen(Color::RED, 1.0, Pen::DASH_DOT_LINE, Pen::FLAT_CAP, Pen::ROUND_JOIN),
        Pen(Color::RED, 1.0, Pen::DASH_DOT_DOT_LINE, Pen::FLAT_CAP, Pen::MITER_JOIN),
        
        Pen(Color::GREEN, 1.5, Pen::NO_LINE, Pen::SQUARE_CAP, Pen::ROUND_JOIN),
        Pen(Color::GREEN, 1.5, Pen::SOLID_LINE, Pen::SQUARE_CAP, Pen::MITER_JOIN),
        Pen(Color::GREEN, 1.5, Pen::DASH_LINE, Pen::SQUARE_CAP, Pen::BEVEL_JOIN),
        Pen(Color::GREEN, 1.5, Pen::DOT_LINE, Pen::SQUARE_CAP, Pen::ROUND_JOIN),
        Pen(Color::GREEN, 1.5, Pen::DASH_DOT_LINE, Pen::SQUARE_CAP, Pen::MITER_JOIN),
        Pen(Color::GREEN, 1.5, Pen::DASH_DOT_DOT_LINE, Pen::SQUARE_CAP, Pen::BEVEL_JOIN),
        
        Pen(Color::BLUE, 2.0, Pen::NO_LINE, Pen::ROUND_CAP, Pen::MITER_JOIN),
        Pen(Color::BLUE, 2.0, Pen::SOLID_LINE, Pen::ROUND_CAP, Pen::BEVEL_JOIN),
        Pen(Color::BLUE, 2.0, Pen::DASH_LINE, Pen::ROUND_CAP, Pen::ROUND_JOIN),
        Pen(Color::BLUE, 2.0, Pen::DOT_LINE, Pen::ROUND_CAP, Pen::MITER_JOIN),
        Pen(Color::BLUE, 2.0, Pen::DASH_DOT_LINE, Pen::ROUND_CAP, Pen::BEVEL_JOIN),
        Pen(Color::BLUE, 2.0, Pen::DASH_DOT_DOT_LINE, Pen::ROUND_CAP, Pen::ROUND_JOIN),
    
        Pen(Color::MAGENTA, 3.0, Pen::NO_LINE, Pen::FLAT_CAP, Pen::BEVEL_JOIN),
        Pen(Color::MAGENTA, 3.0, Pen::SOLID_LINE, Pen::FLAT_CAP, Pen::ROUND_JOIN),
        Pen(Color::MAGENTA, 3.0, Pen::DASH_LINE, Pen::FLAT_CAP, Pen::MITER_JOIN),
        Pen(Color::MAGENTA, 3.0, Pen::DOT_LINE, Pen::FLAT_CAP, Pen::BEVEL_JOIN),
        Pen(Color::MAGENTA, 3.0, Pen::DASH_DOT_LINE, Pen::FLAT_CAP, Pen::ROUND_JOIN),
        Pen(Color::MAGENTA, 3.0, Pen::DASH_DOT_DOT_LINE, Pen::FLAT_CAP, Pen::MITER_JOIN),
        
        Pen(Color::CYAN, 5.0, Pen::NO_LINE, Pen::SQUARE_CAP, Pen::ROUND_JOIN),
        Pen(Color::CYAN, 5.0, Pen::SOLID_LINE, Pen::SQUARE_CAP, Pen::MITER_JOIN),
        Pen(Color::CYAN, 5.0, Pen::DASH_LINE, Pen::SQUARE_CAP, Pen::BEVEL_JOIN),
        Pen(Color::CYAN, 5.0, Pen::DOT_LINE, Pen::SQUARE_CAP, Pen::ROUND_JOIN),
        Pen(Color::CYAN, 5.0, Pen::DASH_DOT_LINE, Pen::SQUARE_CAP, Pen::MITER_JOIN),
        Pen(Color::CYAN, 5.0, Pen::DASH_DOT_DOT_LINE, Pen::SQUARE_CAP, Pen::BEVEL_JOIN),
        
        Pen(Color::YELLOW, 10.0, Pen::NO_LINE, Pen::ROUND_CAP, Pen::MITER_JOIN),
        Pen(Color::YELLOW, 10.0, Pen::SOLID_LINE, Pen::ROUND_CAP, Pen::BEVEL_JOIN),
        Pen(Color::YELLOW, 10.0, Pen::DASH_LINE, Pen::ROUND_CAP, Pen::ROUND_JOIN),
        Pen(Color::YELLOW, 10.0, Pen::DOT_LINE, Pen::ROUND_CAP, Pen::MITER_JOIN),
        Pen(Color::YELLOW, 10.0, Pen::DASH_DOT_LINE, Pen::ROUND_CAP, Pen::BEVEL_JOIN),
        Pen(Color::YELLOW, 10.0, Pen::DASH_DOT_DOT_LINE, Pen::ROUND_CAP, Pen::ROUND_JOIN)
    };

    plp.resize(5);

    double y = 140.0;

    for (std::size_t i = 0; i < 7; y += 170.0, i++) {
        for (std::size_t j = 0; j < 6; j++) {
            plp.setPen(test_pens[i * 6 + j]);

            plp[0](0) = -1.0 * 20.0 * j;
            plp[0](1) = 1.0 * 20.0 * j;

            plp[1](0) = 1.0 * 20.0 * j;
            plp[1](1) = 1.0 * 20.0 * j;

            plp[2](0) = 0.5 * 20.0 * j;
            plp[2](1) = -1.0 * 20.0 * j;
            
            plp[3](0) = -1.5 * 20.0 * j;
            plp[3](1) = -0.5 * 20.0 * j;

            plp[4](0) = -1.8 * 20.0 * j;
            plp[4](1) = 0.5 * 20.0 * j;

            plp.translate(Math::vec(195.0, y));

            checkClone(plp);

            plp.render(renderer);

            Rectangle2D bbox;
            plp.getBounds(bbox, 0);

            renderer.setPen(Color::RED);
            renderer.setBrush(Brush());
            renderer.drawRectangle(bbox.getMin()(0), bbox.getMin()(1), bbox.getWidth(), bbox.getHeight());

            BOOST_CHECK(cairo_surface_status(surf_ptr.get()) == CAIRO_STATUS_SUCCESS);
            BOOST_CHECK(cairo_status(ctxt_ptr.get()) == CAIRO_STATUS_SUCCESS);
        }
    }

    BOOST_CHECK(cairo_surface_write_to_png(surf_ptr.get(), "PolylinePrimitive2DTest.png") == CAIRO_STATUS_SUCCESS);

# endif // HAVE_CAIRO_PNG_SUPPORT
#endif // HAVE_CAIRO
}

/* 
 * PenExport.cpp 
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


#include <sstream>
#include <iomanip>

#include <boost/python.hpp>

#include "CDPL/Vis/Pen.hpp"

#include "Base/ObjectIdentityCheckVisitor.hpp"
#include "Base/CopyAssOp.hpp"

#include "ClassExports.hpp"


namespace
{

    const char* toString(CDPL::Vis::Pen::LineStyle style)
    {
        using namespace CDPL;
        
        switch (style) {

            case Vis::Pen::NO_LINE:
                return "NO_LINE";

            case Vis::Pen::SOLID_LINE:
                return "SOLID_LINE";

            case Vis::Pen::DASH_LINE:
                return "DASH_LINE";

            case Vis::Pen::DOT_LINE:
                return "DOT_LINE";

            case Vis::Pen::DASH_DOT_LINE:
                return "DASH_DOT_LINE";
                
            case Vis::Pen::DASH_DOT_DOT_LINE:
                return "DASH_DOT_DOT_LINE";

            default:
                return "?";
        }
    }

    const char* toString(CDPL::Vis::Pen::CapStyle style)
    {
        using namespace CDPL;
        
        switch (style) {

            case Vis::Pen::FLAT_CAP:
                return "FLAT_CAP";

            case Vis::Pen::SQUARE_CAP:
                return "SQUARE_CAP";

            case Vis::Pen::ROUND_CAP:
                return "ROUND_CAP";

            default:
                return "?";
        }
    }

    const char* toString(CDPL::Vis::Pen::JoinStyle style)
    {
        using namespace CDPL;
        
        switch (style) {

            case Vis::Pen::MITER_JOIN:
                return "MITER_JOIN";

            case Vis::Pen::BEVEL_JOIN:
                return "BEVEL_JOIN";

            case Vis::Pen::ROUND_JOIN:
                return "ROUND_JOIN";
                
            default:
                return "?";
        }
    }
    
    std::string toString(const CDPL::Vis::Color& col)
    {
        std::ostringstream oss;

        oss << "Color(";
        
        if (col == CDPL::Vis::Color())
            oss << ')';
        
        else {
            oss << "r=" << col.getRed() << ", g=" << col.getGreen() << ", b=" << col.getBlue();

            if (col.getAlpha() != 1.0)
                oss << ", a=" << col.getAlpha();

            oss << ')';
        }
        
        return oss.str();
    }

    std::string penToString(const CDPL::Vis::Pen& pen)
    {
        std::ostringstream oss;

        oss << "CDPL.Vis.Pen(";
        
        if (pen == CDPL::Vis::Pen())
            oss << ')';
        
        else {
            oss << "color=" << toString(pen.getColor()) << ", width=" << pen.getWidth() << ", line_style=" << toString(pen.getLineStyle())
                << ", cap_style=" << toString(pen.getCapStyle()) << ", join_style=" << toString(pen.getJoinStyle()) << ')';
        }
        
        return oss.str();
    }
}


void CDPLPythonVis::exportPen()
{
    using namespace boost;
    using namespace CDPL;

    python::class_<Vis::Pen> pen_class("Pen", python::no_init);
    python::scope scope = pen_class;

    python::enum_<Vis::Pen::LineStyle>("LineStyle")
        .value("NO_LINE", Vis::Pen::NO_LINE)
        .value("SOLID_LINE", Vis::Pen::SOLID_LINE)
        .value("DASH_LINE", Vis::Pen::DASH_LINE)
        .value("DOT_LINE", Vis::Pen::DOT_LINE)
        .value("DASH_DOT_LINE", Vis::Pen::DASH_DOT_LINE)
        .value("DASH_DOT_DOT_LINE", Vis::Pen::DASH_DOT_DOT_LINE)
        .export_values();

    python::enum_<Vis::Pen::CapStyle>("CapStyle")
        .value("FLAT_CAP", Vis::Pen::FLAT_CAP)
        .value("SQUARE_CAP", Vis::Pen::SQUARE_CAP)
        .value("ROUND_CAP", Vis::Pen::ROUND_CAP)
        .export_values();

    python::enum_<Vis::Pen::JoinStyle>("JoinStyle")
        .value("MITER_JOIN", Vis::Pen::MITER_JOIN)
        .value("BEVEL_JOIN", Vis::Pen::BEVEL_JOIN)
        .value("ROUND_JOIN", Vis::Pen::ROUND_JOIN)
        .export_values();
    
    pen_class
        .def(python::init<>(python::arg("self")))    
        .def(python::init<const Vis::Pen&>((python::arg("self"), python::arg("pen"))))    
        .def(python::init<Vis::Pen::LineStyle>((python::arg("self"), python::arg("line_style"))))
        .def(python::init<const Vis::Color&, double, Vis::Pen::LineStyle, Vis::Pen::CapStyle, Vis::Pen::JoinStyle>(
                 (python::arg("self"), python::arg("color"), python::arg("width") = 1.0, 
                  python::arg("line_style") = Vis::Pen::SOLID_LINE, 
                  python::arg("cap_style") = Vis::Pen::ROUND_CAP, 
                  python::arg("join_style") = Vis::Pen::ROUND_JOIN)))    
        .def(CDPLPythonBase::ObjectIdentityCheckVisitor<Vis::Pen>())    
        .def("assign", CDPLPythonBase::copyAssOp<Vis::Pen>(),
             (python::arg("self"), python::arg("pen")), python::return_self<>())
        .def("getCapStyle", &Vis::Pen::getCapStyle, python::arg("self"))    
        .def("setCapStyle", &Vis::Pen::setCapStyle, (python::arg("self"), python::arg("cap_style")))    
        .def("getColor", &Vis::Pen::getColor, python::arg("self"), python::return_internal_reference<1>())    
        .def("setColor", &Vis::Pen::setColor, (python::arg("self"), python::arg("color")))
        .def("getJoinStyle", &Vis::Pen::getJoinStyle, python::arg("self"))    
        .def("setJoinStyle", &Vis::Pen::setJoinStyle, (python::arg("self"), python::arg("join_style"))) 
        .def("getLineStyle", &Vis::Pen::getLineStyle, python::arg("self"))    
        .def("setLineStyle", &Vis::Pen::setLineStyle, (python::arg("self"), python::arg("line_style")))    
        .def("getWidth", &Vis::Pen::getWidth, python::arg("self"))    
        .def("setWidth", &Vis::Pen::setWidth, (python::arg("self"), python::arg("width")))
        .def("__str__", &penToString, python::arg("self"))
        .def("__eq__", &Vis::Pen::operator==, (python::arg("self"), python::arg("pen")))
        .def("__ne__", &Vis::Pen::operator!=, (python::arg("self"), python::arg("pen")))
        .add_property("capStyle", &Vis::Pen::getCapStyle, &Vis::Pen::setCapStyle)
        .add_property("lineStyle", &Vis::Pen::getLineStyle, &Vis::Pen::setLineStyle)
        .add_property("joinStyle", &Vis::Pen::getJoinStyle, &Vis::Pen::setJoinStyle)
        .add_property("color", python::make_function(&Vis::Pen::getColor, python::return_internal_reference<1>()),
                      &Vis::Pen::setColor)
        .add_property("width", &Vis::Pen::getWidth, &Vis::Pen::setWidth);

    python::implicitly_convertible<Vis::Pen::LineStyle, Vis::Pen>();
    python::implicitly_convertible<Vis::Color, Vis::Pen>();
}

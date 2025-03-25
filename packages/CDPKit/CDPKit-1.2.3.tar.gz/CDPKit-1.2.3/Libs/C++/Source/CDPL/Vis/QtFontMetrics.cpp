/* 
 * QtFontMetrics.cpp 
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


#include <QFontMetricsF>
#include <QFont>
#include <QRectF>
#include <QString>

#include "CDPL/Vis/QtFontMetrics.hpp"
#include "CDPL/Vis/QtObjectFactory.hpp"
#include "CDPL/Vis/Font.hpp"
#include "CDPL/Vis/Rectangle2D.hpp"
#include "CDPL/Internal/StringUtilities.hpp"


using namespace CDPL;


Vis::QtFontMetrics::QtFontMetrics(QPaintDevice* paint_dev): 
    qPaintDevice(paint_dev), qFontMetrics(new QFontMetricsF(QFont(), paint_dev)) {}

Vis::QtFontMetrics::~QtFontMetrics() {}

void Vis::QtFontMetrics::setFont(const Font& font)
{
    qFontMetrics = std::unique_ptr<QFontMetricsF>(new QFontMetricsF(QtObjectFactory::createQFont(font), qPaintDevice));
}

double Vis::QtFontMetrics::getAscent() const
{
    return qFontMetrics->ascent();
}

double Vis::QtFontMetrics::getDescent() const
{
    return qFontMetrics->descent();
} 

double Vis::QtFontMetrics::getHeight() const
{
    return qFontMetrics->height();
}

double Vis::QtFontMetrics::getLeading() const
{
    return qFontMetrics->leading();
} 

double Vis::QtFontMetrics::getWidth(const std::string& str) const
{
    return qFontMetrics->width(QString::fromStdString(str));
} 

double Vis::QtFontMetrics::getWidth(char ch) const
{
    return qFontMetrics->width(ch);
} 

void Vis::QtFontMetrics::getBounds(const std::string& str, Rectangle2D& bounds) const
{
    if (str.size() == 1)
        return getBounds(str[0], bounds);

    QRectF str_bounds = qFontMetrics->boundingRect(QString::fromStdString(str));

    bounds.setMin(str_bounds.left(), 0.0);
    bounds.setMax(str_bounds.right(), 0.0);

    for (char c : str) {
        str_bounds = qFontMetrics->boundingRect(c);

        bounds.addPoint(bounds.getMin()[0], str_bounds.top());
        bounds.addPoint(bounds.getMax()[0], str_bounds.bottom());
    }

    if (!str.empty()) {
        if (Internal::IsWhitespace()(str.back()))
            bounds.addPoint(getWidth(str), 0.0);
        
        for (char c : str)
            if (!Internal::IsWhitespace()(c))
                return;

        bounds.addPoint(0.0, 0.0);
    }
} 

void Vis::QtFontMetrics::getBounds(char ch, Rectangle2D& bounds) const
{
    if (Internal::IsWhitespace()(ch)) {
        bounds.setBounds(0.0, 0.0, getWidth(ch), 0.0);
        return;
    }
    
    QRectF ch_bounds = qFontMetrics->boundingRect(ch);

    bounds.setBounds(ch_bounds.left(), ch_bounds.top(), ch_bounds.right(), ch_bounds.bottom());
} 

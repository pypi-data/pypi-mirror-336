## 
# CairoFontMetricsTest.py 
#
# This file is part of the Chemical Data Processing Toolkit
#
# Copyright (C) 2003 Thomas Seidel <thomas.seidel@univie.ac.at>
#
# This program is free software you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation either
# version 2 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program see the file COPYING. If not, write to
# the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
##
    

import unittest

import cairo

from CDPL.Vis import Font
from CDPL.Vis import Pen
from CDPL.Vis import Brush
from CDPL.Vis import Color
from CDPL.Vis import Rectangle2D
from CDPL.Math import vec
 
from CDPL.Vis.CairoBackend import CairoFontMetrics
from CDPL.Vis.CairoBackend import CairoRenderer2D


class TestCase(unittest.TestCase):

    def runTest(self):
        """Testing CairoFontMetrics"""

        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 300)
        ctxt = cairo.Context(surf)
        
        renderer = CairoRenderer2D(ctxt)
        fm = CairoFontMetrics(ctxt)
    
        bounds = Rectangle2D()
    
        #-----
    
        y = 40.0
    
        font = Font()
        text = 'Default Font'
    
        renderer.setPen(Color.BLUE)
        renderer.setFont(font)
    
        renderer.drawText(10.0, y, text)
    
        fm.setFont(font)
        fm.getBounds(text, bounds)
    
        bounds.translate(vec(10.0, y))
    
        renderer.setPen(Color.GREEN)
        renderer.drawRectangle(bounds.getMin()(0), bounds.getMin()(1), bounds.getWidth(), bounds.getHeight())
    
        renderer.setPen(Color.YELLOW)
        renderer.drawLine(bounds.getMin()(0), y, bounds.getMin()(0) + fm.getWidth(text), y)
    
        renderer.setPen(Color.MAGENTA)
        renderer.drawLine(50.0, y, 50.0, y - fm.getAscent())
    
        renderer.drawLine(70.0, y, 70.0, y + fm.getDescent())
    
        renderer.setPen(Color.MAGENTA)
        renderer.drawLine(5.0, bounds.getMax()(1), 5.0, bounds.getMax()(1) - fm.getHeight())
    
        fm.getBounds(text[0], bounds)
    
        bounds.translate(vec(10.0, y))
    
        renderer.setPen(Color.RED)
        renderer.drawRectangle(bounds.getMin()(0), bounds.getMin()(1), bounds.getWidth(), bounds.getHeight())
    
        renderer.setPen(Color.MAGENTA)
        renderer.drawLine(bounds.getMin()(0), y - 4.0, bounds.getMin()(0) + fm.getWidth(text[0]), y - 4.0)
    
        #-----
    
        y += 50.0
    
        font.assign(Font('Helvetica', 35.0))
        text = 'Helvetica 35'
    
        renderer.setPen(Color.BLUE)
        renderer.setFont(font)
    
        renderer.drawText(10.0, y, text)
    
        fm.setFont(font)
        fm.getBounds(text, bounds)
    
        bounds.translate(vec(10.0, y))
    
        renderer.setPen(Color.GREEN)
        renderer.drawRectangle(bounds.getMin()(0), bounds.getMin()(1), bounds.getWidth(), bounds.getHeight())
    
        renderer.setPen(Color.YELLOW)
        renderer.drawLine(bounds.getMin()(0), y, bounds.getMin()(0) + fm.getWidth(text), y)
    
        renderer.setPen(Color.MAGENTA)
        renderer.drawLine(50.0, y, 50.0, y - fm.getAscent())
    
        renderer.drawLine(70.0, y, 70.0, y + fm.getDescent())
    
        renderer.setPen(Color.MAGENTA)
        renderer.drawLine(5.0, bounds.getMax()(1), 5.0, bounds.getMax()(1) - fm.getHeight())
    
        fm.getBounds(text[0], bounds)
    
        bounds.translate(vec(10.0, y))
    
        renderer.setPen(Color.RED)
        renderer.drawRectangle(bounds.getMin()(0), bounds.getMin()(1), bounds.getWidth(), bounds.getHeight())
    
        renderer.setPen(Color.MAGENTA)
        renderer.drawLine(bounds.getMin()(0), y - 4.0, bounds.getMin()(0) + fm.getWidth(text[0]), y - 4.0)
    
        #-----
    
        y += 50.0
    
        font.assign(Font('Times', 35.0))
        font.setBold(True)
    
        text = 'Times 35 bold'
    
        renderer.setPen(Color.BLUE)
        renderer.setFont(font)
    
        renderer.drawText(10.0, y, text)
    
        fm.setFont(font)
        fm.getBounds(text, bounds)
    
        bounds.translate(vec(10.0, y))
    
        renderer.setPen(Color.GREEN)
        renderer.drawRectangle(bounds.getMin()(0), bounds.getMin()(1), bounds.getWidth(), bounds.getHeight())
    
        renderer.setPen(Color.YELLOW)
        renderer.drawLine(bounds.getMin()(0), y, bounds.getMin()(0) + fm.getWidth(text), y)
    
        renderer.setPen(Color.MAGENTA)
        renderer.drawLine(50.0, y, 50.0, y - fm.getAscent())
    
        renderer.drawLine(70.0, y, 70.0, y + fm.getDescent())
    
        renderer.setPen(Color.MAGENTA)
        renderer.drawLine(5.0, bounds.getMax()(1), 5.0, bounds.getMax()(1) - fm.getHeight())
    
        fm.getBounds(text[0], bounds)
    
        bounds.translate(vec(10.0, y))
    
        renderer.setPen(Color.RED)
        renderer.drawRectangle(bounds.getMin()(0), bounds.getMin()(1), bounds.getWidth(), bounds.getHeight())
    
        renderer.setPen(Color.MAGENTA)
        renderer.drawLine(bounds.getMin()(0), y - 4.0, bounds.getMin()(0) + fm.getWidth(text[0]), y - 4.0)
    
        #-----
    
        y += 50.0
    
        font.assign(Font('Courier', 35.0))
        font.setItalic(True)
    
        text = '  Courier 35 italic  '
    
        renderer.setPen(Color.BLUE)
        renderer.setFont(font)
    
        renderer.drawText(10.0, y, text)
    
        fm.setFont(font)
        fm.getBounds(text, bounds)
    
        bounds.translate(vec(10.0, y))
    
        renderer.setPen(Color.GREEN)
        renderer.drawRectangle(bounds.getMin()(0), bounds.getMin()(1), bounds.getWidth(), bounds.getHeight())
    
        renderer.setPen(Color.YELLOW)
        renderer.drawLine(bounds.getMin()(0), y, bounds.getMin()(0) + fm.getWidth(text), y)
    
        renderer.setPen(Color.MAGENTA)
        renderer.drawLine(50.0, y, 50.0, y - fm.getAscent())
    
        renderer.drawLine(70.0, y, 70.0, y + fm.getDescent())
    
        renderer.setPen(Color.MAGENTA)
        renderer.drawLine(5.0, bounds.getMax()(1), 5.0, bounds.getMax()(1) - fm.getHeight())
    
        fm.getBounds(text[0], bounds)
    
        bounds.translate(vec(10.0, y))
    
        renderer.setPen(Color.RED)
        renderer.drawRectangle(bounds.getMin()(0), bounds.getMin()(1), bounds.getWidth(), bounds.getHeight())

        renderer.setPen(Color.MAGENTA)
        renderer.drawLine(bounds.getMin()(0), y - 4.0, bounds.getMin()(0) + fm.getWidth(text[0]), y - 4.0)
    
        #-----
    
        y += 50.0
    
        font.assign(Font('Default', 35.0))
        font.setBold(True)
        font.setItalic(True)
    
        text = 'Default 35 bold italic'
    
        renderer.setPen(Color.BLUE)
        renderer.setFont(font)
    
        renderer.drawText(10.0, y, text)
    
        fm.setFont(font)
        fm.getBounds(text, bounds)
    
        bounds.translate(vec(10.0, y))
    
        renderer.setPen(Color.GREEN)
        renderer.drawRectangle(bounds.getMin()(0), bounds.getMin()(1), bounds.getWidth(), bounds.getHeight())
    
        renderer.setPen(Color.YELLOW)
        renderer.drawLine(bounds.getMin()(0), y, bounds.getMin()(0) + fm.getWidth(text), y)
    
        renderer.setPen(Color.MAGENTA)
        renderer.drawLine(50.0, y, 50.0, y - fm.getAscent())
    
        renderer.drawLine(70.0, y, 70.0, y + fm.getDescent())
    
        renderer.setPen(Color.MAGENTA)
        renderer.drawLine(5.0, bounds.getMax()(1), 5.0, bounds.getMax()(1) - fm.getHeight())
    
        fm.getBounds(text[0], bounds)
    
        bounds.translate(vec(10.0, y))
    
        renderer.setPen(Color.RED)
        renderer.drawRectangle(bounds.getMin()(0), bounds.getMin()(1), bounds.getWidth(), bounds.getHeight())
    
        renderer.setPen(Color.MAGENTA)
        renderer.drawLine(bounds.getMin()(0), y - 4.0, bounds.getMin()(0) + fm.getWidth(text[0]), y - 4.0)
    
        #-----
    
        surf.write_to_png('CairoFontMetricsTest.png')

/* 
 * DataRecordPainter.hpp 
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


#ifndef CHOX_DATARECORDPAINTER_HPP
#define CHOX_DATARECORDPAINTER_HPP

#include <memory>

#include <QString>

#include "CDPL/Vis/QtRenderer2D.hpp"

#include "DataRecordVisitor.hpp"


namespace ChOX
{

    class DataRecord;
    class Settings;
    class RecordDataVisitor;

    class DataRecordPainter : private DataRecordVisitor
    {

      public:
        typedef std::shared_ptr<DataRecordPainter> SharedPointer;

        DataRecordPainter(CDPL::Vis::QtFontMetrics&, QPainter&, const Settings&, const DataRecord&);

        ~DataRecordPainter();

        void drawRecord(int rec_no, double vp_width, double vp_height);

        void accept(RecordDataVisitor& visitor);

        void update();

      private:
        enum DataType
        {

            MOLECULE,
            REACTION,
            VOID
        };

        void drawRecordNumber(int rec_no, double vp_width, double vp_height) const;
        void drawRecordName(double vp_width, double vp_height) const;

        bool setupViewport(double vp_width, double vp_height) const;

        void visit(const ConcreteDataRecord<CDPL::Chem::Reaction>&);
        void visit(const ConcreteDataRecord<CDPL::Chem::Molecule>&);

        typedef std::shared_ptr<CDPL::Vis::View2D>             DataViewPointer;
        typedef std::shared_ptr<CDPL::Base::PropertyContainer> PropertyContainerPointer;

        QPainter&                 painter;
        const Settings&           settings;
        PropertyContainerPointer  data;
        DataViewPointer           dataView;
        QString                   recordName;
        CDPL::Vis::QtRenderer2D   renderer;
        CDPL::Vis::QtFontMetrics& fontMetrics;
        bool                      recordNosVisible;
        bool                      recordNamesVisible;
        DataType                  dataType;
    };
} // namespace ChOX

#endif // CHOX_DATARECORDPAINTER_HPP

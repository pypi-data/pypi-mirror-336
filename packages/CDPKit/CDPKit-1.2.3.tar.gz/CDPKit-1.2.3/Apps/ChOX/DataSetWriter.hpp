/* 
 * DataSetWriter.hpp 
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


#ifndef CHOX_DATASETWRITER_HPP
#define CHOX_DATASETWRITER_HPP

#include <string>

#include <QObject>
#include <QString>

#include "DataRecordVisitor.hpp"


class QWidget;


namespace ChOX
{

    class Settings;
    class DataSet;
    class RecordDataVisitor;

    class DataSetWriter : public QObject,
                          private DataRecordVisitor
    {

        Q_OBJECT

      public:
        DataSetWriter(const DataSet& data_set, QWidget* parent, const QString& file_name,
                      const QString& filter, const Settings& settings, bool selection);

        ~DataSetWriter();

        void write();

        void setRecordDataVisitor(RecordDataVisitor* visitor);
        
      signals:
        void errorMessage(const QString&);
        void statusMessage(const QString&);

      private:
        void visit(const ConcreteDataRecord<CDPL::Chem::Reaction>&);
        void visit(const ConcreteDataRecord<CDPL::Chem::Molecule>&);

        template <typename T>
        void writeRecords(const std::string& def_format);

        const DataSet&     dataSet;
        QWidget*           parent;
        QString            fileName;
        QString            filter;
        const Settings&    settings;
        bool               writeSelection;
        RecordDataVisitor* recDataVisitor;
    };
} // namespace ChOX

#endif // CHOX_DATASETWRITER_HPP

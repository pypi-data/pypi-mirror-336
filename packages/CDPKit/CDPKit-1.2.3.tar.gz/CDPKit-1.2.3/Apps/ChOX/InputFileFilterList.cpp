/* 
 * InputFileFilterList.cpp 
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


#include "CDPL/Base/DataIOManager.hpp"

#include "InputFileFilterList.hpp"
#include "DataSet.hpp"


namespace
{

    template <typename T>    
    void appendInputFilters(QString& filters)
    {
        using namespace CDPL;
        using namespace Base;

        typename DataIOManager<T>::InputHandlerIterator handlers_end = DataIOManager<T>::getInputHandlersEnd();

        for (typename DataIOManager<T>::InputHandlerIterator h_it = DataIOManager<T>::getInputHandlersBegin(); 
             h_it != handlers_end; ++h_it) {

            const DataFormat& fmt_descr = (*h_it)->getDataFormat();

            if (filters.contains(QString::fromStdString(fmt_descr.getDescription())))
                continue;

            filters.append(QString::fromStdString(fmt_descr.getDescription()));
            filters.append(" (");

            DataFormat::ConstFileExtensionIterator exts_end = fmt_descr.getFileExtensionsEnd();

            for (DataFormat::ConstFileExtensionIterator e_it = fmt_descr.getFileExtensionsBegin(); e_it != exts_end; ++e_it) {
                filters.append(" *.");
                filters.append(QString::fromStdString(*e_it));
            }

            filters.append(" );");
        }
    }
}


using namespace ChOX;


InputFileFilterList::InputFileFilterList(const DataSet& data_set)
{
    if (data_set.getSize() == 0) {
        appendInputFilters<CDPL::Chem::Reaction>(filterString);
        appendInputFilters<CDPL::Chem::Molecule>(filterString);

    } else
        data_set.getRecord(0).accept(*this);

    QStringList::operator=(filterString.split(';', QString::SkipEmptyParts));
}

InputFileFilterList::InputFileFilterList()
{
    appendInputFilters<CDPL::Chem::Reaction>(filterString);
    appendInputFilters<CDPL::Chem::Molecule>(filterString);

    QStringList::operator=(filterString.split(';', QString::SkipEmptyParts));

    append("All Files (*)");
}

void InputFileFilterList::visit(const ConcreteDataRecord<CDPL::Chem::Reaction>&)
{
    appendInputFilters<CDPL::Chem::Reaction>(filterString);
}

void InputFileFilterList::visit(const ConcreteDataRecord<CDPL::Chem::Molecule>&)
{
    appendInputFilters<CDPL::Chem::Molecule>(filterString);
}

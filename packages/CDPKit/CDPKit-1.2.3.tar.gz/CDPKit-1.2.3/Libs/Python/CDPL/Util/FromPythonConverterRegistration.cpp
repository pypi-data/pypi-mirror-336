/* 
 * FromPythonConverterRegistration.cpp 
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


#include <boost/python/ssize_t.hpp>

#include "CDPL/Util/Array.hpp"

#include "Base/GenericAnyFromPythonConverter.hpp"

#include "ConverterRegistration.hpp"


namespace
{

    template <typename ArrayType>
    struct ArrayFromPySequenceConverter 
    {

        ArrayFromPySequenceConverter() {
            using namespace boost;

            python::converter::registry::insert(&convertible, &construct, python::type_id<ArrayType>());
        }

        static void* convertible(PyObject* obj_ptr) {
            using namespace boost;

            if (!obj_ptr)
                return 0;

            if (!PySequence_Check(obj_ptr))
                return 0;

            python::ssize_t size = PySequence_Size(obj_ptr);

            for (python::ssize_t i = 0; i < size; i++) 
                if (!python::extract<typename ArrayType::ElementType>(PySequence_GetItem(obj_ptr, i)).check())
                    return 0;

            return obj_ptr;
        }

        static void construct(PyObject* obj_ptr, boost::python::converter::rvalue_from_python_stage1_data* data) {
            using namespace boost;

            python::ssize_t size = PySequence_Size(obj_ptr);

            ArrayType array(size);

            for (python::ssize_t i = 0; i < size; i++)
                array.setElement(i, python::extract<typename ArrayType::ElementType>(PySequence_GetItem(obj_ptr, i)));

            void* storage = ((python::converter::rvalue_from_python_storage<ArrayType>*)data)->storage.bytes;

            new (storage) ArrayType();

            static_cast<ArrayType*>(storage)->swap(array);

            data->convertible = storage;
        }
    };
}


void CDPLPythonUtil::registerFromPythonConverters()
{
    using namespace CDPL;

    ArrayFromPySequenceConverter<Util::UIArray>();
    ArrayFromPySequenceConverter<Util::STArray>();
    ArrayFromPySequenceConverter<Util::DArray>();
    ArrayFromPySequenceConverter<Util::SArray>();

    CDPLPythonBase::GenericAnyFromPythonConverter<const Util::UIArray::SharedPointer&>();
    CDPLPythonBase::GenericAnyFromPythonConverter<const Util::STArray::SharedPointer&>();
    CDPLPythonBase::GenericAnyFromPythonConverter<const Util::DArray::SharedPointer&>();
    CDPLPythonBase::GenericAnyFromPythonConverter<const Util::SArray::SharedPointer&>();
}

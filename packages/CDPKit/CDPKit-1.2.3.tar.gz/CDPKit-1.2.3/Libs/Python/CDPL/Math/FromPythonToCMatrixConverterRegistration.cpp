/* 
 * FromPythonToCMatrixConverterRegistration.cpp 
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


#include <boost/python.hpp>
#include <boost/python/ssize_t.hpp>

#include "CDPL/Config.hpp"
#include "CDPL/Math/Matrix.hpp"

#include "ConverterRegistration.hpp"

#ifdef HAVE_NUMPY
# include "NumPy.hpp"
#endif


namespace
{

    template <typename MatrixType>
    struct CMatrixFromPySequenceConverter 
    {

        CMatrixFromPySequenceConverter() {
            using namespace boost;

            python::converter::registry::insert(&convertible, &construct, python::type_id<MatrixType>());
        }

        static void* convertible(PyObject* obj_ptr) {
            using namespace boost;

            if (!obj_ptr)
                return 0;

            if (!PyList_Check(obj_ptr) && !PyTuple_Check(obj_ptr))
                return 0;

            python::ssize_t num_rows = PySequence_Size(obj_ptr);

            if (num_rows != python::ssize_t(MatrixType::Size1))
                return 0;

            for (python::ssize_t i = 0; i < num_rows; i++) {
                PyObject* row_ptr = PySequence_GetItem(obj_ptr, i);

                if (!PySequence_Check(row_ptr))
                    return 0;

                python::ssize_t row_size = PySequence_Size(row_ptr);

                if (row_size > python::ssize_t(MatrixType::Size2))
                    return 0;

                for (python::ssize_t j = 0; j < row_size; j++) 
                    if (!python::extract<typename MatrixType::ValueType>(PySequence_GetItem(row_ptr, j)).check())
                        return 0;
            }

            return obj_ptr;
        }

        static void construct(PyObject* obj_ptr, boost::python::converter::rvalue_from_python_stage1_data* data) {
            using namespace boost;

            void* storage = ((python::converter::rvalue_from_python_storage<MatrixType>*)data)->storage.bytes;

            new (storage) MatrixType();

            MatrixType& mtx = *static_cast<MatrixType*>(storage);

            python::ssize_t num_rows = PySequence_Size(obj_ptr);

            for (python::ssize_t i = 0; i < num_rows; i++) {
                PyObject* row_ptr = PySequence_GetItem(obj_ptr, i);

                python::ssize_t row_size = PySequence_Size(row_ptr);

                for (python::ssize_t j = 0; j < row_size; j++) 
                    mtx(i, j) = python::extract<typename MatrixType::ValueType>(PySequence_GetItem(row_ptr, j));
            }

            data->convertible = storage;
        }
    };

#ifdef HAVE_NUMPY
    template <typename MatrixType>
    struct CMatrixFromNDArrayConverter 
    {

        CMatrixFromNDArrayConverter() {
            using namespace boost;

            python::converter::registry::insert(&convertible, &construct, python::type_id<MatrixType>());
        }

        static void* convertible(PyObject* obj_ptr) {
            using namespace boost;
            using namespace CDPLPythonMath;

            if (!obj_ptr)
                return 0;

            PyArrayObject* arr = NumPy::castToNDArray(obj_ptr);

            if (!arr)
                return 0;

            if (!NumPy::checkSize(arr, MatrixType::Size1, MatrixType::Size2))
                return 0;

            if (!NumPy::checkDataType<typename MatrixType::ValueType>(arr))
                return 0;
            
            return obj_ptr;
        }

        static void construct(PyObject* obj_ptr, boost::python::converter::rvalue_from_python_stage1_data* data) {
            using namespace boost;
            using namespace CDPLPythonMath;

            void* storage = ((python::converter::rvalue_from_python_storage<MatrixType>*)data)->storage.bytes;

            new (storage) MatrixType();

            MatrixType& mtx = *static_cast<MatrixType*>(storage);

            NumPy::copyArray2(mtx, NumPy::castToNDArray(obj_ptr));

            data->convertible = storage;
        }
    };
#endif
}


void CDPLPythonMath::registerFromPythonToCMatrixConverters()
{
    using namespace CDPL;

    CMatrixFromPySequenceConverter<Math::Matrix2F>();
    CMatrixFromPySequenceConverter<Math::Matrix3F>();
    CMatrixFromPySequenceConverter<Math::Matrix4F>();
    CMatrixFromPySequenceConverter<Math::Matrix2D>();
    CMatrixFromPySequenceConverter<Math::Matrix3D>();
    CMatrixFromPySequenceConverter<Math::Matrix4D>();
    CMatrixFromPySequenceConverter<Math::Matrix2L>();
    CMatrixFromPySequenceConverter<Math::Matrix3L>();
    CMatrixFromPySequenceConverter<Math::Matrix4L>();
    CMatrixFromPySequenceConverter<Math::Matrix2UL>();
    CMatrixFromPySequenceConverter<Math::Matrix3UL>();
    CMatrixFromPySequenceConverter<Math::Matrix4UL>();

#ifdef HAVE_NUMPY
    CMatrixFromNDArrayConverter<Math::Matrix2F>();
    CMatrixFromNDArrayConverter<Math::Matrix3F>();
    CMatrixFromNDArrayConverter<Math::Matrix4F>();
    CMatrixFromNDArrayConverter<Math::Matrix2D>();
    CMatrixFromNDArrayConverter<Math::Matrix3D>();
    CMatrixFromNDArrayConverter<Math::Matrix4D>();
    CMatrixFromNDArrayConverter<Math::Matrix2L>();
    CMatrixFromNDArrayConverter<Math::Matrix3L>();
    CMatrixFromNDArrayConverter<Math::Matrix4L>();
    CMatrixFromNDArrayConverter<Math::Matrix2UL>();
    CMatrixFromNDArrayConverter<Math::Matrix3UL>();
    CMatrixFromNDArrayConverter<Math::Matrix4UL>();
#endif
}

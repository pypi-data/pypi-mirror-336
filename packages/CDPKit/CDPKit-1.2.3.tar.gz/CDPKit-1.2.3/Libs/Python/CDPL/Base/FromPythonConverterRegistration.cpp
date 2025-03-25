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


#include <string>
#include <cstdint>
#include <limits>

#include <boost/python.hpp>
#include <boost/numeric/conversion/bounds.hpp>

#include "CDPL/Base/Any.hpp"
#include "CDPL/Base/ControlParameterContainer.hpp"

#include "ConverterRegistration.hpp"
#include "GenericAnyFromPythonConverter.hpp"


namespace
{

    struct AnyFromPyObjectConverter 
    {

        AnyFromPyObjectConverter() {
            using namespace boost;

            python::converter::registry::insert(&convertible, &construct, python::type_id<CDPL::Base::Any>());
        }

        static void* convertible(PyObject* obj_ptr) {
            return obj_ptr;
        }

        static void construct(PyObject* obj_ptr, boost::python::converter::rvalue_from_python_stage1_data* data) {
            using namespace boost;
            using namespace CDPL;

            void* storage = ((python::converter::rvalue_from_python_storage<Base::Any>*)data)->storage.bytes;

            if (obj_ptr == Py_None) 
                new (storage) Base::Any();

            else {
                python::handle<> obj_handle(python::borrowed(obj_ptr));

                new (storage) Base::Any(obj_handle);
            }

            data->convertible = storage;
        }
    };

    template <typename T> struct DefaultConversionPolicy;

    template <typename T, typename ConversionPolicy = DefaultConversionPolicy<T> >
    struct AnyFromPythonConverter 
    {

        AnyFromPythonConverter() {
            using namespace boost;

            python::converter::registry::insert(&convertible, &construct, python::type_id<CDPL::Base::Any>());
        }

        static void* convertible(PyObject* obj_ptr) {
            if (!obj_ptr)
                return 0;

            return ConversionPolicy::convertible(obj_ptr);
        }

        static void construct(PyObject* obj_ptr, boost::python::converter::rvalue_from_python_stage1_data* data) {
            using namespace boost;
            using namespace CDPL;

            void* storage = ((python::converter::rvalue_from_python_storage<Base::Any>*)data)->storage.bytes;

            new (storage) Base::Any(python::extract<T>(obj_ptr)());

            data->convertible = storage;
        }
    };

    template <typename T>
    struct DefaultConversionPolicy
    {

        static void* convertible(PyObject* obj_ptr) {
            return (boost::python::extract<T>(obj_ptr).check() ? obj_ptr : 0);
        }
    };

    template <typename T>
    struct PyIntToIntConversionPolicy
    {
        static void* convertible(PyObject* obj_ptr) {
            if (!PyLong_Check(obj_ptr))
                return 0;

            long value = PyLong_AS_LONG(obj_ptr);

            if (std::numeric_limits<T>::max() < value || std::numeric_limits<T>::min() > value)
                return 0;

            return obj_ptr;
        }
    };

    template <typename T>
    struct PyIntToUIntConversionPolicy
    {
        static void* convertible(PyObject* obj_ptr) {
            if (!PyLong_Check(obj_ptr))
                return 0;

            long value = PyLong_AS_LONG(obj_ptr);

            if (value < 0 || static_cast<unsigned long>(std::numeric_limits<T>::max()) < static_cast<unsigned long>(value))
                return 0;

            return obj_ptr;
        }
    };

    template <typename T>
    struct PyFloatConversionPolicy
    {
        static void* convertible(PyObject* obj_ptr) {
            using namespace boost;

            if (!PyFloat_Check(obj_ptr))
                return 0;

            double value = PyFloat_AS_DOUBLE(obj_ptr);

            if (double(numeric::bounds<T>::highest()) < value)
                return 0;
            
            if (double(numeric::bounds<T>::lowest()) > value)
                return 0;
            
            if (double(numeric::bounds<T>::smallest()) > std::abs(value))
                return 0;

            return obj_ptr;
        }
    };

    template <typename T>
    struct PyLongToIntConversionPolicy
    {
        static void* convertible(PyObject* obj_ptr) {
            if (!PyLong_Check(obj_ptr))
                return 0;

            PY_LONG_LONG value = PyLong_AsLongLong(obj_ptr);

            if (PyErr_Occurred()) {
                PyErr_Clear();
                return 0;
            }

            if (std::numeric_limits<T>::max() < value || std::numeric_limits<T>::min() > value)
                return 0;

            return obj_ptr;
        }
    };

    template <typename T>
    struct PyLongToUIntConversionPolicy
    {
        static void* convertible(PyObject* obj_ptr) {
            if (!PyLong_Check(obj_ptr))
                return 0;

            unsigned PY_LONG_LONG value = PyLong_AsUnsignedLongLong(obj_ptr);

            if (PyErr_Occurred()) {
                PyErr_Clear();
                return 0;
            }

            if (std::numeric_limits<T>::max() < value)
                return 0;

            return obj_ptr;
        }
    };
}


void CDPLPythonBase::registerFromPythonConverters()
{
    using namespace CDPL;

    AnyFromPyObjectConverter();

    AnyFromPythonConverter<std::string>();

    AnyFromPythonConverter<double>();
//    AnyFromPythonConverter<double, PyFloatConversionPolicy<double> >();
//    AnyFromPythonConverter<float, PyFloatConversionPolicy<float> >();

    AnyFromPythonConverter<std::uint64_t, PyLongToUIntConversionPolicy<std::uint64_t> >();
    AnyFromPythonConverter<std::int64_t, PyLongToIntConversionPolicy<std::int64_t> >();

    AnyFromPythonConverter<unsigned long, PyLongToUIntConversionPolicy<unsigned long> >();
    AnyFromPythonConverter<signed long, PyLongToIntConversionPolicy<signed long> >();

    AnyFromPythonConverter<unsigned int, PyLongToUIntConversionPolicy<unsigned int> >();
    AnyFromPythonConverter<signed int, PyLongToIntConversionPolicy<signed int> >();

    AnyFromPythonConverter<unsigned short, PyLongToUIntConversionPolicy<unsigned short> >();
    AnyFromPythonConverter<signed short, PyLongToIntConversionPolicy<signed short> >();

    AnyFromPythonConverter<unsigned char, PyLongToUIntConversionPolicy<unsigned char> >();
    AnyFromPythonConverter<signed char, PyLongToIntConversionPolicy<signed char> >();

//    AnyFromPythonConverter<unsigned long, PyIntToUIntConversionPolicy<unsigned long> >();
    AnyFromPythonConverter<signed long, PyIntToIntConversionPolicy<signed long> >();

    AnyFromPythonConverter<unsigned int, PyIntToUIntConversionPolicy<unsigned int> >();
    AnyFromPythonConverter<signed int, PyIntToIntConversionPolicy<signed int> >();

    AnyFromPythonConverter<unsigned short, PyIntToUIntConversionPolicy<unsigned short> >();
    AnyFromPythonConverter<signed short, PyIntToIntConversionPolicy<signed short> >();

    AnyFromPythonConverter<unsigned char, PyIntToUIntConversionPolicy<unsigned char> >();
    AnyFromPythonConverter<signed char, PyIntToIntConversionPolicy<signed char> >();
}

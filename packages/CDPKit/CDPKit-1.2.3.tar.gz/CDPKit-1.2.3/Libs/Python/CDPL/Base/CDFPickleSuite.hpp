/* 
 * CDFPickleSuite.hpp 
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


#ifndef CDPL_PYTHON_BASE_CDFPICKLESUITE_HPP
#define CDPL_PYTHON_BASE_CDFPICKLESUITE_HPP

#include <sstream>

#include <boost/python.hpp>
#include <boost/type_index.hpp>

#include "CDPL/Base/Exceptions.hpp"


namespace CDPLPythonBase
{

    template <typename Type, typename WriterType, typename ReaderType>
    struct CDFPickleSuite : boost::python::pickle_suite
    {

        static boost::python::tuple
        getstate(boost::python::object obj)
        {
            using namespace boost;
            using namespace CDPL;
            
            try {
                std::ostringstream os(std::ios_base::binary | std::ios_base::out);

                if (!WriterType(os).write(python::extract<const Type&>(obj)))
                    throw Base::IOError("unspecified CDF data write error");
                
                return python::make_tuple(obj.attr("__dict__"), os.str());

            } catch (const std::exception& e) {
                throw Base::IOError("CDFPickleSuite: saving state of '" + typeindex::type_id<Type>().pretty_name() +
                                    "' instance failed: " + e.what());
            }
        }

        static void
        setstate(boost::python::object obj, boost::python::tuple state)
        {
            using namespace boost;
            using namespace CDPL;

            try {
                python::extract<python::dict>(obj.attr("__dict__"))().update(state[0]);

                std::istringstream is(python::extract<std::string>(state[1]), std::ios_base::binary | std::ios_base::in);

                if (!ReaderType(is).read(python::extract<Type&>(obj)))
                    throw Base::IOError("unspecified CDF data read error");
                
            } catch (const std::exception& e) {
                throw Base::IOError("CDFPickleSuite: restoring state of '" + typeindex::type_id<Type>().pretty_name() +
                                    "' instance failed: " + e.what());
            }
        }

        static bool getstate_manages_dict() { return true; }
    };
} // namespace CDPLPythonBase

#endif // CDPL_PYTHON_BASE_CDFPICKLESUITE_HPP

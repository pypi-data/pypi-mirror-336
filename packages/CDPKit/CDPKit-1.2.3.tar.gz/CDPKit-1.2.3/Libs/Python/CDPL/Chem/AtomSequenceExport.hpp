/* 
 * AtomSequenceExport.hpp 
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


#ifndef CDPL_PYTHON_CHEM_ATOMSEQUENCEEXPORT_HPP
#define CDPL_PYTHON_CHEM_ATOMSEQUENCEEXPORT_HPP

#include <boost/python.hpp>


namespace
{

    template <typename T>
    struct AtomSequence
    {

        AtomSequence(T& cntnr):
            container(cntnr) {}

        std::size_t getNumAtoms() const
        {
            return container.getNumAtoms();
        }

        const CDPL::Chem::Atom& getAtom(std::size_t idx) const
        {
            return container.getAtom(idx);
        }

        bool containsAtom(CDPL::Chem::Atom& atom) const
        {
            return container.containsAtom(atom);
        }

        T& container;
    };

    template <typename T>
    AtomSequence<T> createAtomSequence(T& cntnr)
    {
        return AtomSequence<T>(cntnr);
    }

    template <typename T>
    struct AtomSequenceExport
    {

        AtomSequenceExport(const char* name)
        {
            using namespace boost;

            python::class_<AtomSequence<T> >(name, python::no_init)
                .def("__len__", &AtomSequence<T>::getNumAtoms, python::arg("self"))
                .def("__getitem__", &AtomSequence<T>::getAtom, (python::arg("self"), python::arg("idx")),
                     python::return_internal_reference<1>())
                .def("__contains__", &AtomSequence<T>::containsAtom, (python::arg("self"), python::arg("atom")));
        }
    };
} // namespace

#endif // CDPL_PYTHON_CHEM_ATOMSEQUENCEEXPORT_HPP

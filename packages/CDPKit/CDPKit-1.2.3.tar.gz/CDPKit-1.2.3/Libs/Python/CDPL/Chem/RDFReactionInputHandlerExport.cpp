/* 
 * RDFReactionInputHandlerExport.cpp 
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

#include "CDPL/Chem/RDFReactionInputHandler.hpp"
#include "CDPL/Chem/RDFGZReactionInputHandler.hpp"
#include "CDPL/Chem/RDFBZ2ReactionInputHandler.hpp"

#include "ClassExports.hpp"


void CDPLPythonChem::exportRDFReactionInputHandler()
{
    using namespace boost;
    using namespace CDPL;

    python::class_<Chem::RDFReactionInputHandler, 
        python::bases<Base::DataInputHandler<Chem::Reaction> > >("RDFReactionInputHandler", python::no_init)
        .def(python::init<>(python::arg("self")));

    python::class_<Chem::RDFGZReactionInputHandler, 
        python::bases<Base::DataInputHandler<Chem::Reaction> > >("RDFGZReactionInputHandler", python::no_init)
        .def(python::init<>(python::arg("self")));

    python::class_<Chem::RDFBZ2ReactionInputHandler, 
        python::bases<Base::DataInputHandler<Chem::Reaction> > >("RDFBZ2ReactionInputHandler", python::no_init)
        .def(python::init<>(python::arg("self")));
}

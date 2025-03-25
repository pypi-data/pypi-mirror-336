/* 
 * BondFunctionExport.cpp 
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

#include "CDPL/ConfGen/BondFunctions.hpp"
#include "CDPL/Chem/Bond.hpp"
#include "CDPL/Chem/MolecularGraph.hpp"

#include "FunctionExports.hpp"


namespace
{

    bool isFragmentLinkBond(CDPL::Chem::Bond& bond, const CDPL::Chem::MolecularGraph& molgraph)
    {
        return CDPL::ConfGen::isFragmentLinkBond(bond, molgraph);
    }

    bool isRotatableBond(CDPL::Chem::Bond& bond, const CDPL::Chem::MolecularGraph& molgraph, bool het_h_rotors)
    {
        return CDPL::ConfGen::isRotatableBond(bond, molgraph, het_h_rotors);
    }
}


void CDPLPythonConfGen::exportBondFunctions()
{
    using namespace boost;
    using namespace CDPL;

    python::def("isFragmentLinkBond", &isFragmentLinkBond, (python::arg("bond"), python::arg("molgraph"))); 
    python::def("isRotatableBond", &isRotatableBond, (python::arg("bond"), python::arg("molgraph"), python::arg("het_h_rotors"))); 
}

/* 
 * AtomFunctionExport.cpp 
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

#include "CDPL/Chem/Atom.hpp"
#include "CDPL/Chem/Fragment.hpp"
#include "CDPL/Biomol/AtomFunctions.hpp"

#include "FunctionExports.hpp"
#include "FunctionWrapper.hpp"


#define MAKE_ATOM_FUNC_WRAPPERS(TYPE, FUNC_SUFFIX)                 \
TYPE get##FUNC_SUFFIX##Wrapper(CDPL::Chem::Atom& atom)             \
{                                                                  \
    return CDPL::Biomol::get##FUNC_SUFFIX(atom);                   \
}                                                                  \
                                                                   \
bool has##FUNC_SUFFIX##Wrapper(CDPL::Chem::Atom& atom)             \
{                                                                  \
    return CDPL::Biomol::has##FUNC_SUFFIX(atom);                   \
}

#define EXPORT_ATOM_FUNCS(FUNC_SUFFIX, ARG_NAME)                                                             \
python::def("get"#FUNC_SUFFIX, &get##FUNC_SUFFIX##Wrapper, python::arg("atom"));                             \
python::def("has"#FUNC_SUFFIX, &has##FUNC_SUFFIX##Wrapper, python::arg("atom"));                             \
python::def("clear"#FUNC_SUFFIX, &Biomol::clear##FUNC_SUFFIX, python::arg("atom"));                          \
python::def("set"#FUNC_SUFFIX, &Biomol::set##FUNC_SUFFIX, (python::arg("atom"), python::arg(#ARG_NAME))); 

#define EXPORT_ATOM_FUNCS_COPY_REF(FUNC_SUFFIX, ARG_NAME)                                                    \
python::def("get"#FUNC_SUFFIX, &get##FUNC_SUFFIX##Wrapper, python::arg("atom"),                              \
            python::return_value_policy<python::copy_const_reference>());                                    \
python::def("has"#FUNC_SUFFIX, &has##FUNC_SUFFIX##Wrapper, python::arg("atom"));                             \
python::def("clear"#FUNC_SUFFIX, &Biomol::clear##FUNC_SUFFIX, python::arg("atom"));                          \
python::def("set"#FUNC_SUFFIX, &Biomol::set##FUNC_SUFFIX, (python::arg("atom"), python::arg(#ARG_NAME))); 


namespace
{

    MAKE_ATOM_FUNC_WRAPPERS(bool, ResidueLeavingAtomFlag)
    MAKE_ATOM_FUNC_WRAPPERS(bool, ResidueLinkingAtomFlag)
    MAKE_ATOM_FUNC_WRAPPERS(const std::string&, ResidueAtomName)
    MAKE_ATOM_FUNC_WRAPPERS(const std::string&, ResidueAltAtomName)
    MAKE_ATOM_FUNC_WRAPPERS(const std::string&, ResidueCode)
    MAKE_ATOM_FUNC_WRAPPERS(bool, HeteroAtomFlag)
    MAKE_ATOM_FUNC_WRAPPERS(long, ResidueSequenceNumber)
    MAKE_ATOM_FUNC_WRAPPERS(char, ResidueInsertionCode)
    MAKE_ATOM_FUNC_WRAPPERS(const std::string&, ChainID)
    MAKE_ATOM_FUNC_WRAPPERS(char, AltLocationID)
    MAKE_ATOM_FUNC_WRAPPERS(const std::string&, EntityID)
    MAKE_ATOM_FUNC_WRAPPERS(std::size_t, ModelNumber)
    MAKE_ATOM_FUNC_WRAPPERS(long, SerialNumber)
    MAKE_ATOM_FUNC_WRAPPERS(double, Occupancy)
    MAKE_ATOM_FUNC_WRAPPERS(double, BFactor)

    MAKE_FUNCTION_WRAPPER1(bool, isPDBBackboneAtom, CDPL::Chem::Atom&);
    MAKE_FUNCTION_WRAPPER3(bool, areInSameResidue, CDPL::Chem::Atom&, CDPL::Chem::Atom&, unsigned int);
    MAKE_FUNCTION_WRAPPER6(void, extractResidueSubstructure, CDPL::Chem::Atom&, CDPL::Chem::MolecularGraph&, CDPL::Chem::Fragment&, bool, unsigned int, bool);

    bool matchesResidueInfoWrapper1(CDPL::Chem::Atom& atom, const std::string& res_code, const std::string& chain_id, 
                                   long res_seq_no, char ins_code, std::size_t model_no, const std::string& atom_name, long serial_no) 
    {
        return CDPL::Biomol::matchesResidueInfo(atom, (res_code.empty() ? 0 : res_code.c_str()), (chain_id.empty() ? 0 : chain_id.c_str()), 
                                                res_seq_no, ins_code, model_no, (atom_name.empty() ? 0 : atom_name.c_str()), serial_no);
     }
}


void CDPLPythonBiomol::exportAtomFunctions()
{
    using namespace boost;
    using namespace CDPL;
    
    EXPORT_ATOM_FUNCS(ResidueLinkingAtomFlag, linking)
    EXPORT_ATOM_FUNCS(ResidueLeavingAtomFlag, leaving)
    EXPORT_ATOM_FUNCS_COPY_REF(ResidueAtomName, name)
    EXPORT_ATOM_FUNCS_COPY_REF(ResidueAltAtomName, name)
    EXPORT_ATOM_FUNCS_COPY_REF(ResidueCode, code)
    EXPORT_ATOM_FUNCS(ResidueSequenceNumber, seq_no)
    EXPORT_ATOM_FUNCS(ResidueInsertionCode, code)
    EXPORT_ATOM_FUNCS(HeteroAtomFlag, is_het)
    EXPORT_ATOM_FUNCS_COPY_REF(ChainID, id)
    EXPORT_ATOM_FUNCS_COPY_REF(EntityID, id)
    EXPORT_ATOM_FUNCS(AltLocationID, id)
    EXPORT_ATOM_FUNCS(ModelNumber, model_no)
    EXPORT_ATOM_FUNCS(SerialNumber, serial_no)
    EXPORT_ATOM_FUNCS(Occupancy, occupancy)
    EXPORT_ATOM_FUNCS(BFactor, factor)

    python::def("isPDBBackboneAtom", &isPDBBackboneAtomWrapper1, python::arg("atom"));
    python::def("areInSameResidue", &areInSameResidueWrapper3, 
                (python::arg("atom1"), python::arg("atom2"), python::arg("flags") = Biomol::AtomPropertyFlag::DEFAULT));
    python::def("extractResidueSubstructure", &extractResidueSubstructureWrapper6,
                (python::arg("atom"), python::arg("molgraph"), python::arg("res_substruct"), 
                 python::arg("cnctd_only") = false, python::arg("flags") = Biomol::AtomPropertyFlag::DEFAULT, python::arg("append") = false));
     python::def("matchesResidueInfo", &matchesResidueInfoWrapper1, 
                (python::arg("atom"), python::arg("res_code") = "", python::arg("chain_id") = "", 
                 python::arg("res_seq_no") = Biomol::IGNORE_SEQUENCE_NO, python::arg("ins_code") = char(0), python::arg("model_no") = 0, 
                 python::arg("atom_name") = "", python::arg("serial_no") = Biomol::IGNORE_SERIAL_NO));
}

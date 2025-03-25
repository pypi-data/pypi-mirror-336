/* 
 * ReactionFunctionExport.cpp 
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

#include "CDPL/Chem/Reaction.hpp"
#include "CDPL/Chem/ReactionFunctions.hpp"

#include "FunctionExports.hpp"
#include "FunctionWrapper.hpp"


#define MAKE_REACTION_FUNC_WRAPPERS(TYPE, FUNC_SUFFIX)      \
TYPE get##FUNC_SUFFIX##Wrapper(CDPL::Chem::Reaction& rxn)   \
{                                                           \
    return get##FUNC_SUFFIX(rxn);                           \
}                                                           \
                                                            \
bool has##FUNC_SUFFIX##Wrapper(CDPL::Chem::Reaction& rxn)   \
{                                                           \
    return has##FUNC_SUFFIX(rxn);                           \
}

#define EXPORT_REACTION_FUNCS(FUNC_SUFFIX, ARG_NAME)                                                        \
python::def("get"#FUNC_SUFFIX, &get##FUNC_SUFFIX##Wrapper, python::arg("rxn"));                             \
python::def("has"#FUNC_SUFFIX, &has##FUNC_SUFFIX##Wrapper, python::arg("rxn"));                             \
python::def("clear"#FUNC_SUFFIX, &Chem::clear##FUNC_SUFFIX, python::arg("rxn"));                            \
python::def("set"#FUNC_SUFFIX, &Chem::set##FUNC_SUFFIX, (python::arg("rxn"), python::arg(#ARG_NAME))); 

#define EXPORT_REACTION_FUNCS_COPY_REF(FUNC_SUFFIX, ARG_NAME)                                               \
python::def("get"#FUNC_SUFFIX, &get##FUNC_SUFFIX##Wrapper, python::arg("rxn"),                              \
            python::return_value_policy<python::copy_const_reference>());                                   \
python::def("has"#FUNC_SUFFIX, &has##FUNC_SUFFIX##Wrapper, python::arg("rxn"));                             \
python::def("clear"#FUNC_SUFFIX, &Chem::clear##FUNC_SUFFIX, python::arg("rxn"));                            \
python::def("set"#FUNC_SUFFIX, &Chem::set##FUNC_SUFFIX, (python::arg("rxn"), python::arg(#ARG_NAME))); 

#define EXPORT_REACTION_FUNCS_COPY_REF_CW(FUNC_SUFFIX, ARG_NAME)                                            \
python::def("get"#FUNC_SUFFIX, &get##FUNC_SUFFIX##Wrapper, python::arg("rxn"),                              \
            python::return_value_policy<python::copy_const_reference,                                       \
            python::with_custodian_and_ward_postcall<0, 1> >());                                            \
python::def("has"#FUNC_SUFFIX, &has##FUNC_SUFFIX##Wrapper, python::arg("rxn"));                             \
python::def("clear"#FUNC_SUFFIX, &Chem::clear##FUNC_SUFFIX, python::arg("rxn"));                            \
python::def("set"#FUNC_SUFFIX, &Chem::set##FUNC_SUFFIX, (python::arg("rxn"), python::arg(#ARG_NAME)));


namespace
{

    MAKE_REACTION_FUNC_WRAPPERS(const std::string&, Name)
    MAKE_REACTION_FUNC_WRAPPERS(const std::string&, Comment)
    MAKE_REACTION_FUNC_WRAPPERS(std::time_t, Timestamp)
    MAKE_REACTION_FUNC_WRAPPERS(const std::string&, MDLUserInitials)
    MAKE_REACTION_FUNC_WRAPPERS(const std::string&, MDLProgramName)
    MAKE_REACTION_FUNC_WRAPPERS(std::size_t, MDLRegistryNumber)
    MAKE_REACTION_FUNC_WRAPPERS(const CDPL::Chem::StringDataBlock::SharedPointer&, ReactionData)
    MAKE_REACTION_FUNC_WRAPPERS(const CDPL::Chem::Molecule::SharedPointer&, MDLMoleculeRecord)
    MAKE_REACTION_FUNC_WRAPPERS(const std::string&, MDLInternalRegistryNumber)
    MAKE_REACTION_FUNC_WRAPPERS(const std::string&, MDLExternalRegistryNumber)
    MAKE_REACTION_FUNC_WRAPPERS(unsigned int, MDLRXNFileVersion)
    MAKE_REACTION_FUNC_WRAPPERS(const CDPL::Chem::MatchExpression<CDPL::Chem::Reaction>::SharedPointer&, MatchExpression)
    MAKE_REACTION_FUNC_WRAPPERS(const CDPL::Chem::FragmentList::SharedPointer&, ComponentGroups)
    MAKE_REACTION_FUNC_WRAPPERS(const CDPL::Chem::AtomMapping::SharedPointer&, AtomMapping)

    boost::python::object generateSMILESWrapper(CDPL::Chem::Reaction& rxn, bool canonical, bool ord_h_deplete,
                                                unsigned int atom_flags, unsigned int bond_flags)
    {
        std::string smiles;

        if (!generateSMILES(rxn, smiles, canonical, ord_h_deplete, atom_flags, bond_flags))
            return boost::python::object();

        return boost::python::str(smiles.c_str());
    } 
}


void CDPLPythonChem::exportReactionFunctions()
{
    using namespace boost;
    using namespace CDPL;

    python::def("setAtomMatchConstraints", &Chem::setAtomMatchConstraints, (python::arg("rxn"), python::arg("constr"), python::arg("overwrite")));
    python::def("setBondMatchConstraints", &Chem::setBondMatchConstraints, (python::arg("rxn"), python::arg("constr"), python::arg("overwrite")));
    python::def("setComponentMatchConstraints", &Chem::setComponentMatchConstraints, (python::arg("rxn"), python::arg("constr"), python::arg("overwrite")));
    python::def("generateMatchExpressions", &Chem::generateMatchExpressions, (python::arg("rxn"), python::arg("overwrite")));
    python::def("initSubstructureSearchQuery", &Chem::initSubstructureSearchQuery, (python::arg("rxn"), python::arg("overwrite")));
    python::def("initSubstructureSearchTarget", &Chem::initSubstructureSearchTarget, (python::arg("rxn"), python::arg("overwrite")));
    
    python::def("getMatchConstraints", &Chem::getMatchConstraints, python::arg("rxn"), 
                python::return_value_policy<python::copy_const_reference, python::with_custodian_and_ward_postcall<0, 1> >());
    python::def("hasMatchConstraints", &Chem::hasMatchConstraints, python::arg("rxn"));
    python::def("setMatchConstraints", &Chem::setMatchConstraints, (python::arg("rxn"), python::arg("constr")));
    python::def("clearMatchConstraints", &Chem::clearMatchConstraints, python::arg("rxn"));

    python::def("generateMatchExpression", static_cast<Chem::MatchExpression<Chem::Reaction>::SharedPointer (*)(const Chem::Reaction&)>(&Chem::generateMatchExpression),
                python::arg("rxn"), python::with_custodian_and_ward_postcall<0, 1>());
    python::def("perceiveAtomMapping", static_cast<Chem::AtomMapping::SharedPointer (*)(const Chem::Reaction&)>(&Chem::perceiveAtomMapping),
                python::arg("rxn"), python::with_custodian_and_ward_postcall<0, 1>());
    python::def("perceiveComponentGroups", static_cast<Chem::FragmentList::SharedPointer (*)(const Chem::Reaction&)>(&Chem::perceiveComponentGroups),
                python::arg("rxn"), python::with_custodian_and_ward_postcall<0, 1>());

    python::def("generateMatchExpression", static_cast<Chem::MatchExpression<Chem::Reaction>::SharedPointer (*)(Chem::Reaction&, bool)>(&Chem::generateMatchExpression),
                (python::arg("rxn"), python::arg("overwrite")), python::with_custodian_and_ward_postcall<0, 1>());
    python::def("perceiveAtomMapping", static_cast<Chem::AtomMapping::SharedPointer (*)(Chem::Reaction&, bool)>(&Chem::perceiveAtomMapping),
                (python::arg("rxn"), python::arg("overwrite")), python::with_custodian_and_ward_postcall<0, 1>());
    python::def("perceiveComponentGroups", static_cast<Chem::FragmentList::SharedPointer (*)(Chem::Reaction&, bool)>(&Chem::perceiveComponentGroups),
                (python::arg("rxn"), python::arg("overwrite")), python::with_custodian_and_ward_postcall<0, 1>());

    python::def("generateSMILES", &generateSMILESWrapper, (python::arg("rxn"), python::arg("canonical") = false, 
                                                           python::arg("ord_h_deplete") = true, python::arg("atom_flags") = Chem::AtomPropertyFlag::DEFAULT, 
                                                           python::arg("bond_flags") = Chem::BondPropertyFlag::DEFAULT));

    python::def("calcHashCode", &Chem::calcHashCode, (python::arg("rxn"), python::arg("role_mask") = Chem::ReactionRole::ALL, 
                                                      python::arg("atom_flags") = Chem::AtomPropertyFlag::DEFAULT,
                                                      python::arg("bond_flags") = Chem::BondPropertyFlag::DEFAULT, 
                                                      python::arg("ord_h_deplete") = true));

    python::def("getMaxComponentGroupID", &Chem::getMaxComponentGroupID, python::arg("rxn"));
    python::def("getMaxAtomMappingID", &Chem::getMaxAtomMappingID, python::arg("rxn"));

    python::def("calcBasicProperties", &Chem::calcBasicProperties,
                (python::arg("rxn"), python::arg("overwrite")));

    EXPORT_REACTION_FUNCS_COPY_REF_CW(MatchExpression, expr)
    EXPORT_REACTION_FUNCS_COPY_REF_CW(ComponentGroups, comp_groups)
    EXPORT_REACTION_FUNCS_COPY_REF_CW(AtomMapping, mapping)
    EXPORT_REACTION_FUNCS_COPY_REF(Name, name)
    EXPORT_REACTION_FUNCS_COPY_REF(Comment, comment)
    EXPORT_REACTION_FUNCS(Timestamp, time)
    EXPORT_REACTION_FUNCS_COPY_REF(MDLUserInitials, initials)
    EXPORT_REACTION_FUNCS_COPY_REF(MDLProgramName, name)
    EXPORT_REACTION_FUNCS(MDLRegistryNumber, reg_no)
    EXPORT_REACTION_FUNCS_COPY_REF(ReactionData, data)
    EXPORT_REACTION_FUNCS_COPY_REF(MDLMoleculeRecord, mol_rec)
    EXPORT_REACTION_FUNCS_COPY_REF(MDLInternalRegistryNumber, reg_no)
    EXPORT_REACTION_FUNCS_COPY_REF(MDLExternalRegistryNumber, reg_no)
    EXPORT_REACTION_FUNCS(MDLRXNFileVersion, version)
}

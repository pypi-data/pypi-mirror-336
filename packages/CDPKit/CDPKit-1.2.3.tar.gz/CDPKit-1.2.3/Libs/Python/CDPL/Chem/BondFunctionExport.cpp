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

#include "CDPL/Chem/Bond.hpp"
#include "CDPL/Chem/BondFunctions.hpp"
#include "CDPL/Chem/StereoDescriptor.hpp"

#include "FunctionExports.hpp"
#include "FunctionWrapper.hpp"


#define MAKE_BOND_FUNC_WRAPPERS(TYPE, FUNC_SUFFIX)                 \
TYPE get##FUNC_SUFFIX##Wrapper(CDPL::Chem::Bond& bond)             \
{                                                                  \
    return get##FUNC_SUFFIX(bond);                                 \
}                                                                  \
                                                                   \
bool has##FUNC_SUFFIX##Wrapper(CDPL::Chem::Bond& bond)             \
{                                                                  \
    return has##FUNC_SUFFIX(bond);                                 \
}

#define EXPORT_BOND_FUNCS(FUNC_SUFFIX, ARG_NAME)                                                             \
python::def("get"#FUNC_SUFFIX, &get##FUNC_SUFFIX##Wrapper, python::arg("bond"));                             \
python::def("has"#FUNC_SUFFIX, &has##FUNC_SUFFIX##Wrapper, python::arg("bond"));                             \
python::def("clear"#FUNC_SUFFIX, &Chem::clear##FUNC_SUFFIX, python::arg("bond"));                            \
python::def("set"#FUNC_SUFFIX, &Chem::set##FUNC_SUFFIX, (python::arg("bond"), python::arg(#ARG_NAME))); 

#define EXPORT_BOND_FUNCS_COPY_REF(FUNC_SUFFIX, ARG_NAME)                                                    \
python::def("get"#FUNC_SUFFIX, &get##FUNC_SUFFIX##Wrapper, python::arg("bond"),                              \
            python::return_value_policy<python::copy_const_reference>());                                    \
python::def("has"#FUNC_SUFFIX, &has##FUNC_SUFFIX##Wrapper, python::arg("bond"));                             \
python::def("clear"#FUNC_SUFFIX, &Chem::clear##FUNC_SUFFIX, python::arg("bond"));                            \
python::def("set"#FUNC_SUFFIX, &Chem::set##FUNC_SUFFIX, (python::arg("bond"), python::arg(#ARG_NAME))); 

#define EXPORT_BOND_FUNCS_COPY_REF_CW(FUNC_SUFFIX, ARG_NAME)                                                 \
python::def("get"#FUNC_SUFFIX, &get##FUNC_SUFFIX##Wrapper, python::arg("bond"),                              \
            python::return_value_policy<python::copy_const_reference,                                        \
            python::with_custodian_and_ward_postcall<0, 1> >());                                             \
python::def("has"#FUNC_SUFFIX, &has##FUNC_SUFFIX##Wrapper, python::arg("bond"));                             \
python::def("clear"#FUNC_SUFFIX, &Chem::clear##FUNC_SUFFIX, python::arg("bond"));                            \
python::def("set"#FUNC_SUFFIX, &Chem::set##FUNC_SUFFIX, (python::arg("bond"), python::arg(#ARG_NAME)));

#define EXPORT_BOND_FUNCS_INT_REF(FUNC_SUFFIX, ARG_NAME)                                                     \
python::def("get"#FUNC_SUFFIX, &get##FUNC_SUFFIX##Wrapper, python::arg("bond"),                              \
            python::return_internal_reference<1>());                                                         \
python::def("has"#FUNC_SUFFIX, &has##FUNC_SUFFIX##Wrapper, python::arg("bond"));                             \
python::def("clear"#FUNC_SUFFIX, &Chem::clear##FUNC_SUFFIX, python::arg("bond"));                            \
python::def("set"#FUNC_SUFFIX, &Chem::set##FUNC_SUFFIX, (python::arg("bond"), python::arg(#ARG_NAME)));


namespace
{

    typedef CDPL::Chem::MatchExpression<CDPL::Chem::Bond, CDPL::Chem::MolecularGraph>::SharedPointer MatchExpressionPtr;
    typedef const MatchExpressionPtr& MatchExpressionPtrRef;

    MAKE_BOND_FUNC_WRAPPERS(const std::string&, MatchExpressionString)
    MAKE_BOND_FUNC_WRAPPERS(std::size_t, Order)
    MAKE_BOND_FUNC_WRAPPERS(bool, AromaticityFlag)
    MAKE_BOND_FUNC_WRAPPERS(bool, RingFlag)
    MAKE_BOND_FUNC_WRAPPERS(unsigned int, CIPConfiguration)
    MAKE_BOND_FUNC_WRAPPERS(unsigned int, SybylType)
    MAKE_BOND_FUNC_WRAPPERS(bool, StereoCenterFlag)
    MAKE_BOND_FUNC_WRAPPERS(const CDPL::Chem::StereoDescriptor&, StereoDescriptor)
    MAKE_BOND_FUNC_WRAPPERS(MatchExpressionPtrRef, MatchExpression)
    MAKE_BOND_FUNC_WRAPPERS(unsigned int, ReactionCenterStatus)
    MAKE_BOND_FUNC_WRAPPERS(unsigned int, Direction)
    MAKE_BOND_FUNC_WRAPPERS(unsigned int, 2DStereoFlag)

    MAKE_FUNCTION_WRAPPER1(const CDPL::Chem::MatchConstraintList::SharedPointer&, getMatchConstraints, CDPL::Chem::Bond&)
    MAKE_FUNCTION_WRAPPER1(bool, hasMatchConstraints, CDPL::Chem::Bond&)

    MAKE_FUNCTION_WRAPPER2(std::size_t, getSizeOfSmallestContainingFragment, CDPL::Chem::Bond&, CDPL::Chem::FragmentList&);
    MAKE_FUNCTION_WRAPPER2(std::size_t, getSizeOfLargestContainingFragment, CDPL::Chem::Bond&, CDPL::Chem::FragmentList&);
    MAKE_FUNCTION_WRAPPER2(std::size_t, getNumContainingFragments, CDPL::Chem::Bond&, CDPL::Chem::FragmentList&);
    MAKE_FUNCTION_WRAPPER2(MatchExpressionPtr, generateMatchExpression, CDPL::Chem::Bond&, CDPL::Chem::MolecularGraph&);
    MAKE_FUNCTION_WRAPPER2(unsigned int, perceiveSybylType, CDPL::Chem::Bond&, CDPL::Chem::MolecularGraph&);

    MAKE_FUNCTION_WRAPPER3(CDPL::Chem::StereoDescriptor, calcStereoDescriptor, CDPL::Chem::Bond&, CDPL::Chem::MolecularGraph&, std::size_t);
    MAKE_FUNCTION_WRAPPER3(void, getContainingFragments, CDPL::Chem::Bond&, CDPL::Chem::FragmentList&, CDPL::Chem::FragmentList&);
    MAKE_FUNCTION_WRAPPER3(bool, isInFragmentOfSize, CDPL::Chem::Bond&, CDPL::Chem::FragmentList&, std::size_t);

    MAKE_FUNCTION_WRAPPER4(unsigned int, calcConfiguration, CDPL::Chem::Bond&, CDPL::Chem::MolecularGraph&, const CDPL::Chem::StereoDescriptor&, const CDPL::Math::Vector3DArray&);

    MAKE_FUNCTION_WRAPPER6(bool, isStereoCenter, CDPL::Chem::Bond&, CDPL::Chem::MolecularGraph&, bool, bool, bool, std::size_t);
    
    std::string generateMatchExpressionStringWrapper(CDPL::Chem::Bond& bond, CDPL::Chem::MolecularGraph& molgraph)
    {
        std::string str;

        generateMatchExpressionString(bond, molgraph, str);
        return str;
    }
}


void CDPLPythonChem::exportBondFunctions()
{
    using namespace boost;
    using namespace CDPL;

    python::def("getSizeOfSmallestContainingFragment", &getSizeOfSmallestContainingFragmentWrapper2,
                (python::arg("bond"), python::arg("frag_list")));
    python::def("getSizeOfLargestContainingFragment", &getSizeOfLargestContainingFragmentWrapper2,
                (python::arg("bond"), python::arg("frag_list")));
    python::def("getNumContainingFragments", &getNumContainingFragmentsWrapper2,
                (python::arg("bond"), python::arg("frag_list")));
    python::def("generateMatchExpression", &generateMatchExpressionWrapper2, 
                (python::arg("bond"), python::arg("molgraph")),
                python::with_custodian_and_ward_postcall<0, 1>());

    python::def("perceiveSybylType", &perceiveSybylTypeWrapper2,
                (python::arg("bond"), python::arg("molgraph")));

    python::def("getContainingFragments", &getContainingFragmentsWrapper3,
                (python::arg("bond"), python::arg("frag_list"), python::arg("cont_frag_list")),
                python::with_custodian_and_ward<3, 2>());
    python::def("isInFragmentOfSize", &isInFragmentOfSizeWrapper3, 
                (python::arg("bond"), python::arg("frag_list"), python::arg("size")));

    python::def("isStereoCenter", &isStereoCenterWrapper6, 
                (python::arg("bond"), python::arg("molgraph"), python::arg("check_asym") = true,
                 python::arg("check_term_n") = true, python::arg("check_order") = true, python::arg("min_ring_size") = 8));
    python::def("calcConfiguration", &calcConfigurationWrapper4,
                (python::arg("bond"), python::arg("molgraph"), python::arg("descr"), python::arg("coords")));

    python::def("calcStereoDescriptor", &calcStereoDescriptorWrapper3, 
                (python::arg("bond"), python::arg("molgraph"), python::arg("dim") = 1));

    python::def("generateMatchExpressionString", &generateMatchExpressionStringWrapper,
                (python::arg("bond"), python::arg("molgraph")));

    python::def("getMatchConstraints", &getMatchConstraintsWrapper1, python::arg("bond"),
                python::return_value_policy<python::copy_const_reference, python::with_custodian_and_ward_postcall<0, 1> >());
    python::def("hasMatchConstraints", &hasMatchConstraintsWrapper1, python::arg("bond"));
    python::def("setMatchConstraints", &Chem::setMatchConstraints, 
                (python::arg("bond"), python::arg("constr")));
    python::def("clearMatchConstraints", &Chem::clearMatchConstraints, python::arg("bond"));

    EXPORT_BOND_FUNCS_COPY_REF(MatchExpressionString, expr_str)
    EXPORT_BOND_FUNCS(Order, order)
    EXPORT_BOND_FUNCS(AromaticityFlag, aromatic)
    EXPORT_BOND_FUNCS(RingFlag, in_ring)
    EXPORT_BOND_FUNCS(CIPConfiguration, config)
    EXPORT_BOND_FUNCS(SybylType, type)
    EXPORT_BOND_FUNCS(StereoCenterFlag, is_center)
    EXPORT_BOND_FUNCS(Direction, dir)
    EXPORT_BOND_FUNCS_INT_REF(StereoDescriptor, descr)
    EXPORT_BOND_FUNCS_COPY_REF_CW(MatchExpression, expr)
    EXPORT_BOND_FUNCS(ReactionCenterStatus, status)
    EXPORT_BOND_FUNCS(2DStereoFlag, flag)
}

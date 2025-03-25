/* 
 * PharmacophoreFunctionExport.cpp 
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

#include "CDPL/Pharm/PharmacophoreFunctions.hpp"
#include "CDPL/Pharm/Pharmacophore.hpp"
#include "CDPL/Pharm/FeatureMapping.hpp"
#include "CDPL/Chem/AtomContainer.hpp"

#include "FunctionExports.hpp"
#include "FunctionWrapper.hpp"


namespace
{

    MAKE_FUNCTION_WRAPPER7(void, createExclusionVolumes, CDPL::Pharm::Pharmacophore&,
                           CDPL::Chem::AtomContainer&, const CDPL::Chem::Atom3DCoordinatesFunction&,
                           double, double, bool, bool);

    MAKE_FUNCTION_WRAPPER6(void, createExclusionVolumes, CDPL::Pharm::Pharmacophore&,
                           CDPL::Pharm::FeatureContainer&, double, double, bool, bool);

    MAKE_FUNCTION_WRAPPER4(bool, removeExclusionVolumesWithClashes, CDPL::Pharm::Pharmacophore&,
                           CDPL::Chem::AtomContainer&, const CDPL::Chem::Atom3DCoordinatesFunction&, double);
    MAKE_FUNCTION_WRAPPER4(bool, resizeExclusionVolumesWithClashes, CDPL::Pharm::Pharmacophore&,
                           CDPL::Chem::AtomContainer&, const CDPL::Chem::Atom3DCoordinatesFunction&, double);

    MAKE_FUNCTION_WRAPPER2(bool, removePositionalDuplicates, CDPL::Pharm::Pharmacophore&, double);
    MAKE_FUNCTION_WRAPPER2(bool, removeFeaturesWithType, CDPL::Pharm::Pharmacophore&, unsigned int);
}


void CDPLPythonPharm::exportPharmacophoreFunctions()
{
    using namespace boost;
    using namespace CDPL;
    
    python::def("generateInteractionPharmacophore", &Pharm::generateInteractionPharmacophore, 
                (python::arg("pharm"), python::arg("iactions"), python::arg("append") = false));
    python::def("createExclusionVolumes", &createExclusionVolumesWrapper7,
                (python::arg("pharm"), python::arg("cntnr"), python::arg("coords_func"), 
                 python::arg("tol") = 0.0, python::arg("min_dist") = 0.0, python::arg("rel_dist") = true, 
                 python::arg("append") = true));
    python::def("createExclusionVolumes", &createExclusionVolumesWrapper6,
                (python::arg("pharm"), python::arg("cntnr"), python::arg("tol") = 0.0, 
                 python::arg("min_dist") = 0.0, python::arg("rel_dist") = true, 
                 python::arg("append") = true));
    python::def("removeExclusionVolumesWithClashes", &removeExclusionVolumesWithClashesWrapper4,
                (python::arg("pharm"), python::arg("cntnr"), python::arg("coords_func"), python::arg("vdw_scaling_fact") = 1.0));
    python::def("resizeExclusionVolumesWithClashes", &resizeExclusionVolumesWithClashesWrapper4,
                (python::arg("pharm"), python::arg("cntnr"), python::arg("coords_func"), python::arg("vdw_scaling_fact") = 1.0));
    python::def("removePositionalDuplicates", &removePositionalDuplicatesWrapper2,
                (python::arg("pharm"), python::arg("pos_tol") = 0.0));
    python::def("removeFeaturesWithType", &removeFeaturesWithTypeWrapper2,
                (python::arg("pharm"), python::arg("type")));
}

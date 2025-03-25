/* 
 * SimilarityFunctionExport.cpp 
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

#include "CDPL/Descr/SimilarityFunctions.hpp"
#include "CDPL/Math/Vector.hpp"

#include "FunctionExports.hpp"


void CDPLPythonDescr::exportSimilarityFunctions()
{
    using namespace boost;
    using namespace CDPL;

    python::def("calcTanimotoSimilarity", static_cast<double(*)(const Util::BitSet&, const Util::BitSet&)>
                (&Descr::calcTanimotoSimilarity), (python::arg("bs1"), python::arg("bs2")));
    python::def("calcTanimotoSimilarity", &Descr::calcTanimotoSimilarity<Math::FVector>, (python::arg("v1"), python::arg("v2")));
    python::def("calcTanimotoSimilarity", &Descr::calcTanimotoSimilarity<Math::DVector>, (python::arg("v1"), python::arg("v2")));
    python::def("calcTanimotoSimilarity", &Descr::calcTanimotoSimilarity<Math::LVector>, (python::arg("v1"), python::arg("v2")));
    python::def("calcTanimotoSimilarity", &Descr::calcTanimotoSimilarity<Math::ULVector>, (python::arg("v1"), python::arg("v2")));
    
    python::def("calcCosineSimilarity", static_cast<double(*)(const Util::BitSet&, const Util::BitSet&)>
                (&Descr::calcCosineSimilarity), (python::arg("bs1"), python::arg("bs2")));
    python::def("calcCosineSimilarity", &Descr::calcCosineSimilarity<Math::FVector>, (python::arg("v1"), python::arg("v2")));
    python::def("calcCosineSimilarity", &Descr::calcCosineSimilarity<Math::DVector>, (python::arg("v1"), python::arg("v2")));
    python::def("calcCosineSimilarity", &Descr::calcCosineSimilarity<Math::LVector>, (python::arg("v1"), python::arg("v2")));
    python::def("calcCosineSimilarity", &Descr::calcCosineSimilarity<Math::ULVector>, (python::arg("v1"), python::arg("v2")));
    
    python::def("calcEuclideanSimilarity", &Descr::calcEuclideanSimilarity, (python::arg("bs1"), python::arg("bs2")));
    python::def("calcDiceSimilarity", &Descr::calcDiceSimilarity, (python::arg("bs1"), python::arg("bs2")));
    python::def("calcManhattanSimilarity", &Descr::calcManhattanSimilarity, (python::arg("bs1"), python::arg("bs2")));
    python::def("calcTverskySimilarity", &Descr::calcTverskySimilarity,
                (python::arg("bs1"), python::arg("bs2"), python::arg("a"), (python::arg("b"))));
    
    python::def("calcHammingDistance", &Descr::calcHammingDistance, (python::arg("bs1"), python::arg("bs2")));
    python::def("calcManhattanDistance", &Descr::calcManhattanDistance<Math::FVector>, (python::arg("v1"), python::arg("v2")));
    python::def("calcManhattanDistance", &Descr::calcManhattanDistance<Math::DVector>, (python::arg("v1"), python::arg("v2")));
    python::def("calcManhattanDistance", &Descr::calcManhattanDistance<Math::LVector>, (python::arg("v1"), python::arg("v2")));
    python::def("calcManhattanDistance", &Descr::calcManhattanDistance<Math::ULVector>, (python::arg("v1"), python::arg("v2")));

    python::def("calcEuclideanDistance", static_cast<double(*)(const Util::BitSet&, const Util::BitSet&)>
                (&Descr::calcEuclideanDistance), (python::arg("bs1"), python::arg("bs2")));
    python::def("calcEuclideanDistance", &Descr::calcEuclideanDistance<Math::FVector>, (python::arg("v1"), python::arg("v2")));
    python::def("calcEuclideanDistance", &Descr::calcEuclideanDistance<Math::DVector>, (python::arg("v1"), python::arg("v2")));
    python::def("calcEuclideanDistance", &Descr::calcEuclideanDistance<Math::LVector>, (python::arg("v1"), python::arg("v2")));
    python::def("calcEuclideanDistance", &Descr::calcEuclideanDistance<Math::ULVector>, (python::arg("v1"), python::arg("v2")));
}

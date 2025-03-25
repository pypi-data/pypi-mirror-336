/* 
 * ControlParameterDefault.hpp 
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

/**
 * \file
 * \brief Definition of constants in namespace CDPL::Biomol::ControlParameterDefault.
 */

#ifndef CDPL_BIOMOL_CONTROLPARAMETERDEFAULT_HPP
#define CDPL_BIOMOL_CONTROLPARAMETERDEFAULT_HPP

#include <cstddef>

#include "CDPL/Biomol/APIPrefix.hpp"
#include "CDPL/Biomol/ResidueDictionary.hpp"
#include "CDPL/Biomol/MMCIFDataProcessingFunction.hpp"


namespace CDPL
{

    namespace Biomol
    {

        /**
         * \brief Provides default values for built-in control-parameters.
         */
        namespace ControlParameterDefault
        {

            /**
             * \brief Default setting (= \c false) for the control-parameter Biomol::ControlParameter::STRICT_ERROR_CHECKING.
             */
            extern CDPL_BIOMOL_API const bool STRICT_ERROR_CHECKING;

            /**
             * \brief Default setting (= \c false) for the control-parameter Biomol::ControlParameter::CHECK_LINE_LENGTH.
             */
            extern CDPL_BIOMOL_API const bool CHECK_LINE_LENGTH;

            /**
             * \since 1.2
             */
            extern CDPL_BIOMOL_API const ResidueDictionary::SharedPointer RESIDUE_DICTIONARY;

            /**
             * \since 1.2
             */
            extern CDPL_BIOMOL_API const bool APPLY_DICT_FORMAL_CHARGES;

            /**
             * \since 1.2
             */
            extern CDPL_BIOMOL_API const bool APPLY_DICT_ATOM_TYPES;

            /**
             * \since 1.2
             */
            extern CDPL_BIOMOL_API const bool CALC_MISSING_FORMAL_CHARGES;

            /**
             * \since 1.2
             */
            extern CDPL_BIOMOL_API const bool PERCEIVE_MISSING_BOND_ORDERS;

            extern CDPL_BIOMOL_API const bool COMBINE_INTERFERING_RESIDUE_COORDINATES;
            
            extern CDPL_BIOMOL_API const bool PDB_APPLY_DICT_ATOM_BONDING_TO_NON_STD_RESIDUES;

            extern CDPL_BIOMOL_API const bool PDB_APPLY_DICT_ATOM_BONDING_TO_STD_RESIDUES;

            extern CDPL_BIOMOL_API const bool PDB_APPLY_DICT_BOND_ORDERS_TO_NON_STD_RESIDUES;

            extern CDPL_BIOMOL_API const bool PDB_APPLY_DICT_BOND_ORDERS_TO_STD_RESIDUES;

            extern CDPL_BIOMOL_API const bool PDB_IGNORE_CONECT_RECORDS;

            extern CDPL_BIOMOL_API const bool PDB_DEDUCE_BOND_ORDERS_FROM_CONECT_RECORDS;

            extern CDPL_BIOMOL_API const bool PDB_IGNORE_FORMAL_CHARGE_FIELD;
    
            extern CDPL_BIOMOL_API const bool PDB_EVALUATE_MASTER_RECORD;

            extern CDPL_BIOMOL_API const bool PDB_TRUNCATE_LINES;

            /**
             * \since 1.2
             */
            extern CDPL_BIOMOL_API const bool PDB_OUTPUT_FORMAL_CHARGES;

            /**
             * \since 1.2
             */
            extern CDPL_BIOMOL_API const bool PDB_OUTPUT_CONECT_RECORDS;

            /**
             * \since 1.2
             */
            extern CDPL_BIOMOL_API const bool PDB_OUTPUT_CONECT_RECORDS_FOR_ALL_BONDS;

            /**
             * \since 1.2
             */
            extern CDPL_BIOMOL_API const bool PDB_OUTPUT_CONECT_RECORDS_REFLECTING_BOND_ORDER;

            extern CDPL_BIOMOL_API const unsigned int PDB_FORMAT_VERSION;

            /**
             * \since 1.2
             */
            extern CDPL_BIOMOL_API const bool MMCIF_APPLY_DICT_ATOM_BONDING;

            /**
             * \since 1.2
             */
            extern CDPL_BIOMOL_API const bool MMCIF_APPLY_DICT_BOND_ORDERS;

            /**
             * \since 1.2
             */
            extern CDPL_BIOMOL_API const bool MMCIF_OUTPUT_BIOPOLYMERS_AS_CHEM_COMP;

            /**
             * \since 1.2
             */
            extern CDPL_BIOMOL_API const MMCIFDataProcessingFunction MMCIF_OUTPUT_DATA_POSTPROC_FUNCTION;
            
        } // namespace ControlParameterDefault
    } // namespace Biomol
} // namespace CDPL

#endif // CDPL_BIOMOL_CONTROLPARAMETERDEFAULT_HPP

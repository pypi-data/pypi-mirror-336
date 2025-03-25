/* 
 * PSDScreeningDBCreatorImpl.hpp 
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


#ifndef CDPL_PHARM_PSDSCREENINGDBCREATORIMPL_HPP
#define CDPL_PHARM_PSDSCREENINGDBCREATORIMPL_HPP

#include <unordered_map>
#include <unordered_set>

#include "CDPL/Pharm/SQLiteDataIOBase.hpp"
#include "CDPL/Pharm/ScreeningDBCreator.hpp"
#include "CDPL/Pharm/BasicPharmacophore.hpp"
#include "CDPL/Pharm/DefaultPharmacophoreGenerator.hpp"
#include "CDPL/Pharm/FeatureTypeHistogram.hpp"
#include "CDPL/Chem/HashCodeCalculator.hpp"
#include "CDPL/Math/VectorArray.hpp"
#include "CDPL/Internal/ByteBuffer.hpp"

#include "PSDFeatureContainerByteBufferWriter.hpp"
#include "PSDMolecularGraphByteBufferWriter.hpp"


namespace CDPL
{

    namespace Pharm
    {

        class ScreeningDBAccessor;

        class PSDScreeningDBCreatorImpl : private SQLiteDataIOBase
        {

          public:
            PSDScreeningDBCreatorImpl();

            ~PSDScreeningDBCreatorImpl();
            
            void open(const std::string& name, ScreeningDBCreator::Mode mode = ScreeningDBCreator::CREATE, bool allow_dup_entries = true);

            void close();

            const std::string& getDatabaseName() const;

            ScreeningDBCreator::Mode getMode() const;

            bool allowDuplicateEntries() const;

            bool process(const Chem::MolecularGraph& molgraph);

            bool merge(const ScreeningDBAccessor& db_acc, const ScreeningDBCreator::ProgressCallbackFunction& func);

            std::size_t getNumProcessed() const;

            std::size_t getNumRejected() const;

            std::size_t getNumDeleted() const;

            std::size_t getNumInserted() const;

          private:
            void setupTables();

            void loadMolHashToIDMap();

            std::size_t deleteEntries(std::uint64_t mol_hash);

            std::int64_t insertMolecule(const Chem::MolecularGraph& molgraph, std::uint64_t mol_hash);

            void genAndInsertPharmData(const Chem::MolecularGraph& molgraph, std::int64_t mol_id);
            void genAndInsertPharmData(const Chem::MolecularGraph& molgraph, std::int64_t mol_id, std::size_t conf_idx);

            void insertPharmacophore(std::int64_t mol_id, std::size_t conf_idx);

            void genFtrCounts();
            void mergeFtrCounts(bool init);
            void insertFtrCounts(std::int64_t mol_id);
            void insertFtrCount(std::int64_t mol_id, unsigned int ftr_type, std::size_t ftr_count);

            void deleteRowsWithMolID(SQLite3StmtPointer& stmt_ptr, const std::string& sql_stmt, std::int64_t mol_id) const;

            void beginTransaction();
            void commitTransaction();
       
            typedef std::unordered_multimap<std::uint64_t, std::int64_t> MolHashToIDMap;
            typedef std::unordered_set<std::uint64_t>                    MolHashSet;

            SQLite3StmtPointer                  beginTransStmt;
            SQLite3StmtPointer                  commitTransStmt;
            SQLite3StmtPointer                  insMoleculeStmt;
            SQLite3StmtPointer                  insPharmStmt;
            SQLite3StmtPointer                  insFtrCountStmt;
            SQLite3StmtPointer                  delMolWithMolIDStmt;
            SQLite3StmtPointer                  delPharmsWithMolIDStmt;
            SQLite3StmtPointer                  delFeatureCountsWithMolIDStmt;
            SQLite3StmtPointer                  delTwoPointPharmsWithMolIDStmt;
            SQLite3StmtPointer                  delThreePointPharmsWithMolIDStmt;
            MolHashToIDMap                      molHashToIDMap;
            MolHashSet                          procMolecules;
            Chem::HashCodeCalculator            hashCalculator;
            Internal::ByteBuffer                byteBuffer;
            PSDFeatureContainerByteBufferWriter pharmWriter;
            PSDMolecularGraphByteBufferWriter   molWriter;
            BasicPharmacophore                  pharmacophore;
            DefaultPharmacophoreGenerator       pharmGenerator;
            FeatureTypeHistogram                featureCounts;
            FeatureTypeHistogram                tmpFeatureCounts;
            Math::Vector3DArray                 coordinates;
            ScreeningDBCreator::Mode            mode;
            bool                                allowDupEntries;
            std::size_t                         numProcessed;
            std::size_t                         numRejected;
            std::size_t                         numDeleted;
            std::size_t                         numInserted;
        };
    } // namespace Pharm
} // namespace CDPL

#endif // CDPL_PHARM_PSDSCREENINGDBCREATORIMPL_HPP

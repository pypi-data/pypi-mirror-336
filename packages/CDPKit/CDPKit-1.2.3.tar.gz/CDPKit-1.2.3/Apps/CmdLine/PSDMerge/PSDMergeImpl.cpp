/* 
 * PSDMergeImpl.cpp
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


#include <cstdlib>
#include <algorithm>
#include <chrono>
#include <functional>

#include "CDPL/Pharm/PSDScreeningDBCreator.hpp"
#include "CDPL/Pharm/PSDScreeningDBAccessor.hpp"
#include "CDPL/Util/FileFunctions.hpp"
#include "CDPL/Base/Exceptions.hpp"
#include "CDPL/Internal/StringUtilities.hpp"

#include "CmdLine/Lib/HelperFunctions.hpp"

#include "PSDMergeImpl.hpp"


using namespace PSDMerge;


struct PSDMergeImpl::MergeDBsProgressCallback
{

    MergeDBsProgressCallback(PSDMergeImpl* parent, double offset, double scale): 
        parent(parent), offset(offset), scale(scale) {}

    bool operator()(double progress) const {
        if (PSDMergeImpl::termSignalCaught())
            return false;

        parent->printProgress("Merging Databases... ", offset + scale * progress);
        return true;
    }

    PSDMergeImpl* parent;
    double         offset;
    double         scale;
};


PSDMergeImpl::PSDMergeImpl(): 
    dropDuplicates(false), creationMode(CDPL::Pharm::ScreeningDBCreator::APPEND)
{
    using namespace std::placeholders;
    
    addOption("input,i", "Input database file(s).", 
              value<StringList>(&inputDatabases)->multitoken()->required());
    addOption("output,o", "Output database file.", 
              value<std::string>(&outputDatabase)->required());
    addOption("mode,m", "Database merge mode (CREATE, APPEND, UPDATE, default: APPEND).", 
              value<std::string>()->notifier(std::bind(&PSDMergeImpl::setCreationMode, this, _1)));
    addOption("drop-duplicates,d", "Drop duplicate molecules (default: false).", 
              value<bool>(&dropDuplicates)->implicit_value(true));
}

const char* PSDMergeImpl::getProgName() const
{
    return "PSDMerge";
}

const char* PSDMergeImpl::getProgAboutText() const
{
    return "Merges multiple pharmacophore-screening databases into a single database.";
}

void PSDMergeImpl::setCreationMode(const std::string& mode_str)
{
    using namespace CDPL::Pharm;
    using namespace CDPL;

    if (Internal::isEqualCI(mode_str, "CREATE"))
        creationMode = ScreeningDBCreator::CREATE;
    else if (Internal::isEqualCI(mode_str, "APPEND"))
        creationMode = ScreeningDBCreator::APPEND;
    else if (Internal::isEqualCI(mode_str, "UPDATE"))
        creationMode = ScreeningDBCreator::UPDATE;
    else
        throwValidationError("mode");
}

int PSDMergeImpl::process()
{
    timer.reset();

    printMessage(INFO, getProgTitleString());
    printMessage(INFO, "");

    checkInputFiles();
    printOptionSummary();

    return mergeDatabases();
}

int PSDMergeImpl::mergeDatabases()
{
    using namespace CDPL;

    typedef std::vector<Pharm::ScreeningDBAccessor::SharedPointer> DBAccessorList;

    std::size_t num_mols = 0;
    std::size_t num_pharms = 0;
    DBAccessorList db_accessors;

    printMessage(INFO, "Analyzing Input Databases...");

    for (std::size_t i = 0; i < inputDatabases.size(); i++) {
        if (termSignalCaught())
            return EXIT_FAILURE;

        Pharm::ScreeningDBAccessor::SharedPointer db_acc(new Pharm::PSDScreeningDBAccessor(inputDatabases[i]));

        num_pharms += db_acc->getNumPharmacophores();
        num_mols += db_acc->getNumMolecules();

        db_accessors.push_back(db_acc);
    }

    if (termSignalCaught())
        return EXIT_FAILURE;

    printMessage(INFO, " - Found " + std::to_string(num_mols) + " molecules/" +
                 std::to_string(num_pharms) + " pharmacophores");
    printMessage(INFO, "");

    Pharm::PSDScreeningDBCreator db_creator(outputDatabase, creationMode, !dropDuplicates);

    if (progressEnabled()) {
        initProgress();
        printMessage(INFO, "Merging Databases...", true, true); 
    } else
        printMessage(INFO, "Merging Databases..."); 

    for (std::size_t i = 0; i < inputDatabases.size(); i++) {
        if (termSignalCaught())
            return EXIT_FAILURE;

        db_creator.merge(*db_accessors[i], 
                         MergeDBsProgressCallback(this, i * 1.0 / inputDatabases.size(), 
                                                  1.0 / inputDatabases.size()));
    }

    printMessage(INFO, "");

    if (termSignalCaught())
        return EXIT_FAILURE;

    printStatistics(db_creator.getNumProcessed(), db_creator.getNumRejected(),
                    db_creator.getNumDeleted(), db_creator.getNumInserted());

    return EXIT_SUCCESS;
}

void PSDMergeImpl::printStatistics(std::size_t num_proc, std::size_t num_rej, 
                                   std::size_t num_del, std::size_t num_ins)
{
    std::size_t proc_time = std::chrono::duration_cast<std::chrono::seconds>(timer.elapsed()).count();
    
    printMessage(INFO, "Statistics:");
    printMessage(INFO, " Processed Molecules: " + std::to_string(num_proc));
    printMessage(INFO, " Rejected  Molecules: " + std::to_string(num_rej));
    printMessage(INFO, " Deleted Molecules:   " + std::to_string(num_del));
    printMessage(INFO, " Inserted Molecules:  " + std::to_string(num_ins));
    printMessage(INFO, " Processing Time:     " + CmdLineLib::formatTimeDuration(proc_time));
}

void PSDMergeImpl::checkInputFiles() const
{
    using namespace CDPL;
    using namespace std::placeholders;
    
    StringList::const_iterator it = std::find_if(inputDatabases.begin(), inputDatabases.end(),
                                                 std::bind(std::logical_not<bool>(), 
                                                           std::bind(Util::fileExists, _1)));
    if (it != inputDatabases.end())
        throw Base::IOError("file '" + *it + "' does not exist");
            
                                                         
    if (std::find_if(inputDatabases.begin(), inputDatabases.end(),
                     std::bind(Util::checkIfSameFile, boost::ref(outputDatabase),
                               _1)) != inputDatabases.end())
        throw Base::ValueError("output file must not occur in list of input files");
}

void PSDMergeImpl::printOptionSummary()
{
    printMessage(VERBOSE, "Option Summary:");
    printMessage(VERBOSE, " Input Databases(s):       " + inputDatabases[0]);
    
    for (StringList::const_iterator it = ++inputDatabases.begin(), end = inputDatabases.end(); it != end; ++it)
        printMessage(VERBOSE, std::string(27, ' ') + *it);

    printMessage(VERBOSE, " Output Database:          " + outputDatabase);
     printMessage(VERBOSE, " Creation Mode:            " + getModeString());
     printMessage(VERBOSE, " Drop Duplicates:          " + std::string(dropDuplicates ? "Yes" : "No"));
    printMessage(VERBOSE, "");
}

std::string PSDMergeImpl::getModeString() const
{
    using namespace CDPL;

    if (creationMode == Pharm::ScreeningDBCreator::CREATE)
        return "CREATE";

    if (creationMode == Pharm::ScreeningDBCreator::APPEND)
        return "APPEND";

    if (creationMode == Pharm::ScreeningDBCreator::UPDATE)
        return "UPDATE";
    
    return "UNKNOWN";
}

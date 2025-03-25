/* 
 * IsoGenImpl.hpp
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


#ifndef ISOGEN_ISOGENIMPL_HPP
#define ISOGEN_ISOGENIMPL_HPP

#include <cstddef>
#include <vector>
#include <string>

#include "CDPL/Util/CompoundDataReader.hpp"
#include "CDPL/Chem/MolecularGraphWriter.hpp"
#include "CDPL/Internal/Timer.hpp"

#include "CmdLine/Lib/CmdLineBase.hpp"


namespace CDPL
{

    namespace Chem
    {

        class Molecule;
    } // namespace Chem
} // namespace CDPL


namespace IsoGen
{

    class IsoGenImpl : public CmdLineLib::CmdLineBase
    {

      public:
        IsoGenImpl();

      private:
        const char* getProgName() const;
        const char* getProgAboutText() const;

        void setInputFormat(const std::string& file_ext);
        void setOutputFormat(const std::string& file_ext);

        int process();
        void genIsomers();

        std::size_t readNextMolecule(CDPL::Chem::Molecule& mol);

        void writeMolecule(const CDPL::Chem::MolecularGraph& mol);

        void setErrorMessage(const std::string& msg);
        bool haveErrorMessage();

        void printMessage(VerbosityLevel level, const std::string& msg, bool nl = true, bool file_only = false);

        void printStatistics();

        void checkInputFiles() const;
        void printOptionSummary();
        void initInputReader();
        void initOutputWriter();

        std::string createMoleculeIdentifier(std::size_t rec_idx, const std::string& mol_name);
        std::string createMoleculeIdentifier(std::size_t rec_idx);

        void addOptionLongDescriptions();

        class InputScanProgressCallback;
        class IsomerGenerationWorker;

        typedef std::vector<std::string>                             StringList;
        typedef CDPL::Util::CompoundDataReader<CDPL::Chem::Molecule> CompMoleculeReader;
        typedef CDPL::Chem::MolecularGraphWriter::SharedPointer      MoleculeWriterPtr;
        typedef CDPL::Internal::Timer                                Timer;

        StringList         inputFiles;
        std::string        outputFile;
        std::size_t        maxNumIsomers;
        std::string        inputFormat;
        std::string        outputFormat;
        bool               enumAtomConfig;
        bool               enumBondConfig;
        bool               incSpecCtrs;
        bool               incSymCtrs;
        bool               incInvNitrogens;
        bool               incBridgeheads;
        bool               incRingBonds;
        bool               use2DCoords;
        bool               use3DCoords;
        std::size_t        minRingSize;
        bool               titleSuffix;
        CompMoleculeReader inputReader;
        MoleculeWriterPtr  outputWriter;
        std::string        errorMessage;
        Timer              timer;
        std::size_t        numProcMols;
        std::size_t        numOutIsomers;
    };
} // namespace IsoGen

#endif // ISOGEN_ISOGENIMPL_HPP

/* 
 * ConformerGenerator.cpp 
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

 
#include "StaticInit.hpp"

#include "CDPL/ConfGen/ConformerGenerator.hpp"

#include "ConformerGeneratorImpl.hpp"


using namespace CDPL;


ConfGen::ConformerGenerator::ConformerGenerator(): 
    impl(new ConformerGeneratorImpl())
{}

ConfGen::ConformerGenerator::~ConformerGenerator() 
{}

const ConfGen::ConformerGeneratorSettings& 
ConfGen::ConformerGenerator::getSettings() const
{
    return impl->getSettings();
}

ConfGen::ConformerGeneratorSettings& 
ConfGen::ConformerGenerator::getSettings()
{
    return impl->getSettings();
}

void ConfGen::ConformerGenerator::clearFragmentLibraries()
{
    impl->clearFragmentLibraries();
}

void ConfGen::ConformerGenerator::addFragmentLibrary(const FragmentLibrary::SharedPointer& lib)
{
    impl->addFragmentLibrary(lib);
}

void ConfGen::ConformerGenerator::clearTorsionLibraries()
{
    impl->clearTorsionLibraries();
}

void ConfGen::ConformerGenerator::addTorsionLibrary(const TorsionLibrary::SharedPointer& lib)
{
    impl->addTorsionLibrary(lib);
}

void ConfGen::ConformerGenerator::setAbortCallback(const CallbackFunction& func)
{
    impl->setAbortCallback(func);
}

const ConfGen::CallbackFunction& ConfGen::ConformerGenerator::getAbortCallback() const
{
    return impl->getAbortCallback();
}

void ConfGen::ConformerGenerator::setTimeoutCallback(const CallbackFunction& func)
{
    impl->setTimeoutCallback(func);
}

const ConfGen::CallbackFunction& ConfGen::ConformerGenerator::getTimeoutCallback() const
{
    return impl->getTimeoutCallback();
}

void ConfGen::ConformerGenerator::setLogMessageCallback(const LogMessageCallbackFunction& func)
{
    impl->setLogMessageCallback(func);
}

const ConfGen::LogMessageCallbackFunction& ConfGen::ConformerGenerator::getLogMessageCallback() const
{
    return impl->getLogMessageCallback();
}

unsigned int ConfGen::ConformerGenerator::generate(const Chem::MolecularGraph& molgraph)
{
    return impl->generate(molgraph, false, 0, 0);
}

unsigned int ConfGen::ConformerGenerator::generate(const Chem::MolecularGraph& molgraph, const Chem::MolecularGraph& fixed_substr)
{
    return impl->generate(molgraph, false, &fixed_substr, 0);
}

unsigned int ConfGen::ConformerGenerator::generate(const Chem::MolecularGraph& molgraph, const Chem::MolecularGraph& fixed_substr,
                                                   const Math::Vector3DArray& fixed_substr_coords)
{
    return impl->generate(molgraph, false, &fixed_substr, &fixed_substr_coords);
}

void ConfGen::ConformerGenerator::setConformers(Chem::MolecularGraph& molgraph) const
{
    impl->setConformers(molgraph);
}

std::size_t ConfGen::ConformerGenerator::getNumConformers() const
{
    return impl->getNumConformers();
}

const ConfGen::ConformerData& ConfGen::ConformerGenerator::getConformer(std::size_t idx) const
{
    if (idx >= impl->getNumConformers())
        throw Base::IndexError("ConformerGenerator: conformer index out of bounds");

    return impl->getConformer(idx);
}

ConfGen::ConformerData& ConfGen::ConformerGenerator::getConformer(std::size_t idx)
{
    if (idx >= impl->getNumConformers())
        throw Base::IndexError("ConformerGenerator: conformer index out of bounds");

    return impl->getConformer(idx);
}

ConfGen::ConformerGenerator::ConstConformerIterator ConfGen::ConformerGenerator::getConformersBegin() const
{
    return impl->getConformersBegin();
}

ConfGen::ConformerGenerator::ConstConformerIterator ConfGen::ConformerGenerator::getConformersEnd() const
{
    return impl->getConformersEnd();
}

ConfGen::ConformerGenerator::ConformerIterator ConfGen::ConformerGenerator::getConformersBegin()
{
    return impl->getConformersBegin();
}

ConfGen::ConformerGenerator::ConformerIterator ConfGen::ConformerGenerator::getConformersEnd()
{
    return impl->getConformersEnd();
}

ConfGen::ConformerGenerator::ConstConformerIterator ConfGen::ConformerGenerator::begin() const
{
    return impl->getConformersBegin();
}

ConfGen::ConformerGenerator::ConstConformerIterator ConfGen::ConformerGenerator::end() const
{
    return impl->getConformersEnd();
}

ConfGen::ConformerGenerator::ConformerIterator ConfGen::ConformerGenerator::begin()
{
    return impl->getConformersBegin();
}

ConfGen::ConformerGenerator::ConformerIterator ConfGen::ConformerGenerator::end()
{
    return impl->getConformersEnd();
}

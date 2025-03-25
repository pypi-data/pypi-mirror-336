#
# This file is part of the Chemical Data Processing Toolkit
#
# Copyright (C) Thomas Seidel <thomas.seidel@univie.ac.at>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; see the file COPYING. If not, write to
# the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
#

##
# \brief NegIonizableFeatureGenerator.
# 
class NegIonizableFeatureGenerator(PatternBasedFeatureGenerator):

    ##
    # \brief Constructs the <tt>NegIonizableFeatureGenerator</tt> instance.
    # 
    # \param chgd_groups_only <tt>True</tt> if features shall be generated only for charged groups.
    # 
    def __init__(chgd_groups_only: bool) -> None: pass

    ##
    # \brief Initializes a copy of the \e %NegIonizableFeatureGenerator instance \a gen.
    # \param gen The \e %NegIonizableFeatureGenerator instance to copy.
    # 
    def __init__(gen: NegIonizableFeatureGenerator) -> None: pass

    ##
    # \brief Perceives the negative ionizable group features of the molecular graph a\ molgraph and adds them to the pharmacophore <em>pharm</em>.
    # 
    # \param molgraph The molecular graph for which to perceive the features.
    # \param pharm The output pharmacophore where to add the generated features.
    # \param chgd_groups_only <tt>True</tt> if features shall be generated only for charged groups.
    # 
    def __init__(molgraph: Chem.MolecularGraph, pharm: Pharmacophore, chgd_groups_only: bool) -> None: pass

    ##
    # \brief Replaces the current state of \a self with a copy of the state of the \c %NegIonizableFeatureGenerator instance \a gen.
    # \param gen The \c %NegIonizableFeatureGenerator instance to copy.
    # \return \a self
    # 
    def assign(gen: NegIonizableFeatureGenerator) -> NegIonizableFeatureGenerator: pass

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
# \brief 
# \param molgraph 
# \return 
#
def calcTPSA(molgraph: Chem.MolecularGraph) -> float: pass

##
# \brief 
# \param molgraph 
# \return 
#
def calcXLogP(molgraph: Chem.MolecularGraph) -> float: pass

##
# \brief 
# \param molgraph 
# \return 
#
def calcLogS(molgraph: Chem.MolecularGraph) -> float: pass

##
# \brief 
# \param molgraph 
# \param sep 
# \return 
#
def generateMolecularFormula(molgraph: Chem.MolecularGraph, sep: str = '') -> object: pass

##
# \brief 
# \param molgraph 
# \return 
#
def getRuleOfFiveScore(molgraph: Chem.MolecularGraph) -> int: pass

##
# \brief 
# \param molgraph 
# \return 
#
def generateMassCompositionString(molgraph: Chem.MolecularGraph) -> object: pass

##
# \brief 
# \param molgraph 
# \param hist 
# \param append 
#
def generateElementHistogram(molgraph: Chem.MolecularGraph, hist: ElementHistogram, append: bool = False) -> None: pass

##
# \brief 
# \param molgraph 
# \param comp 
#
def calcMassComposition(molgraph: Chem.MolecularGraph, comp: MassComposition) -> None: pass

##
# \brief 
# \param molgraph 
# \return 
#
def calcCyclomaticNumber(molgraph: Chem.MolecularGraph) -> int: pass

##
# \brief 
# \param molgraph 
# \param overwrite 
# \param from_logp 
#
def calcAtomHydrophobicities(molgraph: Chem.MolecularGraph, overwrite: bool, from_logp: bool = False) -> None: pass

##
# \brief 
# \param molgraph 
# \param overwrite 
# \param num_iter 
# \param damping 
#
def calcPEOEProperties(molgraph: Chem.MolecularGraph, overwrite: bool, num_iter: int = 20, damping: float = 0.48) -> None: pass

##
# \brief 
# \param molgraph 
# \param overwrite 
#
def calcMHMOProperties(molgraph: Chem.MolecularGraph, overwrite: bool) -> None: pass

##
# \brief 
# \param molgraph 
# \param overwrite 
#
def perceiveHBondDonorAtomTypes(molgraph: Chem.MolecularGraph, overwrite: bool) -> None: pass

##
# \brief 
# \param molgraph 
# \param overwrite 
#
def perceiveHBondAcceptorAtomTypes(molgraph: Chem.MolecularGraph, overwrite: bool) -> None: pass

##
# \brief 
# \param molgraph 
# \return 
#
def calcMass(molgraph: Chem.MolecularGraph) -> float: pass

##
# \brief 
# \param molgraph 
# \param h_rotors 
# \param ring_bonds 
# \param amide_bonds 
# \return 
#
def getRotatableBondCount(molgraph: Chem.MolecularGraph, h_rotors: bool = False, ring_bonds: bool = False, amide_bonds: bool = False) -> int: pass

##
# \brief 
# \param molgraph 
# \return 
#
def getHydrogenBondCount(molgraph: Chem.MolecularGraph) -> int: pass

##
# \brief 
# \param molgraph 
# \return 
#
def getChainBondCount(molgraph: Chem.MolecularGraph) -> int: pass

##
# \brief 
# \param molgraph 
# \return 
#
def getBondCount(molgraph: Chem.MolecularGraph) -> int: pass

##
# \brief 
# \param molgraph 
# \param order 
# \param inc_aro 
# \return 
#
def getBondCount(molgraph: Chem.MolecularGraph, order: int, inc_aro: bool = True) -> int: pass

##
# \brief 
# \param molgraph 
# \return 
#
def getChainAtomCount(molgraph: Chem.MolecularGraph) -> int: pass

##
# \brief 
# \param molgraph 
# \return 
#
def getHBondDonorAtomCount(molgraph: Chem.MolecularGraph) -> int: pass

##
# \brief 
# \param molgraph 
# \return 
#
def getHBondAcceptorAtomCount(molgraph: Chem.MolecularGraph) -> int: pass

##
# \brief 
# \param molgraph 
# \return 
#
def getAtomCount(molgraph: Chem.MolecularGraph) -> int: pass

##
# \brief 
# \param molgraph 
# \param type 
# \param strict 
# \return 
#
def getAtomCount(molgraph: Chem.MolecularGraph, type: int, strict: bool = True) -> int: pass

##
# \brief 
# \param molgraph 
# \return 
#
def getImplicitHydrogenCount(molgraph: Chem.MolecularGraph) -> int: pass

##
# \brief 
# \param molgraph 
# \param flags 
# \return 
#
def getOrdinaryHydrogenCount(molgraph: Chem.MolecularGraph, flags: int = 2147483648) -> int: pass

##
# \brief 
# \param molgraph 
# \param flags 
# \return 
#
def getExplicitOrdinaryHydrogenCount(molgraph: Chem.MolecularGraph, flags: int = 2147483648) -> int: pass

##
# \brief 
# \param molgraph 
# \return 
#
def getComponentCount(molgraph: Chem.MolecularGraph) -> int: pass

##
# \brief 
# \param molgraph 
# \return 
#
def calcMeanPolarizability(molgraph: Chem.MolecularGraph) -> float: pass
